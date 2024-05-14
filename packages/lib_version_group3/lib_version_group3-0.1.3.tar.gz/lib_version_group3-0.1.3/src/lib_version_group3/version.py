# pylint: disable=R0903

"""Module for managing the version of the lib_version_group3 package.

This module provides a class that allows for easy retrieval of the package's
version, making it useful for logs, debugging, and runtime checks.
"""


from importlib.metadata import version, PackageNotFoundError


class VersionUtil:
    """
    Utility class for handling version information of the
    lib_version_group3 package.
    """
    @staticmethod
    def get_version():
        """Retrieve the current version of the lib_version_group3 package.

        Returns:
            str: The version of the lib_version_group3 package if found,
            otherwise returns 'Package not found'.
        """
        package_name = "lib_version_group3"
        try:
            return version(package_name)
        except PackageNotFoundError:
            return "Package not found"
