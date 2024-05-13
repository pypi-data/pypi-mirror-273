with open('README.md', 'r') as f:
    long_description = f.read()

from setuptools import setup, find_packages

setup(
    name='pygeneconverter',
    version = 0.2,
    packages=find_packages(),
    package_data={'pygeneconverter': ['data/query_table.csv']},
    include_package_data=True,
    install_requires=[
        'pandas',
    ],
    description='A Python package for converting Ensembl IDs to HUGO gene symbols and vice versa.',
    long_description=long_description,
    long_description_content_type='text/markdown',
)

