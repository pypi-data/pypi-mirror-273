# python3-cyberfusion-common

Common utilities.

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-common

## Generic

Run the following command to create a source distribution:

    python3 setup.py sdist

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

No configuration is supported.

# Usage

See code.

# Tests

Run tests with pytest:

    pytest tests/

The tests must be run from the project root.
