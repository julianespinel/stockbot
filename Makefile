install:
	pip install -r requirements.txt

test:
	python -m unittest discover

coverage:
	rm -f .coverage
	coverage run -m unittest discover
	coverage report
	coverage html

run:
	python main.py
