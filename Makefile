lint:
	flake8 mahjong --config .flake8

tests:
	python -m unittest discover .