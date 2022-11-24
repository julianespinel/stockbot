install:
	pip install -r src/requirements.txt
	pip install -r infra/requirements.txt

build:
	mypy src
	mypy infra

test:
	python -m unittest discover

coverage:
	rm -f .coverage
	rm -f coverage.svg
	coverage run -m unittest discover
	coverage report
	coverage html
	coverage-badge -o coverage.svg

poll:
	python -m src.poll

monitor:
	python -m src.monitor

deploy:
	cd infra && cdk deploy

destroy:
	cd infra && cdk destroy
