cd ..
python setup.py clean --all
python setup.py sdist bdist_wheel
pip install --upgrade --force-reinstall dist/icare_nlp-0.0.8-py3-none-any.whl
