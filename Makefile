install:
	pip install -r src/requirements.txt
	pip install -r infra/requirements.txt

test:
	cd src/ && python -m unittest discover

coverage:
	rm -f .coverage
	rm -f coverage.svg
	cd src/ \
		&& coverage run -m unittest discover \
		&& mv .coverage ../ \
		&& cd ../
	coverage report
	coverage html
	coverage-badge -o coverage.svg

run:
	python src/main.py

deploy:
	cd infra && cdk deploy

destroy:
	cd infra && cdk destroy
