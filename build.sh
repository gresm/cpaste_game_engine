#!/bin/bash
python3 setup.py all build
python3 setup.py all sdist bdist_wheel
twine upload --skip-existing -r testpypi dist/*