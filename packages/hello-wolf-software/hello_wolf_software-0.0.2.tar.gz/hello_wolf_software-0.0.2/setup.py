# setup.py

"""Setup script."""

from setuptools import setup, find_packages

with open("README.MD", 'r', encoding='UTF-8') as f:
    long_description: str = f.read()

setup(
    name='hello-wolf-software',
    version='0.0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hello=hello_wolf_software.hello:main',
        ],
    },
    author='Wolf Software',
    author_email='pypi@wolfsoftware.com',
    description='A simple hello world test',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DevelopersToolbox/hello-wolf-software',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
