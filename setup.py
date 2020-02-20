import setuptools
from instrumental_dl.__version__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="instrumental-dl",
    version=__version__,

    python_requires='>=3.6',
    install_requires=['youtube_dl>=2020.2.16'],
    data_files=[("config", ["config/arg_help.json", "config/keywords",
        "config/logging.conf"])],
    include_package_data=True,

    description="A command line tool to easily download song instrumentals from Youtube.",
    author="QualityHammer",
    author_email="agingllama@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QualityHammer/instrumental-downloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    entry_points={
        "console_scripts": ["instrumental-dl=instrumental_dl.client:run"]
    }
)
