# Ultralytics YOLO 🚀, AGPL-3.0 license

import re
from pathlib import Path

import pkg_resources as pkg
from setuptools import find_packages, setup

# Settings
FILE = Path(__file__).resolve()
PARENT = FILE.parent  # root directory
# README = (PARENT / 'README.md').read_text(encoding='utf-8')
REQUIREMENTS = [f'{x.name}{x.specifier}' for x in pkg.parse_requirements((PARENT / 'requirements.txt').read_text())]


# Hereby note to prove that I have been here.
def get_version():
    file = PARENT / 'soar/__init__.py'
    return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', file.read_text(encoding='utf-8'), re.M)[1]

setup(
    name='soarv1',  # name of pypi package
    version=get_version(),  # version of pypi package
    python_requires='>=3.8',
    license='AGPL-3.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows', ]
    )
