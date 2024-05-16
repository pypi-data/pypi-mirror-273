from setuptools import setup, find_packages

with open('README.md', "r") as f:
    description = f.read()

setup(
    name = 'gcs_convert_csv_to_parquet',
    version = '0.0',
    packages = find_packages(),
    install_requires = [],
    entry_points = {"console_scripts" : [
        "gcs_convert_csv_to_parquet = gcs_convert_csv_to_parquet:gcs_convert_csv_to_parquet",
    ],},
    long_description=description,
    long_description_content_type="text/markdown",
)