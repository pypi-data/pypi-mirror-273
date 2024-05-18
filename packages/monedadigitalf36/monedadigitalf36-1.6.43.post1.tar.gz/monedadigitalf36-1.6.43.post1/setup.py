from setuptools import setup, find_packages


version = '1.6.43r1'

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="monedadigitalf36",
    version='1.6.43.post1',

    author="Gehtsoft USA, LLC",
    author_email="contact@gehtsoftusa.com",

    url="https://github.com/AmadoRamos/forexconect.git",
    download_url=f"https://github.com/AmadoRamos/forexconect36/archive/refs/tags/v{version}.zip",

    description="ForexConnect API is a trading API for the FXCM Group: https://www.fxcm.com/uk/",

    packages=['forexconnect36'],
    #include = ["forexconnect/lib/*", 'lib/*'],
    install_requires=[],

    license='Other/Proprietary License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True, # for MANIFEST.in
    python_requires='>=3.6.0',

    #package_data={package: ["py.typed", "*.pyi", "**/*.pyi"] for package in find_packages()},
    zip_safe=False,
)