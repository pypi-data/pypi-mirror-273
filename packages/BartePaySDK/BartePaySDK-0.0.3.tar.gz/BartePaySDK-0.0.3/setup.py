# setup.py
from setuptools import setup, find_packages

setup(
    name='BartePaySDK',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Wilson Nadim',
    author_email='wilson@barte.com',
    description='SDK para interação com a API da Barte.',
    license='MIT',
    keywords='barte pay sdk',
)
