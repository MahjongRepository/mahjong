format:
	isort mahjong/*
	black mahjong/*

lint:
	isort --check-only mahjong/*
	black --check mahjong/*
	flake8 mahjong --config .flake8

tests:
	python -m unittest discover .

check: format lint tests

build_package:
	rm -r build dist mahjong.egg-info
	python3 setup.py sdist bdist_wheel