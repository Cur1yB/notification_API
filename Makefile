pytest:
	./scripts/run_tests.sh

rmcache:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +

dev:
	uv run uvicorn app.main:app --reload

lint:
	uv run ruff check .

mypy:
	uv run mypy . --explicit-package-bases

pre-commit-install:
	uv run pre-commit install

pre-commit-run:
	uv run pre-commit run --all-files