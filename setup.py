import re

from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('migrator/__init__.py') as f:
    version = _version_re.search(f.read()).group(1)


setup(
    name='migrator',
    version=version,
    url='http://github.com/afonasev/migrator',
    author='Afonasev Evgeniy',
    author_email='ea.afonasev@gmail.com',
    packages=['migrator'],
    install_requires=[
        'Click',
    ],
)
