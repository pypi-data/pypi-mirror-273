from setuptools import setup, find_packages

setup(
    name="prodmatic",
    version="2024.05.14",
    description="A Python package for seamless management and pricing of in-app products and subscriptions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Gopala Krishna Koduri",
    author_email="gopal@riyazapp.com",
    url="https://github.com/musicmuni/prodmatic",
    project_urls={
        "Source Code": "https://github.com/musicmuni/prodmatic",
        "Issue Tracker": "https://github.com/musicmuni/prodmatic/issues",
        "Connect w/ Author": "https://linkedin.com/in/gopalkoduri",
        "Riyaz - Learn to sing": "https://riyazapp.com",
    },
    packages=find_packages(),
    package_data={
        "prodmatic": [
            "resources/*.csv",
            "resources/*.json",
        ],
    },
    include_package_data=True,
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pyrestcountries",
        "pppfy",
        "moneymatters",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
