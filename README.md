# mahjong

[![Mahjong lib](https://github.com/MahjongRepository/mahjong/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/MahjongRepository/mahjong/actions/workflows/lint_and_test.yml)

This library can calculate hand cost (han, fu with details, yaku, and scores) for riichi mahjong (Japanese version).

Also calculating of shanten is supported.

The code was validated on tenhou.net phoenix replays in total on **11,120,125 hands**.

So, we can say that our hand calculator works the same way that tenhou.net hand calculation.

## How to install

```bash
pip install mahjong
```

## Supported rules and usage examples

You can find usage examples and information about all supported rules variations in the [wiki](https://github.com/MahjongRepository/mahjong/wiki)

## Local development setup

To set up the project locally for development:

1. Clone the repository:

    ```bash
    git clone https://github.com/MahjongRepository/mahjong.git
    cd mahjong
    ```

2. Setup env using [uv](https://github.com/astral-sh/uv):

    ```bash
    uv venv
    ```

3. Run tests to verify setup:

    ```bash
    make tests
    # Or directly:
    uv run pytest
    ```

4. Run full checks before committing:

    ```bash
    make check   # Runs format, lint, and tests
    ```
