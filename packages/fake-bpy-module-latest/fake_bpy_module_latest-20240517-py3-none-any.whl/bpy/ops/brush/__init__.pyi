import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def add(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Add brush by mode type

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def add_gpencil(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Add brush for Grease Pencil

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def curve_preset(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    shape: typing.Any | None = "SMOOTH",
):
    """Set brush shape

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param shape: Mode
    :type shape: typing.Any | None
    """

    ...

def reset(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Return brush to defaults based on current tool

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def scale_size(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    scalar: typing.Any | None = 1.0,
):
    """Change brush size by a scalar

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param scalar: Scalar, Factor to scale brush size by
    :type scalar: typing.Any | None
    """

    ...

def sculpt_curves_falloff_preset(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    shape: typing.Any | None = "SMOOTH",
):
    """Set Curve Falloff Preset

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param shape: Mode
    :type shape: typing.Any | None
    """

    ...

def stencil_control(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    mode: typing.Any | None = "TRANSLATION",
    texmode: typing.Any | None = "PRIMARY",
):
    """Control the stencil brush

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param mode: Tool
    :type mode: typing.Any | None
    :param texmode: Tool
    :type texmode: typing.Any | None
    """

    ...

def stencil_fit_image_aspect(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    use_repeat: bool | typing.Any | None = True,
    use_scale: bool | typing.Any | None = True,
    mask: bool | typing.Any | None = False,
):
    """When using an image texture, adjust the stencil size to fit the image aspect ratio

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param use_repeat: Use Repeat, Use repeat mapping values
    :type use_repeat: bool | typing.Any | None
    :param use_scale: Use Scale, Use texture scale values
    :type use_scale: bool | typing.Any | None
    :param mask: Modify Mask Stencil, Modify either the primary or mask stencil
    :type mask: bool | typing.Any | None
    """

    ...

def stencil_reset_transform(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    mask: bool | typing.Any | None = False,
):
    """Reset the stencil transformation to the default

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param mask: Modify Mask Stencil, Modify either the primary or mask stencil
    :type mask: bool | typing.Any | None
    """

    ...
