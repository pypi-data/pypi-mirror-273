import typing
import bpy_types

GenericType = typing.TypeVar("GenericType")

class LightMapPack(bpy_types.Operator):
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

class prettyface:
    """ """

    children: typing.Any
    """ """

    has_parent: typing.Any
    """ """

    height: typing.Any
    """ """

    rot: typing.Any
    """ """

    uv: typing.Any
    """ """

    width: typing.Any
    """ """

    xoff: typing.Any
    """ """

    yoff: typing.Any
    """ """

    def place(self, xoff, yoff, xfac, yfac, margin_w, margin_h):
        """

        :param xoff:
        :param yoff:
        :param xfac:
        :param yfac:
        :param margin_w:
        :param margin_h:
        """
        ...

    def spin(self):
        """ """
        ...

def lightmap_uvpack(
    meshes,
    PREF_SEL_ONLY,
    PREF_NEW_UVLAYER,
    PREF_PACK_IN_ONE,
    PREF_BOX_DIV,
    PREF_MARGIN_DIV,
):
    """ """

    ...

def unwrap(operator, context, kwargs):
    """ """

    ...
