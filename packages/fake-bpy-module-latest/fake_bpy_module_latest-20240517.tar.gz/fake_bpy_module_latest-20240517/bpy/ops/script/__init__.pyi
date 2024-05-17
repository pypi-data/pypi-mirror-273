import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def execute_preset(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    filepath: str | typing.Any = "",
    menu_idname: str | typing.Any = "",
):
    """Load a preset

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str | typing.Any
    :param menu_idname: Menu ID Name, ID name of the menu this was called from
    :type menu_idname: str | typing.Any
    """

    ...

def python_file_run(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    filepath: str | typing.Any = "",
):
    """Run Python file

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param filepath: Path
    :type filepath: str | typing.Any
    """

    ...

def reload(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Reload scripts

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...
