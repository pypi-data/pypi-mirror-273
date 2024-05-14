from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

with open("LICENSE", "r") as li:
    lic = li.read()

setup(
    name="ducttape-calpads",
    version="0.4.0",
    author="Yusuph Mkangara",
    author_email="ymkangara@summitps.org",
    description="Extension of the duct-tape package to automate CALPADS data extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=lic,
    url="https://github.com/SummitPublicSchools/ducttape-calpads",
    packages=find_packages(include=["ducttape_calpads"]),
    install_requires=["duct-tape>=0.24.0, <1.0.0"]
)
