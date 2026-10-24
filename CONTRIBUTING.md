# Contributing to mahjong

Welcome! We're glad you're interested in contributing.

## Issues

For larger changes, consider opening an issue first to discuss the approach.

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

## Pull requests

### Set up a development environment

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

### Run checks

Run these commands from the repository root before submitting a pull request:

```bash
uv run --no-sync prek run --all-files
uv run --no-sync pytest
```

Some checks may modify files automatically. Review and stage any changes, then rerun the checks.
These checks also run in CI.

For individual checks without automatic fixes:

```bash
uv run --no-sync ruff check
uv run --no-sync ruff format --check
uv run --no-sync ty check
```

If Make is available, you can also use:

```bash
make lint
make type
make tests
make check  # Applies formatting and lint fixes, then runs all checks and tests.
```

### Add regression tests

Tests live in [tests/](tests/). Name test files `tests_*.py`, not `test_*.py`,
as this project uses a naming convention that differs from pytest's default.

When adding regression tests:

- Place them alongside related tests.
- Use `pytest.mark.parametrize` when several cases exercise the same behavior.
- Reuse the helpers in [tests/utils_for_tests.py](tests/utils_for_tests.py) where they make the inputs easier to read.
- For a bug fix, confirm that the test fails before the fix and passes afterward.
- Keep examples small and make any non-default rule settings explicit.
- Assert the expected result, including relevant error conditions or scoring details.

During development, run a focused subset without the full-suite coverage requirement:

```bash
uv run --no-sync pytest --no-cov tests/tests_shanten.py
```

The full test command above includes doctests and requires 100% line coverage.
Run the full suite after the focused checks; `--no-cov` is only for running a subset during development.

### Update documentation

- Public API documentation is built from [docs/source/](docs/source/) and Python docstrings.
- Runnable examples live in [examples/](examples/).
- Wiki sources live in [.github/wiki/](.github/wiki/); edit these files so changes can be reviewed
  and published by the existing workflow.

Build the API documentation from `docs/`:

```bash
cd docs
uv run --no-sync make html
```

On Windows without Make, use:

```powershell
cd docs
uv run --no-sync .\make.bat html
```

Open `build/html/index.html` to review the result and inspect the build output for warnings.
Run examples from the repository root with `uv run --no-sync examples/FILE.py` and check the output.

### Submit a pull request

- Keep each pull request focused on one problem or improvement, and link the related issue if there is one.
- Briefly describe the change. If an issue already explains it, a reference such as `Fixes #123`
  or `Closes #123` is enough.
- Preserve existing public APIs and default rule behavior where possible. Discuss intentional compatibility
  changes explicitly, and update affected examples and documentation.
- Updating [CHANGELOG.md](CHANGELOG.md) is not required in pull requests; the project owner updates it
  before each release.
- Use a descriptive title with an appropriate Conventional Commit prefix, such as `fix:`, `feat:`,
  `docs:`, or `ci:`, consistent with the repository's recent history.
- Submit upstream contributions against `MahjongRepository/mahjong`'s `master` branch unless a maintainer
  has agreed on another target. If a pull request depends on an unmerged change, state the dependency
  and intended merge order clearly; a draft pull request can make the proposal available for review.

Review the repository's [MIT license](LICENSE.txt) when preparing contributions.
