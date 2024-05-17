from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

__version__ = '0.1.0.5'
setup(
    name='drremote',
    version=__version__,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='',
    license='MIT',
    author='Dieter Stockhausen',
    author_email='dieter@schwingenhausen.at',
    description="DRRemote is a python modul which offers access to Davinci Resolve Studio.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    download_url=f'https://github.com/sto3014/DRRemote/archive/refs/heads/main.zip',
    keywords='python davinci resolve api',
    entry_points={
        "console_scripts": [
            'drremote = drremote:run_main'
        ]
    }
)
