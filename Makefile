-include .env
PROJECTNAME=$(shell basename "$(PWD)")

MAKEFILAGS += --silent

.PHONY: help
all: help
help: Makefile
	@echo
	@echo " Choose a command run in "$(PROJECTNAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' | sed -e 's/^/ /'
	@echo

## install: Install dependency
install:
	@echo " > Installing dependency"
	@pip install -r dev-requirements.txt

## ruff: ruff check pep8
ruff:
	@echo " > Checking pep8"
	@ruff check .

## rufffix: Fix pep8
rufffix:
	@echo " > Fixing pep8"
	@ruff check . --fix

## format: Auto format code
format:
	@echo " > Formating code..."
	@ruff format .

## unittest: Run all unit test
unittest:
	@echo " > Testing..."
	@python -m pytest --cov=./

## flake8: Run flake8
flake8:
	@echo " > Running flake8 check"
	@flake8 . --count --exit-zero --max-complexity=8 --max-line-length=80 --statistic

## clean: Clean release file
clean:
	@echo " > Cleaning release file"
	@rm ./dist/* 2> /dev/null

## piptar: Pip build a tar package
piptar: clean
	@echo " > Pip building..."
	@python -m build

## pipedit: Pip install in edit mode
pipedit:
	@echo " > Pip Install in edit mode"
	@pip install -e .

## pypitest: Upload package to testpypi
pypitest:
	@echo "Uploading to testpypi"
	@python -m twine upload --repository testpypi dist/*

## pypiupload: Upload package to pypi
pypiupload:
	@echo "Uploading to pypi"
	@python -m twine upload --repository pypi dist/*
