install:
	pip install -r requirements.txt

test:
	python -m unittest discover

coverage:
	coverage run -m unittest discover
	coverage report

run:
	python main.py
