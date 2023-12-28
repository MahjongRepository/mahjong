format:
	isort mahjong/*
	black mahjong/*

lint:
	isort --check-only mahjong/*
	black --check mahjong/*
	flake8 mahjong --config .flake8

tests:
	PYTHONPATH=./mahjong pytest --cov=mahjong --cov-report=term --cov-report=html

check: format lint tests

build-package:
	rm -rf build dist mahjong.egg-info
	python setup.py sdist bdist_wheel

build-and-release: build-package
	twine upload dist/*
