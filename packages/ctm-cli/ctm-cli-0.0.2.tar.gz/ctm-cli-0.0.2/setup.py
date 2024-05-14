import setuptools
from ctm_cli import __version__
version = __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ctm-cli",
    version=version,
    author="Huseyin G.",
    author_email="huseyim@gmail.com",
    description="A command-line tool for managing configurations, tasks, and schedules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gomleksiz/ctm-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'click>=8.0.0',
        'pyyaml>=5.4.1',
        'apscheduler>=3.7.0',
    ],
    entry_points={
        'console_scripts': [
            'ctm=ctm_cli.main:run',
        ],
    },
)
