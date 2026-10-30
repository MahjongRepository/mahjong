# Releasing mahjong

Releases are prepared in a pull request, built and validated after merging, approved by a second
maintainer, then published to PyPI before the GitHub Release is published. Supported versions are
`X.Y.Z` and `X.Y.Z.devN`. Maintenance releases for older series and other prerelease formats are
outside this workflow's initial scope.

## Implementation responsibilities

GitHub and network operations are visible as individual workflow steps. Python only edits local
release files, reads fetched snapshots and validates release state; it never invokes `gh`, makes
HTTP requests, pushes a branch/tag, or creates a pull request or Release.

| Responsibility | Implementation |
| --- | --- |
| Fetch releases, PRs, refs and Environment settings | Workflow `gh api` steps |
| Generate the change list | Workflow `gh api .../releases/generate-notes` |
| Read PyPI metadata | Workflow `curl` steps; only HTTP 404 is treated as absent |
| Update package/lock versions | Workflow `uv version --no-sync <version>` |
| Edit changelog and validate metadata/artifact hashes | `scripts/release.py`, using local files |
| Commit/push the preparation and create its PR | Workflow `git` and `gh pr create` steps |
| Create the immutable version tag | Workflow `git tag` and `git push` steps |
| Upload the validated distributions | Workflow `uv publish` step |
| Create the GitHub Release or attach missing assets on retry | Workflow `gh release create/upload` steps |

The snapshots live in a temporary directory on each Ubuntu runner. Python writes the validated
identifiers and decisions to step outputs and emits a list of missing assets; the workflow uses
those results for subsequent commands. Preparation dry-run skips commit/push/PR steps. Release
dry-run skips the entire publishing job. Moving commands into YAML does not remove the validation
or approval gates, but it makes the workflow longer and exposes the sequence of remote operations
directly in the Actions log.

## One-time setup (repository administrator and PyPI project owner)

Configure these settings **before merging the first release preparation PR**. The implementation
does not configure them automatically. GitHub repository permissions and PyPI project roles are
independent. A collaborator can implement the workflows and approve releases without owning the
PyPI project.

1. In `MahjongRepository/mahjong`, create the GitHub Environment **`pypi`**:
   - Required reviewers: **`Nihisil`** and **`Apricot-S`**.
   - Enable **Prevent self-review**. One eligible reviewer approves; both approvals are not required.
   - Disable **Allow administrators to bypass configured protection rules**.
   - Restrict deployment branches to **`master`**. The workflow runs on the merged branch, even
     though it creates a tag later; do not restrict this environment to tags only.
2. In the existing PyPI **`mahjong`** project's **Manage → Publishing**, add a GitHub Trusted Publisher:

   | Field | Value |
   | --- | --- |
   | Owner | `MahjongRepository` |
   | Repository | `mahjong` |
   | Workflow filename | `release.yml` |
   | Environment | `pypi` |

   Register the top-level workflow, not a reusable build workflow. No PyPI API token is required.
3. Allow GitHub Actions to create pull requests in **Settings → Actions → General**. Organization
   policy may also need to allow this. The preparation workflow uses `GITHUB_TOKEN`, not a PAT.
   GitHub may require a maintainer to approve CI runs created by the bot's PR events. Confirm this
   behavior on the repository before the first release and approve those runs when requested.
4. Protect `master`: require review by someone other than the PR author, dismiss stale approvals,
   require the branch to be current before merging, and require the relevant existing CI checks
   plus **`release-preparation`**. Review workflow and release-tool changes carefully.
   The publication workflow also rejects a release whose source is not the merge's first parent.
5. Confirm the two maintainers can review deployments and test approval/rejection on a separate
   non-publishing test environment. For a merge-triggered release, GitHub's self-review restriction
   applies to the person who initiated the publication run (normally the person who merged), not
   necessarily the person who originally ran Prepare release. Do not auto-merge preparation PRs
   with a bot: retain a human merge and independent publication approval.
6. Review old PyPI tokens, other Trusted Publishers and manual publication access. They are separate
   publishing paths that this workflow cannot restrict. Agree on retiring unnecessary credentials
   or documenting an emergency procedure; do not revoke them before the replacement is validated.

The workflow checks the two reviewers, self-review prevention and administrator bypass settings
before building a production release. Repository protections still need to be configured and
maintained by the administrator; Trusted Publishing does not review package contents.

References: [GitHub environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments),
[Trusted Publisher setup](https://docs.pypi.org/trusted-publishers/adding-a-publisher/),
[workflow trigger behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## Prepare and review

1. Optionally write important changes and deprecation notices between the `unreleased` markers in
   `CHANGELOG.md` in ordinary PRs. These entries remain editable during release review.
2. From `master`, manually run **Prepare release**, supplying the full version, for example
   `2.2.0.dev1`. Start with **dry-run enabled** to inspect the preview artifact. Dry-run updates only
   the disposable checkout; it creates no branch, PR, tag, Release or PyPI upload.
3. Run again with **dry-run disabled** to open `release/{version}` against `master`. The workflow
   uses `uv version --no-sync <version>` to update `pyproject.toml` and `uv.lock`, retains existing
   dependency pins, generates release notes via GitHub's API, and records the source commit.
   Only one preparation PR should be open at a time.
4. Review the version, lock-file diff, hand-written explanations and generated list. The date in
   the changelog is the preparation date in UTC, not a promise of the eventual publication date.
   Prior history is preserved. Do not edit structural marker comments or the release manifest.
5. If you edit manual explanations in the preparation PR, run Prepare release again with the same
   version to record the updated notes. Refresh also if `master` advances. Refresh replaces the
   generated list while preserving manual edits; conflicting edits to manual notes on both branches
   stop the workflow and must be reconciled explicitly. Edits to the generated list are replaced
   on refresh; place enduring explanations in the target version's manual block. Unrelated code
   changes on the preparation branch stop refresh rather than being silently discarded.
6. Approve bot-triggered CI runs if GitHub requests it. Review the final refreshed PR and merge it
   with a human account only when all required checks pass. Do not use a branch-update button to
   resolve a stale preparation: regenerate it from the current `master` instead.

Version inputs are canonical stable or dev versions, with no `v` prefix or leading zeroes. They must
advance the current package version. Existing tags, GitHub Releases and PyPI distributions are
rejected during preparation. The tag format is `v{version}`.

### Dev releases and the eventual stable release

For example, prepare `2.2.0.dev1`, then `2.2.0.dev2`, then `2.2.0`. Each follows the same checks and
approval and publishes to **production PyPI**. Dev GitHub Releases are marked prerelease and are
explicitly excluded from Latest. Stable Releases are marked Latest.

Dev notes compare against the preceding supported release tag reachable from the source commit.
Stable notes always compare against the preceding **stable** tag, so they include all changes made
during dev releases. Hand-written notes remain in `Unreleased` during dev releases and are cleared
only when preparing a stable release. Previous dev release sections are preserved.

## Validate, approve and publish

Merging the preparation PR starts **Release**. It verifies the preparation PR identity and source
commit, then runs the existing lint/type/test matrix, a strict documentation build without deploying,
and wheel/sdist validation on three operating systems. All reusable workflows check out the same
merged SHA. Path filters on ordinary CI do not skip these release checks.

The **validated** job records the exact distribution names and SHA-256 hashes and shows the version,
source and merge commits, preparer and final notes in its job summary. Before approving `pypi`, check
this summary, the merged preparation PR and all validation jobs. Reject unexpected results.

After approval, the workflow verifies those same distribution files, creates the tag without moving
an existing tag, uploads to PyPI using Trusted Publishing, verifies the uploaded hashes, and creates
the GitHub Release with the reviewed notes and the same files. The publication job does not rebuild
the package. Publication runs are serialized and are not canceled by newer runs.

## Dry-run and initial validation

Manually dispatching **Release** is **always a dry-run**, even in upstream: it performs identification,
builds and checks, and records artifacts, but never enters the publication job. Dispatch it on a
prepared branch containing `.github/release.json`. An ordinary implementation branch has no release
manifest and cannot be treated as a prepared release.

Forks may exercise preparation and Release dry-runs but cannot enter production publication. The
preparation workflow accepts the fork's default branch to allow an isolated rehearsal. Creating a
fork preparation PR is a write operation and is separate from preparation dry-run. No Trusted
Publisher should be configured for the fork against the production `mahjong` project.

Before the first production dev release:

- Validate preparation, refresh and the full non-publishing flow in the fork.
- Have the administrator complete the settings above and verify independent approval behavior.
- Review and merge the implementation upstream, then prepare the agreed dev version if unused.
- Review its preparation PR and independently approve publication.
- Install that exact version from PyPI in a fresh environment and run the distribution smoke check.
- Verify that GitHub Release publication followed PyPI, and check prerelease/Latest flags and assets.

## Recovery

Use **Re-run failed jobs** on the original Release run to retain the successful build artifacts and
validation record. Do not prepare a fresh run from the current `master` as a substitute. Approval is
still required when the publication job runs again. Artifact retention/expiry is visible in the run;
if artifacts have expired, stop and investigate rather than replacing them with an unreviewed build.
Artifact names include the attempt number; downstream jobs use immutable IDs, including when a
retry reuses successful build jobs from an earlier attempt.

| State | Action |
| --- | --- |
| Validation failed, no tag/upload | Fix the problem, refresh/review the preparation if needed; do not bypass failed checks. |
| Tag exists, PyPI absent | Retry failed jobs using the original artifacts; the existing tag must resolve to the same SHA. |
| Both PyPI files match exactly, GitHub Release absent | Retry failed jobs; PyPI upload is skipped and the Release is created. |
| GitHub Release exists with only some assets | Retry failed jobs; matching existing assets are kept and missing assets are uploaded. |
| PyPI has only some files, extra files, or different hashes | Automatic retry stops. Investigate with the project owner; do not use `--skip-existing` to hide a mismatch. |
| Tag, Release notes, flags or existing asset hashes differ | Automatic retry stops. Investigate rather than overwriting published state. |

PyPI versions cannot be replaced by uploading different contents under the same file name. For a
bad release, agree on yanking it and issuing a new version (for example the next dev number).
Old token-based `make build-and-release` is removed; do not work around the review/approval flow by
uploading a local build. Configuration changes, yanking and emergency publication remain owner-led
operations and are not automated by these workflows.

If an outdated preparation was merged despite the required checks, publication stops before creating
a tag. Revert that preparation in a reviewed PR, reconcile any manual notes, then prepare the version
again. Do not bypass the source-commit check or manually edit its manifest to claim a different base.
