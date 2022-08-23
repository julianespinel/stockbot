install:
	pip install -r requirements.txt

test:
	python -m unittest discover

coverage:
	rm -f .coverage
	coverage run -m unittest discover
	coverage report
	coverage html
	coverage-badge -o coverage.svg

run:
	python main.py
