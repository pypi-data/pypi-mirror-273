from setuptools import find_packages, setup
from pathlib import Path

extras = {
    "postgres": ["psycopg2-binary"],
    "mysql": ["mysql-connector-python"],
    "snowflake": ["snowflake-connector-python"],
    "bigquery": ["google-cloud-bigquery"],
    "redshift": ["psycopg2-binary"],
    "databricks": ["databricks-sql-connector"],
}

__version__ = "0.0.27"


def package_files(directory):
    paths = []
    for path in Path(directory).rglob("*"):
        if path.is_file():
            paths.append(str(path.relative_to(directory)))
    return paths


setup(
    name="datasherlock",
    version=__version__,
    description="datasherlock",
    long_description=Path("README.md").read_text().strip(),
    long_description_content_type="text/markdown",
    author="datasherlock",
    author_email="founder@datasherlock.io",
    url="http://datasherlock.io",
    packages=find_packages(),
    py_modules=["datasherlock"],
    package_data={"": package_files("datasherlock")},
    install_requires=[
        "grpcio-tools==1.50.0",
        "protobuf==4.21.9",
        "psycopg2-binary>=2.9.5",
        "prompt-toolkit>=3.0.38",
        "uvicorn",
        "tqdm",
        "pandas",
        "pwinput",
        "tabulate",
    ],
    extras_require=extras,
    zip_safe=False,
    keywords="datasherlock",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
