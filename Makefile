.PHONY: prepare clean dist upload

clean:
	rm -rf *.egg-info/ build/ dist/ __pycache__

upload: clean
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
