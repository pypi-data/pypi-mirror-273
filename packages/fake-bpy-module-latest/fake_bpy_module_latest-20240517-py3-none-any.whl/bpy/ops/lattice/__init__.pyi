import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def flip(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    axis: typing.Any | None = "U",
):
    """Mirror all control points without inverting the lattice deform

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param axis: Flip Axis, Coordinates along this axis get flipped
    :type axis: typing.Any | None
    """

    ...

def make_regular(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Set UVW control points a uniform distance apart

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def select_all(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    action: typing.Any | None = "TOGGLE",
):
    """Change selection of all UVW control points

        :type override_context: dict[str, typing.Any] | bpy.types.Context | None
        :type execution_context: str | int | None
        :type undo: bool | None
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :type action: typing.Any | None
    """

    ...

def select_less(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Deselect vertices at the boundary of each selection region

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def select_mirror(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    axis: typing.Any | None = {"X"},
    extend: bool | typing.Any | None = False,
):
    """Select mirrored lattice points

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param axis: Axis
    :type axis: typing.Any | None
    :param extend: Extend, Extend the selection
    :type extend: bool | typing.Any | None
    """

    ...

def select_more(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Select vertex directly linked to already selected ones

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def select_random(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    ratio: typing.Any | None = 0.5,
    seed: typing.Any | None = 0,
    action: typing.Any | None = "SELECT",
):
    """Randomly select UVW control points

        :type override_context: dict[str, typing.Any] | bpy.types.Context | None
        :type execution_context: str | int | None
        :type undo: bool | None
        :param ratio: Ratio, Portion of items to select randomly
        :type ratio: typing.Any | None
        :param seed: Random Seed, Seed for the random number generator
        :type seed: typing.Any | None
        :param action: Action, Selection action to execute

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :type action: typing.Any | None
    """

    ...

def select_ungrouped(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    extend: bool | typing.Any | None = False,
):
    """Select vertices without a group

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param extend: Extend, Extend the selection
    :type extend: bool | typing.Any | None
    """

    ...
