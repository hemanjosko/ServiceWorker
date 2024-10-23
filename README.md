# ServiceWorker
https://packaging.python.org/en/latest/tutorials/packaging-projects/

python -m pip install --upgrade pip
python -m pip install --upgrade build
python -m build
python -m pip install --upgrade twine

python -m twine upload --repository ServiceWorker dist/*

python -m twine upload dist/*
enter api key 