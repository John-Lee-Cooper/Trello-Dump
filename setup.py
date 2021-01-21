#!/usr/bin/env python

from setuptools import setup
from pathlib import Path

# The text of the README file in directory containing this file
README = (Path(__file__).parent / "README.md").read_text()

setup(
    name="trello-dump",
    version="0.0.1",
    description="Trello Dump is a utility to dump the contents of a Trello board to an Excel spreadsheet.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="trello,oauth,click",
    install_requires=['certifi==2020.12.5', 'chardet==3.0.4', 'click==7.1.2', 'idna==2.10', 'numpy==1.19.4', 'oauthlib==3.1.0', 'pandas==1.2.0', 'py-trello==0.17.1', 'python-dateutil==2.8.1', 'pytz==2020.4', 'pyyaml==5.3.1', 'requests-oauthlib==1.3.0', 'requests==2.25.0', 'six==1.15.0', 'typer==0.3.2', 'urllib3==1.26.2', 'xlsxwriter==1.3.7'],
    # dependency_links="",
    packages=['trellod'],
    data_files=[],
    python_requires=">=3.6",
    entry_points=dict(console_scripts=["trellod=trellod.trellod:main"]),
    url="https://github.com/John-Lee-Cooper/trello-dump/",
    download_url="https://github.com/John-Lee-Cooper/trello-dump/archive/1.0.0.tar.gz",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    license="GPL",
    author="John Lee Cooper",
    author_email="john.lee.cooper@gatech.edu",
)
