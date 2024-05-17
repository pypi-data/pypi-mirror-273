import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def create(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    name: str | typing.Any = "Collection",
):
    """Create an object collection from selected objects

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param name: Name, Name of the new collection
    :type name: str | typing.Any
    """

    ...

def export_all(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Invoke all configured exporters on this collection

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def exporter_add(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    name: str | typing.Any = "",
):
    """Add Exporter

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param name: Name, FileHandler idname
    :type name: str | typing.Any
    """

    ...

def exporter_export(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    index: typing.Any | None = 0,
):
    """Invoke the export operation

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param index: Index, Exporter index
    :type index: typing.Any | None
    """

    ...

def exporter_remove(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    index: typing.Any | None = 0,
):
    """Remove Exporter

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param index: Index, Exporter index
    :type index: typing.Any | None
    """

    ...

def objects_add_active(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    collection: str | int | typing.Any | None = "",
):
    """Add the object to an object collection that contains the active object

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param collection: Collection, The collection to add other selected objects to
    :type collection: str | int | typing.Any | None
    """

    ...

def objects_remove(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    collection: str | int | typing.Any | None = "",
):
    """Remove selected objects from a collection

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param collection: Collection, The collection to remove this object from
    :type collection: str | int | typing.Any | None
    """

    ...

def objects_remove_active(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    collection: str | int | typing.Any | None = "",
):
    """Remove the object from an object collection that contains the active object

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param collection: Collection, The collection to remove other selected objects from
    :type collection: str | int | typing.Any | None
    """

    ...

def objects_remove_all(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Remove selected objects from all collections

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...
