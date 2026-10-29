"""Prepare and verify releases; all remote writes require an explicit command."""

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
from urllib.error import HTTPError
from urllib.request import urlopen

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


def api(path: str, data: dict[str, Any] | None = None, method: str | None = None) -> Any:  # noqa: ANN401
    """Call GitHub using the job's token without placing it in command arguments."""
    args = ["gh", "api", path, "--method", method or ("POST" if data is not None else "GET")]
    if data is not None:
        args.extend(["--input", "-"])
    result = run(*args, input_text=json.dumps(data) if data is not None else None)
    return json.loads(result) if result else None


def pages(path: str) -> list[dict[str, Any]]:
    """Read every page of a list endpoint."""
    result = json.loads(run("gh", "api", path, "--paginate", "--slurp"))
    return [item for page in result for item in page]


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


def pypi_files(version: str) -> dict[str, str]:
    """Read the existing file names and hashes without downloading or executing packages."""
    version_key(version)
    try:
        with urlopen(f"https://pypi.org/pypi/mahjong/{version}/json", timeout=30) as response:
            data = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return {}
        raise
    return {item["filename"]: item["digests"]["sha256"] for item in data["urls"]}


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


def prepare(version: str, dry_run: bool) -> None:
    """Generate changes locally, then explicitly create or update the preparation PR."""
    version_key(version)
    repo = os.environ["GITHUB_REPOSITORY"]
    base = "master" if repo == UPSTREAM else api(f"repos/{repo}")["default_branch"]
    require(os.environ["GITHUB_REF"] == f"refs/heads/{base}", "Run preparation from the default branch")
    require(not run("git", "status", "--porcelain", "--untracked-files=no"), "Checkout must be clean")
    require(version_key(version) > version_key(run("uv", "version", "--short")), "Version must increase")
    require(not run("git", "tag", "--list", f"v{version}"), "Tag already exists")
    require(not pypi_files(version), "Version already exists on PyPI")
    releases = pages(f"repos/{repo}/releases?per_page=100")
    require(not any(r["tag_name"] == f"v{version}" for r in releases), "GitHub Release already exists")
    branch = f"release/{version}"
    prs = pages(f"repos/{repo}/pulls?state=open&base={base}&per_page=100")
    preparations = [pr for pr in prs if pr["head"]["ref"].startswith("release/")]
    require(all(pr["head"]["ref"] == branch for pr in preparations), "Another release preparation PR is open")
    require(len(preparations) <= 1, "Multiple preparation PRs found")
    source = run("git", "rev-parse", "HEAD")
    content = CHANGELOG.read_text(encoding="utf-8")
    original = marked(content, "unreleased")
    manual = original
    expected_head = ""
    if preparations:
        pr = preparations[0]
        require(pr["head"]["repo"]["full_name"] == repo, "Preparation PR must belong to this repository")
        expected_head = pr["head"]["sha"]
        run("git", "fetch", "origin", expected_head)
        old = json.loads(run("git", "show", f"{expected_head}:{MANIFEST.as_posix()}"))
        require(old["version"] == version, "Unexpected preparation version")
        edited = marked(marked(run("git", "show", f"{expected_head}:CHANGELOG.md"), f"release:{version}"), "manual")
        manual = merge_manual(original, edited, old["manual_source"])
    tag = previous_tag(version)
    generated = api(
        f"repos/{repo}/releases/generate-notes",
        {
            "tag_name": f"v{version}",
            "previous_tag_name": tag,
            "target_commitish": source,
        },
    )["body"]
    run("uv", "version", "--no-sync", version)
    CHANGELOG.write_text(
        update_changelog(content, version, manual, generated, datetime.now(timezone.utc).date().isoformat()),
        encoding="utf-8",
    )
    data = {
        "version": version,
        "source_sha": source,
        "previous_tag": tag,
        "manual_source": original,
        "prepared_by": os.environ["GITHUB_ACTOR"],
        "notes_sha256": digest(release_body(CHANGELOG.read_text(encoding="utf-8"), version).encode()),
    }
    MANIFEST.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    Path("release-preview.md").write_text(
        release_body(CHANGELOG.read_text(encoding="utf-8"), version), encoding="utf-8"
    )
    Path("release-preview.patch").write_text(run("git", "diff") + "\n", encoding="utf-8")
    if dry_run:
        output(version=version, source=source, mode="dry-run")
        return
    run("git", "switch", "-c", branch)
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run("git", "add", *sorted(ALLOWED_FILES))
    run("git", "commit", "-m", f"chore: prepare release {version}")
    run("git", "push", f"--force-with-lease=refs/heads/{branch}:{expected_head}", "origin", f"HEAD:refs/heads/{branch}")
    if preparations:
        url = preparations[0]["html_url"]
    else:
        url = api(
            f"repos/{repo}/pulls",
            {
                "title": f"chore: prepare release {version}",
                "head": branch,
                "base": base,
                "body": "Review the version, manual notes and generated changes. "
                "Refresh this PR if its base changes.\n\n"
                "M04: https://github.com/MahjongRepository/mahjong/issues/333",
            },
        )["html_url"]
    output(version=version, source=source, pr=url)


def check_pr() -> None:
    """Reject stale or modified release preparations before they can be merged."""
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    pr = event["pull_request"]
    repo = os.environ["GITHUB_REPOSITORY"]
    files = pages(f"repos/{repo}/pulls/{pr['number']}/files?per_page=100")
    if MANIFEST.as_posix() not in {f["filename"] for f in files}:
        return
    data = load_manifest()
    require(pr["head"]["repo"]["full_name"] == repo, "Release PR cannot come from a fork")
    require(pr["head"]["ref"] == f"release/{data['version']}", "Unexpected release branch")
    base = api(f"repos/{repo}/git/ref/heads/{pr['base']['ref']}")["object"]["sha"]
    require(data["source_sha"] == base, "Release preparation is stale; run Prepare release again")
    verify_contents(data)


def verify(dry_run: bool) -> None:
    """Resolve the release identity before granting any publishing permissions."""
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
        prs = pages(f"repos/{repo}/commits/{sha}/pulls?per_page=100")
        matches = [
            pr
            for pr in prs
            if pr["merged_at"]
            and pr["merge_commit_sha"] == sha
            and pr["base"]["ref"] == "master"
            and pr["head"]["ref"] == f"release/{data['version']}"
            and pr["head"]["repo"]
            and pr["head"]["repo"]["full_name"] == repo
        ]
        require(len(matches) == 1, "Expected exactly one merged release preparation PR")
        settings = api(f"repos/{repo}/environments/pypi")
        reviewers = [rule for rule in settings["protection_rules"] if rule["type"] == "required_reviewers"]
        require(
            len(reviewers) == 1 and reviewers[0]["prevent_self_review"],
            "Enable required reviewers and prevent self-review",
        )
        logins = {reviewer["reviewer"]["login"] for reviewer in reviewers[0]["reviewers"] if reviewer["type"] == "User"}
        require(logins == {"Nihisil", "Apricot-S"}, "Expected the two agreed publication reviewers")
        require(len(reviewers[0]["reviewers"]) == 2, "Only the two agreed reviewers may approve")
        require(settings["can_admins_bypass"] is False, "Disable administrator bypass")
        policy = settings.get("deployment_branch_policy") or {}
        require(policy.get("custom_branch_policies"), "Restrict the environment to master")
        rules = api(f"repos/{repo}/environments/pypi/deployment-branch-policies")["branch_policies"]
        require(
            [(rule["name"], rule["type"]) for rule in rules] == [("master", "branch")],
            "Only the master branch may deploy",
        )
    Path("release-notes.md").write_text(body, encoding="utf-8")
    output(
        version=data["version"], sha=sha, tag=f"v{data['version']}", prerelease=str(".dev" in data["version"]).lower()
    )


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


def publication_state(directory: Path) -> None:
    """Check immutable artifacts, an existing tag and PyPI before upload or retry."""
    data = load_manifest()
    record_data = json.loads(Path("release-artifacts.json").read_text(encoding="utf-8"))
    sha = run("git", "rev-parse", "HEAD")
    require(record_data["sha"] == sha and record_data["version"] == data["version"], "Artifact identity mismatch")
    local = file_hashes(directory, data["version"])
    require(local == record_data["files"], "Artifact hashes changed after validation")
    tag = f"v{data['version']}"
    refs = run("git", "ls-remote", "origin", f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}").splitlines()
    if refs:
        resolved = {line.split()[1]: line.split()[0] for line in refs}
        require(
            resolved.get(f"refs/tags/{tag}^{{}}", resolved.get(f"refs/tags/{tag}")) == sha,
            "Existing tag points elsewhere",
        )
    state = publish_state(local, pypi_files(data["version"]))
    if not refs:
        require(state == "new", "PyPI exists without the expected tag; investigate")
        run("git", "tag", tag, sha)
        run("git", "push", "origin", f"refs/tags/{tag}")
    output(state=state)


def github_release(directory: Path) -> None:
    """Publish reviewed notes and the same files only after verifying PyPI success."""
    data = load_manifest()
    files = file_hashes(directory, data["version"])
    require(publish_state(files, pypi_files(data["version"])) == "published", "PyPI publication is not complete")
    repo = os.environ["GITHUB_REPOSITORY"]
    tag = f"v{data['version']}"
    body = verify_contents(data)
    existing = [r for r in pages(f"repos/{repo}/releases?per_page=100") if r["tag_name"] == tag]
    prerelease = ".dev" in data["version"]
    if existing:
        release = existing[0]
        require(
            not release["draft"] and release["body"].strip() == body.strip() and release["prerelease"] == prerelease,
            "Existing GitHub Release differs; investigate",
        )
        assets = {asset["name"]: asset.get("digest") for asset in release["assets"]}
        require(
            all(name in files and value == f"sha256:{files[name]}" for name, value in assets.items()),
            "Existing Release assets differ",
        )
        missing = files.keys() - assets.keys()
        if missing:
            run("gh", "release", "upload", tag, "--repo", repo, *(str(directory / name) for name in sorted(missing)))
        return
    Path("release-notes.md").write_text(body, encoding="utf-8")
    args = [
        "gh",
        "release",
        "create",
        tag,
        "--repo",
        repo,
        "--verify-tag",
        "--title",
        tag,
        "--notes-file",
        "release-notes.md",
        "--latest=false" if prerelease else "--latest",
    ]
    if prerelease:
        args.append("--prerelease")
    run(*args, *(str(directory / name) for name in files))


def main() -> None:
    """Dispatch one explicit release operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=["prepare", "check-pr", "verify", "record", "publication-state", "github-release"]
    )
    parser.add_argument("--version")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    args = parser.parse_args()
    if args.command == "prepare":
        require(args.version, "--version is required")
        prepare(args.version, args.dry_run)
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
        sys.exit(1)
