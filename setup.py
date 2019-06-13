from setuptools import setup, find_packages

import os

version = "1.0.0"

_base = os.path.dirname(os.path.abspath(__file__))
_requirements = os.path.join(_base, 'requirements.txt')

install_requirements = []
with open(_requirements) as f:
    install_requirements = f.read().splitlines()

setup(
    name="webin-project-registration",
    author='Sam Holt',
    author_email='holt@ebi.ac.uk',
    url='https://github.com/enasequence/dcat-webin-bioproject-set-submission',
    version=version,
    packages=find_packages(),
    install_requires=install_requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'study_subs=src.study_subs:main'
        ],
    },
)
