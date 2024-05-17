import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def dummy_progress(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def extension_disable(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Turn off this extension

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def extension_online_access(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    enable: bool | typing.Any | None = False,
):
    """Handle online access

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param enable: Enable
    :type enable: bool | typing.Any | None
    """

    ...

def extension_theme_disable(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    pkg_id: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
):
    """Turn off this theme

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param pkg_id: Package ID
    :type pkg_id: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    """

    ...

def extension_theme_enable(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    pkg_id: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
):
    """Turn off this theme

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param pkg_id: Package ID
    :type pkg_id: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    """

    ...

def extensions_enable_not_installed(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Turn on this extension

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def extensions_show_for_update(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Show add-on preferences

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def obsolete_marked(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Zeroes package versions, useful for development - to test upgrading

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def pkg_display_errors_clear(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def pkg_install(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    repo_directory: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
    pkg_id: str | typing.Any = "",
    enable_on_install: bool | typing.Any | None = True,
    url: str | typing.Any = "",
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param repo_directory: Repo Directory
    :type repo_directory: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    :param pkg_id: Package ID
    :type pkg_id: str | typing.Any
    :param enable_on_install: Enable on Install, Enable after installing
    :type enable_on_install: bool | typing.Any | None
    :param url: URL
    :type url: str | typing.Any
    """

    ...

def pkg_install_files(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    filter_glob: str | typing.Any = "*.zip",
    directory: str | typing.Any = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    filepath: str | typing.Any = "",
    repo: str | int | typing.Any | None = "",
    enable_on_install: bool | typing.Any | None = True,
    url: str | typing.Any = "",
):
    """Install an extension from a file into a locally managed repository

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param filter_glob: filter_glob
    :type filter_glob: str | typing.Any
    :param directory: Directory
    :type directory: str | typing.Any
    :param files: files
    :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
    :param filepath: filepath
    :type filepath: str | typing.Any
    :param repo: Local Repository, The local repository to install extensions into
    :type repo: str | int | typing.Any | None
    :param enable_on_install: Enable on Install, Enable after installing
    :type enable_on_install: bool | typing.Any | None
    :param url: URL
    :type url: str | typing.Any
    """

    ...

def pkg_install_marked(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    enable_on_install: bool | typing.Any | None = True,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param enable_on_install: Enable on Install, Enable after installing
    :type enable_on_install: bool | typing.Any | None
    """

    ...

def pkg_mark_clear(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    pkg_id: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param pkg_id: Package ID
    :type pkg_id: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    """

    ...

def pkg_mark_set(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    pkg_id: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param pkg_id: Package ID
    :type pkg_id: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    """

    ...

def pkg_show_clear(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    pkg_id: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param pkg_id: Package ID
    :type pkg_id: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    """

    ...

def pkg_show_set(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    pkg_id: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param pkg_id: Package ID
    :type pkg_id: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    """

    ...

def pkg_show_settings(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    pkg_id: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param pkg_id: Package ID
    :type pkg_id: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    """

    ...

def pkg_status_clear(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def pkg_uninstall(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    repo_directory: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
    pkg_id: str | typing.Any = "",
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param repo_directory: Repo Directory
    :type repo_directory: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    :param pkg_id: Package ID
    :type pkg_id: str | typing.Any
    """

    ...

def pkg_uninstall_marked(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def pkg_upgrade_all(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    use_active_only: bool | typing.Any | None = False,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param use_active_only: Active Only, Only sync the active repository
    :type use_active_only: bool | typing.Any | None
    """

    ...

def repo_lock(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Lock repositories - to test locking

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def repo_sync(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    repo_directory: str | typing.Any = "",
    repo_index: typing.Any | None = -1,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param repo_directory: Repo Directory
    :type repo_directory: str | typing.Any
    :param repo_index: Repo Index
    :type repo_index: typing.Any | None
    """

    ...

def repo_sync_all(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    use_active_only: bool | typing.Any | None = False,
):
    """Undocumented, consider contributing.

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param use_active_only: Active Only, Only sync the active repository
    :type use_active_only: bool | typing.Any | None
    """

    ...

def repo_unlock(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Unlock repositories - to test unlocking

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...
