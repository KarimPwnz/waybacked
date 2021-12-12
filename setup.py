import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="waybacked",
    version="0.1",
    license="MIT",
    author="karimpwnz",
    author_email="karim@karimrahal.com",
    description="Get URLs from the Wayback Machine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karimpwnz/waybacked",
    project_urls={
        "Bug Tracker": "https://github.com/karimpwnz/waybacked/issues", },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
    ],
    packages=["waybacked"],
    entry_points={"console_scripts": ["waybacked = waybacked.__main__:main"]},
    python_requires=">=3.6",
    install_requires=[
        "requests >= 2.25.1"
    ],
)
