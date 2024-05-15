from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Streaming video data via networks'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="django_multi_bulk_updater",
    version=VERSION,
    author="Sushil",
    author_email="SushilPrasad60649@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['django'],
    keywords=['django bulk updater', 'bulk updater', 'bulk', 'chunk updater','python django'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)