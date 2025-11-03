.PHONY: install run test cov fmt lint clean

install:
	python -m pip install --upgrade pip
	pip install --no-cache-dir -r requirements.txt

run:
	flask --app app/create_app.py --debug run -h 0.0.0.0 -p 5000

test:
	pytest -q

cov:
	coverage run -m pytest
	coverage report -m
	coverage html

fmt:
	black .
	isort .

lint:
	flake8 .

clean:
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage __pycache__ */__pycache__
