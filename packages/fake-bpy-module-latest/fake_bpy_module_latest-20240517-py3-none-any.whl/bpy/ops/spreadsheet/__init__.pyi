import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def add_row_filter_rule(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Add a filter to remove rows from the displayed data

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def change_spreadsheet_data_source(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    component_type: typing.Any | None = 0,
    attribute_domain_type: typing.Any | None = 0,
):
    """Change visible data source in the spreadsheet

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param component_type: Component Type
    :type component_type: typing.Any | None
    :param attribute_domain_type: Attribute Domain Type
    :type attribute_domain_type: typing.Any | None
    """

    ...

def remove_row_filter_rule(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    index: typing.Any | None = 0,
):
    """Remove a row filter from the rules

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param index: Index
    :type index: typing.Any | None
    """

    ...

def toggle_pin(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Turn on or off pinning

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...
