from setuptools import setup, find_packages

setup(
    name="Hvectorizer",
    version="0.1.0",
    author="Simean Hamado",
    author_email="fatihamtech@gmail.com",
    description="This package aims to facilitate natural languange processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://example.com/mypackage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Add your dependencies here
        #'numpy',
        # 'requests',
    ],
    include_package_data=True,
    package_data={
        # Include any package data files here
        # '': ['*.txt', '*.md'],
    },
)
