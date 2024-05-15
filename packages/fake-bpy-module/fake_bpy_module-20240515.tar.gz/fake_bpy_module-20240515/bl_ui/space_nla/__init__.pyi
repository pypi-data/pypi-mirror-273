import typing
import bl_ui.space_dopesheet
import bpy_types

GenericType = typing.TypeVar("GenericType")

class NLA_HT_header(bpy_types.Header, bpy_types._GenericUI):
    """ """

    bl_rna: typing.Any
    """ """

    bl_space_type: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, context):
        """

        :param context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_add(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    bl_translation_context: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, _context):
        """

        :param _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_channel_context_menu(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, _context):
        """

        :param _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_context_menu(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_editor_menus(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_marker(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_marker_select(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, _context):
        """

        :param _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_select(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, _context):
        """

        :param _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_snap_pie(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, _context):
        """

        :param _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_strips(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_strips_transform(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, _context):
        """

        :param _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_tracks(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    bl_translation_context: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, _context):
        """

        :param _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_view(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_MT_view_pie(bpy_types.Menu, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, _context):
        """

        :param _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param _context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
        add_operator_props,
    ):
        """

        :param searchpaths:
        :param operator:
        :param props_default:
        :param prop_filepath:
        :param filter_ext:
        :param filter_path:
        :param display_name:
        :param add_operator:
        :param add_operator_props:
        """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_PT_action(
    bpy_types.Panel,
    bl_ui.space_dopesheet.DopesheetActionPanelBase,
    bpy_types._GenericUI,
):
    """ """

    bl_category: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_region_type: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    bl_space_type: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_generic_panel(self, _context, layout, action):
        """

        :param _context:
        :param layout:
        :param action:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_resolve(self):
        """ """
        ...

    def poll(self, context):
        """

        :param context:
        """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_PT_filters(
    bpy_types.Panel,
    bl_ui.space_dopesheet.DopesheetFilterPopoverBase,
    bpy_types._GenericUI,
):
    """ """

    bl_label: typing.Any
    """ """

    bl_region_type: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    bl_space_type: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_generic_filters(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def draw_search_filters(self, context, layout, generic_filters_only):
        """

        :param context:
        :param layout:
        :param generic_filters_only:
        """
        ...

    def draw_standard_filters(self, context, layout):
        """

        :param context:
        :param layout:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class NLA_PT_snapping(bpy_types.Panel, bpy_types._GenericUI):
    """ """

    bl_label: typing.Any
    """ """

    bl_region_type: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    bl_space_type: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def append(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
        ...

    def draw(self, context):
        """

        :param context:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def get(self):
        """ """
        ...

    def id_properties_clear(self):
        """ """
        ...

    def id_properties_ensure(self):
        """ """
        ...

    def id_properties_ui(self):
        """ """
        ...

    def is_extended(self):
        """ """
        ...

    def is_property_hidden(self):
        """ """
        ...

    def is_property_overridable_library(self):
        """ """
        ...

    def is_property_readonly(self):
        """ """
        ...

    def is_property_set(self):
        """ """
        ...

    def items(self):
        """ """
        ...

    def keyframe_delete(self):
        """ """
        ...

    def keyframe_insert(self):
        """ """
        ...

    def keys(self):
        """ """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_resolve(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def prepend(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def remove(self, draw_func):
        """

        :param draw_func:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...
