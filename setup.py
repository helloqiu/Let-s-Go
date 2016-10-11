# -*- encoding: utf-8 -*-
import os
from setuptools import setup, find_packages


dev_requires = [
    'flake8',
]


def fetch_dependencies(file_name):
    deps = []
    for line in open(file_name).read().splitlines():
        if line.startswith("-r "):
            deps.append(fetch_dependencies(line[3:]))
        else:
            deps.append(line)
    return deps

install_requires = fetch_dependencies('requirements.txt')


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="Let's Go",
    description=read('README.md'),
    long_description=read('README.md'),
    license='General Public License',
    platforms=['OS Independent'],
    keywords='NoneGroupTeam Let-s-Go',
    author='NoneGroupTeam',
    author_email='lc4t0.0@gmail.com',
    url="https://github.com/NoneGroupTeam/Let-s-Go",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
)
