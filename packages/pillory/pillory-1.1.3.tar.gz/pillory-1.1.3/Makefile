PY_FILES := $(shell find . -name '*.py')

build/htmlcov/index.html: .coverage
	coverage html --directory=build/htmlcov

.coverage: build/coverage-pillory build/coverage-example
	coverage combine --keep $^

build/coverage-%: test_%.py $(PY_FILES) | build
	coverage run --data-file=$@ $<

build:
	mkdir build

clean:
	rm -rf build .coverage

.PHONY: clean
