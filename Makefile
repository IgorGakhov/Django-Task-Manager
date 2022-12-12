install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test ./task_manager/tests/

test-coverage:
	poetry run coverage run manage.py test ./task_manager/tests/
	poetry run coverage report --omit=*/tests/*,*/migrations/*,*/__init__.py
	poetry run coverage xml --omit=*/tests/*,*/migrations/*,*/__init__.py

freeze:
	poetry run pip --disable-pip-version-check list --format=freeze > requirements.txt

prepare-translations:
	django-admin makemessages -l ru

compile-translations:
	django-admin compilemessages

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

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
	echo "\n\n\n ! Test checkup process...\n"
	make test

dev-start:
	poetry run python manage.py runserver

# Database dump example:
# poetry run ./manage.py dumpdata {app:users}.{db:users} --indent {indent:2} > {path:tests/fixtures}/{name:users}.{format:json}
