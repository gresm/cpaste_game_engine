#!/bin/bash
python3 setup.py all build
python3 setup.py all sdist bdist_wheel
twine upload -r testpypi dist/cpaste[-_]api*
twine upload -r testpypi dist/cpaste[-_]core*
twine upload -r testpypi dist/cpaste[-_]editor*
twine upload -r testpypi dist/cpaste[-_][0-9]*
twine upload -r testpypi dist/*