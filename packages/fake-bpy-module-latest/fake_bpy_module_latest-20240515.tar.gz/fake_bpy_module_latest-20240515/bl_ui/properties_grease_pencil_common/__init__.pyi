import typing
import bpy_types

GenericType = typing.TypeVar("GenericType")

class AnnotationDataPanel:
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_region_type: typing.Any
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_header(self, context):
        """

        :param context:
        """
        ...

    def draw_layers(self, context, layout, gpd):
        """

        :param context:
        :param layout:
        :param gpd:
        """
        ...

class AnnotationDrawingToolsPanel:
    """ """

    bl_category: typing.Any
    """ """

    bl_label: typing.Any
    """ """

    bl_region_type: typing.Any
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

class AnnotationOnionSkin:
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_region_type: typing.Any
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_header(self, context):
        """

        :param context:
        """
        ...

    def poll(self, context):
        """

        :param context:
        """
        ...

class GPENCIL_MT_cleanup(bpy_types.Menu, bpy_types._GenericUI):
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

class GPENCIL_MT_gpencil_draw_delete(bpy_types.Menu, bpy_types._GenericUI):
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

class GPENCIL_MT_layer_active(bpy_types.Menu, bpy_types._GenericUI):
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

class GPENCIL_MT_layer_mask_menu(bpy_types.Menu, bpy_types._GenericUI):
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

class GPENCIL_MT_material_active(bpy_types.Menu, bpy_types._GenericUI):
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

class GPENCIL_MT_move_to_layer(bpy_types.Menu, bpy_types._GenericUI):
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

class GPENCIL_MT_snap(bpy_types.Menu, bpy_types._GenericUI):
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

class GPENCIL_MT_snap_pie(bpy_types.Menu, bpy_types._GenericUI):
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

class GPENCIL_UL_annotation_layer(bpy_types.UIList, bpy_types._GenericUI):
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

    def draw_item(
        self,
        _context,
        layout,
        _data,
        item,
        icon,
        _active_data,
        _active_propname,
        _index,
    ):
        """

        :param _context:
        :param layout:
        :param _data:
        :param item:
        :param icon:
        :param _active_data:
        :param _active_propname:
        :param _index:
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

class GPENCIL_UL_layer(bpy_types.UIList, bpy_types._GenericUI):
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

    def draw_item(
        self,
        _context,
        layout,
        _data,
        item,
        icon,
        _active_data,
        _active_propname,
        _index,
    ):
        """

        :param _context:
        :param layout:
        :param _data:
        :param item:
        :param icon:
        :param _active_data:
        :param _active_propname:
        :param _index:
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

class GPENCIL_UL_masks(bpy_types.UIList, bpy_types._GenericUI):
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

    def draw_item(
        self,
        _context,
        layout,
        _data,
        item,
        icon,
        _active_data,
        _active_propname,
        _index,
    ):
        """

        :param _context:
        :param layout:
        :param _data:
        :param item:
        :param icon:
        :param _active_data:
        :param _active_propname:
        :param _index:
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

class GREASE_PENCIL_MT_layer_active(bpy_types.Menu, bpy_types._GenericUI):
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

class GREASE_PENCIL_MT_move_to_layer(bpy_types.Menu, bpy_types._GenericUI):
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

class GREASE_PENCIL_MT_snap(bpy_types.Menu, bpy_types._GenericUI):
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

class GREASE_PENCIL_MT_snap_pie(bpy_types.Menu, bpy_types._GenericUI):
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

class GreasePencilBrushFalloff:
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

class GreasePencilDisplayPanel:
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_header(self, context):
        """

        :param context:
        """
        ...

    def poll(self, context):
        """

        :param context:
        """
        ...

class GreasePencilFlipTintColors(bpy_types.Operator):
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

class GreasePencilLayerAdjustmentsPanel:
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

class GreasePencilLayerDisplayPanel:
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

class GreasePencilLayerMasksPanel:
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_header(self, context):
        """

        :param context:
        """
        ...

class GreasePencilLayerRelationsPanel:
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

class GreasePencilLayerTransformPanel:
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

class GreasePencilMaterialsPanel:
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

class GreasePencilSculptAdvancedPanel:
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

class GreasePencilSimplifyPanel:
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_header(self, context):
        """

        :param context:
        """
        ...

class GreasePencilVertexcolorPanel:
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...
