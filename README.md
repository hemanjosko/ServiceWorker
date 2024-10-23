# ServiceWorker
https://packaging.python.org/en/latest/tutorials/packaging-projects/

py -m pip install --upgrade pip
py -m pip install --upgrade build
py -m build
py -m pip install --upgrade twine
py -m twine upload --repository ServiceWorker dist/*