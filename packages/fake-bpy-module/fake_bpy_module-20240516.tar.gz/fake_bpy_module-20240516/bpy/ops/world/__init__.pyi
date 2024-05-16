import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def convert_volume_to_mesh(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Convert the volume of a world to a mesh.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def new(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Create a new world Data-Block

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...
