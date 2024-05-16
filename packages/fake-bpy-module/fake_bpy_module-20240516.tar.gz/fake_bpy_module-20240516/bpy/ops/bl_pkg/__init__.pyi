import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def dummy_progress(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def extension_disable(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Turn off this extension

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def extension_online_access(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    enable: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Handle online access

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param enable: Enable
    :type enable: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def extension_theme_disable(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    pkg_id: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
):
    """Turn off this theme

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param pkg_id: Package ID
    :type pkg_id: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    """

    ...

def extension_theme_enable(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    pkg_id: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
):
    """Turn off this theme

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param pkg_id: Package ID
    :type pkg_id: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    """

    ...

def extensions_enable_not_installed(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Turn on this extension

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def extensions_show_for_update(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Show add-on preferences

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def obsolete_marked(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Zeroes package versions, useful for development - to test upgrading

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def pkg_display_errors_clear(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def pkg_install(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    repo_directory: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
    pkg_id: typing.Union[str, typing.Any] = "",
    enable_on_install: typing.Optional[typing.Union[bool, typing.Any]] = True,
    url: typing.Union[str, typing.Any] = "",
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param repo_directory: Repo Directory
    :type repo_directory: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    :param pkg_id: Package ID
    :type pkg_id: typing.Union[str, typing.Any]
    :param enable_on_install: Enable on Install, Enable after installing
    :type enable_on_install: typing.Optional[typing.Union[bool, typing.Any]]
    :param url: URL
    :type url: typing.Union[str, typing.Any]
    """

    ...

def pkg_install_files(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filter_glob: typing.Union[str, typing.Any] = "*.zip",
    directory: typing.Union[str, typing.Any] = "",
    files: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    ] = None,
    filepath: typing.Union[str, typing.Any] = "",
    repo: typing.Optional[typing.Union[str, int, typing.Any]] = "",
    enable_on_install: typing.Optional[typing.Union[bool, typing.Any]] = True,
    url: typing.Union[str, typing.Any] = "",
):
    """Install an extension from a file into a locally managed repository

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param filter_glob: filter_glob
    :type filter_glob: typing.Union[str, typing.Any]
    :param directory: Directory
    :type directory: typing.Union[str, typing.Any]
    :param files: files
    :type files: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]]
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    :param repo: Local Repository, The local repository to install extensions into
    :type repo: typing.Optional[typing.Union[str, int, typing.Any]]
    :param enable_on_install: Enable on Install, Enable after installing
    :type enable_on_install: typing.Optional[typing.Union[bool, typing.Any]]
    :param url: URL
    :type url: typing.Union[str, typing.Any]
    """

    ...

def pkg_install_marked(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    enable_on_install: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param enable_on_install: Enable on Install, Enable after installing
    :type enable_on_install: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def pkg_mark_clear(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    pkg_id: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param pkg_id: Package ID
    :type pkg_id: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    """

    ...

def pkg_mark_set(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    pkg_id: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param pkg_id: Package ID
    :type pkg_id: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    """

    ...

def pkg_show_clear(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    pkg_id: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param pkg_id: Package ID
    :type pkg_id: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    """

    ...

def pkg_show_set(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    pkg_id: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param pkg_id: Package ID
    :type pkg_id: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    """

    ...

def pkg_show_settings(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    pkg_id: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param pkg_id: Package ID
    :type pkg_id: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    """

    ...

def pkg_status_clear(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def pkg_uninstall(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    repo_directory: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
    pkg_id: typing.Union[str, typing.Any] = "",
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param repo_directory: Repo Directory
    :type repo_directory: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    :param pkg_id: Package ID
    :type pkg_id: typing.Union[str, typing.Any]
    """

    ...

def pkg_uninstall_marked(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def pkg_upgrade_all(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    use_active_only: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param use_active_only: Active Only, Only sync the active repository
    :type use_active_only: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def repo_lock(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Lock repositories - to test locking

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def repo_sync(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    repo_directory: typing.Union[str, typing.Any] = "",
    repo_index: typing.Optional[typing.Any] = -1,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param repo_directory: Repo Directory
    :type repo_directory: typing.Union[str, typing.Any]
    :param repo_index: Repo Index
    :type repo_index: typing.Optional[typing.Any]
    """

    ...

def repo_sync_all(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    use_active_only: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param use_active_only: Active Only, Only sync the active repository
    :type use_active_only: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def repo_unlock(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Unlock repositories - to test unlocking

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...
