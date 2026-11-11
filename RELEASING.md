# Releasing mahjong

Prepare each release in a PR. Publish the reviewed version to PyPI, then to GitHub.
This workflow supports version formats `X.Y.Z` and `X.Y.Z.devN`.
Releases for older maintenance series are outside its scope.

## Prerequisites

The repository administrator and PyPI project owner must maintain these settings:

- Protect `master` with the ruleset settings below.
- Allow GitHub Actions to create preparation PRs.
  In **Settings → Actions → General → Workflow permissions**,
  enable **Allow GitHub Actions to create and approve pull requests** and click **Save**.
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

### Protect `master` with a branch ruleset

In **Settings → Rulesets → Rulesets**, create or edit a branch ruleset targeting `master`.
Set **Enforcement status** to **Active**. Enable the following parent rules to reveal
their sub-options:

1. **Require a pull request before merging**:
   - Set **Required approvals** to **1** or more.
   - Enable **Require approval of the most recent reviewable push**. The latest push
     must be approved by someone other than the person who pushed it; GitHub also
     prevents PR authors from approving their own PRs.
   - Optionally enable **Dismiss stale pull request approvals when new commits are pushed**
     to require a new review after further changes.
2. **Require status checks to pass**:
   - Enable **Require branches to be up to date before merging**.
   - Use **Add checks** to require `release-preparation`.
     If it is unavailable, open or update a PR containing `.github/workflows/check_release.yml`
     so the check runs, then return to add it.

Only require other CI checks if they run for every PR targeting `master`.
The current lint, test, documentation and distribution workflows use path filters;
requiring their checks can leave unrelated PRs blocked with pending checks.
See [GitHub's guidance on skipped required checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks#handling-skipped-but-required-checks).

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
   It uses `pypa/gh-action-pypi-publish` with Trusted Publishing to generate PEP 740
   publish attestations and upload them with the validated files to PyPI.
   It then creates the GitHub Release using the reviewed notes and the same wheel and sdist files.
6. Check the PyPI version and provenance attestations, GitHub Release notes, attached files
   and prerelease/Latest flags.

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
The workflow validates and builds the release. It does not generate publish attestations,
create a tag, publish to PyPI or create a GitHub Release.
Forks can also run preparation workflows and Release dry-runs.
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
