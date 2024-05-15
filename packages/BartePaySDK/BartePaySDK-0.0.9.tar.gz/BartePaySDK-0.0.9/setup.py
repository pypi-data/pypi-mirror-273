# setup.py
from setuptools import setup, find_packages

setup(
    name='BartePaySDK',
    version='0.0.9',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Engenharia de Plataforma da Barte',
    author_email='devops@barte.com',
    description='SDK para interação com a API da Barte.',
    license='MIT',
    keywords='barte pay sdk',
)
