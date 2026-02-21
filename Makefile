pytest:
	./scripts/test_integration.sh

rmcache:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
