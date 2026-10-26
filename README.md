# mahjong

[![PyPI](https://img.shields.io/pypi/v/mahjong.svg)](https://pypi.python.org/pypi/mahjong)
[![License](https://img.shields.io/pypi/l/mahjong.svg)](https://pypi.python.org/pypi/mahjong)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/mahjong.svg)](https://pypi.python.org/pypi/mahjong)
[![PyPI Downloads](https://img.shields.io/pypi/dm/mahjong.svg?label=PyPI%20downloads)](https://pypi.org/project/mahjong/)
[![Linters and tests](https://github.com/MahjongRepository/mahjong/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/MahjongRepository/mahjong/actions/workflows/lint_and_test.yml)
[![API Docs](https://img.shields.io/badge/api-master-yellow.svg)](https://mahjongrepository.github.io/mahjong)

Japanese riichi mahjong hand calculator library.

Compute hand cost (han, fu, yaku, and scores), validate winning hands, and calculate shanten (minimum tiles to tenpai).

The code was validated on tenhou.net phoenix replays: **26,148,050** four-player and **8,406,421** three-player winning hands.

So, we can say that our hand calculator works the same way that tenhou.net hand calculation.

## Documentation

- [API reference](https://mahjongrepository.github.io/mahjong)
- [Wiki](https://github.com/MahjongRepository/mahjong/wiki) — Supported rules and usage examples

## How to install

```bash
pip install mahjong
```

## Local development setup

To set up the project locally for development:

1. Clone the repository:

    ```bash
    git clone https://github.com/MahjongRepository/mahjong.git
    cd mahjong
    ```

2. Setup env using [uv](https://github.com/astral-sh/uv):

    ```bash
    uv sync
    ```

3. Install the Git hooks using [prek](https://prek.j178.dev/):

    ```bash
    uv run prek install
    ```

    Changes to Python files (`.py` or `.pyi`), `pyproject.toml`, `uv.lock`, or `.pre-commit-config.yaml`
    trigger all three hooks. Ruff runs lint fixes and formatting across its configured project scope,
    followed by ty type checks on the entire `mahjong` package, using the tool versions installed from `uv.lock`.
    Review any automatic fixes and stage the updated files before committing again. After changing the hook configuration,
    check all tracked files with:

    ```bash
    uv run prek run --all-files
    ```

    Hooks stop at the first failure or automatic change. Rerun them after fixing and staging changes;
    ty runs only after both Ruff hooks pass.

    CI runs the same hooks in a single job using `uv run --no-sync prek run --all-files`.
    It installs only the `hooks` dependency group (prek, Ruff, and ty), without test or documentation dependencies:

    ```bash
    uv sync --locked --no-default-groups --group hooks --no-install-project
    ```

    Hook commands use `--no-sync` to reuse the prepared environment without installing the default `dev` group.
    Run `uv sync` after dependency updates to keep the hook tools up to date.

4. Run tests to verify setup:

    ```bash
    make tests
    # Or directly:
    uv run pytest
    ```

5. Run full checks before committing:

    ```bash
    make check   # Runs format, lint, type checks, and tests
    ```

    The Git hooks run Ruff and ty; run tests separately as part of the full checks above.

## License

This library is licensed under the [MIT license](LICENSE.txt).
