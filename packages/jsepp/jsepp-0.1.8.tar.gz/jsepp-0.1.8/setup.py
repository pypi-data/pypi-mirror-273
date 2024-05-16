from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_des = f.read()

setup(
    name='jsepp',
    version='0.1.8',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'pymongo',
        'numpy',
        'pandas',
        'openpyxl',
        'scipy',
        'statsmodels',
        'haversine'
    ],
    author='Hansen Zhao',
    author_email='zhaohs12@163.com',
    description='a package for general environmental data processing',
    long_description=long_des
)