# Task runner for pyfilechoose (Linux / macOS / CI).
# Windows users: run the equivalent tasks with .\tasks.ps1 <task>.

.PHONY: help install docs docs-serve docs-build docs-deploy test build clean

help:
	@echo "Usage: make <task>"
	@echo ""
	@echo "  install       Install the package with dev + docs extras"
	@echo "  docs-serve    Live preview of the docs (http://127.0.0.1:8000)"
	@echo "  docs-build    Build the static site into ./site"
	@echo "  docs-deploy   Publish the docs to GitHub Pages"
	@echo "  test          Run the test suite"
	@echo "  build         Build wheel + sdist into ./dist"
	@echo "  clean         Remove build artifacts"

install:
	python -m pip install -e ".[dev,docs]"

docs: docs-serve

docs-serve:
	python -m mkdocs serve

docs-build:
	python -m mkdocs build --strict

docs-deploy:
	python -m mkdocs gh-deploy --force

test:
	python -m pytest

build: clean
	python -m build
	python -m twine check dist/*

clean:
	rm -rf dist build site src/pyfilechoose.egg-info
