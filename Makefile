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

check: format lint type tests

build-package:
	rm -rf build dist mahjong.egg-info
	uv build

# make build-and-release token=your_pypi_token
build-and-release: build-package
	uv publish --token $(token)
