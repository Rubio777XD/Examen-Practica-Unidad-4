.PHONY: install run test cov clean

install:
        python -m pip install --upgrade pip
        pip install -r requirements.txt

run:
        flask --app app/create_app.py --debug run -h 0.0.0.0 -p 5001

test:
	pytest -q

cov:
        coverage run -m pytest
        coverage report -m
        coverage html

clean:
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage __pycache__ */__pycache__
