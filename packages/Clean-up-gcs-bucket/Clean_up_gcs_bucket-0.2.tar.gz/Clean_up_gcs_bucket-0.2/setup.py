from setuptools import setup, find_packages

with open('README.md', "r") as f:
    description = f.read()

setup(
    name = 'Clean_up_gcs_bucket',
    version = '0.2',
    packages = find_packages(),
    install_requires = [],
    entry_points = {"console_scripts" : [
        "Clean_up_gcs_bucket = Clean_up_gcs_bucket:clean_up_gcs_bucket",
    ],},
    long_description=description,
    long_description_content_type="text/markdown",
)