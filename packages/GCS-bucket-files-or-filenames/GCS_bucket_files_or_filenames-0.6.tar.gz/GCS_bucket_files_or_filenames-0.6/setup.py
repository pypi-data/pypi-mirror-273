from setuptools import setup, find_packages

with open('README.md', "r") as f:
    description = f.read()

setup(
    name = 'GCS_bucket_files_or_filenames',
    version = '0.6',
    packages = find_packages(),
    install_requires = [],
    entry_points = {"console_scripts" : [
        "GCS_bucket_files_or_filenames = GCS_bucket_files_or_filenames:files_in_bucket",
    ],},
    long_description=description,
    long_description_content_type="text/markdown",
)
