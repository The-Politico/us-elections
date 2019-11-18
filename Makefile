test:
	pytest -v

ship:
	pipenv run python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing
