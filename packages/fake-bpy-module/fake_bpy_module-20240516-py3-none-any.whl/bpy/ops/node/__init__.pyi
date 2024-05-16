import typing
import bl_operators.node
import bpy.ops.transform
import bpy.types

GenericType = typing.TypeVar("GenericType")

def add_collection(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    name: typing.Union[str, typing.Any] = "",
    session_uid: typing.Optional[typing.Any] = 0,
):
    """Add a collection info node to the current node editor

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of the data-block to use by the operator
    :type name: typing.Union[str, typing.Any]
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: typing.Optional[typing.Any]
    """

    ...

def add_file(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filepath: typing.Union[str, typing.Any] = "",
    directory: typing.Union[str, typing.Any] = "",
    files: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    ] = None,
    hide_props_region: typing.Optional[typing.Union[bool, typing.Any]] = True,
    check_existing: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_blender: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_backup: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_image: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_movie: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_python: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_font: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_sound: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_text: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_archive: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_btx: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_collada: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_alembic: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_usd: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_obj: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_volume: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_folder: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_blenlib: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filemode: typing.Optional[typing.Any] = 9,
    relative_path: typing.Optional[typing.Union[bool, typing.Any]] = True,
    show_multiview: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_multiview: typing.Optional[typing.Union[bool, typing.Any]] = False,
    display_type: typing.Optional[typing.Any] = "DEFAULT",
    sort_method: typing.Optional[typing.Any] = "",
    name: typing.Union[str, typing.Any] = "",
    session_uid: typing.Optional[typing.Any] = 0,
):
    """Add a file node to the current node editor

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param filepath: File Path, Path to file
        :type filepath: typing.Union[str, typing.Any]
        :param directory: Directory, Directory of the file
        :type directory: typing.Union[str, typing.Any]
        :param files: Files
        :type files: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]]
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: typing.Optional[typing.Union[bool, typing.Any]]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_blender: Filter .blend files
        :type filter_blender: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_backup: Filter .blend files
        :type filter_backup: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_image: Filter image files
        :type filter_image: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_movie: Filter movie files
        :type filter_movie: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_python: Filter Python files
        :type filter_python: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_font: Filter font files
        :type filter_font: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_sound: Filter sound files
        :type filter_sound: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_text: Filter text files
        :type filter_text: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_archive: Filter archive files
        :type filter_archive: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_btx: Filter btx files
        :type filter_btx: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_collada: Filter COLLADA files
        :type filter_collada: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_usd: Filter USD files
        :type filter_usd: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_obj: Filter OBJ files
        :type filter_obj: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_folder: Filter folders
        :type filter_folder: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: typing.Optional[typing.Union[bool, typing.Any]]
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Optional[typing.Any]
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: typing.Optional[typing.Union[bool, typing.Any]]
        :param show_multiview: Enable Multi-View
        :type show_multiview: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_multiview: Use Multi-View
        :type use_multiview: typing.Optional[typing.Union[bool, typing.Any]]
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: typing.Optional[typing.Any]
        :param sort_method: File sorting mode

    DEFAULT
    Default -- Automatically determine sort method for files.

    FILE_SORT_ALPHA
    Name -- Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension -- Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date -- Sort files by modification time.

    FILE_SORT_SIZE
    Size -- Sort files by size.
        :type sort_method: typing.Optional[typing.Any]
        :param name: Name, Name of the data-block to use by the operator
        :type name: typing.Union[str, typing.Any]
        :param session_uid: Session UID, Session UID of the data-block to use by the operator
        :type session_uid: typing.Optional[typing.Any]
    """

    ...

def add_group(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    name: typing.Union[str, typing.Any] = "",
    session_uid: typing.Optional[typing.Any] = 0,
    show_datablock_in_node: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Add an existing node group to the current node editor

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of the data-block to use by the operator
    :type name: typing.Union[str, typing.Any]
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: typing.Optional[typing.Any]
    :param show_datablock_in_node: Show the datablock selector in the node
    :type show_datablock_in_node: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def add_group_asset(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    asset_library_type: typing.Optional[typing.Union[str, int]] = "LOCAL",
    asset_library_identifier: typing.Union[str, typing.Any] = "",
    relative_asset_identifier: typing.Union[str, typing.Any] = "",
):
    """Add a node group asset to the active node tree

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param asset_library_type: Asset Library Type
    :type asset_library_type: typing.Optional[typing.Union[str, int]]
    :param asset_library_identifier: Asset Library Identifier
    :type asset_library_identifier: typing.Union[str, typing.Any]
    :param relative_asset_identifier: Relative Asset Identifier
    :type relative_asset_identifier: typing.Union[str, typing.Any]
    """

    ...

def add_mask(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    name: typing.Union[str, typing.Any] = "",
    session_uid: typing.Optional[typing.Any] = 0,
):
    """Add a mask node to the current node editor

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of the data-block to use by the operator
    :type name: typing.Union[str, typing.Any]
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: typing.Optional[typing.Any]
    """

    ...

def add_material(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    name: typing.Union[str, typing.Any] = "",
    session_uid: typing.Optional[typing.Any] = 0,
):
    """Add a material node to the current node editor

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of the data-block to use by the operator
    :type name: typing.Union[str, typing.Any]
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: typing.Optional[typing.Any]
    """

    ...

def add_node(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    use_transform: typing.Optional[typing.Union[bool, typing.Any]] = False,
    settings: typing.Optional[
        bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    ] = None,
    type: typing.Union[str, typing.Any] = "",
):
    """Add a node to the active tree

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param use_transform: Use Transform, Start transform operator after inserting the node
    :type use_transform: typing.Optional[typing.Union[bool, typing.Any]]
    :param settings: Settings, Settings to be applied on the newly created node
    :type settings: typing.Optional[bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]]
    :param type: Node Type, Node type
    :type type: typing.Union[str, typing.Any]
    """

    ...

def add_object(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    name: typing.Union[str, typing.Any] = "",
    session_uid: typing.Optional[typing.Any] = 0,
):
    """Add an object info node to the current node editor

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of the data-block to use by the operator
    :type name: typing.Union[str, typing.Any]
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: typing.Optional[typing.Any]
    """

    ...

def add_repeat_zone(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    use_transform: typing.Optional[typing.Union[bool, typing.Any]] = False,
    settings: typing.Optional[
        bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    ] = None,
    offset: typing.Optional[typing.Any] = (150.0, 0.0),
):
    """Add a repeat zone that allows executing nodes a dynamic number of times

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param use_transform: Use Transform, Start transform operator after inserting the node
    :type use_transform: typing.Optional[typing.Union[bool, typing.Any]]
    :param settings: Settings, Settings to be applied on the newly created node
    :type settings: typing.Optional[bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]]
    :param offset: Offset, Offset of nodes from the cursor when added
    :type offset: typing.Optional[typing.Any]
    """

    ...

def add_reroute(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    path: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]
    ] = None,
    cursor: typing.Optional[typing.Any] = 8,
):
    """Add a reroute node

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param path: Path
    :type path: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]]
    :param cursor: Cursor
    :type cursor: typing.Optional[typing.Any]
    """

    ...

def add_simulation_zone(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    use_transform: typing.Optional[typing.Union[bool, typing.Any]] = False,
    settings: typing.Optional[
        bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    ] = None,
    offset: typing.Optional[typing.Any] = (150.0, 0.0),
):
    """Add simulation zone input and output nodes to the active tree

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param use_transform: Use Transform, Start transform operator after inserting the node
    :type use_transform: typing.Optional[typing.Union[bool, typing.Any]]
    :param settings: Settings, Settings to be applied on the newly created node
    :type settings: typing.Optional[bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]]
    :param offset: Offset, Offset of nodes from the cursor when added
    :type offset: typing.Optional[typing.Any]
    """

    ...

def attach(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Attach active node to a frame

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def backimage_fit(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Fit the background image to the view

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def backimage_move(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Move node backdrop

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def backimage_sample(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Use mouse to sample background image

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def backimage_zoom(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    factor: typing.Optional[typing.Any] = 1.2,
):
    """Zoom in/out the background image

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param factor: Factor
    :type factor: typing.Optional[typing.Any]
    """

    ...

def bake_node_item_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add bake item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def bake_node_item_move(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    direction: typing.Optional[typing.Any] = "UP",
):
    """Move active bake item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param direction: Direction, Move direction
    :type direction: typing.Optional[typing.Any]
    """

    ...

def bake_node_item_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove active bake item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def clear_viewer_border(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Clear the boundaries for viewer operations

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def clipboard_copy(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Copy the selected nodes to the internal clipboard

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def clipboard_paste(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    offset: typing.Optional[typing.Any] = (0.0, 0.0),
):
    """Paste nodes from the internal clipboard to the active node tree

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param offset: Location, The 2D view location for the center of the new nodes, or unchanged if not set
    :type offset: typing.Optional[typing.Any]
    """

    ...

def collapse_hide_unused_toggle(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Toggle collapsed nodes and hide unused sockets

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def cryptomatte_layer_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add a new input layer to a Cryptomatte node

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def cryptomatte_layer_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove layer from a Cryptomatte node

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def deactivate_viewer(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Deactivate selected viewer node in geometry nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def delete(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def delete_reconnect(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove nodes and reconnect nodes as if deletion was muted

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def detach(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Detach selected nodes from parents

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def detach_translate_attach(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    NODE_OT_detach: typing.Optional[detach] = None,
    TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate] = None,
    NODE_OT_attach: typing.Optional[attach] = None,
):
    """Detach nodes, move and attach to frame

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param NODE_OT_detach: Detach Nodes, Detach selected nodes from parents
    :type NODE_OT_detach: typing.Optional[detach]
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate]
    :param NODE_OT_attach: Attach Nodes, Attach active node to a frame
    :type NODE_OT_attach: typing.Optional[attach]
    """

    ...

def duplicate(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    keep_inputs: typing.Optional[typing.Union[bool, typing.Any]] = False,
    linked: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Duplicate selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param keep_inputs: Keep Inputs, Keep the input links to duplicated nodes
    :type keep_inputs: typing.Optional[typing.Union[bool, typing.Any]]
    :param linked: Linked, Duplicate node but not node trees, linking to the original data
    :type linked: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def duplicate_move(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    NODE_OT_duplicate: typing.Optional[duplicate] = None,
    NODE_OT_translate_attach: typing.Optional[translate_attach] = None,
):
    """Duplicate selected nodes and move them

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param NODE_OT_duplicate: Duplicate Nodes, Duplicate selected nodes
    :type NODE_OT_duplicate: typing.Optional[duplicate]
    :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame
    :type NODE_OT_translate_attach: typing.Optional[translate_attach]
    """

    ...

def duplicate_move_keep_inputs(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    NODE_OT_duplicate: typing.Optional[duplicate] = None,
    NODE_OT_translate_attach: typing.Optional[translate_attach] = None,
):
    """Duplicate selected nodes keeping input links and move them

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param NODE_OT_duplicate: Duplicate Nodes, Duplicate selected nodes
    :type NODE_OT_duplicate: typing.Optional[duplicate]
    :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame
    :type NODE_OT_translate_attach: typing.Optional[translate_attach]
    """

    ...

def duplicate_move_linked(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    NODE_OT_duplicate: typing.Optional[duplicate] = None,
    NODE_OT_translate_attach: typing.Optional[translate_attach] = None,
):
    """Duplicate selected nodes, but not their node trees, and move them

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param NODE_OT_duplicate: Duplicate Nodes, Duplicate selected nodes
    :type NODE_OT_duplicate: typing.Optional[duplicate]
    :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame
    :type NODE_OT_translate_attach: typing.Optional[translate_attach]
    """

    ...

def enum_definition_item_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add menu item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def enum_definition_item_move(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    direction: typing.Optional[typing.Any] = "UP",
):
    """Move active menu item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param direction: Direction, Move direction
    :type direction: typing.Optional[typing.Any]
    """

    ...

def enum_definition_item_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove active menu item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def find_node(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Search for a node by name and focus and select it

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def gltf_settings_node_operator(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add a node to the active tree for glTF export

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def group_edit(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    exit: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Edit node group

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param exit: Exit
    :type exit: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def group_insert(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Insert selected nodes into a node group

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def group_make(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Make group from selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def group_separate(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    type: typing.Optional[typing.Any] = "COPY",
):
    """Separate selected nodes from the node group

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param type: Type

    COPY
    Copy -- Copy to parent node tree, keep group intact.

    MOVE
    Move -- Move to parent node tree, remove from group.
        :type type: typing.Optional[typing.Any]
    """

    ...

def group_ungroup(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Ungroup selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def hide_socket_toggle(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Toggle unused node socket display

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def hide_toggle(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Toggle hiding of selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def index_switch_item_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add bake item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def index_switch_item_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    index: typing.Optional[typing.Any] = 0,
):
    """Remove an item from the index switch

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param index: Index, Index to remove
    :type index: typing.Optional[typing.Any]
    """

    ...

def insert_offset(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Automatically offset nodes on insertion

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def interface_item_duplicate(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add a copy of the active item to the interface

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def interface_item_new(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    item_type: typing.Optional[typing.Any] = "INPUT",
):
    """Add a new item to the interface

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param item_type: Item Type, Type of the item to create
    :type item_type: typing.Optional[typing.Any]
    """

    ...

def interface_item_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove active item from the interface

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def join(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Attach selected nodes to a new common frame

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def link(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    detach: typing.Optional[typing.Union[bool, typing.Any]] = False,
    drag_start: typing.Optional[typing.Any] = (0.0, 0.0),
    inside_padding: typing.Optional[typing.Any] = 2.0,
    outside_padding: typing.Optional[typing.Any] = 0.0,
    speed_ramp: typing.Optional[typing.Any] = 1.0,
    max_speed: typing.Optional[typing.Any] = 26.0,
    delay: typing.Optional[typing.Any] = 0.5,
    zoom_influence: typing.Optional[typing.Any] = 0.5,
):
    """Use the mouse to create a link between two nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param detach: Detach, Detach and redirect existing links
    :type detach: typing.Optional[typing.Union[bool, typing.Any]]
    :param drag_start: Drag Start, The position of the mouse cursor at the start of the operation
    :type drag_start: typing.Optional[typing.Any]
    :param inside_padding: Inside Padding, Inside distance in UI units from the edge of the region within which to start panning
    :type inside_padding: typing.Optional[typing.Any]
    :param outside_padding: Outside Padding, Outside distance in UI units from the edge of the region at which to stop panning
    :type outside_padding: typing.Optional[typing.Any]
    :param speed_ramp: Speed Ramp, Width of the zone in UI units where speed increases with distance from the edge
    :type speed_ramp: typing.Optional[typing.Any]
    :param max_speed: Max Speed, Maximum speed in UI units per second
    :type max_speed: typing.Optional[typing.Any]
    :param delay: Delay, Delay in seconds before maximum speed is reached
    :type delay: typing.Optional[typing.Any]
    :param zoom_influence: Zoom Influence, Influence of the zoom factor on scroll speed
    :type zoom_influence: typing.Optional[typing.Any]
    """

    ...

def link_make(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    replace: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Make a link between selected output and input sockets

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param replace: Replace, Replace socket connections with the new links
    :type replace: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def link_viewer(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Link to viewer node

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def links_cut(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    path: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]
    ] = None,
    cursor: typing.Optional[typing.Any] = 12,
):
    """Use the mouse to cut (remove) some links

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param path: Path
    :type path: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]]
    :param cursor: Cursor
    :type cursor: typing.Optional[typing.Any]
    """

    ...

def links_detach(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove all links to selected nodes, and try to connect neighbor nodes together

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def links_mute(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    path: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]
    ] = None,
    cursor: typing.Optional[typing.Any] = 35,
):
    """Use the mouse to mute links

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param path: Path
    :type path: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]]
    :param cursor: Cursor
    :type cursor: typing.Optional[typing.Any]
    """

    ...

def move_detach_links(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    NODE_OT_links_detach: typing.Optional[links_detach] = None,
    TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate] = None,
):
    """Move a node to detach links

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param NODE_OT_links_detach: Detach Links, Remove all links to selected nodes, and try to connect neighbor nodes together
    :type NODE_OT_links_detach: typing.Optional[links_detach]
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate]
    """

    ...

def move_detach_links_release(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    NODE_OT_links_detach: typing.Optional[links_detach] = None,
    NODE_OT_translate_attach: typing.Optional[translate_attach] = None,
):
    """Move a node to detach links

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param NODE_OT_links_detach: Detach Links, Remove all links to selected nodes, and try to connect neighbor nodes together
    :type NODE_OT_links_detach: typing.Optional[links_detach]
    :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame
    :type NODE_OT_translate_attach: typing.Optional[translate_attach]
    """

    ...

def mute_toggle(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Toggle muting of selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def new_geometry_node_group_assign(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Create a new geometry node group and assign it to the active modifier

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def new_geometry_node_group_tool(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Create a new geometry node group for a tool

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def new_geometry_nodes_modifier(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Create a new modifier with a new geometry node group

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def new_node_tree(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    type: typing.Optional[typing.Union[str, int, typing.Any]] = "",
    name: typing.Union[str, typing.Any] = "NodeTree",
):
    """Create a new node tree

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param type: Tree Type
    :type type: typing.Optional[typing.Union[str, int, typing.Any]]
    :param name: Name
    :type name: typing.Union[str, typing.Any]
    """

    ...

def node_color_preset_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Optional[typing.Union[bool, typing.Any]] = False,
    remove_active: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Add or remove a Node Color Preset

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of the preset, used to make the path name
    :type name: typing.Union[str, typing.Any]
    :param remove_name: remove_name
    :type remove_name: typing.Optional[typing.Union[bool, typing.Any]]
    :param remove_active: remove_active
    :type remove_active: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def node_copy_color(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Copy color to all selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def options_toggle(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Toggle option buttons display for selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def output_file_add_socket(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    file_path: typing.Union[str, typing.Any] = "Image",
):
    """Add a new input to a file output node

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param file_path: File Path, Subpath of the output file
    :type file_path: typing.Union[str, typing.Any]
    """

    ...

def output_file_move_active_socket(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    direction: typing.Optional[typing.Any] = "DOWN",
):
    """Move the active input of a file output node up or down the list

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param direction: Direction
    :type direction: typing.Optional[typing.Any]
    """

    ...

def output_file_remove_active_socket(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove the active input from a file output node

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def parent_set(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Attach selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def preview_toggle(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Toggle preview display for selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def read_viewlayers(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Read all render layers of all used scenes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def render_changed(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Render current scene, when input node's layer has been changed

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def repeat_zone_item_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add repeat zone item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def repeat_zone_item_move(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    direction: typing.Optional[typing.Any] = "UP",
):
    """Move active repeat zone item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param direction: Direction, Move direction
    :type direction: typing.Optional[typing.Any]
    """

    ...

def repeat_zone_item_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove active repeat zone item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def resize(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Resize a node

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    extend: typing.Optional[typing.Union[bool, typing.Any]] = False,
    deselect: typing.Optional[typing.Union[bool, typing.Any]] = False,
    toggle: typing.Optional[typing.Union[bool, typing.Any]] = False,
    deselect_all: typing.Optional[typing.Union[bool, typing.Any]] = False,
    select_passthrough: typing.Optional[typing.Union[bool, typing.Any]] = False,
    location: typing.Optional[typing.Any] = (0, 0),
    socket_select: typing.Optional[typing.Union[bool, typing.Any]] = False,
    clear_viewer: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Select the node under the cursor

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param extend: Extend, Extend selection instead of deselecting everything first
    :type extend: typing.Optional[typing.Union[bool, typing.Any]]
    :param deselect: Deselect, Remove from selection
    :type deselect: typing.Optional[typing.Union[bool, typing.Any]]
    :param toggle: Toggle Selection, Toggle the selection
    :type toggle: typing.Optional[typing.Union[bool, typing.Any]]
    :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor
    :type deselect_all: typing.Optional[typing.Union[bool, typing.Any]]
    :param select_passthrough: Only Select Unselected, Ignore the select action when the element is already selected
    :type select_passthrough: typing.Optional[typing.Union[bool, typing.Any]]
    :param location: Location, Mouse location
    :type location: typing.Optional[typing.Any]
    :param socket_select: Socket Select
    :type socket_select: typing.Optional[typing.Union[bool, typing.Any]]
    :param clear_viewer: Clear Viewer, Deactivate geometry nodes viewer when clicking in empty space
    :type clear_viewer: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def select_all(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    action: typing.Optional[typing.Any] = "TOGGLE",
):
    """(De)select all nodes

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :type action: typing.Optional[typing.Any]
    """

    ...

def select_box(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    tweak: typing.Optional[typing.Union[bool, typing.Any]] = False,
    xmin: typing.Optional[typing.Any] = 0,
    xmax: typing.Optional[typing.Any] = 0,
    ymin: typing.Optional[typing.Any] = 0,
    ymax: typing.Optional[typing.Any] = 0,
    wait_for_input: typing.Optional[typing.Union[bool, typing.Any]] = True,
    mode: typing.Optional[typing.Any] = "SET",
):
    """Use box selection to select nodes

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param tweak: Tweak, Only activate when mouse is not over a node (useful for tweak gesture)
        :type tweak: typing.Optional[typing.Union[bool, typing.Any]]
        :param xmin: X Min
        :type xmin: typing.Optional[typing.Any]
        :param xmax: X Max
        :type xmax: typing.Optional[typing.Any]
        :param ymin: Y Min
        :type ymin: typing.Optional[typing.Any]
        :param ymax: Y Max
        :type ymax: typing.Optional[typing.Any]
        :param wait_for_input: Wait for Input
        :type wait_for_input: typing.Optional[typing.Union[bool, typing.Any]]
        :param mode: Mode

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :type mode: typing.Optional[typing.Any]
    """

    ...

def select_circle(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    x: typing.Optional[typing.Any] = 0,
    y: typing.Optional[typing.Any] = 0,
    radius: typing.Optional[typing.Any] = 25,
    wait_for_input: typing.Optional[typing.Union[bool, typing.Any]] = True,
    mode: typing.Optional[typing.Any] = "SET",
):
    """Use circle selection to select nodes

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param x: X
        :type x: typing.Optional[typing.Any]
        :param y: Y
        :type y: typing.Optional[typing.Any]
        :param radius: Radius
        :type radius: typing.Optional[typing.Any]
        :param wait_for_input: Wait for Input
        :type wait_for_input: typing.Optional[typing.Union[bool, typing.Any]]
        :param mode: Mode

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :type mode: typing.Optional[typing.Any]
    """

    ...

def select_grouped(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    extend: typing.Optional[typing.Union[bool, typing.Any]] = False,
    type: typing.Optional[typing.Any] = "TYPE",
):
    """Select nodes with similar properties

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param extend: Extend, Extend selection instead of deselecting everything first
    :type extend: typing.Optional[typing.Union[bool, typing.Any]]
    :param type: Type
    :type type: typing.Optional[typing.Any]
    """

    ...

def select_lasso(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    tweak: typing.Optional[typing.Union[bool, typing.Any]] = False,
    path: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]
    ] = None,
    mode: typing.Optional[typing.Any] = "SET",
):
    """Select nodes using lasso selection

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param tweak: Tweak, Only activate when mouse is not over a node (useful for tweak gesture)
        :type tweak: typing.Optional[typing.Union[bool, typing.Any]]
        :param path: Path
        :type path: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]]
        :param mode: Mode

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :type mode: typing.Optional[typing.Any]
    """

    ...

def select_link_viewer(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    NODE_OT_select: typing.Optional[select] = None,
    NODE_OT_link_viewer: typing.Optional[link_viewer] = None,
):
    """Select node and link it to a viewer node

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param NODE_OT_select: Select, Select the node under the cursor
    :type NODE_OT_select: typing.Optional[select]
    :param NODE_OT_link_viewer: Link to Viewer Node, Link to viewer node
    :type NODE_OT_link_viewer: typing.Optional[link_viewer]
    """

    ...

def select_linked_from(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Select nodes linked from the selected ones

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_linked_to(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Select nodes linked to the selected ones

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_same_type_step(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    prev: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Activate and view same node type, step by step

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param prev: Previous
    :type prev: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def shader_script_update(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Update shader script node with new sockets and options from the script

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def simulation_zone_item_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add simulation zone item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def simulation_zone_item_move(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    direction: typing.Optional[typing.Any] = "UP",
):
    """Move active simulation zone item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param direction: Direction, Move direction
    :type direction: typing.Optional[typing.Any]
    """

    ...

def simulation_zone_item_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove active simulation zone item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def switch_view_update(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Update views of selected node

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def translate_attach(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate] = None,
    NODE_OT_attach: typing.Optional[attach] = None,
):
    """Move nodes and attach to frame

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate]
    :param NODE_OT_attach: Attach Nodes, Attach active node to a frame
    :type NODE_OT_attach: typing.Optional[attach]
    """

    ...

def translate_attach_remove_on_cancel(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate] = None,
    NODE_OT_attach: typing.Optional[attach] = None,
):
    """Move nodes and attach to frame

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate]
    :param NODE_OT_attach: Attach Nodes, Attach active node to a frame
    :type NODE_OT_attach: typing.Optional[attach]
    """

    ...

def tree_path_parent(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Go to parent node tree

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def view_all(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Resize view so you can see all nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def view_selected(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Resize view so you can see selected nodes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def viewer_border(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    xmin: typing.Optional[typing.Any] = 0,
    xmax: typing.Optional[typing.Any] = 0,
    ymin: typing.Optional[typing.Any] = 0,
    ymax: typing.Optional[typing.Any] = 0,
    wait_for_input: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Set the boundaries for viewer operations

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param xmin: X Min
    :type xmin: typing.Optional[typing.Any]
    :param xmax: X Max
    :type xmax: typing.Optional[typing.Any]
    :param ymin: Y Min
    :type ymin: typing.Optional[typing.Any]
    :param ymax: Y Max
    :type ymax: typing.Optional[typing.Any]
    :param wait_for_input: Wait for Input
    :type wait_for_input: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...
