"""
This module initializes the `lib_version_group3` package.

It provides access to the VersionUtil and the version string of the library.
"""


from .version import __version__, VersionUtil

__all__ = ["VersionUtil", "__version__"]
