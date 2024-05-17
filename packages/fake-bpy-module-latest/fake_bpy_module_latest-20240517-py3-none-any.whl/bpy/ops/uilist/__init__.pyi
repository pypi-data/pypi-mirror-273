import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def entry_add(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    list_path: str | typing.Any = "",
    active_index_path: str | typing.Any = "",
):
    """Add an entry to the list after the current active item

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param list_path: list_path
    :type list_path: str | typing.Any
    :param active_index_path: active_index_path
    :type active_index_path: str | typing.Any
    """

    ...

def entry_move(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    list_path: str | typing.Any = "",
    active_index_path: str | typing.Any = "",
    direction: typing.Any | None = "UP",
):
    """Move an entry in the list up or down

        :type override_context: dict[str, typing.Any] | bpy.types.Context | None
        :type execution_context: str | int | None
        :type undo: bool | None
        :param list_path: list_path
        :type list_path: str | typing.Any
        :param active_index_path: active_index_path
        :type active_index_path: str | typing.Any
        :param direction: Direction

    UP
    UP -- UP.

    DOWN
    DOWN -- DOWN.
        :type direction: typing.Any | None
    """

    ...

def entry_remove(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    list_path: str | typing.Any = "",
    active_index_path: str | typing.Any = "",
):
    """Remove the selected entry from the list

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param list_path: list_path
    :type list_path: str | typing.Any
    :param active_index_path: active_index_path
    :type active_index_path: str | typing.Any
    """

    ...
