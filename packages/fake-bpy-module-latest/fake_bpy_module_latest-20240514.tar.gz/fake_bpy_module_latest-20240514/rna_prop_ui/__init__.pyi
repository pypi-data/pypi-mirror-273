import typing

GenericType = typing.TypeVar("GenericType")

class PropertyPanel:
    """ """

    bl_label: typing.Any
    """ """

    bl_options: typing.Any
    """ """

    bl_order: typing.Any
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

    def poll(self, context):
        """

        :param context:
        """
        ...

def draw(layout, context, context_member, property_type, use_edit):
    """ """

    ...

def rna_idprop_context_value(context, context_member, property_type):
    """ """

    ...

def rna_idprop_has_properties(rna_item):
    """ """

    ...

def rna_idprop_quote_path(prop):
    """ """

    ...

def rna_idprop_ui_create(
    item,
    prop,
    default,
    min,
    max,
    soft_min,
    soft_max,
    description,
    overridable,
    subtype,
    step,
    precision,
    id_type,
    items,
):
    """ """

    ...

def rna_idprop_ui_prop_clear(item, prop):
    """ """

    ...

def rna_idprop_ui_prop_default_set(item, prop, value):
    """ """

    ...

def rna_idprop_ui_prop_update(item, prop):
    """ """

    ...

def rna_idprop_value_item_type(value):
    """ """

    ...

def rna_idprop_value_to_python(value):
    """ """

    ...
