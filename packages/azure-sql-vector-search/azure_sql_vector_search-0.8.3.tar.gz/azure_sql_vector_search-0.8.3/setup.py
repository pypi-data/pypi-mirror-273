from setuptools import setup, find_packages

with open('README.md') as readme_file:
    project_long_description = readme_file.read()

project_description = "Azure SQL Vector Search Clients"

PROJECT_VERSION: str = "0.8.3"

setup(
    name='azure_sql_vector_search',
    version=PROJECT_VERSION,
    author='Microsoft Corporation',
    url="https://github.com/projectAcetylcholine/sql_vector_search",
    packages=find_packages(),
    install_requires=['pyodbc >= 5.1.0', 'sqlalchemy >= 2.0.30', 'numpy >= 1.26.4'],
    license='MIT License',
    description=project_description,
    keywords="azure sql vector search langchain",
    long_description=project_long_description,
    long_description_content_type='text/markdown'
)
