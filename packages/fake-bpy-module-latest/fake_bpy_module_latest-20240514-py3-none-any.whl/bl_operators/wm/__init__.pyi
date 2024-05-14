import typing
import bpy_types

GenericType = typing.TypeVar("GenericType")

class BatchRenameAction(bpy_types.PropertyGroup):
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_pointer(self):
        """ """
        ...

    def bl_rna_get_subclass(self):
        """ """
        ...

    def bl_rna_get_subclass_py(self):
        """ """
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

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_MT_region_toggle_pie(bpy_types.Menu, bpy_types._GenericUI):
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

class WM_MT_splash(bpy_types.Menu, bpy_types._GenericUI):
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

class WM_MT_splash_about(bpy_types.Menu, bpy_types._GenericUI):
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

class WM_MT_splash_quick_setup(bpy_types.Menu, bpy_types._GenericUI):
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

class WM_OT_batch_rename(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def check(self, context):
        """

        :param context:
        """
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

    def execute(self, context):
        """

        :param context:
        """
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

    def invoke(self, context, event):
        """

        :param context:
        :param event:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_collection_boolean_set(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_cycle_array(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_cycle_enum(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_cycle_int(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_menu_enum(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_modal_mouse(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def invoke(self, context, event):
        """

        :param context:
        :param event:
        """
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

    def modal(self, context, event):
        """

        :param context:
        :param event:
        """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_resolve(self):
        """ """
        ...

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_pie_enum(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
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

    def invoke(self, context, event):
        """

        :param context:
        :param event:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_scale_float(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_scale_int(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_set_boolean(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_set_enum(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_set_float(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_set_id(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_set_int(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_set_string(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_set_value(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_toggle(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_context_toggle_enum(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
        """
        ...

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_doc_view(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, _context):
        """

        :param _context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_doc_view_manual(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, _context):
        """

        :param _context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_drop_blend_file(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def draw_menu(self, menu, _context):
        """

        :param menu:
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

    def invoke(self, context, _event):
        """

        :param context:
        :param _event:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_operator_cheat_sheet(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, _context):
        """

        :param _context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_operator_pie_enum(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def description(self, context, props):
        """

        :param context:
        :param props:
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

    def invoke(self, context, event):
        """

        :param context:
        :param event:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_owner_disable(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_owner_enable(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_path_open(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, _context):
        """

        :param _context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_properties_add(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_properties_context_change(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_properties_edit(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def check(self, context):
        """

        :param context:
        """
        ...

    def convert_custom_property_to_string(self, item, name):
        """

        :param item:
        :param name:
        """
        ...

    def draw(self, _context):
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

    def execute(self, context):
        """

        :param context:
        """
        ...

    def get(self):
        """ """
        ...

    def get_property_id_type(self, item, property_name):
        """

        :param item:
        :param property_name:
        """
        ...

    def get_property_type(self, item, property_name):
        """

        :param item:
        :param property_name:
        """
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

    def invoke(self, context, _event):
        """

        :param context:
        :param _event:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_type_update_cb(self, context):
        """

        :param context:
        """
        ...

    def property_unset(self):
        """ """
        ...

    def subtype_items_cb(self, context):
        """

        :param context:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_properties_edit_value(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def execute(self, context):
        """

        :param context:
        """
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

    def invoke(self, context, _event):
        """

        :param context:
        :param _event:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_properties_remove(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_sysinfo(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, _context):
        """

        :param _context:
        """
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

    def invoke(self, context, _event):
        """

        :param context:
        :param _event:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_tool_set_by_id(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_tool_set_by_index(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_toolbar(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def keymap_from_toolbar(self, context, space_type, use_fallback_keys, use_reset):
        """

        :param context:
        :param space_type:
        :param use_fallback_keys:
        :param use_reset:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_toolbar_fallback_pie(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def invoke(self, context, event):
        """

        :param context:
        :param event:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_toolbar_prompt(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def invoke(self, context, event):
        """

        :param context:
        :param event:
        """
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

    def modal(self, context, event):
        """

        :param context:
        :param event:
        """
        ...

    def path_from_id(self):
        """ """
        ...

    def path_resolve(self):
        """ """
        ...

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_url_open(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, _context):
        """

        :param _context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

class WM_OT_url_open_preset(bpy_types.Operator):
    """ """

    bl_idname: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_rna: typing.Any
    """ """

    id_data: typing.Any
    """ """

    preset_items: typing.Any
    """ """

    def as_keywords(self, ignore):
        """

        :param ignore:
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def execute(self, context):
        """

        :param context:
        """
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

    def poll_message_set(self):
        """ """
        ...

    def pop(self):
        """ """
        ...

    def property_overridable_library_set(self):
        """ """
        ...

    def property_unset(self):
        """ """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

def context_path_decompose(data_path):
    """ """

    ...

def context_path_to_rna_property(context, data_path):
    """ """

    ...

def context_path_validate(context, data_path):
    """ """

    ...

def description_from_data_path(base, data_path, prefix, value):
    """ """

    ...

def execute_context_assign(context):
    """ """

    ...

def operator_path_is_undo(context, data_path):
    """ """

    ...

def operator_path_undo_return(context, data_path):
    """ """

    ...

def operator_value_is_undo(value):
    """ """

    ...

def operator_value_undo_return(value):
    """ """

    ...

def rna_path_prop_search_for_context(context, edit_text):
    """ """

    ...
