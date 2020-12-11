# SPEC_REPO format: <host.com>/<owner>/<project>
SPEC_REPO_URL_WITH_AUTH := https://$(SPEC_REPO_USERNAME):$(SPEC_REPO_PASSWORD)@$(SPEC_REPO)
SPEC_REPO_BRANCH_OR_COMMIT := $(if $(SPEC_REPO_BRANCH_OR_COMMIT),$(SPEC_REPO_BRANCH_OR_COMMIT),master)
TMPDIR = $(PWD)/tmp/out

.PHONY: generate test package deploy

generate:
	docker run -e LANGUAGES=python \
		-e SPEC_REPO_URL=$(SPEC_REPO_URL_WITH_AUTH) \
		-e SPEC_REPO_BRANCH_OR_COMMIT=$(SPEC_REPO_BRANCH_OR_COMMIT) \
		-e SERVICES="app-registry identity ingest catalog collect provisioner action kvstore search ml forwarders streams" \
		-v $(TMPDIR):/opt/generated \
		scpcodegen:latest \
		generate
	scripts/copy_generated_files.sh $(TMPDIR)
	rm -rf $(TMPDIR)

update_dependencies:
	pip3 freeze > requirements.txt

test: test_integration

test_integration:
	tox -e py38

test_specific:
	sh ./scripts/test_specific.sh

package:
	python setup.py sdist bdist_wheel

prerelease:
	sh ./scripts/prerelease.sh

deploy: package
	pip install twine
#	echo "Uploading to internal pypi ..."
#	twine upload -s -u "$(SPLUNK_PYPI_USERNAME)" -p "$(SPLUNK_PYPI_PASSWORD)" --repository-url "$(SPLUNK_PYPI_REPO)" dist/*
ifdef UPLOAD_TO_PYPI
	echo "Uploading to public pypi ..."
	twine upload -s -u "$(PYPI_USERNAME)" -p "$(PYPI_PASSWORD)" dist/*
endif
