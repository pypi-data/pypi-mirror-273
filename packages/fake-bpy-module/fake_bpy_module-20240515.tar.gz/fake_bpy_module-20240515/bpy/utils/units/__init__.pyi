"""
This module contains some data/methods regarding units handling.

"""

import typing

GenericType = typing.TypeVar("GenericType")

def to_string(
    unit_system: typing.Optional[str],
    unit_category: typing.Optional[str],
    value: typing.Optional[float],
    precision: typing.Optional[int] = 3,
    split_unit: typing.Optional[bool] = False,
    compatible_unit: typing.Optional[bool] = False,
) -> str:
    """Convert a given input float value into a string with units.

        :param unit_system: The unit system, from `bpy.utils.units.systems`.
        :type unit_system: typing.Optional[str]
        :param unit_category: The category of data we are converting (length, area, rotation, etc.),
    from `bpy.utils.units.categories`.
        :type unit_category: typing.Optional[str]
        :param value: The value to convert to a string.
        :type value: typing.Optional[float]
        :param precision: Number of digits after the comma.
        :type precision: typing.Optional[int]
        :param split_unit: Whether to use several units if needed (1m1cm), or always only one (1.01m).
        :type split_unit: typing.Optional[bool]
        :param compatible_unit: Whether to use keyboard-friendly units (1m2) or nicer utf-8 ones (1m²).
        :type compatible_unit: typing.Optional[bool]
        :return: The converted string.
        :rtype: str
    """

    ...

def to_value(
    unit_system: typing.Optional[str],
    unit_category: typing.Optional[str],
    str_input: typing.Optional[str],
    str_ref_unit: typing.Optional[str] = None,
) -> float:
    """Convert a given input string into a float value.

        :param unit_system: The unit system, from `bpy.utils.units.systems`.
        :type unit_system: typing.Optional[str]
        :param unit_category: The category of data we are converting (length, area, rotation, etc.),
    from `bpy.utils.units.categories`.
        :type unit_category: typing.Optional[str]
        :param str_input: The string to convert to a float value.
        :type str_input: typing.Optional[str]
        :param str_ref_unit: A reference string from which to extract a default unit, if none is found in str_input.
        :type str_ref_unit: typing.Optional[str]
        :return: The converted/interpreted value.
        :rtype: float
    """

    ...

categories: typing.Any
""" Constant value bpy.utils.units.categories(NONE='NONE', LENGTH='LENGTH', AREA='AREA', VOLUME='VOLUME', MASS='MASS', ROTATION='ROTATION', TIME='TIME', TIME_ABSOLUTE='TIME_ABSOLUTE', VELOCITY='VELOCITY', ACCELERATION='ACCELERATION', CAMERA='CAMERA', POWER='POWER', TEMPERATURE='TEMPERATURE', WAVELENGTH='WAVELENGTH')
"""

systems: typing.Any
""" Constant value bpy.utils.units.systems(NONE='NONE', METRIC='METRIC', IMPERIAL='IMPERIAL')
"""
