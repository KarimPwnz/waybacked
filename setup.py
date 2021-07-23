import setuptools

setuptools.setup(
    name="waybacked",
    author="Karim Rahal",
    author_email="karim@karimrahal.com",
    version="0.1",
    license="MIT",
    packages=["waybacked"],
    entry_points={"console_scripts": ["waybacked = waybacked.__main__:main"]},
    python_requires=">=3.6",
    install_requires=[
        "requests >= 2.25.1"
    ],
)
