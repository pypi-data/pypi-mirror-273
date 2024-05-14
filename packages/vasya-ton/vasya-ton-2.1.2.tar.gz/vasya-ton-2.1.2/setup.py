from setuptools import setup
import setuptools

requirements = ["tonsdk>=1.0.13", "ton>=0.26", "aiohttp>=3.8.1", "setuptools>=65.3.0", "requests>=2.28.1", "pytonlib>=0.0.46", "graphql-query>=1.0.3"]

setup(
    name='vasya-ton',
    version='2.1.2',
    packages=['vasya-ton', 'vasya-ton/Contracts', 'vasya-ton/Providers'],
    url='',
    license='MIT License',
    author='vasyait',
    author_email='cyrbatoff@gmail.com',
    description='Explore TON Blockchain with python',
    install_requires=requirements,
)
