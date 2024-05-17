from setuptools import setup, find_packages

setup(
    name="html2object",
    version="1.1.0",
    author="boterop",
    author_email="boterop22@gmail.com",
    description="Tools to handle the CRUD of .html files as objects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/boterop/html2object",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="html, utils, html_utils, html_element, html_parser, html_writer, html_reader, html_crud, html_object, html_file, html_utils.py, html_element.py, html_parser.py, html_writer.py, html_reader.py, html_crud.py, html_object.py, html_file.py, html2object, html2object.py, html2object.py",
    install_requires=[],
    python_requires=">=3.6",
)
