import codecs
import os
from distutils.version import LooseVersion

from setuptools import setup, find_packages
import src.pygcode.__version__ as metadata

# Setup template thanks to: Hynek Schlawack
#   https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
###################################################################

NAME = "pygcode"
PACKAGES = find_packages(where="src")
HERE = os.path.abspath(os.path.dirname(__file__))

KEYWORDS = ['gcode', 'cnc', 'parser', 'interpreter']
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",  # see src/pygcode/__init__.py
    "Intended Audience :: Developers",
    "Intended Audience :: Manufacturing",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
]
INSTALL_REQUIRES = [
    'argparse',  # Python command-line parsing library
    'euclid3',  # 2D and 3D vector, matrix, quaternion and geometry module.
    'six',  # Python 2 and 3 compatibility utilities
]
SCRIPTS = [
    'scripts/pygcode-norm',
    'scripts/pygcode-crop',
]

###################################################################


def read(*parts):
    """
    Build an absolute path from *parts* and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


if __name__ == "__main__":

    setup(
        name=NAME,
        description=metadata.__description__,
        license=metadata.__license__,
        url=metadata.__url__,
        version=metadata.__version__,
        author=metadata.__author__,
        author_email=metadata.__email__,
        maintainer=metadata.__author__,
        maintainer_email=metadata.__email__,
        keywords=KEYWORDS,
        long_description=read("README.rst"),
        packages=PACKAGES,
        package_dir={"": "src"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        scripts=SCRIPTS,
    )
