"""
This module has a similar scope to os.path, containing utility
functions for dealing with paths in Blender.

"""

import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def abspath(
    path,
    start: typing.Optional[typing.Union[str, bytes]] = None,
    library: typing.Optional[bpy.types.Library] = None,
) -> str:
    """Returns the absolute path relative to the current blend file
    using the "//" prefix.

        :param start: Relative to this path,
    when not set the current filename is used.
        :type start: typing.Optional[typing.Union[str, bytes]]
        :param library: The library this path is from. This is only included for
    convenience, when the library is not None its path replaces start.
        :type library: typing.Optional[bpy.types.Library]
        :return: The absolute path.
        :rtype: str
    """

    ...

def abspath(path, start, library):
    """ """

    ...

def basename(path) -> str:
    """Equivalent to os.path.basename, but skips a "//" prefix.Use for Windows compatibility.

    :return: The base name of the given path.
    :rtype: str
    """

    ...

def basename(path):
    """ """

    ...

def clean_name(
    name: typing.Optional[typing.Union[str, bytes]], replace: typing.Optional[str] = "_"
) -> str:
    """Returns a name with characters replaced that
    may cause problems under various circumstances,
    such as writing to a file.All characters besides A-Z/a-z, 0-9 are replaced with "_"
    or the replace argument if defined.

        :param name: The path name.
        :type name: typing.Optional[typing.Union[str, bytes]]
        :param replace: The replacement for non-valid characters.
        :type replace: typing.Optional[str]
        :return: The cleaned name.
        :rtype: str
    """

    ...

def clean_name(name, replace):
    """ """

    ...

def display_name(
    name: typing.Optional[str],
    has_ext: typing.Optional[bool] = True,
    title_case: typing.Optional[bool] = True,
) -> str:
    """Creates a display string from name to be used menus and the user interface.
    Intended for use with filenames and module names.

        :param name: The name to be used for displaying the user interface.
        :type name: typing.Optional[str]
        :param has_ext: Remove file extension from name.
        :type has_ext: typing.Optional[bool]
        :param title_case: Convert lowercase names to title case.
        :type title_case: typing.Optional[bool]
        :return: The display string.
        :rtype: str
    """

    ...

def display_name(name, has_ext, title_case):
    """ """

    ...

def display_name_from_filepath(name: typing.Optional[str]) -> str:
    """Returns the path stripped of directory and extension,
    ensured to be utf8 compatible.

        :param name: The file path to convert.
        :type name: typing.Optional[str]
        :return: The display name.
        :rtype: str
    """

    ...

def display_name_from_filepath(name):
    """ """

    ...

def display_name_to_filepath(name: typing.Optional[str]) -> str:
    """Performs the reverse of display_name using literal versions of characters
    which aren't supported in a filepath.

        :param name: The display name to convert.
        :type name: typing.Optional[str]
        :return: The file path.
        :rtype: str
    """

    ...

def display_name_to_filepath(name):
    """ """

    ...

def ensure_ext(
    filepath: typing.Optional[str],
    ext: typing.Optional[str],
    case_sensitive: typing.Optional[bool] = False,
) -> str:
    """Return the path with the extension added if it is not already set.

        :param filepath: The file path.
        :type filepath: typing.Optional[str]
        :param ext: The extension to check for, can be a compound extension. Should
    start with a dot, such as '.blend' or '.tar.gz'.
        :type ext: typing.Optional[str]
        :param case_sensitive: Check for matching case when comparing extensions.
        :type case_sensitive: typing.Optional[bool]
        :return: The file path with the given extension.
        :rtype: str
    """

    ...

def ensure_ext(filepath, ext, case_sensitive):
    """ """

    ...

def is_subdir(path: typing.Optional[typing.Union[str, bytes]], directory) -> bool:
    """Returns true if path in a subdirectory of directory.
    Both paths must be absolute.

        :param path: An absolute path.
        :type path: typing.Optional[typing.Union[str, bytes]]
        :return: Whether or not the path is a subdirectory.
        :rtype: bool
    """

    ...

def is_subdir(path, directory):
    """ """

    ...

def module_names(
    path: typing.Optional[str],
    recursive: typing.Optional[bool] = False,
    package: typing.Optional[str] = "",
) -> typing.List[str]:
    """Return a list of modules which can be imported from path.

    :param path: a directory to scan.
    :type path: typing.Optional[str]
    :param recursive: Also return submodule names for packages.
    :type recursive: typing.Optional[bool]
    :param package: Optional string, used as the prefix for module names (without the trailing ".").
    :type package: typing.Optional[str]
    :return: a list of string pairs (module_name, module_file).
    :rtype: typing.List[str]
    """

    ...

def module_names(path, recursive, package):
    """ """

    ...

def native_pathsep(path: typing.Optional[str]) -> str:
    """Replace the path separator with the systems native os.sep.

    :param path: The path to replace.
    :type path: typing.Optional[str]
    :return: The path with system native separators.
    :rtype: str
    """

    ...

def native_pathsep(path):
    """ """

    ...

def reduce_dirs(dirs: typing.Optional[typing.List[str]]) -> typing.List[str]:
    """Given a sequence of directories, remove duplicates and
    any directories nested in one of the other paths.
    (Useful for recursive path searching).

        :param dirs: Sequence of directory paths.
        :type dirs: typing.Optional[typing.List[str]]
        :return: A unique list of paths.
        :rtype: typing.List[str]
    """

    ...

def reduce_dirs(dirs):
    """ """

    ...

def relpath(
    path: typing.Optional[typing.Union[str, bytes]],
    start: typing.Optional[typing.Union[str, bytes]] = None,
) -> str:
    """Returns the path relative to the current blend file using the "//" prefix.

        :param path: An absolute path.
        :type path: typing.Optional[typing.Union[str, bytes]]
        :param start: Relative to this path,
    when not set the current filename is used.
        :type start: typing.Optional[typing.Union[str, bytes]]
        :return: The relative path.
        :rtype: str
    """

    ...

def relpath(path, start):
    """ """

    ...

def resolve_ncase(path: typing.Optional[str]) -> str:
    """Resolve a case insensitive path on a case sensitive system,
    returning a string with the path if found else return the original path.

        :param path: The path name to resolve.
        :type path: typing.Optional[str]
        :return: The resolved path.
        :rtype: str
    """

    ...

def resolve_ncase(path):
    """ """

    ...
