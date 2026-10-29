format:
	uv run --no-sync ruff format
	uv run --no-sync ruff check --fix

lint:
	uv run --no-sync ruff format --check
	uv run --no-sync ruff check

type:
	uv run --no-sync ty check

.PHONY: tests
tests:
	uv run --no-sync pytest

check: lint type tests

build-package:
	rm -rf build dist mahjong.egg-info
	uv build
