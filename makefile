clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf dist
	rm -rf dist.zip

verify:
	python -m pytest	

package:
	mkdir dist
	pip install -r requirements-prod.txt -t dist
	cp -r src/ dist/
	zip -r dist.zip dist

all:
	make clean verify package	