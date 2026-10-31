"""Release tooling tests never publish, push, or call a live remote service."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from scripts import release


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
    "text", ["", "<!-- x:end --><!-- x:start -->", "<!-- x:start --><!-- x:start --><!-- x:end -->"]
)
def test_malformed_markers_stop_release(text: str) -> None:
    with pytest.raises(ValueError, match=r"Expected|Invalid|reviewers|self-review|Production"):
        release.marked(text, "x")


def test_stable_notes_start_at_last_stable_tag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value="v2.0.0\nv2.1.0\nv2.2.0.dev1\nv2.2.0.dev2\nv99bad"))
    assert release.previous_tag("2.2.0") == "v2.1.0"
    assert release.previous_tag("2.2.0.dev3") == "v2.2.0.dev2"


@pytest.fixture
def checkout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    Path("pyproject.toml").write_text('[project]\nname = "mahjong"\nversion = "2.2.0.dev1"\n')
    Path("uv.lock").write_text('[[package]]\nname = "mahjong"\nversion = "2.2.0.dev1"\n')
    release.CHANGELOG.write_text(release.UNRELEASED.format(manual="Deprecation notice."))
    notes = Path("notes.md")
    notes.write_text("## What's Changed\n- Fix a bug\n")
    return notes


def test_preparation_allows_review_edits_without_regeneration(checkout: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value="diff"))
    release.prepare("2.2.0.dev1", checkout)
    release.CHANGELOG.write_text(release.CHANGELOG.read_text().replace("Deprecation notice.", "Reviewed explanation."))
    assert "Reviewed explanation." in release.check_contents()
    release.verify(None)
    assert "Reviewed explanation." in Path("release-notes.md").read_text()


@pytest.mark.parametrize("file", ["uv.lock", "CHANGELOG.md"])
def test_mismatched_release_files_stop_publication(
    checkout: Path,
    monkeypatch: pytest.MonkeyPatch,
    file: str,
) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value="diff"))
    release.prepare("2.2.0.dev1", checkout)
    path = Path(file)
    path.write_text(path.read_text().replace("2.2.0.dev1", "2.2.0.dev2"))
    with pytest.raises(ValueError, match=r"differs|Expected one"):
        release.verify(None)


def test_repeated_preparation_preserves_existing_edits(checkout: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value="diff"))
    release.prepare("2.2.0.dev1", checkout)
    content = release.CHANGELOG.read_text()
    with pytest.raises(ValueError, match="already exists"):
        release.prepare("2.2.0.dev1", checkout)
    assert release.CHANGELOG.read_text() == content


@pytest.mark.parametrize(("old", "expected"), [("2.1.0", True), ("2.2.0.dev1", False)])
def test_version_change_detection(
    checkout: Path,
    monkeypatch: pytest.MonkeyPatch,
    old: str,
    expected: bool,
) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value="diff"))
    release.prepare("2.2.0.dev1", checkout)
    monkeypatch.setattr(release, "run", Mock(return_value=f'[project]\nversion = "{old}"'))
    assert release.check_change("a" * 40) is expected


@pytest.mark.usefixtures("checkout")
def test_version_decrease_stops_publication(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value='[project]\nversion = "2.2.0"'))
    with pytest.raises(ValueError, match="Version must increase"):
        release.verify("a" * 40)


@pytest.mark.usefixtures("checkout")
def test_ordinary_pr_does_not_need_release_notes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value='[project]\nversion = "2.2.0.dev1"'))
    assert not release.check_change("a" * 40)


@pytest.mark.usefixtures("checkout")
def test_plan_rejects_an_existing_tag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value="v2.2.0"))
    with pytest.raises(ValueError, match="Tag already exists"):
        release.plan("2.2.0")


@pytest.mark.usefixtures("checkout")
def test_dependency_only_push_skips_release_without_requiring_notes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release, "run", Mock(return_value='[project]\nversion = "2.2.0.dev1"'))
    result = Path("outputs.txt")
    monkeypatch.setenv("GITHUB_OUTPUT", str(result.resolve()))
    release.verify("a" * 40)
    assert result.read_text() == "release=false\n"
    assert not Path("release-notes.md").exists()


@pytest.mark.parametrize("version", ["2.2.0.dev1", "2.2.0"])
def test_release_after_normal_branch_updates(
    checkout: Path,
    version: str,
) -> None:
    release.run("git", "init")
    release.run("git", "config", "user.name", "Release test")
    release.run("git", "config", "user.email", "release@example.invalid")
    Path("pyproject.toml").write_text('[project]\nname = "mahjong"\nversion = "2.1.0"\n')
    release.run("git", "add", ".")
    release.run("git", "commit", "-m", "Initial state")
    base = release.run("git", "rev-parse", "HEAD")
    release.run("git", "tag", "v2.1.0")
    release.plan(version)
    for file in ("pyproject.toml", "uv.lock"):
        path = Path(file)
        path.write_text(path.read_text().replace("2.1.0", version).replace("2.2.0.dev1", version))
    release.prepare(version, checkout)
    release.run("git", "add", ".")
    release.run("git", "commit", "-m", "Prepare release")
    # A later ordinary branch update and direct review edits need no regeneration.
    Path("README.md").write_text("An ordinary change included in the final review.")
    release.CHANGELOG.write_text(release.CHANGELOG.read_text().replace("Deprecation notice.", "Final reviewed note."))
    release.run("git", "add", ".")
    release.run("git", "commit", "-m", "Review and update preparation")
    assert release.check_change(base)
    result = Path("outputs.txt")
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("GITHUB_OUTPUT", str(result.resolve()))
        release.verify(base)
    assert "release=true\n" in result.read_text()
    assert "Final reviewed note." in Path("release-notes.md").read_text()


@pytest.mark.usefixtures("checkout")
def test_non_release_push_with_real_git_history(monkeypatch: pytest.MonkeyPatch) -> None:
    release.run("git", "init")
    release.run("git", "config", "user.name", "Release test")
    release.run("git", "config", "user.email", "release@example.invalid")
    release.run("git", "add", ".")
    release.run("git", "commit", "-m", "Initial state")
    base = release.run("git", "rev-parse", "HEAD")
    with Path("pyproject.toml").open("a") as stream:
        stream.write('description = "Dependency and metadata update without a release"\n')
    release.run("git", "add", "pyproject.toml")
    release.run("git", "commit", "-m", "Update metadata without changing the version")
    result = Path("outputs.txt")
    monkeypatch.setenv("GITHUB_OUTPUT", str(result.resolve()))
    release.verify(base)
    assert result.read_text() == "release=false\n"
    assert not Path("release-notes.md").exists()
