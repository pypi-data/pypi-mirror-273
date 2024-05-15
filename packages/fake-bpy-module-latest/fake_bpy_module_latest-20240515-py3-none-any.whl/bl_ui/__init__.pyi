import typing
import bpy_types

from . import anim
from . import asset_shelf
from . import generic_ui_list
from . import node_add_menu
from . import node_add_menu_compositor
from . import node_add_menu_geometry
from . import node_add_menu_shader
from . import node_add_menu_texture
from . import properties_animviz
from . import properties_collection
from . import properties_constraint
from . import properties_data_armature
from . import properties_data_bone
from . import properties_data_camera
from . import properties_data_curve
from . import properties_data_curves
from . import properties_data_empty
from . import properties_data_gpencil
from . import properties_data_grease_pencil
from . import properties_data_lattice
from . import properties_data_light
from . import properties_data_lightprobe
from . import properties_data_mesh
from . import properties_data_metaball
from . import properties_data_modifier
from . import properties_data_pointcloud
from . import properties_data_shaderfx
from . import properties_data_speaker
from . import properties_data_volume
from . import properties_freestyle
from . import properties_grease_pencil_common
from . import properties_mask_common
from . import properties_material
from . import properties_material_gpencil
from . import properties_object
from . import properties_output
from . import properties_paint_common
from . import properties_particle
from . import properties_physics_cloth
from . import properties_physics_common
from . import properties_physics_dynamicpaint
from . import properties_physics_field
from . import properties_physics_fluid
from . import properties_physics_geometry_nodes
from . import properties_physics_rigidbody
from . import properties_physics_rigidbody_constraint
from . import properties_physics_softbody
from . import properties_render
from . import properties_scene
from . import properties_texture
from . import properties_view_layer
from . import properties_workspace
from . import properties_world
from . import space_clip
from . import space_console
from . import space_dopesheet
from . import space_filebrowser
from . import space_graph
from . import space_image
from . import space_info
from . import space_nla
from . import space_node
from . import space_outliner
from . import space_properties
from . import space_sequencer
from . import space_spreadsheet
from . import space_statusbar
from . import space_text
from . import space_time
from . import space_toolsystem_common
from . import space_toolsystem_toolbar
from . import space_topbar
from . import space_userpref
from . import space_view3d
from . import space_view3d_toolbar
from . import temp_anim_layers
from . import utils

GenericType = typing.TypeVar("GenericType")

class UI_MT_button_context_menu(bpy_types.Menu, bpy_types._GenericUI):
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

class UI_MT_list_item_context_menu(bpy_types.Menu, bpy_types._GenericUI):
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

class UI_UL_list(bpy_types.UIList, bpy_types._GenericUI):
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

    def driver_add(self):
        """ """
        ...

    def driver_remove(self):
        """ """
        ...

    def filter_items_by_name(self, pattern, bitflag, items, propname, flags, reverse):
        """

        :param pattern:
        :param bitflag:
        :param items:
        :param propname:
        :param flags:
        :param reverse:
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

    def sort_items_by_name(self, items, propname):
        """

        :param items:
        :param propname:
        """
        ...

    def sort_items_helper(self, sort_data, key, reverse):
        """

        :param sort_data:
        :param key:
        :param reverse:
        """
        ...

    def type_recast(self):
        """ """
        ...

    def values(self):
        """ """
        ...

def register():
    """ """

    ...

def translation_update(_):
    """ """

    ...

def unregister():
    """ """

    ...
