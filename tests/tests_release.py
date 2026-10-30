"""Release tooling tests never publish, push, or call a live remote service."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest

from scripts import release


@pytest.fixture(autouse=True)
def snapshots(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    directory = tmp_path / "snapshots"
    directory.mkdir()
    monkeypatch.setenv("RELEASE_DATA", str(directory))


def write_snapshot(name: str, data: object) -> None:
    release.data_file(name).write_text(json.dumps(data), encoding="utf-8")


@pytest.mark.parametrize("version", ["2.2.0", "2.2.0.dev1", "0.0.0", "12.123.1234.dev0"])
def test_supported_versions(version: str) -> None:
    release.version_key(version)


@pytest.mark.parametrize(
    "version",
    [
        "v2.2.0",
        "02.2.0",
        "2.2",
        "2.2.0rc1",
        "2.2.0.dev01",
        "2.2.0.post1",
        "2.2.0\n",
        "2.2.0;echo bad",
        "2.2.0.dev\u0661",
        "2.\u0662.0",
        "../../bad",
    ],
)
def test_invalid_versions(version: str) -> None:
    with pytest.raises(ValueError, match=r"Expected X\.Y\.Z"):
        release.version_key(version)


def test_numeric_version_order() -> None:
    versions = ["2.1.9", "2.1.10", "2.2.0.dev1", "2.2.0.dev2", "2.2.0.dev10", "2.2.0", "2.2.1"]
    shuffled = list(reversed(versions))
    assert sorted(shuffled, key=release.version_key) == versions


def test_dev_notes_survive_until_stable_release() -> None:
    old = "2.1.0 (Oct 24, 2026)\n-------------------\n\nExisting history\n"
    text = "## Unreleased\n\n" + release.UNRELEASED.format(manual="Important deprecation.") + "\n\n" + old
    for version in ("2.2.0.dev1", "2.2.0.dev2", "2.2.0"):
        text = release.update_changelog(
            text, version, release.marked(text, "unreleased"), "## What's Changed\n- Fix", "2026-10-29"
        )
        assert "Important deprecation." in release.release_body(text, version)
        assert text.endswith(old)
    assert release.marked(text, "unreleased") == ""
    assert "<!--" not in release.release_body(text, "2.2.0")


@pytest.mark.parametrize(
    ("current", "edited", "original", "expected"),
    [
        ("new on master", "old", "old", "new on master"),
        ("old", "edited on PR", "old", "edited on PR"),
        ("same edit", "same edit", "old", "same edit"),
    ],
)
def test_refresh_preserves_manual_edits(current: str, edited: str, original: str, expected: str) -> None:
    assert release.merge_manual(current, edited, original) == expected


def test_conflicting_manual_edits_require_reconciliation() -> None:
    with pytest.raises(ValueError, match="both branches"):
        release.merge_manual("edit on master", "edit on PR", "original")


@pytest.mark.parametrize(
    "text", ["", "<!-- x:end --><!-- x:start -->", "<!-- x:start --><!-- x:start --><!-- x:end -->"]
)
def test_malformed_markers_stop_release(text: str) -> None:
    with pytest.raises(ValueError, match=r"Expected|Invalid|reviewers|self-review|Production"):
        release.marked(text, "x")


def test_stable_notes_start_at_last_stable_tag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value="v2.0.0\nv2.1.0\nv2.2.0.dev1\nv2.2.0.dev2\nv99bad"))
    assert release.previous_tag("2.2.0") == "v2.1.0"
    assert release.previous_tag("2.2.0.dev3") == "v2.2.0.dev2"


def test_distribution_files_must_match_exactly(tmp_path: Path) -> None:
    directory = tmp_path / "dist"
    directory.mkdir()
    for name in ("mahjong-2.2.0.dev1-py3-none-any.whl", "mahjong-2.2.0.dev1.tar.gz"):
        (directory / name).write_bytes(name.encode())
    files = release.file_hashes(directory, "2.2.0.dev1")
    assert len(files) == 2
    (directory / "unexpected.whl").write_bytes(b"unvalidated")
    with pytest.raises(ValueError, match="exactly"):
        release.file_hashes(directory, "2.2.0.dev1")


def test_partial_or_changed_pypi_publication_stops_retry() -> None:
    local = {"wheel": "hash1", "sdist": "hash2"}
    assert release.publish_state(local, {}) == "new"
    assert release.publish_state(local, local) == "published"
    for remote in ({"wheel": "hash1"}, {"wheel": "changed", "sdist": "hash2"}):
        with pytest.raises(ValueError, match="partial"):
            release.publish_state(local, remote)


@pytest.fixture
def prepared_checkout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[dict[str, Any], Mock]:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".github").mkdir()
    version = "2.2.0.dev1"
    changelog = release.update_changelog(
        release.UNRELEASED.format(manual="Notice"), version, "Notice", "## What's Changed\n- Fix", "2026-10-29"
    )
    Path("CHANGELOG.md").write_text(changelog, encoding="utf-8")
    data = {
        "version": version,
        "source_sha": "a" * 40,
        "previous_tag": "v2.1.0",
        "manual_source": "Notice",
        "prepared_by": "Apricot-S",
        "notes_sha256": release.digest(release.release_body(changelog, version).encode()),
    }
    release.MANIFEST.write_text(json.dumps(data), encoding="utf-8")

    def command(*args: str, **_kwargs: object) -> str:
        if args[:2] == ("uv", "version"):
            return version
        if args[:3] == ("git", "diff", "--name-only"):
            return "\n".join(sorted(release.ALLOWED_FILES))
        if args[:3] == ("git", "rev-parse", "HEAD"):
            return "b" * 40
        if args[:3] == ("git", "show", "-s"):
            return "a" * 40
        if args[:2] == ("git", "ls-remote"):
            return "b" * 40 + "\trefs/tags/v2.2.0.dev1"
        return ""

    mocked = Mock(side_effect=command)
    monkeypatch.setattr(release, "run", mocked)
    monkeypatch.setenv("GITHUB_REPOSITORY", release.UPSTREAM)
    monkeypatch.setenv("GITHUB_REF", "refs/heads/master")
    monkeypatch.setenv("GITHUB_EVENT_NAME", "push")
    return data, mocked


def test_reviewed_body_changes_need_refresh(prepared_checkout: tuple[dict[str, Any], Mock]) -> None:
    data, _ = prepared_checkout
    assert "Notice" in release.verify_contents(data)
    release.CHANGELOG.write_text(release.CHANGELOG.read_text().replace("Notice", "Edited"))
    with pytest.raises(ValueError, match="refresh"):
        release.verify_contents(data)


def test_release_pr_cannot_contain_other_changes(
    prepared_checkout: tuple[dict[str, Any], Mock], monkeypatch: pytest.MonkeyPatch
) -> None:
    data, _ = prepared_checkout
    monkeypatch.setattr(release, "run", Mock(side_effect=[data["version"], ".github/release.json\nmahjong/tile.py"]))
    with pytest.raises(ValueError, match="Unexpected files"):
        release.verify_contents(data)


@pytest.fixture
def protection(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    settings = {
        "can_admins_bypass": False,
        "deployment_branch_policy": {"custom_branch_policies": True},
        "protection_rules": [
            {
                "type": "required_reviewers",
                "prevent_self_review": True,
                "reviewers": [{"type": "User", "reviewer": {"login": name}} for name in ("Nihisil", "Apricot-S")],
            }
        ],
    }
    values = {
        "environment.json": settings,
        "branch-policies.json": {"branch_policies": [{"name": "master", "type": "branch"}]},
        "merged-prs.json": [
            [
                {
                    "merged_at": "today",
                    "merge_commit_sha": "b" * 40,
                    "base": {"ref": "master"},
                    "head": {"ref": "release/2.2.0.dev1", "repo": {"full_name": release.UPSTREAM}},
                }
            ]
        ],
    }
    monkeypatch.setattr(release, "read_json", Mock(side_effect=lambda name: values[name]))
    return settings


@pytest.mark.usefixtures("prepared_checkout")
def test_production_requires_protection(protection: dict[str, Any]) -> None:
    release.verify(dry_run=False)
    protection["can_admins_bypass"] = True
    with pytest.raises(ValueError, match="bypass"):
        release.verify(dry_run=False)


@pytest.mark.parametrize("setting", ["self_review", "missing_reviewer", "extra_team", "unrestricted_branch"])
@pytest.mark.usefixtures("prepared_checkout")
def test_invalid_approval_settings_stop_publication(protection: dict[str, Any], setting: str) -> None:
    rule = protection["protection_rules"][0]
    if setting == "self_review":
        rule["prevent_self_review"] = False
    elif setting == "missing_reviewer":
        rule["reviewers"].pop()
    elif setting == "extra_team":
        rule["reviewers"].append({"type": "Team", "reviewer": {"name": "others"}})
    else:
        protection["deployment_branch_policy"] = None
    with pytest.raises(ValueError, match=r"reviewers|self-review|master"):
        release.verify(dry_run=False)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("GITHUB_REPOSITORY", "Apricot-S/mahjong"),
        ("GITHUB_REF", "refs/heads/other"),
        ("GITHUB_EVENT_NAME", "workflow_dispatch"),
    ],
)
@pytest.mark.usefixtures("prepared_checkout", "protection")
def test_fork_ref_and_dispatch_cannot_publish(monkeypatch: pytest.MonkeyPatch, key: str, value: str) -> None:
    monkeypatch.setenv(key, value)
    with pytest.raises(ValueError, match="Production"):
        release.verify(dry_run=False)


@pytest.mark.usefixtures("prepared_checkout", "protection")
def test_direct_push_is_not_release_preparation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "read_pages", Mock(return_value=[]))
    with pytest.raises(ValueError, match="merged release"):
        release.verify(dry_run=False)


@pytest.mark.usefixtures("protection")
def test_base_must_match_merge_parent(prepared_checkout: tuple[dict[str, Any], Mock]) -> None:
    data, _ = prepared_checkout
    data["source_sha"] = "c" * 40
    release.MANIFEST.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="base changed"):
        release.verify(dry_run=False)


@pytest.mark.usefixtures("prepared_checkout")
def test_pypi_success_required_before_github_release(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "file_hashes", Mock(return_value={"wheel": "h1", "sdist": "h2"}))
    write_snapshot("pypi.json", {"urls": []})
    with pytest.raises(ValueError, match="not complete"):
        release.github_release(Path("dist"))


def pypi_snapshot(files: dict[str, str]) -> None:
    write_snapshot(
        "pypi.json",
        {
            "info": {"version": "2.2.0.dev1"},
            "urls": [{"filename": name, "digests": {"sha256": value}} for name, value in files.items()],
        },
    )


def test_release_creation_is_planned_without_remote_writes(
    prepared_checkout: tuple[dict[str, Any], Mock],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, command = prepared_checkout
    files = {"wheel": "h1", "sdist": "h2"}
    monkeypatch.setattr(release, "file_hashes", Mock(return_value=files))
    pypi_snapshot(files)
    write_snapshot("releases.json", [[]])
    result = Mock()
    monkeypatch.setattr(release, "output", result)
    release.github_release(Path("dist"))
    result.assert_called_once_with(exists="false")
    assert set(release.read_json("missing-assets.json")) == set(files)
    assert not any(call.args[0] == "gh" for call in command.call_args_list)


def test_retry_plans_only_missing_release_assets(
    prepared_checkout: tuple[dict[str, Any], Mock],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data, command = prepared_checkout
    files = {"wheel": "h1", "sdist": "h2"}
    monkeypatch.setattr(release, "file_hashes", Mock(return_value=files))
    pypi_snapshot(files)
    write_snapshot(
        "releases.json",
        [
            [
                {
                    "tag_name": "v2.2.0.dev1",
                    "draft": False,
                    "prerelease": True,
                    "body": release.release_body(release.CHANGELOG.read_text(), data["version"]),
                    "assets": [{"name": "wheel", "digest": "sha256:h1"}],
                }
            ]
        ],
    )
    result = Mock()
    monkeypatch.setattr(release, "output", result)
    release.github_release(Path("dist"))
    result.assert_called_once_with(exists="true")
    assert release.read_json("missing-assets.json") == ["sdist"]
    assert not any(call.args[0] == "gh" for call in command.call_args_list)


def test_retry_detects_tampered_distribution(
    prepared_checkout: tuple[dict[str, Any], Mock],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data, _ = prepared_checkout
    Path("release-artifacts.json").write_text(
        json.dumps({"sha": "b" * 40, "version": data["version"], "files": {"wheel": "original"}})
    )
    monkeypatch.setattr(release, "file_hashes", Mock(return_value={"wheel": "modified"}))
    with pytest.raises(ValueError, match="hashes changed"):
        release.publication_state(Path("dist"))


def test_retry_reuses_tag_and_skips_upload(
    prepared_checkout: tuple[dict[str, Any], Mock],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data, command = prepared_checkout
    files = {"wheel": "h1", "sdist": "h2"}
    Path("release-artifacts.json").write_text(json.dumps({"sha": "b" * 40, "version": data["version"], "files": files}))
    monkeypatch.setattr(release, "file_hashes", Mock(return_value=files))
    pypi_snapshot(files)
    release.data_file("tag-refs.txt").write_text("b" * 40 + "\trefs/tags/v2.2.0.dev1\n")
    result = Mock()
    monkeypatch.setattr(release, "output", result)
    release.publication_state(Path("dist"))
    result.assert_called_once_with(state="published", tag_exists="true")
    assert not any(call.args[:2] == ("git", "push") for call in command.call_args_list)


def test_preparation_plan_validates_before_network(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_REPOSITORY", release.UPSTREAM)
    monkeypatch.setenv("GITHUB_REF", "refs/heads/master")
    responses = {
        ("git", "rev-parse", "HEAD"): "a" * 40,
        ("uv", "version", "--short"): "2.1.0",
        ("git", "tag", "--merged", "HEAD", "--list", "v*"): "v2.1.0",
    }
    command = Mock(side_effect=lambda *args: responses.get(args, ""))
    monkeypatch.setattr(release, "run", command)
    release.plan("2.2.0.dev1")
    data = release.read_json("plan.json")
    assert data["source"] == "a" * 40
    assert data["previous_tag"] == "v2.1.0"
    assert data["branch"] == "release/2.2.0.dev1"
    assert all(call.args[0] in {"git", "uv"} for call in command.call_args_list)


@pytest.mark.parametrize("collision", ["pypi", "release", "other_pr", "foreign_pr"])
def test_remote_collisions_stop_preparation(monkeypatch: pytest.MonkeyPatch, collision: str) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", release.UPSTREAM)
    write_snapshot("plan.json", {"version": "2.2.0.dev1", "branch": "release/2.2.0.dev1"})
    write_snapshot("releases.json", [[{"tag_name": "v2.2.0.dev1"}]] if collision == "release" else [[]])
    pypi_snapshot({"wheel": "h1"} if collision == "pypi" else {})
    ref = "release/2.3.0" if collision == "other_pr" else "release/2.2.0.dev1"
    repo = "someone/mahjong" if collision == "foreign_pr" else release.UPSTREAM
    write_snapshot("pulls.json", [[{"head": {"ref": ref, "sha": "c" * 40, "repo": {"full_name": repo}}}]])
    with pytest.raises(ValueError, match=r"exists|Another|belong"):
        release.preparation_state()


def test_ordinary_pr_does_not_need_release_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    event = Path("event.json")
    event.write_text(json.dumps({"pull_request": {"number": 1}}))
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    write_snapshot("pr-files.json", [[{"filename": "mahjong/tile.py"}]])
    release.check_pr()


def test_stale_release_pr_requires_regeneration(
    prepared_checkout: tuple[dict[str, Any], Mock],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data, _ = prepared_checkout
    event = Path("event.json")
    event.write_text(
        json.dumps(
            {
                "pull_request": {
                    "number": 1,
                    "head": {"repo": {"full_name": release.UPSTREAM}, "ref": f"release/{data['version']}"},
                    "base": {"ref": "master"},
                }
            }
        )
    )
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    write_snapshot("pr-files.json", [[{"filename": ".github/release.json"}]])
    write_snapshot("base-ref.json", {"object": {"sha": "c" * 40}})
    with pytest.raises(ValueError, match="stale"):
        release.check_pr()


@pytest.mark.parametrize("extra_change", [False, True])
def test_refresh_preserves_reviewed_notes_and_refuses_unrelated_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    extra_change: bool,
) -> None:
    monkeypatch.chdir(tmp_path)
    Path(".github").mkdir()
    current = release.UNRELEASED.format(manual="Original explanation")
    release.CHANGELOG.write_text(current, encoding="utf-8")
    edited = release.update_changelog(current, "2.2.0.dev1", "Reviewed explanation", "Old generated list", "2026-10-28")
    monkeypatch.setenv("GITHUB_ACTOR", "Apricot-S")
    responses = {("uv", "version", "--short"): "2.2.0.dev1", ("git", "rev-parse", "HEAD"): "a" * 40}
    monkeypatch.setattr(release, "run", Mock(side_effect=lambda *args: responses.get(args, "")))
    write_snapshot("plan.json", {"version": "2.2.0.dev1", "source": "a" * 40, "previous_tag": "v2.1.0"})
    write_snapshot(
        "old-manifest.json", {"version": "2.2.0.dev1", "source_sha": "b" * 40, "manual_source": "Original explanation"}
    )
    release.data_file("old-files.txt").write_text("mahjong/tile.py" if extra_change else "CHANGELOG.md")
    release.data_file("old-changelog.md").write_text(edited)
    release.data_file("generated-notes.md").write_text("New generated list")
    if extra_change:
        with pytest.raises(ValueError, match="other changes"):
            release.prepare()
    else:
        release.prepare()
        preview = Path("release-preview.md").read_text()
        assert "Reviewed explanation" in preview
        assert "New generated list" in preview
        assert "Old generated list" not in preview
