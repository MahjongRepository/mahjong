format:
	uv run ruff format
	uv run ruff check --fix

lint:
	uv run ruff format --check
	uv run ruff check

type:
	uv run ty check

.PHONY: tests
tests:
	uv run pytest

check: format lint type tests

build-package:
	rm -rf build dist mahjong.egg-info
	uv build

# make build-and-release token=your_pypi_token
build-and-release: build-package
	uv publish --token $(token)
