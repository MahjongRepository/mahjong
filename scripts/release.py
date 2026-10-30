"""Edit release files and validate snapshots; remote operations live in the workflows."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

UPSTREAM = "MahjongRepository/mahjong"
MANIFEST = Path(".github/release.json")
CHANGELOG = Path("CHANGELOG.md")
ALLOWED_FILES = {"pyproject.toml", "uv.lock", CHANGELOG.as_posix(), MANIFEST.as_posix()}
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:\.dev(0|[1-9][0-9]*))?")
UNRELEASED = "<!-- unreleased:start -->\n{manual}\n<!-- unreleased:end -->"
SECTION = (
    "<!-- release:{version}:start -->\n"
    "## {version} ({day})\n\n"
    "<!-- manual:start -->\n{manual}\n<!-- manual:end -->\n\n"
    "<!-- generated:start -->\n{generated}\n<!-- generated:end -->\n"
    "<!-- release:{version}:end -->"
)


def require(condition: object, message: str) -> None:
    """Stop before making a change when a precondition is not satisfied."""
    if not condition:
        raise ValueError(message)


def run(*args: str, input_text: str | None = None) -> str:
    """Run a command without interpreting any input as shell code."""
    return subprocess.run(  # noqa: S603
        args, input=input_text, text=True, encoding="utf-8", capture_output=True, check=True
    ).stdout.strip()


def digest(data: bytes) -> str:
    """Return a SHA-256 digest."""
    return hashlib.sha256(data).hexdigest()


def version_key(version: str) -> tuple[int, int, int, int, int]:
    """Order the canonical stable and dev versions supported by this workflow."""
    match = VERSION.fullmatch(version)
    require(match, "Expected X.Y.Z or X.Y.Z.devN with no leading zeroes")
    assert match is not None  # noqa: S101
    major, minor, patch, dev = match.groups()
    return int(major), int(minor), int(patch), int(dev is None), int(dev or 0)


def marked(text: str, name: str) -> str:
    """Read exactly one explicitly delimited block."""
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    require(text.count(start) == text.count(end) == 1, f"Expected one {name} block")
    require(text.index(start) < text.index(end), f"Invalid {name} block order")
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def merge_manual(current: str, edited: str, original: str) -> str:
    """Preserve edits on either side; ask for reconciliation if both changed."""
    if edited == original:
        return current
    require(current in {original, edited}, "Manual notes changed on both branches; reconcile them before refreshing")
    return edited


def release_body(changelog: str, version: str) -> str:
    """Extract the reviewed body, removing only our structural comments."""
    section = marked(changelog, f"release:{version}")
    require(section.startswith(f"## {version} ("), "Changelog version heading does not match")
    manual = marked(section, "manual")
    generated = marked(section, "generated")
    return "\n\n".join(part for part in (manual, generated) if part) + "\n"


def update_changelog(content: str, version: str, manual: str, generated: str, day: str) -> str:
    """Keep old releases intact and retain dev notes for the eventual stable release."""
    version_key(version)
    require(f"<!-- release:{version}:start -->" not in content, "Release already exists in changelog")
    marked(content, "unreleased")
    # Preserve existing whitespace outside the explicitly marked region.
    start = content.index("<!-- unreleased:start -->")
    end = content.index("<!-- unreleased:end -->") + len("<!-- unreleased:end -->")
    retained = manual if ".dev" in version else ""
    replacement = UNRELEASED.format(manual=retained)
    section = SECTION.format(version=version, day=day, manual=manual, generated=generated.rstrip())
    return content[:start] + replacement + "\n\n" + section + content[end:]


def publish_state(local: dict[str, str], remote: dict[str, str]) -> str:
    """Distinguish a new release, a completed release and unsafe partial publication."""
    if not remote:
        return "new"
    require(remote == local, "PyPI files differ or publication is partial; stop and investigate")
    return "published"


def file_hashes(directory: Path, version: str) -> dict[str, str]:
    """Accept exactly the wheel and sdist for the expected distribution version."""
    version_key(version)
    expected = {f"mahjong-{version}-py3-none-any.whl", f"mahjong-{version}.tar.gz"}
    require({p.name for p in directory.iterdir()} == expected, "Expected exactly the mahjong wheel and sdist")
    require(all(not p.is_symlink() and p.is_file() for p in directory.iterdir()), "Invalid distribution file")
    return {name: digest((directory / name).read_bytes()) for name in sorted(expected)}


def output(**values: object) -> None:
    """Expose validated single-line values to the workflow."""
    if "GITHUB_OUTPUT" in os.environ:
        with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as stream:
            for key, value in values.items():
                require("\n" not in str(value), "Multiline workflow output")
                stream.write(f"{key}={value}\n")
    print(json.dumps(values))  # noqa: T201


def load_manifest() -> dict[str, Any]:
    """Read the release description checked into the prepared commit."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    version_key(data["version"])
    require(re.fullmatch(r"[0-9a-f]{40}", data["source_sha"]), "Invalid source SHA")
    require(
        data["previous_tag"].startswith("v") and VERSION.fullmatch(data["previous_tag"][1:]), "Invalid previous tag"
    )
    return data


def verify_contents(data: dict[str, Any]) -> str:
    """Check the version, reviewed notes and allowed preparation diff."""
    require(run("uv", "version", "--short") == data["version"], "Project version differs from release manifest")
    body = release_body(CHANGELOG.read_text(encoding="utf-8"), data["version"])
    require(digest(body.encode()) == data["notes_sha256"], "Release notes changed; refresh the preparation PR")
    changed = set(run("git", "diff", "--name-only", data["source_sha"], "HEAD").splitlines())
    require(MANIFEST.as_posix() in changed and changed <= ALLOWED_FILES, "Unexpected files in release preparation")
    return body


def previous_tag(version: str) -> str:
    """Stable notes always start at the previous stable tag, including all dev changes."""
    tags = run("git", "tag", "--merged", "HEAD", "--list", "v*").splitlines()
    candidates = [tag for tag in tags if VERSION.fullmatch(tag[1:]) and version_key(tag[1:]) < version_key(version)]
    if ".dev" not in version:
        candidates = [tag for tag in candidates if ".dev" not in tag]
    require(candidates, "No previous release tag found")
    return max(candidates, key=lambda tag: version_key(tag[1:]))


def record(directory: Path) -> None:
    """Save the validated distribution hashes before the approval gate."""
    data = load_manifest()
    files = file_hashes(directory, data["version"])
    payload = {"sha": run("git", "rev-parse", "HEAD"), "version": data["version"], "files": files}
    Path("release-artifacts.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    summary = f"## Release {data['version']}\n\nCommit: `{payload['sha']}`\n\n"
    summary += f"Prepared by: `{data['prepared_by']}`; source: `{data['source_sha']}`\n\n"
    summary += "\n".join(f"- `{name}`: `{value}`" for name, value in files.items())
    summary += "\n\n" + release_body(CHANGELOG.read_text(encoding="utf-8"), data["version"])
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a", encoding="utf-8") as stream:
            stream.write(summary)


def data_file(name: str) -> Path:
    """Locate workflow-provided snapshots outside the source checkout."""
    return Path(os.environ.get("RELEASE_DATA", "release-data")) / name


def read_json(name: str) -> Any:  # noqa: ANN401
    """Read a previously fetched response; this tool never makes network requests."""
    return json.loads(data_file(name).read_text(encoding="utf-8"))


def read_pages(name: str) -> list[dict[str, Any]]:
    """Flatten gh api --paginate --slurp responses."""
    return [item for page in read_json(name) for item in page]


def pypi_files(version: str) -> dict[str, str]:
    """Read the names and hashes in a workflow-fetched PyPI response."""
    version_key(version)
    data = read_json("pypi.json")
    if data.get("info"):
        require(data["info"]["version"] == version, "PyPI response version differs")
    return {item["filename"]: item["digests"]["sha256"] for item in data["urls"]}


def plan(version: str) -> None:
    """Validate local inputs before the workflow fetches any remote state."""
    version_key(version)
    base = "master" if os.environ["GITHUB_REPOSITORY"] == UPSTREAM else os.environ["DEFAULT_BRANCH"]
    require(os.environ["GITHUB_REF"] == f"refs/heads/{base}", "Run preparation from the default branch")
    require(not run("git", "status", "--porcelain", "--untracked-files=no"), "Checkout must be clean")
    require(version_key(version) > version_key(run("uv", "version", "--short")), "Version must increase")
    require(not run("git", "tag", "--list", f"v{version}"), "Tag already exists")
    data = {
        "version": version,
        "base": base,
        "source": run("git", "rev-parse", "HEAD"),
        "branch": f"release/{version}",
        "previous_tag": previous_tag(version),
    }
    data_file("plan.json").parent.mkdir(parents=True, exist_ok=True)
    data_file("plan.json").write_text(json.dumps(data), encoding="utf-8")
    output(**data)


def preparation_state() -> None:
    """Validate existing remote objects before fetching or updating a preparation branch."""
    data = read_json("plan.json")
    version = data["version"]
    version_key(version)
    require(not pypi_files(version), "Version already exists on PyPI")
    require(
        not any(r["tag_name"] == f"v{version}" for r in read_pages("releases.json")), "GitHub Release already exists"
    )
    prs = [pr for pr in read_pages("pulls.json") if pr["head"]["ref"].startswith("release/")]
    require(all(pr["head"]["ref"] == data["branch"] for pr in prs), "Another release preparation PR is open")
    require(len(prs) <= 1, "Multiple preparation PRs found")
    head = ""
    if prs:
        pr = prs[0]
        require(
            pr["head"]["repo"]["full_name"] == os.environ["GITHUB_REPOSITORY"],
            "Preparation PR must belong to this repository",
        )
        head = pr["head"]["sha"]
        require(re.fullmatch(r"[0-9a-f]{40}", head), "Invalid preparation head SHA")
    output(head_sha=head)


def prepare() -> None:
    """Edit only local release files using fetched notes and optional previous PR files."""
    data = read_json("plan.json")
    version = data["version"]
    version_key(version)
    require(run("git", "rev-parse", "HEAD") == data["source"], "Source commit changed during preparation")
    require(run("uv", "version", "--short") == version, "uv version must set the requested version first")
    content = CHANGELOG.read_text(encoding="utf-8")
    original = marked(content, "unreleased")
    manual = original
    if data_file("old-manifest.json").exists():
        old = read_json("old-manifest.json")
        require(old["version"] == version, "Unexpected preparation version")
        require(re.fullmatch(r"[0-9a-f]{40}", old["source_sha"]), "Invalid previous preparation source")
        changed = set(data_file("old-files.txt").read_text(encoding="utf-8").splitlines())
        require(changed <= ALLOWED_FILES, "Preparation PR contains other changes; preserve them in a separate PR")
        edited = marked(
            marked(data_file("old-changelog.md").read_text(encoding="utf-8"), f"release:{version}"), "manual"
        )
        manual = merge_manual(original, edited, old["manual_source"])
    generated = data_file("generated-notes.md").read_text(encoding="utf-8")
    CHANGELOG.write_text(
        update_changelog(content, version, manual, generated, datetime.now(timezone.utc).date().isoformat()),
        encoding="utf-8",
    )
    manifest = {
        "version": version,
        "source_sha": data["source"],
        "previous_tag": data["previous_tag"],
        "manual_source": original,
        "prepared_by": os.environ["GITHUB_ACTOR"],
        "notes_sha256": digest(release_body(CHANGELOG.read_text(encoding="utf-8"), version).encode()),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    Path("release-preview.md").write_text(
        release_body(CHANGELOG.read_text(encoding="utf-8"), version), encoding="utf-8"
    )
    Path("release-preview.patch").write_text(run("git", "diff") + "\n", encoding="utf-8")


def check_pr() -> None:
    """Reject stale or modified release preparations using fetched PR metadata."""
    pr = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))["pull_request"]
    if MANIFEST.as_posix() not in {file["filename"] for file in read_pages("pr-files.json")}:
        return
    data = load_manifest()
    require(pr["head"]["repo"]["full_name"] == os.environ["GITHUB_REPOSITORY"], "Release PR cannot come from a fork")
    require(pr["head"]["ref"] == f"release/{data['version']}", "Unexpected release branch")
    require(
        data["source_sha"] == read_json("base-ref.json")["object"]["sha"],
        "Release preparation is stale; run Prepare release again",
    )
    verify_contents(data)


def verify(dry_run: bool) -> None:
    """Check local identity and, for production, workflow-fetched approval settings."""
    data = load_manifest()
    body = verify_contents(data)
    sha = run("git", "rev-parse", "HEAD")
    repo = os.environ["GITHUB_REPOSITORY"]
    if not dry_run:
        require(
            repo == UPSTREAM and os.environ["GITHUB_REF"] == "refs/heads/master", "Production is upstream master only"
        )
        require(os.environ["GITHUB_EVENT_NAME"] == "push", "Production must start with a merged preparation")
        parents = run("git", "show", "-s", "--format=%P", "HEAD").split()
        require(parents and parents[0] == data["source_sha"], "Preparation base changed before merge; prepare again")
        matches = [
            pr
            for pr in read_pages("merged-prs.json")
            if pr["merged_at"]
            and pr["merge_commit_sha"] == sha
            and pr["base"]["ref"] == "master"
            and pr["head"]["ref"] == f"release/{data['version']}"
            and pr["head"]["repo"]
            and pr["head"]["repo"]["full_name"] == repo
        ]
        require(len(matches) == 1, "Expected exactly one merged release preparation PR")
        settings = read_json("environment.json")
        reviewers = [rule for rule in settings["protection_rules"] if rule["type"] == "required_reviewers"]
        require(
            len(reviewers) == 1 and reviewers[0]["prevent_self_review"],
            "Enable required reviewers and prevent self-review",
        )
        logins = {r["reviewer"]["login"] for r in reviewers[0]["reviewers"] if r["type"] == "User"}
        require(logins == {"Nihisil", "Apricot-S"}, "Expected the two agreed publication reviewers")
        require(len(reviewers[0]["reviewers"]) == 2, "Only the two agreed reviewers may approve")
        require(settings["can_admins_bypass"] is False, "Disable administrator bypass")
        require(
            (settings.get("deployment_branch_policy") or {}).get("custom_branch_policies"),
            "Restrict the environment to master",
        )
        rules = read_json("branch-policies.json")["branch_policies"]
        require([(r["name"], r["type"]) for r in rules] == [("master", "branch")], "Only the master branch may deploy")
    Path("release-notes.md").write_text(body, encoding="utf-8")
    output(
        version=data["version"], sha=sha, tag=f"v{data['version']}", prerelease=str(".dev" in data["version"]).lower()
    )


def publication_state(directory: Path) -> None:
    """Check validated hashes, fetched tag refs and PyPI state without publishing."""
    data = load_manifest()
    record_data = json.loads(Path("release-artifacts.json").read_text(encoding="utf-8"))
    sha = run("git", "rev-parse", "HEAD")
    require(record_data["sha"] == sha and record_data["version"] == data["version"], "Artifact identity mismatch")
    files = file_hashes(directory, data["version"])
    require(files == record_data["files"], "Artifact hashes changed after validation")
    refs = data_file("tag-refs.txt").read_text(encoding="utf-8").splitlines()
    if refs:
        tag = f"v{data['version']}"
        resolved = {line.split()[1]: line.split()[0] for line in refs}
        require(
            resolved.get(f"refs/tags/{tag}^{{}}", resolved.get(f"refs/tags/{tag}")) == sha,
            "Existing tag points elsewhere",
        )
    state = publish_state(files, pypi_files(data["version"]))
    require(refs or state == "new", "PyPI exists without the expected tag; investigate")
    output(state=state, tag_exists=str(bool(refs)).lower())


def github_release(directory: Path) -> None:
    """Validate release creation/recovery and write the asset plan for gh commands."""
    data = load_manifest()
    files = file_hashes(directory, data["version"])
    require(publish_state(files, pypi_files(data["version"])) == "published", "PyPI publication is not complete")
    body = verify_contents(data)
    existing = [r for r in read_pages("releases.json") if r["tag_name"] == f"v{data['version']}"]
    require(len(existing) <= 1, "Multiple GitHub Releases for the same tag")
    assets = {}
    if existing:
        release = existing[0]
        require(
            not release["draft"]
            and release["body"].strip() == body.strip()
            and release["prerelease"] == (".dev" in data["version"]),
            "Existing GitHub Release differs; investigate",
        )
        assets = {asset["name"]: asset.get("digest") for asset in release["assets"]}
        require(
            all(name in files and value == f"sha256:{files[name]}" for name, value in assets.items()),
            "Existing Release assets differ",
        )
    data_file("missing-assets.json").write_text(json.dumps(sorted(files.keys() - assets.keys())), encoding="utf-8")
    Path("release-notes.md").write_text(body, encoding="utf-8")
    output(exists=str(bool(existing)).lower())


def main() -> None:
    """Run one local editing or validation operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=[
            "plan",
            "preparation-state",
            "prepare",
            "check-pr",
            "verify",
            "record",
            "publication-state",
            "github-release",
        ],
    )
    parser.add_argument("--version")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    args = parser.parse_args()
    if args.command == "plan":
        require(args.version, "--version is required")
        plan(args.version)
    elif args.command == "preparation-state":
        preparation_state()
    elif args.command == "prepare":
        prepare()
    elif args.command == "check-pr":
        check_pr()
    elif args.command == "verify":
        verify(args.dry_run)
    elif args.command == "record":
        record(args.dist)
    elif args.command == "publication-state":
        publication_state(args.dist)
    else:
        github_release(args.dist)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"Release stopped: {error}", file=sys.stderr)  # noqa: T201
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr.strip(), file=sys.stderr)  # noqa: T201
        sys.exit(1)
