format:
	uv run ruff format

lint:
	uv run ruff check

.PHONY: tests
tests:
	uv run pytest --cov=mahjong --cov-report=term --cov-report=html

check: format lint tests

build-package:
	rm -rf build dist mahjong.egg-info
	uv build

# make build-and-release token=your_pypi_token
build-and-release: build-package
	uv publish --token $(token)
