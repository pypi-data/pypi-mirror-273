import typing

GenericType = typing.TypeVar("GenericType")

def new_triangles(
    range: typing.Optional[tuple],
    coords: typing.Optional[typing.Sequence[bytes]],
    colors: typing.Optional[typing.Sequence[bytes]],
) -> int:
    """Create a new icon from triangle geometry.

    :param range: Pair of ints.
    :type range: typing.Optional[tuple]
    :param coords: Sequence of bytes (6 floats for one triangle) for (X, Y) coordinates.
    :type coords: typing.Optional[typing.Sequence[bytes]]
    :param colors: Sequence of ints (12 for one triangles) for RGBA.
    :type colors: typing.Optional[typing.Sequence[bytes]]
    :return: Unique icon value (pass to interface icon_value argument).
    :rtype: int
    """

    ...

def new_triangles_from_file(filepath: typing.Optional[str]) -> int:
    """Create a new icon from triangle geometry.

    :param filepath: File path.
    :type filepath: typing.Optional[str]
    :return: Unique icon value (pass to interface icon_value argument).
    :rtype: int
    """

    ...

def release(icon_id):
    """Release the icon."""

    ...
