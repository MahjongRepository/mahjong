format:
	isort mahjong/*
	black mahjong/*

lint:
	isort --check-only mahjong/*
	black --check mahjong/*
	flake8 mahjong --config .flake8

tests:
	python -m unittest discover .