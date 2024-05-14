
from setuptools import setup, find_packages

setup(
    name='py_scaffold',
    version='0.1',
    packages=find_packages(),
    scripts=['main.py'],
    entry_points={
        'console_scripts': [
            'py-scaffold = main:main',
        ],
    },
    package_data={'stubs': ['_class.stub.py', '_wiki.stub.py']},
    include_package_data=True,
    install_requires=[],
    author='devinci-it',
    description='A Python project scaffold tool',
    url='https://github.com/devinci-it/devinci-pyutils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
