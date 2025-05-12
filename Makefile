SHELL=/bin/bash
.DEFAULT_GOAL := default

.PHONY: lint
lint:
	@echo "-----------------------------"
	@echo "- Run linters and formatters -"
	@echo "-----------------------------"
	SKIP=no-commit-to-branch pre-commit run --all-files

.PHONY: run
run:
	@echo "Running the application."
	poetry run uvicorn app.api.app:app --reload
