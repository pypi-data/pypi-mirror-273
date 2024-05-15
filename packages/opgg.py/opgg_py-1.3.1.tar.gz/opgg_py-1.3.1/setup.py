from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="opgg.py",
    version="1.3.1",
    description="An unofficial Python library for scraping/accessing data from OP.GG",  # Optional
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShoobyDoo/OPGG.py",
    # This should be your name or the name of the organization which owns the
    # project.
    author="ShoobyDoo",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="opgg, league-of-legends, web-scraping, summoner, data, riot-api",  # Optional
    packages=find_packages(),  # Required
    python_requires=">=3.11, <4",
    install_requires=["beautifulsoup4", "requests"],  # Optional
    project_urls={  # Optional
        "Bug Reports": "https://github.com/ShoobyDoo/OPGG.py/issues",
        "Source": "https://github.com/ShoobyDoo/OPGG.py",
    },
)