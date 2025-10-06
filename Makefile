# Makefile for Insider Test Automation Project

.PHONY: help install test test-html test-chrome test-firefox clean setup-env

# Default target
help:
	@echo "Available commands:"
	@echo "  install        - Install dependencies"
	@echo "  setup-env      - Setup environment files"
	@echo "  test           - Run main test"
	@echo "  test-html      - Run test with HTML report"
	@echo "  test-chrome    - Run test with Chrome"
	@echo "  test-firefox   - Run test with Firefox"
	@echo "  clean          - Clean up generated files"

# Install dependencies
install:
	pip install -r requirements.txt

# Setup environment
setup-env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from .env.example"; \
	else \
		echo ".env file already exists"; \
	fi
	@mkdir -p logs reports screenshots

# Run main test
test:
	pytest tests/test_insider_careers.py -v

# Run test with HTML report
test-html:
	pytest tests/test_insider_careers.py -v --html=reports/report.html --self-contained-html

# Run test with Chrome
test-chrome:
	pytest tests/test_insider_careers.py -v --browser=chrome

# Run test with Firefox
test-firefox:
	pytest tests/test_insider_careers.py -v --browser=firefox

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf reports/
	rm -rf screenshots/
	rm -rf logs/

# Development setup
setup: install setup-env
	@echo "Setup complete! Run 'make test' to start testing."