.PHONY: prepare clean dist upload

clean:
	rm -rf *.egg-info/ build/ dist/ __pycache__

upload: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal
	twine upload dist/*