import codecs
import os
from distutils.version import LooseVersion

from setuptools import setup, find_packages
import _version_ as metadata

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
    'argparse==1.4.0',  # Python command-line parsing library
    'euclid3==0.01',  # 2D and 3D vector, matrix, quaternion and geometry module.
    'six==1.16.0',  # Python 2 and 3 compatibility utilities
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


def assert_version_classifier(version_str):
    """
    Verify version consistency:
    version number must correspond to the correct "Development Status" classifier
    :raises: ValueError if error found, but ideally this function does nothing
    """
    V = lambda v: LooseVersion(v)
    # cast version
    version = V(version_str)

    # get "Development  Status" classifier
    dev_status_list = [x for x in CLASSIFIERS if x.startswith("Development Status ::")]
    if len(dev_status_list) != 1:
        raise ValueError("must be 1 'Development Status' in CLASSIFIERS")
    classifier = dev_status_list.pop()

    version_map = [
        (V('0.1'), "Development Status :: 2 - Pre-Alpha"),
        (V('0.2'), "Development Status :: 3 - Alpha"),
        (V('0.3'), "Development Status :: 4 - Beta"),
        (V('1.0'), "Development Status :: 5 - Production/Stable"),
    ]

    for (test_ver, test_classifier) in reversed(sorted(version_map, key=lambda x: x[0])):
        if version >= test_ver:
            if classifier == test_classifier:
                return  # all good, now forget any of this ever happened
            else:
                raise ValueError("for version {ver} classifier should be \n'{good}'\nnot\n'{bad}'".format(
                    ver=str(version), good=test_classifier, bad=classifier
                ))


if __name__ == "__main__":
    version = metadata._version_
    assert_version_classifier(version)

    setup(
        name=NAME,
        description=metadata.__description__,
        license=metadata.__license__,
        url=metadata.__url__,
        version=version,
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
        setup_requires=INSTALL_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        scripts=SCRIPTS,
    )
