# Releasing mahjong

Maintainers prepare releases in a PR, then publish the reviewed version to PyPI and GitHub.
Supported versions are `X.Y.Z` and `X.Y.Z.devN`; older maintenance series are outside this workflow.

## Prerequisites

The repository administrator and PyPI project owner must maintain these settings:

- Protect `master` with independent review, an up-to-date branch and passing CI, including
  `release-preparation`. Allow GitHub Actions to create preparation PRs.
- Configure the **`pypi`** GitHub Environment with required reviewers, self-review prevention,
  administrator bypass disabled and deployment restricted to the **`master` branch**.
- Configure a PyPI Trusted Publisher for the existing **`mahjong`** project:

  | Field | Value |
  | --- | --- |
  | Owner | `MahjongRepository` |
  | Repository | `mahjong` |
  | Workflow filename | `release.yml` |
  | Environment | `pypi` |

See [GitHub Environment configuration](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
and [PyPI Trusted Publisher setup](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).
The workflow relies on these protections; it does not configure them or verify their settings.

## Prepare and publish

1. From `master`, run **Prepare release** with an unused version newer than the current project
   version, without a `v` prefix. Start with **dry-run enabled** and review its preview artifact.
2. Run again with **dry-run disabled** to create `release/{version}` and its preparation PR.
   The workflow updates `pyproject.toml`, `uv.lock` and `CHANGELOG.md`, combining hand-written
   `Unreleased` notes with GitHub's generated change list.
3. Review the version, lock-file diff and release notes. Edit the PR directly as needed, keeping
   the changelog's structural comments intact. If `master` advances, update the branch and review
   the notes again; the generated list is not refreshed automatically.
4. Approve bot-created CI runs if GitHub requests it. Obtain independent review and merge using
   a human account when all required checks pass. Merge, squash and rebase are supported.
5. **Release** validates and builds the merged commit. A different maintainer reviews the results
   and the **identify** job summary, then approves the **`pypi`** deployment. After approval, the
   workflow creates `v{version}`, publishes the validated files to PyPI, then creates the GitHub
   Release with the reviewed notes and the same files.
6. Check the PyPI version, GitHub Release notes, attached files and prerelease/Latest flags.

Only one preparation PR should be open. Preparation does not update an existing PR or overwrite
its branch. To start over, save any needed edits, close the old PR and remove its branch first.

Do not directly push version changes to `master` or merge several release preparations together.
A `master` push changing `pyproject.toml` starts Release; if the version is unchanged, it skips
release validation and publication successfully.

## Dev releases

For example, release `2.2.0.dev1`, then `2.2.0.dev2`, then `2.2.0`. Dev releases use **production PyPI**,
follow the same review and approval process, and are GitHub prereleases excluded from Latest.
Stable Releases are Latest.

Dev notes compare against the preceding supported tag; stable notes compare against the preceding
stable tag, including changes made during dev releases. Hand-written notes remain in `Unreleased`
until stable preparation. If editing dev notes that should carry into stable, update `Unreleased` too.

## Dry-run

Manually running **Release** is always a dry-run, including upstream. Select a prepared branch
with matching project/lock versions and a changelog section. It validates and builds without
creating a tag, publishing to PyPI or creating a GitHub Release. Forks can also run preparation
and Release dry-runs; production publication is restricted to upstream `master` pushes.

## Failed releases

Automatic recovery is not provided. Keep the original run, merged commit and validated artifacts.
Do not blindly rerun publication once a tag or upload exists, or substitute a local rebuild.

| State | Action |
| --- | --- |
| Validation failed before a tag or upload | Retry transient failed checks. For code fixes, use a reviewed PR and prepare a new version. |
| PyPI publication succeeded, GitHub Release is missing | Create the GitHub Release from the original run's notes and files, with the appropriate prerelease/Latest flags. Do not repeat the PyPI upload. |
| A tag, PyPI upload or GitHub Release is partial or inconsistent | Investigate with the owner before completing publication or issuing a new version. Do not move existing tags or mask mismatches with `--skip-existing`. |

Use the original validated files for recovery. If they have expired, agree on a recovery plan with
the owner. PyPI files cannot be replaced under an existing filename; yanking and emergency
publication require owner coordination and independent approval.
