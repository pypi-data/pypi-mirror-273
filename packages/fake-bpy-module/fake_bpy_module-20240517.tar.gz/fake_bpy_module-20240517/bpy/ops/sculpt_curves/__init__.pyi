import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def brush_stroke(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    | None = None,
    mode: typing.Any | None = "NORMAL",
):
    """Sculpt curves using a brush

        :type override_context: dict[str, typing.Any] | bpy.types.Context | None
        :type execution_context: str | int | None
        :type undo: bool | None
        :param stroke: Stroke
        :type stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement] | None
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.

    SMOOTH
    Smooth -- Switch brush to smooth mode for duration of stroke.
        :type mode: typing.Any | None
    """

    ...

def min_distance_edit(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Change the minimum distance used by the density brush

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def select_grow(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    distance: typing.Any | None = 0.1,
):
    """Select curves which are close to curves that are selected already

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param distance: Distance, By how much to grow the selection
    :type distance: typing.Any | None
    """

    ...

def select_random(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    seed: typing.Any | None = 0,
    partial: bool | typing.Any | None = False,
    probability: typing.Any | None = 0.5,
    min: typing.Any | None = 0.0,
    constant_per_curve: bool | typing.Any | None = True,
):
    """Randomizes existing selection or create new random selection

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param seed: Seed, Source of randomness
    :type seed: typing.Any | None
    :param partial: Partial, Allow points or curves to be selected partially
    :type partial: bool | typing.Any | None
    :param probability: Probability, Chance of every point or curve being included in the selection
    :type probability: typing.Any | None
    :param min: Min, Minimum value for the random selection
    :type min: typing.Any | None
    :param constant_per_curve: Constant per Curve, The generated random number is the same for every control point of a curve
    :type constant_per_curve: bool | typing.Any | None
    """

    ...
