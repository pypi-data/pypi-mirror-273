from setuptools import find_packages, setup

setup(
    name="procedure_data_tool",
    version="0.0.1",
    description="add description XXXX____XXXX____XX___XX_",
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Josue Estrada",
    author_email="jramiroem@gmail.com",
    license="MIT",
    # install_requires=[],
    install_requires=[
        'openpyxl',
        'python-docx',
    ],
    # extras_require={
    #     # "dev": [pytest>=7.0]
    # }
    # python_requires=">=3.60",
    # classifiers=[
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    # ],
)
