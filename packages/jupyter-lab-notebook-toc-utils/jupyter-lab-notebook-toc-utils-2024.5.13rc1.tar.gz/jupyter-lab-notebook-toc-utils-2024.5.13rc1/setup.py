import setuptools
import os
import logging
import tbd_calver_versioning

# Set the logging level
logging.basicConfig(
    level=logging.DEBUG,
    filename="setup.py.log",
    format="%(asctime)s %(levelname)s [ %(filename)s:%(lineno)s - %(funcName)20s() ] - %(message)s"
)

# Read the text from the requirements file
with open('requirements.txt') as file:
    lines = file.readlines()
    install_requires = [line.rstrip() for line in lines]

# Read the text from the README
with open('README.md', "r") as fh:
    long_description = fh.read()   

# Set the directory for the source code to be installed
source_code_dir = "src"

# Determine which versioning scheme to use
VERSION_FOR_PYPI = None
try:
    VERSION_FOR_PYPI = os.environ['VERSION_FOR_PYPI']
except Exception as e:
    logging.warning(f"The environment variable VERSION_FOR_PYPI was not set. Defaulting to 'false'.")
    VERSION_FOR_PYPI="false"

if VERSION_FOR_PYPI == "true":
    version_number = tbd_calver_versioning.determine_version_number(adjust_for_pypi=True)
else:
    version_number = tbd_calver_versioning.determine_version_number()
    
# Run the setuptools setup function to install our code
package_name = "jupyter-lab-notebook-toc-utils"
setuptools.setup(
    name=package_name,
    version=version_number,
    author="tschneider",
    author_email="tschneider@live.com",
    description="Tools for creating a table of contents for a jupyter lab notebook.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={
        "": source_code_dir
    },
    install_requires= install_requires,
    classifiers=[
        "Programming Language :: Unix Shell",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    url=""
)