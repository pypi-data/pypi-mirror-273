from setuptools import setup, find_packages

with open('README.md', "r") as f:
    description = f.read()

setup(
    name = 'Compress_csv_files_gcs_bucket',
    version = '0.1',
    packages = find_packages(),
    install_requires = [],
    entry_points = {"console_scripts" : [
        "Compress_csv_files_gcs_bucket = Compress_csv_files_gcs_bucket:compress_csv_files_gcs_bucket",
    ],},
    long_description=description,
    long_description_content_type="text/markdown",
)