from setuptools import setup

from instrumental_dl.version import __version__


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="instrumental_dl",
    version=__version__,
    packages=[
        'instrumental_dl', 'instrumental_dl.common',
        'instrumental_dl.logger', 'instrumental_dl.config'
    ],
    data_files=[
        ('config', ['instrumental_dl/config/keywords.txt',
                    'instrumental_dl/config/arg_help.txt'])
    ],
    include_package_data=True,

    install_requires=['youtube_dl>=2019.9.28'],
    python_requires='>=3.6',

    author="QualityHammer",
    author_email="agingllama@gmail.com",
    description="Download the instrumental for almost any song",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='instrumental downloader',
    url='https://github.com/QualityHammer/instrumental-downloader',

    entry_points={
        'console_scripts': [
            'instrumental_dl=instrumental_dl:main'
        ]
    }
)
