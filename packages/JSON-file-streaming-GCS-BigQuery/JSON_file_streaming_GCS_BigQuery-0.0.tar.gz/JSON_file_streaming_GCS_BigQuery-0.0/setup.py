from setuptools import setup, find_packages

with open('README.md', "r") as f:
    description = f.read()

setup(
    name = 'JSON_file_streaming_GCS_BigQuery',
    version = '0.0',
    packages = find_packages(),
    install_requires = [],
    entry_points = {"console_scripts" : [
        "JSON_file_streaming_GCS_BigQuery = JSON_file_streaming_GCS_BigQuery:process_json_file_streaming",
    ],},
    long_description=description,
    long_description_content_type="text/markdown",
)
