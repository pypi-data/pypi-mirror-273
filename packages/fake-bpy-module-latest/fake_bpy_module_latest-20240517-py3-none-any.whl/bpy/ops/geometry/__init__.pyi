import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def attribute_add(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    name: str | typing.Any = "",
    domain: str | int | None = "POINT",
    data_type: str | int | None = "FLOAT",
):
    """Add attribute to geometry

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param name: Name, Name of new attribute
    :type name: str | typing.Any
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: str | int | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: str | int | None
    """

    ...

def attribute_convert(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    mode: typing.Any | None = "GENERIC",
    domain: str | int | None = "POINT",
    data_type: str | int | None = "FLOAT",
):
    """Change how the attribute is stored

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Any | None
    :param domain: Domain, Which geometry element to move the attribute to
    :type domain: str | int | None
    :param data_type: Data Type
    :type data_type: str | int | None
    """

    ...

def attribute_remove(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Remove attribute from geometry

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def color_attribute_add(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    name: str | typing.Any = "",
    domain: str | int | None = "POINT",
    data_type: str | int | None = "FLOAT_COLOR",
    color: typing.Any | None = (0.0, 0.0, 0.0, 1.0),
):
    """Add color attribute to geometry

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param name: Name, Name of new color attribute
    :type name: str | typing.Any
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: str | int | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: str | int | None
    :param color: Color, Default fill color
    :type color: typing.Any | None
    """

    ...

def color_attribute_convert(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    domain: str | int | None = "POINT",
    data_type: str | int | None = "FLOAT_COLOR",
):
    """Change how the color attribute is stored

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: str | int | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: str | int | None
    """

    ...

def color_attribute_duplicate(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Duplicate color attribute

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def color_attribute_remove(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Remove color attribute from geometry

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def color_attribute_render_set(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    name: str | typing.Any = "Color",
):
    """Set default color attribute used for rendering

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param name: Name, Name of color attribute
    :type name: str | typing.Any
    """

    ...

def execute_node_group(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    asset_library_type: str | int | None = "LOCAL",
    asset_library_identifier: str | typing.Any = "",
    relative_asset_identifier: str | typing.Any = "",
    name: str | typing.Any = "",
    session_uid: typing.Any | None = 0,
    mouse_position: typing.Any | None = (0, 0),
):
    """Execute a node group on geometry

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param asset_library_type: Asset Library Type
    :type asset_library_type: str | int | None
    :param asset_library_identifier: Asset Library Identifier
    :type asset_library_identifier: str | typing.Any
    :param relative_asset_identifier: Relative Asset Identifier
    :type relative_asset_identifier: str | typing.Any
    :param name: Name, Name of the data-block to use by the operator
    :type name: str | typing.Any
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: typing.Any | None
    :param mouse_position: Mouse Position, Mouse coordinates in region space
    :type mouse_position: typing.Any | None
    """

    ...

def geometry_randomization(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    value: bool | typing.Any | None = False,
):
    """Toggle geometry randomization for debugging purposes

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param value: Value, Randomize the order of geometry elements (e.g. vertices or edges) after some operations where there are no guarantees about the order. This avoids accidentally depending on something that may change in the future
    :type value: bool | typing.Any | None
    """

    ...
