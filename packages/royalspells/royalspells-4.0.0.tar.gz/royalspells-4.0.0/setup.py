import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="royalspells",
    version="4.0.0",
    author="Stefano Pigozzi",
    author_email="me@steffo.eu",
    description="Meaningless fantasy spell stats generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steffo99/royalspells",
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 6 - Mature",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ]
)
