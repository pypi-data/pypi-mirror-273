import typing
import bpy.ops.transform
import bpy.types

GenericType = typing.TypeVar("GenericType")

def brush_stroke(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    stroke: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    ] = None,
    mode: typing.Optional[typing.Any] = "NORMAL",
):
    """Draw a new stroke in the active Grease Pencil object

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param stroke: Stroke
        :type stroke: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]]
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.

    SMOOTH
    Smooth -- Switch brush to smooth mode for duration of stroke.
        :type mode: typing.Optional[typing.Any]
    """

    ...

def caps_set(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    type: typing.Optional[typing.Any] = "ROUND",
):
    """Change curve caps mode (rounded or flat)

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param type: Type

    ROUND
    Rounded -- Set as default rounded.

    FLAT
    Flat.

    START
    Toggle Start.

    END
    Toggle End.
        :type type: typing.Optional[typing.Any]
    """

    ...

def clean_loose(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    limit: typing.Optional[typing.Any] = 1,
):
    """Remove loose points

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param limit: Limit, Number of points to consider stroke as loose
    :type limit: typing.Optional[typing.Any]
    """

    ...

def copy(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Copy the selected Grease Pencil points or strokes to the internal clipboard

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def cyclical_set(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    type: typing.Optional[typing.Any] = "TOGGLE",
):
    """Close or open the selected stroke adding a segment from last to first point

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param type: Type
    :type type: typing.Optional[typing.Any]
    """

    ...

def delete(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Delete selected strokes or points

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def delete_frame(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    type: typing.Optional[typing.Any] = "ACTIVE_FRAME",
):
    """Delete Grease Pencil Frame(s)

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param type: Type, Method used for deleting Grease Pencil frames

    ACTIVE_FRAME
    Active Frame -- Deletes current frame in the active layer.

    ALL_FRAMES
    All Active Frames -- Delete active frames for all layers.
        :type type: typing.Optional[typing.Any]
    """

    ...

def dissolve(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    type: typing.Optional[typing.Any] = "POINTS",
):
    """Delete selected points without splitting strokes

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param type: Type, Method used for dissolving stroke points

    POINTS
    Dissolve -- Dissolve selected points.

    BETWEEN
    Dissolve Between -- Dissolve points between selected points.

    UNSELECT
    Dissolve Unselect -- Dissolve all unselected points.
        :type type: typing.Optional[typing.Any]
    """

    ...

def duplicate(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Duplicate the selected points

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def duplicate_move(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    GREASE_PENCIL_OT_duplicate: typing.Optional[typing.Any] = None,
    TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate] = None,
):
    """Make copies of the selected Grease Pencil strokes and move them

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param GREASE_PENCIL_OT_duplicate: Duplicate, Duplicate the selected points
    :type GREASE_PENCIL_OT_duplicate: typing.Optional[typing.Any]
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate]
    """

    ...

def extrude(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Extrude the selected points

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def extrude_move(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    GREASE_PENCIL_OT_extrude: typing.Optional[typing.Any] = None,
    TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate] = None,
):
    """Extrude selected points and move them

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param GREASE_PENCIL_OT_extrude: Extrude Stroke Points, Extrude the selected points
    :type GREASE_PENCIL_OT_extrude: typing.Optional[typing.Any]
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate]
    """

    ...

def insert_blank_frame(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    all_layers: typing.Optional[typing.Union[bool, typing.Any]] = False,
    duration: typing.Optional[typing.Any] = 0,
):
    """Insert a blank frame on the current scene frame

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param all_layers: All Layers, Insert a blank frame in all editable layers
    :type all_layers: typing.Optional[typing.Union[bool, typing.Any]]
    :param duration: Duration
    :type duration: typing.Optional[typing.Any]
    """

    ...

def layer_active(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    layer: typing.Optional[typing.Any] = 0,
):
    """Set the active Grease Pencil layer

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param layer: Grease Pencil Layer
    :type layer: typing.Optional[typing.Any]
    """

    ...

def layer_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    new_layer_name: typing.Union[str, typing.Any] = "Layer",
):
    """Add a new Grease Pencil layer in the active object

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param new_layer_name: Name, Name of the new layer
    :type new_layer_name: typing.Union[str, typing.Any]
    """

    ...

def layer_duplicate(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    empty_keyframes: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Make a copy of the active Grease Pencil layer

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param empty_keyframes: Empty Keyframes, Add Empty Keyframes
    :type empty_keyframes: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def layer_group_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    new_layer_group_name: typing.Union[str, typing.Any] = "",
):
    """Add a new Grease Pencil layer group in the active object

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param new_layer_group_name: Name, Name of the new layer group
    :type new_layer_group_name: typing.Union[str, typing.Any]
    """

    ...

def layer_group_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    keep_children: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Remove Grease Pencil layer group in the active object

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param keep_children: Keep children nodes, Keep the children nodes of the group and only delete the group itself
    :type keep_children: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def layer_hide(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    unselected: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Hide selected/unselected Grease Pencil layers

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param unselected: Unselected, Hide unselected rather than selected layers
    :type unselected: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def layer_isolate(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    affect_visibility: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Make only active layer visible/editable

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param affect_visibility: Affect Visibility, Also affect the visibility
    :type affect_visibility: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def layer_lock_all(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    lock: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Lock all Grease Pencil layers to prevent them from being accidentally modified

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param lock: Lock Value, Lock/Unlock all layers
    :type lock: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def layer_mask_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    name: typing.Union[str, typing.Any] = "",
):
    """Add new layer as masking

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param name: Layer, Name of the layer
    :type name: typing.Union[str, typing.Any]
    """

    ...

def layer_mask_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove Layer Mask

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def layer_mask_reorder(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    direction: typing.Optional[typing.Any] = "UP",
):
    """Reorder the active Grease Pencil mask layer up/down in the list

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param direction: Direction
    :type direction: typing.Optional[typing.Any]
    """

    ...

def layer_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove the active Grease Pencil layer

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def layer_reorder(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    target_layer_name: typing.Union[str, typing.Any] = "Layer",
    location: typing.Optional[typing.Any] = "ABOVE",
):
    """Reorder the active Grease Pencil layer

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param target_layer_name: Target Name, Name of the target layer
    :type target_layer_name: typing.Union[str, typing.Any]
    :param location: Location
    :type location: typing.Optional[typing.Any]
    """

    ...

def layer_reveal(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Show all Grease Pencil layers

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def material_copy_to_object(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    only_active: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Append Materials of the active Grease Pencil to other object

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param only_active: Only Active, Append only active material, uncheck to append all materials
    :type only_active: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def material_hide(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    invert: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Hide active/inactive Grease Pencil material(s)

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param invert: Invert, Hide inactive materials instead of the active one
    :type invert: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def material_lock_all(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Lock all Grease Pencil materials to prevent them from being accidentally modified

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def material_lock_unselected(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Lock any material not used in any selected stroke

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def material_lock_unused(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Lock and hide any material not used

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def material_reveal(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Unhide all hidden Grease Pencil materials

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def material_select(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    deselect: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Select/Deselect all Grease Pencil strokes using current material

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param deselect: Deselect, Unselect strokes
    :type deselect: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def material_unlock_all(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Unlock all Grease Pencil materials so that they can be edited

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def move_to_layer(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    target_layer_name: typing.Union[str, typing.Any] = "Layer",
    add_new_layer: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Move selected strokes to another layer

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param target_layer_name: Name, Target Grease Pencil Layer
    :type target_layer_name: typing.Union[str, typing.Any]
    :param add_new_layer: New Layer, Move selection to a new layer
    :type add_new_layer: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def paste(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    paste_back: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Paste Grease Pencil points or strokes from the internal clipboard to the active layer

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param paste_back: Paste on Back, Add pasted strokes behind all strokes
    :type paste_back: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def primitive_arc(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    subdivision: typing.Optional[typing.Any] = 62,
    type: typing.Optional[typing.Any] = "ARC",
):
    """Create predefined grease pencil stroke arcs

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: typing.Optional[typing.Any]
    :param type: Type, Type of shape
    :type type: typing.Optional[typing.Any]
    """

    ...

def primitive_box(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    subdivision: typing.Optional[typing.Any] = 3,
    type: typing.Optional[typing.Any] = "BOX",
):
    """Create predefined grease pencil stroke boxes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: typing.Optional[typing.Any]
    :param type: Type, Type of shape
    :type type: typing.Optional[typing.Any]
    """

    ...

def primitive_circle(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    subdivision: typing.Optional[typing.Any] = 94,
    type: typing.Optional[typing.Any] = "CIRCLE",
):
    """Create predefined grease pencil stroke circles

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: typing.Optional[typing.Any]
    :param type: Type, Type of shape
    :type type: typing.Optional[typing.Any]
    """

    ...

def primitive_curve(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    subdivision: typing.Optional[typing.Any] = 62,
    type: typing.Optional[typing.Any] = "CURVE",
):
    """Create predefined grease pencil stroke curve shapes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: typing.Optional[typing.Any]
    :param type: Type, Type of shape
    :type type: typing.Optional[typing.Any]
    """

    ...

def primitive_line(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    subdivision: typing.Optional[typing.Any] = 6,
    type: typing.Optional[typing.Any] = "LINE",
):
    """Create predefined grease pencil stroke lines

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: typing.Optional[typing.Any]
    :param type: Type, Type of shape
    :type type: typing.Optional[typing.Any]
    """

    ...

def primitive_polyline(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    subdivision: typing.Optional[typing.Any] = 6,
    type: typing.Optional[typing.Any] = "POLYLINE",
):
    """Create predefined grease pencil stroke polylines

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: typing.Optional[typing.Any]
    :param type: Type, Type of shape
    :type type: typing.Optional[typing.Any]
    """

    ...

def reorder(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    direction: typing.Optional[typing.Any] = "TOP",
):
    """Change the display order of the selected strokes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param direction: Direction
    :type direction: typing.Optional[typing.Any]
    """

    ...

def sculpt_paint(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    stroke: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    ] = None,
    mode: typing.Optional[typing.Any] = "NORMAL",
):
    """Draw a new stroke in the active Grease Pencil object

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param stroke: Stroke
        :type stroke: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]]
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.

    SMOOTH
    Smooth -- Switch brush to smooth mode for duration of stroke.
        :type mode: typing.Optional[typing.Any]
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
    """(De)select all visible strokes

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

def select_alternate(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    deselect_ends: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Select alternated points in strokes with already selected points

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param deselect_ends: Deselect Ends, (De)select the first and last point of each stroke
    :type deselect_ends: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def select_ends(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    amount_start: typing.Optional[typing.Any] = 0,
    amount_end: typing.Optional[typing.Any] = 1,
):
    """Select end points of strokes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param amount_start: Amount Start, Number of points to select from the start
    :type amount_start: typing.Optional[typing.Any]
    :param amount_end: Amount End, Number of points to select from the end
    :type amount_end: typing.Optional[typing.Any]
    """

    ...

def select_less(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Shrink the selection by one point

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_linked(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Select all points in curves with any point selection

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_more(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Grow the selection by one point

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_random(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    ratio: typing.Optional[typing.Any] = 0.5,
    seed: typing.Optional[typing.Any] = 0,
    action: typing.Optional[typing.Any] = "SELECT",
):
    """Selects random points from the current strokes selection

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param ratio: Ratio, Portion of items to select randomly
        :type ratio: typing.Optional[typing.Any]
        :param seed: Random Seed, Seed for the random number generator
        :type seed: typing.Optional[typing.Any]
        :param action: Action, Selection action to execute

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :type action: typing.Optional[typing.Any]
    """

    ...

def separate(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    mode: typing.Optional[typing.Any] = "SELECTED",
):
    """Separate the selected geometry into a new grease pencil object

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param mode: Mode

    SELECTED
    Selection -- Separate selected geometry.

    MATERIAL
    By Material -- Separate by material.

    LAYER
    By Layer -- Separate by layer.
        :type mode: typing.Optional[typing.Any]
    """

    ...

def set_active_material(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Set the selected stroke material as the active material

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def set_material(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    slot: typing.Optional[typing.Union[str, int, typing.Any]] = "DEFAULT",
):
    """Set active material

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param slot: Material Slot
    :type slot: typing.Optional[typing.Union[str, int, typing.Any]]
    """

    ...

def set_selection_mode(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    mode: typing.Optional[typing.Union[str, int]] = "POINT",
):
    """Change the selection mode for Grease Pencil strokes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param mode: Mode
    :type mode: typing.Optional[typing.Union[str, int]]
    """

    ...

def set_uniform_opacity(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    opacity: typing.Optional[typing.Any] = 1.0,
):
    """Set all stroke points to same opacity

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param opacity: Opacity
    :type opacity: typing.Optional[typing.Any]
    """

    ...

def set_uniform_thickness(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    thickness: typing.Optional[typing.Any] = 0.1,
):
    """Set all stroke points to same thickness

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param thickness: Thickness, Thickness
    :type thickness: typing.Optional[typing.Any]
    """

    ...

def snap_cursor_to_selected(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Snap cursor to center of selected points

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def snap_to_cursor(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    use_offset: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Snap selected points/strokes to the cursor

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param use_offset: With Offset, Offset the entire stroke instead of selected points only
    :type use_offset: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def snap_to_grid(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Snap selected points to the nearest grid points

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def stroke_cutter(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    path: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]
    ] = None,
):
    """Delete stroke points in between intersecting strokes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param path: Path
    :type path: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath]]
    """

    ...

def stroke_material_set(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    material: typing.Union[str, typing.Any] = "",
):
    """Assign the active material slot to the selected strokes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param material: Material, Name of the material
    :type material: typing.Union[str, typing.Any]
    """

    ...

def stroke_simplify(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    factor: typing.Optional[typing.Any] = 0.01,
):
    """Simplify selected strokes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param factor: Factor
    :type factor: typing.Optional[typing.Any]
    """

    ...

def stroke_smooth(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    iterations: typing.Optional[typing.Any] = 10,
    factor: typing.Optional[typing.Any] = 1.0,
    smooth_ends: typing.Optional[typing.Union[bool, typing.Any]] = False,
    keep_shape: typing.Optional[typing.Union[bool, typing.Any]] = False,
    smooth_position: typing.Optional[typing.Union[bool, typing.Any]] = True,
    smooth_radius: typing.Optional[typing.Union[bool, typing.Any]] = True,
    smooth_opacity: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Smooth selected strokes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param iterations: Iterations
    :type iterations: typing.Optional[typing.Any]
    :param factor: Factor
    :type factor: typing.Optional[typing.Any]
    :param smooth_ends: Smooth Endpoints
    :type smooth_ends: typing.Optional[typing.Union[bool, typing.Any]]
    :param keep_shape: Keep Shape
    :type keep_shape: typing.Optional[typing.Union[bool, typing.Any]]
    :param smooth_position: Position
    :type smooth_position: typing.Optional[typing.Union[bool, typing.Any]]
    :param smooth_radius: Radius
    :type smooth_radius: typing.Optional[typing.Union[bool, typing.Any]]
    :param smooth_opacity: Opacity
    :type smooth_opacity: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def stroke_subdivide(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    number_cuts: typing.Optional[typing.Any] = 1,
    only_selected: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Subdivide between continuous selected points of the stroke adding a point half way between them

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param number_cuts: Number of Cuts
    :type number_cuts: typing.Optional[typing.Any]
    :param only_selected: Selected Points, Smooth only selected points in the stroke
    :type only_selected: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def stroke_subdivide_smooth(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    GREASE_PENCIL_OT_stroke_subdivide: typing.Optional[typing.Any] = None,
    GREASE_PENCIL_OT_stroke_smooth: typing.Optional[typing.Any] = None,
):
    """Subdivide strokes and smooth them

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param GREASE_PENCIL_OT_stroke_subdivide: Subdivide Stroke, Subdivide between continuous selected points of the stroke adding a point half way between them
    :type GREASE_PENCIL_OT_stroke_subdivide: typing.Optional[typing.Any]
    :param GREASE_PENCIL_OT_stroke_smooth: Smooth Stroke, Smooth selected strokes
    :type GREASE_PENCIL_OT_stroke_smooth: typing.Optional[typing.Any]
    """

    ...

def stroke_switch_direction(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Change direction of the points of the selected strokes

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def weight_brush_stroke(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    stroke: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    ] = None,
    mode: typing.Optional[typing.Any] = "NORMAL",
):
    """Draw weight on stroke points in the active Grease Pencil object

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param stroke: Stroke
        :type stroke: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]]
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.

    SMOOTH
    Smooth -- Switch brush to smooth mode for duration of stroke.
        :type mode: typing.Optional[typing.Any]
    """

    ...

def weight_sample(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Set the weight of the Draw tool to the weight of the vertex under the mouse cursor

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def weight_toggle_direction(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Toggle Add/Subtract for the weight paint draw tool

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...
