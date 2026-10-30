# Releasing mahjong

Prepare each release in a PR. Publish the reviewed version to PyPI, then to GitHub.
This workflow supports version formats `X.Y.Z` and `X.Y.Z.devN`.
Releases for older maintenance series are outside its scope.

## Prerequisites

The repository administrator and PyPI project owner must maintain these settings:

- Protect `master`. Require independent review, an up-to-date PR branch and passing CI.
  Include `release-preparation` among the required checks.
- Allow GitHub Actions to create preparation PRs.
- Configure the **`pypi`** GitHub Environment to require reviewer approval.
  Prevent self-review. Disable administrator bypass.
  Restrict deployments to the **`master` branch**.

Configure a PyPI Trusted Publisher for the existing **`mahjong`** project with these values:

| Field | Value |
| --- | --- |
| Owner | `MahjongRepository` |
| Repository | `mahjong` |
| Workflow filename | `release.yml` |
| Environment | `pypi` |

See [GitHub Environment configuration](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
and [PyPI Trusted Publisher setup](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).
The workflow relies on these protections. It does not configure them or verify their settings.

## Prepare and publish

1. Choose an unused version newer than the current project version. Omit the `v` prefix.
   Run **Prepare release** from `master` with **dry-run enabled**.
   Review the preview artifact.
2. Run the workflow again with **dry-run disabled**.
   This creates the `release/{version}` branch and its preparation PR.
   The workflow updates `pyproject.toml`, `uv.lock` and `CHANGELOG.md`.
   The changelog combines hand-written `Unreleased` notes with GitHub's generated change list.
3. Review the version, lock-file diff and release notes. Edit the PR directly as needed.
   Preserve the changelog's structural comments.
   If `master` advances, update the PR branch and review the notes again.
   The workflow does not refresh the generated list automatically.
4. Approve bot-created CI runs if GitHub requests it. Obtain independent review before merging.
   Merge using a human account once all required checks pass.
   Merge commits, squash merges and rebase merges are supported.
5. **Release** validates and builds the merged commit.
   A maintainer other than the person who merged the PR must review the results and the
   **identify** job summary. That maintainer then approves the **`pypi`** deployment.
   After approval, the workflow creates the `v{version}` tag.
   It publishes the validated files to PyPI, then creates the GitHub Release.
   The GitHub Release uses the reviewed notes and the same files.
6. Check the PyPI version, GitHub Release notes, attached files and prerelease/Latest flags.

Keep only one preparation PR open. The preparation workflow does not update an existing PR
or overwrite its branch. To start over, first save any edits you want to keep.
Then close the old PR and delete its branch.

Do not push version changes directly to `master`. Do not merge several release preparations together.
A push to `master` starts Release if it changes `pyproject.toml`.
Release skips validation and publication successfully if the project version is unchanged.

## Dev releases

For example, a release sequence is `2.2.0.dev1`, `2.2.0.dev2`, then `2.2.0`.
Dev releases publish to **production PyPI**. They follow the same review and approval process
as stable releases. Dev GitHub Releases are prereleases and are excluded from Latest.
Stable Releases are marked Latest.

Dev notes compare against the preceding supported tag.
Stable notes compare against the preceding stable tag.
They include changes made during dev releases.
Hand-written notes remain in `Unreleased` until stable release preparation.
If you edit dev notes that should carry into the stable release, update `Unreleased` too.

## Dry-run

Manually running **Release** is always a dry-run, including upstream.
Select a prepared branch with matching project/lock versions and a changelog section.
The workflow validates and builds the release. It does not create a tag, publish to PyPI or
create a GitHub Release. Forks can also run preparation workflows and Release dry-runs.
Production publication requires a push to upstream `master`.

## Failed releases

Automatic recovery is not provided. Keep the original run, merged commit and validated artifacts.
Do not blindly rerun publication once a tag or upload exists.

| State | Action |
| --- | --- |
| Validation failed before a tag or upload | Retry checks that failed because of transient errors. For code fixes, use a reviewed PR. Then prepare a new version. |
| PyPI publication succeeded but the GitHub Release is missing | Create the GitHub Release from the original run's notes and files. Set the appropriate prerelease/Latest flags. Do not repeat the PyPI upload. |
| Partial publication or inconsistent release state | Investigate with the owner before completing publication or issuing a new version. Do not move existing tags. Do not use `--skip-existing` to hide mismatches. |

Use the original validated files for recovery. Do not replace them with a local rebuild.
If the artifacts have expired, agree on a recovery plan with the owner.
PyPI files cannot be replaced under an existing filename.
Yanking and emergency publication require owner coordination and independent approval.
