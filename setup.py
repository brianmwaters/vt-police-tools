"""Setup script."""

import glob
import importlib
import os
import setuptools

import vt_police_tools


def components(path):
    """Split a POSIX path into components."""
    head, tail = os.path.split(os.path.normpath(path))
    if head == "":
        return [tail]
    elif head == "/":
        return [head + tail]
    else:
        return components(head) + [tail]


def strip_leading_component(path):
    """Remove the leading component from a POSIX path."""
    return os.path.join(*components(path)[1:])


def _package_data_glob(glob_):
    return [strip_leading_component(path) for path in
            glob.iglob(glob_, recursive=True)]


def _package_data_globs(*globs):
    paths = []
    for glob_ in globs:
        paths += _package_data_glob(glob_)
    return paths


def _read_readme(readme):
    with open(readme, "r") as file_:
        return file_.read()


setuptools.setup(
    name="vt-police-tools",
    version=vt_police_tools.__version__,
    description="Tools for cleaning Vermont police data",
    long_description=_read_readme("./README.rst"),
    long_description_content_type="text/x-rst",
    keywords="police vermont",
    author="BTV CopWatch",
    author_email="info@btvcopwatch.org",
    url="https://github.com/brianmwaters/vt-police-tools/",
    project_urls={
        "BTV CopWatch": "https://www.btvcopwatch.org/",
        "OpenOversight": "https://www.openoversight.com/",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Other Audience",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Other/Nonlisted Topic",
    ],
    python_requires="~=3.7",
    install_requires=[
        "pandas~=1.1.0",
    ],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "vpt=vt_police_tools.cli:main",
        ],
    },
    package_data={
        "vt_police_tools": _package_data_globs(
            "./vt_police_tools/data/**",
            "./vt_police_tools/scripts/**",
        ),
    },
)
