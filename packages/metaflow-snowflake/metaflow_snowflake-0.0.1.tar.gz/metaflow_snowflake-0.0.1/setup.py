from setuptools import setup, find_namespace_packages

version = "0.0.1"

setup(
    name="metaflow-snowflake",
    version=version,
    description="Utility functions for using common Snowflake actions with Metaflow.",
    author="Outerbounds",
    author_email="hello@outerbounds.co",
    packages=find_namespace_packages(include=["metaflow_extensions.*"]),
    py_modules=[
        "metaflow_extensions",
    ],
)
