# this rule should be the default
.PHONY: dev-setup
dev-setup: install-deps
	mkdir -p logs run
	$(MAKE) static-dev
	./manage.py migrate
	touch inboxen/wsgi.py
	$(info You're now set for Inboxen development)

.PHONY: install-deps
install-deps: install-py-deps install-js-deps

.PHONY: install-py-deps
install-py-deps:
	pip install -U -r requirements-dev.txt

.PHONY: install-js-deps
install-js-deps:
	npm install

.PHONY: tests-py
tests-py: install-deps
	$(MAKE) static
	./manage.py test

.PHONY: tests-py-coverage
tests-py-coverage: install-deps
	INBOXEN_TESTING=1 $(MAKE) static-dev
	pip install coverage
	coverage run --branch ./manage.py test

.PHONY: tests-js
tests-js: install-deps
	npx grunt tests

.PHONY: update-js-requirements
update-js-requirements:
	npm update
	npm audit fix

.PHONY: static
static:
	npx grunt

.PHONY: static-dev
static-dev: static
	./manage.py compilemessages
	./manage.py collectstatic --clear --noinput

.PHONY: release
release: install-deps
	[[ -z `git status --porcelain` ]] || (echo "git repo is dirty, commit your changes first!"; exit 1)
	_scripts/release-prep.sh
	$(MAKE) static
	python setup.py sdist
	twine check dist/*
	twine upload dist/*
