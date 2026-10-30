# Releasing mahjong

A manual workflow creates a preparation PR. After review and merge, the release workflow builds
and tests the merged commit, waits for independent approval, then creates a tag, publishes to PyPI
and creates the GitHub Release. Supported versions are `X.Y.Z` and `X.Y.Z.devN`. Older maintenance
series and other prerelease formats are outside the initial scope.

## Responsibilities

Workflow steps handle GitHub operations with `gh`, version updates with `uv version --no-sync`,
Git pushes and Trusted Publishing with `uv publish`. `scripts/release.py` only edits local notes
and checks versions and changelog structure. It never makes network requests or publishes.

`pyproject.toml` is the source of the release version. A `master` push changing this file starts
Release, which compares its version before and after the push. If the version is unchanged (for
example, a dependency update), release validation and publication jobs are skipped successfully.
Reviewed notes in the merged commit are used verbatim, excluding structural comments.

## One-time setup (repository administrator and PyPI project owner)

Complete these settings **before merging the first preparation PR**. GitHub repository permissions
and PyPI project roles are independent; the owner should configure the settings they control.

1. Create the GitHub Environment **`pypi`** in `MahjongRepository/mahjong`:
   - Required reviewers: **`Nihisil`** and **`Apricot-S`**. One reviewer approves, not both.
   - Enable **Prevent self-review**.
   - Disable **Allow administrators to bypass configured protection rules**.
   - Allow deployments only from the **`master` branch**, not tags. The job runs on the merged
     branch and creates the tag later.
2. In the existing PyPI **`mahjong`** project's **Manage → Publishing**, add a Trusted Publisher:

   | Field | Value |
   | --- | --- |
   | Owner | `MahjongRepository` |
   | Repository | `mahjong` |
   | Workflow filename | `release.yml` |
   | Environment | `pypi` |

   Register the top-level workflow. No PyPI API token is needed.
3. Allow GitHub Actions to create PRs in **Settings → Actions → General**, including any required
   organization policy. Preparation uses `GITHUB_TOKEN`, not a PAT. Approve bot-created PR CI runs
   if GitHub requests it; confirm this behavior before the first release.
4. Protect `master`: require independent PR review, dismiss stale approvals, require an up-to-date
   branch and the relevant existing CI checks plus **`release-preparation`**. Review workflow and
   release-tool changes carefully. Only merge the reviewed preparation PR to start a release;
   do not directly push version changes to `master`.
5. Verify independent deployment approval on a separate non-publishing test environment.
   Self-review prevention applies to the workflow initiator, normally the person who merged the
   preparation PR. Use a human merge and a different maintainer's publication approval.
6. Review older PyPI tokens and other publishing paths with the owner. Retire unnecessary
   credentials only after the replacement is validated, or document their emergency use.

The workflow relies on these repository and Environment protections. It does not inspect their
configuration through the API on every release. The administrator must maintain them.

References: [GitHub environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments),
[Trusted Publishers](https://docs.pypi.org/trusted-publishers/adding-a-publisher/),
[workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## Prepare and review

1. Optionally add important changes and deprecations between the `unreleased` markers in
   `CHANGELOG.md` in ordinary PRs.
2. On `master`, run **Prepare release** with a full version such as `2.2.0.dev1`, initially with
   **dry-run enabled**. Inspect its preview artifact. This only changes the disposable checkout.
3. Run with **dry-run disabled** to create `release/{version}` and open its preparation PR.
   The workflow updates `pyproject.toml` and `uv.lock`, generates the change list with GitHub's
   Release Notes API and combines it with the hand-written notes. Existing dependency pins remain.
   The changelog date is the UTC preparation date.
4. Review and edit the PR directly, including the generated list if necessary. Keep structural
   marker comments intact and keep the version identical in the project and lock file.
   Preparation never updates an existing PR or replaces its branch; another open preparation PR
   or an existing same-name branch causes it to stop.
5. If `master` advances, update the PR branch normally, resolve conflicts and review the resulting
   notes and CI. Refresh the generated list manually if new changes belong in the release; use the
   same `previous_tag_name` policy described below. The workflow does not check that the list is
   exhaustive. To start over, close the old PR and remove its branch after saving any needed edits.
6. Approve CI runs if requested, obtain independent review, then merge with a human account when
   all required checks pass. Normal merge, squash and rebase are supported; the final merged commit
   is the one built and tagged. Do not batch several release preparations into one push.

Versions have no `v` prefix or leading zeroes and must advance the current project version.
Existing version tags are rejected. Use an unused PyPI version; preparation does not query PyPI
or existing GitHub Releases. Conflicts there fail during publication and require manual handling.
Tags use `v{version}`.

### Dev releases

Prepare `2.2.0.dev1`, then `2.2.0.dev2`, then `2.2.0` as needed. All publish to **production PyPI**
with the same validation and approval. Dev GitHub Releases are prereleases and excluded from Latest;
stable Releases are Latest.

Dev notes compare against the preceding supported tag reachable from the preparation commit.
Stable notes compare against the preceding **stable** tag, including changes made during dev releases.
Hand-written notes remain in `Unreleased` during dev releases and are cleared when preparing stable.
If editing a dev release's manual notes, also update `Unreleased` when they should carry into stable.
Existing dev release sections are preserved.

## Validate, approve and publish

Merging the version update starts **Release**. It checks that the push increased the project
version and that the project, lock file and changelog agree. It runs the existing lint/type/test matrix,
strict documentation build without deployment, and wheel/sdist installation checks on three systems.
All reusable workflows use the same merged SHA, regardless of ordinary CI path filters.

Documentation builds are shared in `build_docs.yml`. The normal `docs.yml` workflow calls it
and requests a Pages artifact only when deployment is intended. Release calls it without Pages
artifact upload; deployment permissions and the `github-pages` Environment belong only to `docs.yml`.

Before approving **`pypi`**, review the merged PR, validation results and the version, commit and notes
in the **identify** job summary. The publication job downloads the same distribution artifact by its
immutable ID; it never rebuilds. After approval it creates the tag, runs `uv publish` with Trusted
Publishing, then creates the GitHub Release with the reviewed notes and the same distributions.
A failed PyPI upload prevents GitHub Release creation. Runs are serialized and not auto-canceled.

## Dry-run and initial validation

Manually starting **Release** is **always a dry-run**, including upstream. It validates and builds
but skips the entire publication job. Run it on a prepared branch with a matching project/lock
version and changelog section. An ordinary implementation branch is not a prepared release.

Forks can run preparation and Release dry-runs, but the publication job explicitly requires an
upstream `master` push. Preparation accepts the fork's default branch for an isolated rehearsal.
Never configure the fork as a Trusted Publisher for the production PyPI project.

Before the first production dev release:

- Test preview, preparation PR creation, direct notes editing, duplicate-preparation rejection and
  the complete Release dry-run in the fork.
- Have the owner complete the settings and verify independent approval behavior.
- Review and merge the implementation upstream, then prepare and approve the agreed unused dev version.
- Install the published version in a fresh environment and run the distribution smoke check.
- Confirm PyPI preceded the GitHub Release, and inspect prerelease/Latest flags and attached files.

## Manual recovery

Automatic recovery is intentionally outside this workflow. A rerun does not skip an existing tag,
PyPI upload or GitHub Release, and does not compare remote hashes or upload only missing assets.
Do not blindly rerun publication after it has started. Keep the original run, merged SHA and build
artifact ID for investigation. Download distributions from that successful build, not a local rebuild.

| Failure point | Maintainer action |
| --- | --- |
| Validation, before any tag/upload | Retry transient failed checks. For code changes, use a reviewed fix and a new preparation; reconcile the already merged version/notes explicitly. No publication occurs while checks fail. |
| Approval rejected, before publication | Resolve the review concern. Retry only after confirming no tag/upload was made. |
| Tag created, PyPI not yet complete | Check the tag target and PyPI state with the owner. Do not move a tag or blindly retry. Complete publication from the original artifact through the agreed approved recovery procedure, or abandon this version and prepare a higher one. |
| PyPI complete, GitHub Release absent | Leave PyPI and the tag unchanged. Create the GitHub Release manually with the original run's notes, correct flags and original artifacts. Do not repeat PyPI publication. |
| GitHub Release or assets partially created | Inspect the existing Release and complete it manually using the original notes and artifacts. |
| Wrong or partially published PyPI contents | Investigate with the owner; decide whether to complete unchanged original files or yank and issue a new version. Do not mask mismatches with `--skip-existing`. |
| Original artifacts expired | Stop and agree a recovery plan with the owner. A rebuild is not the already validated artifact. |

Any resumed PyPI publication must use a documented owner-approved recovery path that preserves
independent approval. The default workflow supplies no automatic resume command. PyPI files cannot
be replaced under an existing filename. Yanking and emergency publication are owner-led operations.
The old token-based `make build-and-release` target remains removed.
