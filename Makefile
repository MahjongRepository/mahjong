format:
	uv run ruff format mahjong

lint:
	uv run ruff check mahjong

.PHONY: tests
tests:
	uv run pytest --cov=mahjong --cov-report=term --cov-report=html

check: format lint tests

build-package:
	rm -rf build dist mahjong.egg-info
	uv build

build-and-release: build-package
	uv publish
