# Contributing to mahjong

Contributions to hand calculation, tests, documentation, and development tooling are welcome.
For substantial changes to algorithms, public APIs, or rule interpretation, discuss the approach
in an issue before investing in a large implementation.

## Report a bug or propose a change

Search the existing [issues](https://github.com/MahjongRepository/mahjong/issues) and
[pull requests](https://github.com/MahjongRepository/mahjong/pulls) before opening a new one.
Include a small runnable example. If the behavior differs between `mahjong` versions, Python versions,
or operating systems, mention those differences.

For hand-calculation or rule-related reports, it helps to include:

- Expected and actual yaku, han, fu, points, or error. For shanten or agari reports, give the expected
  and actual shanten number or winning-hand result instead.
- The rule reference or comparison result supporting the expectation. Identify differences in optional
  rules when comparing against another calculator.

The [Wiki](https://github.com/MahjongRepository/mahjong/wiki) describes supported rules and usage examples.

## Set up a development environment

Use a supported Python version (currently Python 3.10 or newer) and install
[uv](https://docs.astral.sh/uv/getting-started/installation/).
Fork the repository on GitHub, clone your fork, and create a branch for your change:

```bash
git clone https://github.com/YOUR-USERNAME/mahjong.git
cd mahjong
git switch -c your-change
uv sync --locked
uv run --no-sync prek install
```

Replace `YOUR-USERNAME` and `your-change` with your GitHub username and branch name.
The default `dev` dependency group includes the tools for hooks, tests, and documentation.
Run `uv sync --locked` again after switching branches or pulling dependency updates, especially
if you previously installed only a subset of dependency groups.

Dependency definitions and tool settings live in [pyproject.toml](pyproject.toml).
If you intentionally change dependencies, update [uv.lock](uv.lock) with `uv lock` and include
any resulting lockfile changes in your pull request. Do not edit the lockfile by hand.

## Run checks

Run these commands from the repository root before submitting a pull request:

```bash
uv run --no-sync prek run --all-files
uv run --no-sync pytest
```

The hooks run Ruff lint fixes, Ruff formatting, and then ty type checks, using the versions installed
from `uv.lock`. Changes to `.py` or `.pyi` files, `pyproject.toml`, `uv.lock`, or the hook configuration
trigger all three hooks. Each tool checks its configured project scope; ty currently checks `mahjong`.

Hooks stop at the first failure or automatic change. Review the changes, stage the updated files,
and rerun the hooks until they pass. The hooks do not run tests. CI runs the same hooks on all tracked
files and runs the test suite across its configured Python implementations and versions.

For individual checks without automatic fixes:

```bash
uv run --no-sync ruff check
uv run --no-sync ruff format --check
uv run --no-sync ty check
```

If you use Make, the existing `make lint`, `make type`, and `make tests` targets run these checks.
`make check` also applies formatting and lint fixes before running the checks and tests.
The direct uv commands work without Make, including on Windows.

## Add regression tests

Tests live in [tests/](tests/). Pytest discovers files named `tests_*.py`, as configured in `pyproject.toml`.
Add a regression test alongside related tests and use `pytest.mark.parametrize` when several cases
exercise the same behavior. Reuse the helpers in [tests/utils_for_tests.py](tests/utils_for_tests.py)
where they make the inputs easier to read.

For a bug fix, confirm that the new test reproduces the bug before the fix and passes afterward.
Keep the example small, and make any non-default rule settings explicit. Assert the expected result,
including relevant error conditions or scoring details, rather than only checking that the call succeeds.

During development, run a focused subset without the full-suite coverage requirement:

```bash
uv run --no-sync pytest --no-cov tests/tests_shanten.py
```

The full test command above includes doctests and requires 100% line coverage. Always run it after
the focused checks; passing a subset with `--no-cov` does not replace full-suite validation.

## Update documentation

- Public API documentation is built from [docs/source/](docs/source/) and Python docstrings.
- Runnable examples live in [examples/](examples/).
- Wiki sources live in [.github/wiki/](.github/wiki/); edit these files so changes can be reviewed
  and published by the existing workflow.

Build the API documentation from `docs/`:

```bash
cd docs
uv run --no-sync make html
```

On Windows without Make, run the following from the `docs/` directory:

```powershell
uv run --no-sync .\make.bat html
```

Open `build/html/index.html` to review the result and inspect the build output for warnings.
Run examples from the repository root with `uv run --no-sync examples/FILE.py` and check the output.

## Prepare a pull request

- Keep each pull request focused on one problem or improvement, and link the related issue if there is one.
- Explain the previous behavior, the intended result, and the reason for the change. List the checks
  you ran and mention any checks you could not run.
- Preserve existing public APIs and default rule behavior where possible. Discuss intentional compatibility
  changes explicitly, and update affected examples and documentation.
- Add a [CHANGELOG.md](CHANGELOG.md) entry for user-visible changes, following its existing structure.
  Describe breaking changes and migration steps when applicable.
- Use a descriptive title with an appropriate Conventional Commit prefix, such as `fix:`, `feat:`,
  `docs:`, or `ci:`, consistent with the repository's recent history.
- Submit upstream contributions against `MahjongRepository/mahjong`'s `master` branch unless a maintainer
  has agreed on another target. If a pull request depends on an unmerged change, state the dependency
  and intended merge order clearly; a draft pull request can make the proposal available for review.

Review the repository's [MIT license](LICENSE.txt) when preparing contributions.
