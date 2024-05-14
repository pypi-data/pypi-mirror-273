from setuptools import setup, find_packages
VERSION = '0.0.59'
DESCRIPTION = 'Phenom Public Apis SDK for Python'
def read_readme():
    with open('README.md', 'r') as f:
        return f.read()
# Setting up
setup(
    name="phenomApis",
    version=VERSION,
    author="phenom",
    author_email="8297991468h@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=read_readme(),
    packages=find_packages(),
    keywords=['resumeparser', 'exsearch'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)