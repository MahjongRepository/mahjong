"""Prepare release files and check their versions; remote operations live in workflows."""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

CHANGELOG = Path("CHANGELOG.md")
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


def version_key(version: str) -> tuple[int, int, int, int, int]:
    """Order the canonical stable and dev versions supported by this workflow."""
    match = VERSION.fullmatch(version)
    require(match, "Expected X.Y.Z or X.Y.Z.devN with no leading zeroes")
    assert match is not None
    major, minor, patch, dev = match.groups()
    return int(major), int(minor), int(patch), int(dev is None), int(dev or 0)


def marked(text: str, name: str) -> str:
    """Read exactly one explicitly delimited block."""
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    require(text.count(start) == text.count(end) == 1, f"Expected one {name} block")
    require(text.index(start) < text.index(end), f"Invalid {name} block order")
    return text.split(start, 1)[1].split(end, 1)[0].strip()


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


def output(**values: object) -> None:
    """Expose validated single-line values to the workflow."""
    if "GITHUB_OUTPUT" in os.environ:
        with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as stream:
            for key, value in values.items():
                require("\n" not in str(value), "Multiline workflow output")
                stream.write(f"{key}={value}\n")
    print(json.dumps(values))


def project_version() -> str:
    """Read the canonical version from the project metadata."""
    version = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    version_key(version)
    return version


def check_contents() -> str:
    """Check the lock file and changelog against the project version."""
    version = project_version()
    packages = tomllib.loads(Path("uv.lock").read_text(encoding="utf-8"))["package"]
    versions = [package["version"] for package in packages if package["name"] == "mahjong"]
    require(versions == [version], "Lock file version differs")
    return release_body(CHANGELOG.read_text(encoding="utf-8"), version)


def check_change(base: str) -> bool:
    """Validate version changes; ordinary PRs do not need release metadata."""
    require(re.fullmatch(r"[0-9a-f]{40}", base), "Expected a base commit SHA")
    old = tomllib.loads(run("git", "show", f"{base}:pyproject.toml"))["project"]["version"]
    version = project_version()
    if old == version:
        return False
    require(version_key(version) > version_key(old), "Version must increase")
    check_contents()
    return True


def previous_tag(version: str) -> str:
    """Stable notes always start at the previous stable tag, including all dev changes."""
    tags = run("git", "tag", "--merged", "HEAD", "--list", "v*").splitlines()
    candidates = [tag for tag in tags if VERSION.fullmatch(tag[1:]) and version_key(tag[1:]) < version_key(version)]
    if ".dev" not in version:
        candidates = [tag for tag in candidates if ".dev" not in tag]
    require(candidates, "No previous release tag found")
    return max(candidates, key=lambda tag: version_key(tag[1:]))


def plan(version: str) -> None:
    """Validate the requested version and select the notes comparison tag."""
    require(version_key(version) > version_key(project_version()), "Version must increase")
    require(not run("git", "tag", "--list", f"v{version}"), "Tag already exists")
    output(version=version, branch=f"release/{version}", previous_tag=previous_tag(version))


def prepare(version: str, notes: Path) -> None:
    """Create the initial release notes for the requested project version."""
    require(project_version() == version, "Set the requested project version first")
    content = CHANGELOG.read_text(encoding="utf-8")
    manual = marked(content, "unreleased")
    CHANGELOG.write_text(
        update_changelog(
            content, version, manual, notes.read_text(encoding="utf-8"), datetime.now(timezone.utc).date().isoformat()
        ),
        encoding="utf-8",
    )
    body = check_contents()
    Path("release-preview.md").write_text(body, encoding="utf-8")
    Path("release-preview.patch").write_text(run("git", "diff") + "\n", encoding="utf-8")


def verify(base: str | None) -> None:
    """Identify a release and write the reviewed notes for publication."""
    if base is not None and not check_change(base):
        output(release="false")
        return
    body = check_contents()
    version = project_version()
    sha = run("git", "rev-parse", "HEAD")
    Path("release-notes.md").write_text(body, encoding="utf-8")
    output(release="true", version=version, sha=sha, tag=f"v{version}", prerelease=str(".dev" in version).lower())
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a", encoding="utf-8") as stream:
            stream.write(f"## Release {version}\n\nCommit: `{sha}`\n\n{body}")


def main() -> None:
    """Run one local preparation or validation operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "prepare", "check-pr", "verify"])
    parser.add_argument("--version")
    parser.add_argument("--notes", type=Path)
    parser.add_argument("--base")
    args = parser.parse_args()
    match args.command:
        case "plan":
            require(args.version, "--version is required")
            plan(args.version)
        case "prepare":
            require(args.version and args.notes, "--version and --notes are required")
            prepare(args.version, args.notes)
        case "check-pr":
            require(args.base, "--base is required")
            check_change(args.base)
        case "verify":
            verify(args.base)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"Release stopped: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr.strip(), file=sys.stderr)
        sys.exit(1)
