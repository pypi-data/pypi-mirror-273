from setuptools import setup, find_packages

# Reading the README.md file for long description in PyPI site
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='data-quality-validation-pydeequ',
    version='1.1',
    author='Ketan Kirange',
    author_email='k.kirange@reply.com',
    description='A library for data quality validation using PyDeequ and to send email notification.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pydeequ',
        'boto3',
        'pyyaml',  
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='data quality validation pydeequ',
)
