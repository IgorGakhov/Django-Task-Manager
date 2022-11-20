install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run pytest -s
	poetry run pytest --cov=task_manager

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

freeze:
	poetry run pip --disable-pip-version-check list --format=freeze > requirements.txt

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-force-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

fast-check:
	echo "\n\n\n ! Build process...\n"
	make build
	echo "\n\n\n ! Package-force-reinstall process...\n"
	make package-force-reinstall
	echo "\n\n\n ! Lint checkup process...\n"
	make lint

dev-start:
	poetry run python manage.py runserver
