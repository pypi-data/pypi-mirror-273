"""setup.py"""
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='hombre_tools',  # Required

    version='0.1.25',  # Required
    description='tools for daily usage',  # Optional
    url='https://github.com/hombre66/hombre_tools',  # Optional

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=['numpy',
                      'pandas',
                      'pyOpenSSL',
                      'pyperclip',
                      'python-dateutil',
                      'python-settings',
                      'pywin32',
                      'pywin32-ctypes',
                      'pywinpty',
                      'requests',
                      'seaborn',
                      'SQLAlchemy',
                      'sqlparse',
                      'tables',
                      'urllib3',
                      'zipp',
                      'lxml'],
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    data_files=[('hombre_tools/tools/catalog', ['hombre_tools/tools/catalog/catalog_new.h5'])], 

)
