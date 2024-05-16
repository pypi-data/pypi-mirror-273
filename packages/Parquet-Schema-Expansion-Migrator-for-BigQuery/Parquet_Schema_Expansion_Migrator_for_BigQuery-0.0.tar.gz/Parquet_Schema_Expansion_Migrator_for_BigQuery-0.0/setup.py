from setuptools import setup, find_packages

with open('README.md', "r") as f:
    description = f.read()

setup(
    name = 'Parquet_Schema_Expansion_Migrator_for_BigQuery',
    version = '0.0',
    packages = find_packages(),
    install_requires = [],
    entry_points = {"console_scripts" : [
        "Parquet_Schema_Expansion_Migrator_for_BigQuery = Parquet_Schema_Expansion_Migrator_for_BigQuery:Parquet_Schema_Expansion_Migrator_for_BigQuery",
    ],},
    long_description=description,
    long_description_content_type="text/markdown",
)