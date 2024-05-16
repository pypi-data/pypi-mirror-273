"""
This module contains utility functions specific to blender but
not associated with blenders internal data.

bpy.utils.previews.rst
bpy.utils.units.rst

:maxdepth: 1
:caption: Submodules

"""

import typing
from . import previews
from . import units

GenericType = typing.TypeVar("GenericType")

def app_template_paths(path: typing.Optional[str] = None):
    """Returns valid application template paths.

    :param path: Optional subdir.
    :type path: typing.Optional[str]
    :return: app template paths.
    """

    ...

def app_template_paths(path):
    """ """

    ...

def blend_paths(
    absolute: typing.Optional[bool] = False,
    packed: typing.Optional[bool] = False,
    local: typing.Optional[bool] = False,
) -> typing.List[str]:
    """Returns a list of paths to external files referenced by the loaded .blend file.

    :param absolute: When true the paths returned are made absolute.
    :type absolute: typing.Optional[bool]
    :param packed: When true skip file paths for packed data.
    :type packed: typing.Optional[bool]
    :param local: When true skip linked library paths.
    :type local: typing.Optional[bool]
    :return: path list.
    :rtype: typing.List[str]
    """

    ...

def escape_identifier(string: typing.Optional[str]) -> str:
    """Simple string escaping function used for animation paths.

    :param string: text
    :type string: typing.Optional[str]
    :return: The escaped string.
    :rtype: str
    """

    ...

def execfile(filepath: typing.Optional[str], mod=None):
    """Execute a file path as a Python script.

    :param filepath: Path of the script to execute.
    :type filepath: typing.Optional[str]
    :param mod: Optional cached module, the result of a previous execution.
    :return: The module which can be passed back in as mod.
    """

    ...

def execfile(filepath, mod):
    """ """

    ...

def flip_name(
    name: typing.Optional[str], strip_digits: typing.Optional[bool] = False
) -> str:
    """Flip a name between left/right sides, useful for
    mirroring bone names.

        :param name: Bone name to flip.
        :type name: typing.Optional[str]
        :param strip_digits: Whether to remove .### suffix.
        :type strip_digits: typing.Optional[bool]
        :return: The flipped name.
        :rtype: str
    """

    ...

def is_path_builtin(path):
    """ """

    ...

def keyconfig_init():
    """ """

    ...

def keyconfig_init():
    """ """

    ...

def keyconfig_set(filepath, report=None):
    """ """

    ...

def keyconfig_set(filepath, report):
    """ """

    ...

def load_scripts(
    reload_scripts: typing.Optional[bool] = False,
    refresh_scripts: typing.Optional[bool] = False,
    extensions: typing.Optional[bool] = True,
):
    """Load scripts and run each modules register function.

        :param reload_scripts: Causes all scripts to have their unregister method
    called before loading.
        :type reload_scripts: typing.Optional[bool]
        :param refresh_scripts: only load scripts which are not already loaded
    as modules.
        :type refresh_scripts: typing.Optional[bool]
        :param extensions: Loads additional scripts (add-ons & app-templates).
        :type extensions: typing.Optional[bool]
    """

    ...

def load_scripts(reload_scripts, refresh_scripts, extensions):
    """ """

    ...

def load_scripts_extensions(reload_scripts):
    """ """

    ...

def make_rna_paths(
    struct_name: typing.Optional[str],
    prop_name: typing.Optional[str],
    enum_name: typing.Optional[str],
):
    """Create RNA "paths" from given names.

        :param struct_name: Name of a RNA struct (like e.g. "Scene").
        :type struct_name: typing.Optional[str]
        :param prop_name: Name of a RNA struct's property.
        :type prop_name: typing.Optional[str]
        :param enum_name: Name of a RNA enum identifier.
        :type enum_name: typing.Optional[str]
        :return: A triple of three "RNA paths"
    (most_complete_path, "struct.prop", "struct.prop:'enum'").
    If no enum_name is given, the third element will always be void.
    """

    ...

def make_rna_paths(struct_name, prop_name, enum_name):
    """ """

    ...

def manual_language_code(default="en") -> str:
    """

        :return: The language code used for user manual URL component based on the current language user-preference,
    falling back to the default when unavailable.
        :rtype: str
    """

    ...

def manual_language_code(default):
    """ """

    ...

def manual_map():
    """ """

    ...

def manual_map():
    """ """

    ...

def modules_from_path(
    path: typing.Optional[str], loaded_modules: typing.Optional[set]
) -> list:
    """Load all modules in a path and return them as a list.

        :param path: this path is scanned for scripts and packages.
        :type path: typing.Optional[str]
        :param loaded_modules: already loaded module names, files matching these
    names will be ignored.
        :type loaded_modules: typing.Optional[set]
        :return: all loaded modules.
        :rtype: list
    """

    ...

def modules_from_path(path, loaded_modules):
    """ """

    ...

def preset_find(name, preset_path, display_name=False, ext=".py"):
    """ """

    ...

def preset_find(name, preset_path, display_name, ext):
    """ """

    ...

def preset_paths(subdir: typing.Optional[str]) -> list:
    """Returns a list of paths for a specific preset.

    :param subdir: preset subdirectory (must not be an absolute path).
    :type subdir: typing.Optional[str]
    :return: script paths.
    :rtype: list
    """

    ...

def preset_paths(subdir):
    """ """

    ...

def refresh_script_paths():
    """Run this after creating new script paths to update sys.path"""

    ...

def refresh_script_paths():
    """ """

    ...

def register_class(cls):
    """Register a subclass of a Blender type class.

        :param cls: Blender type class in:
    `bpy.types.Panel`, `bpy.types.UIList`,
    `bpy.types.Menu`, `bpy.types.Header`,
    `bpy.types.Operator`, `bpy.types.KeyingSetInfo`,
    `bpy.types.RenderEngine`, `bpy.types.AssetShelf`,
    `bpy.types.FileHandler`
    """

    ...

def register_classes_factory(classes):
    """Utility function to create register and unregister functions
    which simply registers and unregisters a sequence of classes.

    """

    ...

def register_classes_factory(classes):
    """ """

    ...

def register_cli_command(
    id: typing.Optional[str], execute: typing.Optional[typing.Callable]
):
    """Register a command, accessible via the (-c / --command) command-line argument.Custom CommandsRegistering commands makes it possible to conveniently expose command line
    functionality via commands passed to (-c / --command).Using Python Argument ParsingThis example shows how the Python argparse module can be used with a custom command.Using argparse is generally recommended as it has many useful utilities and
    generates a --help message for your command.

        :param id: The command identifier (must pass an str.isidentifier check).

    If the id is already registered, a warning is printed and the command is inaccessible to prevent accidents invoking the wrong command.
        :type id: typing.Optional[str]
        :param execute: Callback, taking a single list of strings and returns an int.
    The arguments are built from all command-line arguments following the command id.
    The return value should be 0 for success, 1 on failure (specific error codes from the os module can also be used).
        :type execute: typing.Optional[typing.Callable]
        :return: The command handle which can be passed to `unregister_cli_command`.
    """

    ...

def register_manual_map(manual_hook):
    """ """

    ...

def register_manual_map(manual_hook):
    """ """

    ...

def register_submodule_factory(
    module_name: typing.Optional[str],
    submodule_names: typing.Optional[typing.List[str]],
):
    """Utility function to create register and unregister functions
    which simply load submodules,
    calling their register & unregister functions.

        :param module_name: The module name, typically __name__.
        :type module_name: typing.Optional[str]
        :param submodule_names: List of submodule names to load and unload.
        :type submodule_names: typing.Optional[typing.List[str]]
        :return: register and unregister functions.
    """

    ...

def register_submodule_factory(module_name, submodule_names):
    """ """

    ...

def register_tool(
    tool_cls,
    after=None,
    separator: typing.Optional[bool] = False,
    group: typing.Optional[bool] = False,
):
    """Register a tool in the toolbar.

    :param after: Optional identifiers this tool will be added after.
    :param separator: When true, add a separator before this tool.
    :type separator: typing.Optional[bool]
    :param group: When true, add a new nested group of tools.
    :type group: typing.Optional[bool]
    """

    ...

def register_tool(tool_cls, after, separator, group):
    """ """

    ...

def resource_path(
    type: typing.Optional[str],
    major: typing.Optional[int] = None[0],
    minor: typing.Optional[str] = None[1],
) -> str:
    """Return the base path for storing system files.

    :param type: string in ['USER', 'LOCAL', 'SYSTEM'].
    :type type: typing.Optional[str]
    :param major: major version, defaults to current.
    :type major: typing.Optional[int]
    :param minor: minor version, defaults to current.
    :type minor: typing.Optional[str]
    :return: the resource path (not necessarily existing).
    :rtype: str
    """

    ...

def script_path_user():
    """returns the env var and falls back to home dir or None"""

    ...

def script_path_user():
    """ """

    ...

def script_paths(
    subdir: typing.Optional[str] = None,
    user_pref: typing.Optional[bool] = True,
    check_all: typing.Optional[bool] = False,
    use_user=True,
) -> list:
    """Returns a list of valid script paths.

    :param subdir: Optional subdir.
    :type subdir: typing.Optional[str]
    :param user_pref: Include the user preference script paths.
    :type user_pref: typing.Optional[bool]
    :param check_all: Include local, user and system paths rather just the paths Blender uses.
    :type check_all: typing.Optional[bool]
    :return: script paths.
    :rtype: list
    """

    ...

def script_paths(subdir, user_pref, check_all, use_user):
    """ """

    ...

def script_paths_pref():
    """ """

    ...

def smpte_from_frame(frame: typing.Optional[int], fps=None, fps_base=None) -> str:
    """Returns an SMPTE formatted string from the frame:
    HH:MM:SS:FF.If fps and fps_base are not given the current scene is used.

        :param frame: frame number.
        :type frame: typing.Optional[int]
        :return: the frame string.
        :rtype: str
    """

    ...

def smpte_from_frame(frame, fps, fps_base):
    """ """

    ...

def smpte_from_seconds(
    time: typing.Optional[typing.Union[int, float]], fps=None, fps_base=None
) -> str:
    """Returns an SMPTE formatted string from the time:
    HH:MM:SS:FF.If fps and fps_base are not given the current scene is used.

        :param time: time in seconds.
        :type time: typing.Optional[typing.Union[int, float]]
        :return: the frame string.
        :rtype: str
    """

    ...

def smpte_from_seconds(time, fps, fps_base):
    """ """

    ...

def time_from_frame(frame, fps, fps_base):
    """ """

    ...

def time_to_frame(time, fps, fps_base):
    """ """

    ...

def unescape_identifier(string: typing.Optional[str]) -> str:
    """Simple string un-escape function used for animation paths.
    This performs the reverse of escape_identifier.

        :param string: text
        :type string: typing.Optional[str]
        :return: The un-escaped string.
        :rtype: str
    """

    ...

def unregister_class(cls):
    """Unload the Python class from blender.

        :param cls: Blender type class,
    see `bpy.utils.register_class` for classes which can
    be registered.
    """

    ...

def unregister_cli_command(handle):
    """Unregister a CLI command.

    :param handle: The return value of `register_cli_command`.
    """

    ...

def unregister_manual_map(manual_hook):
    """ """

    ...

def unregister_manual_map(manual_hook):
    """ """

    ...

def unregister_tool(tool_cls):
    """ """

    ...

def unregister_tool(tool_cls):
    """ """

    ...

def user_resource(
    resource_type,
    path: typing.Optional[str] = "",
    create: typing.Optional[bool] = False,
) -> str:
    """Return a user resource path (normally from the users home directory).

        :param path: Optional subdirectory.
        :type path: typing.Optional[str]
        :param create: Treat the path as a directory and create
    it if its not existing.
        :type create: typing.Optional[bool]
        :return: a path.
        :rtype: str
    """

    ...

def user_resource(resource_type, path, create):
    """ """

    ...
