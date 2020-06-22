clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf dist.zip

verify:
	python -m pytest	

package:
	zip -j dist.zip src/*

all:
	make clean verify package	