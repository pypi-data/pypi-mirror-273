"""Module for managing the version of the lib_version_group3 package.

This module provides a class that allows for easy retrieval of the package's
version, making it useful for logs, debugging, and runtime checks.
"""


class VersionUtil:
    """
    Utility class for handling version information of the
    lib_version_group3 package.
    """
    # pylint: disable=R0903

    @staticmethod
    def get_version():
        """Retrieve the current version of the library.

        Returns:
            str: The current library version.
        """
        return __version__


__version__ = '0.0.1'
