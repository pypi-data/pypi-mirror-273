from setuptools import find_packages, setup

setup(
    name="procedure_data_tool",
    version="0.0.6",
    description="Reference tool for DST Waste Transfer Procedures Based on automatically generated route",
    packages=find_packages(include=['procedure_data_tool', 'procedure_data_tool.*']),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Josue Estrada",
    author_email="jramiroem@gmail.com",
    license="MIT",
    install_requires=[
        'openpyxl',
        'python-docx',
        'networkx',
        'matplotlib',
    ],
    include_package_data=True,

)
