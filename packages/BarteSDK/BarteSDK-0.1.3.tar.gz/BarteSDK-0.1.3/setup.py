# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='BarteSDK',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Engenharia de Plataforma da Barte',
    author_email='devops@barte.com',
    description='SDK para interação com a API da Barte.',
    license='MIT',
    keywords='barte pay sdk',
    long_description=long_description,
    long_description_content_type="text/markdown",    
)
