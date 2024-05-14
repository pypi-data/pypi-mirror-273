import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def addon_disable(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    module: typing.Union[str, typing.Any] = "",
):
    """Turn off this extension

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param module: Module, Module name of the add-on to disable
    :type module: typing.Union[str, typing.Any]
    """

    ...

def addon_enable(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    module: typing.Union[str, typing.Any] = "",
):
    """Turn on this extension

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param module: Module, Module name of the add-on to enable
    :type module: typing.Union[str, typing.Any]
    """

    ...

def addon_expand(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    module: typing.Union[str, typing.Any] = "",
):
    """Display information and preferences for this add-on

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param module: Module, Module name of the add-on to expand
    :type module: typing.Union[str, typing.Any]
    """

    ...

def addon_install(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    overwrite: typing.Optional[typing.Union[bool, typing.Any]] = True,
    target: typing.Optional[typing.Union[str, int, typing.Any]] = "",
    filepath: typing.Union[str, typing.Any] = "",
    filter_folder: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_python: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_glob: typing.Union[str, typing.Any] = "*.py;*.zip",
):
    """Install an add-on

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param overwrite: Overwrite, Remove existing add-ons with the same ID
    :type overwrite: typing.Optional[typing.Union[bool, typing.Any]]
    :param target: Target Path
    :type target: typing.Optional[typing.Union[str, int, typing.Any]]
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    :param filter_folder: Filter folders
    :type filter_folder: typing.Optional[typing.Union[bool, typing.Any]]
    :param filter_python: Filter Python
    :type filter_python: typing.Optional[typing.Union[bool, typing.Any]]
    :param filter_glob: filter_glob
    :type filter_glob: typing.Union[str, typing.Any]
    """

    ...

def addon_refresh(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Scan add-on directories for new modules

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def addon_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    module: typing.Union[str, typing.Any] = "",
):
    """Delete the add-on from the file system

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param module: Module, Module name of the add-on to remove
    :type module: typing.Union[str, typing.Any]
    """

    ...

def addon_show(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    module: typing.Union[str, typing.Any] = "",
):
    """Show add-on preferences

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param module: Module, Module name of the add-on to expand
    :type module: typing.Union[str, typing.Any]
    """

    ...

def app_template_install(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    overwrite: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filepath: typing.Union[str, typing.Any] = "",
    filter_folder: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_glob: typing.Union[str, typing.Any] = "*.zip",
):
    """Install an application template

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param overwrite: Overwrite, Remove existing template with the same ID
    :type overwrite: typing.Optional[typing.Union[bool, typing.Any]]
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    :param filter_folder: Filter folders
    :type filter_folder: typing.Optional[typing.Union[bool, typing.Any]]
    :param filter_glob: filter_glob
    :type filter_glob: typing.Union[str, typing.Any]
    """

    ...

def asset_library_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    directory: typing.Union[str, typing.Any] = "",
    hide_props_region: typing.Optional[typing.Union[bool, typing.Any]] = True,
    check_existing: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_blender: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_backup: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_image: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_movie: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_python: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_font: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_sound: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_text: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_archive: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_btx: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_collada: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_alembic: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_usd: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_obj: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_volume: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_folder: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_blenlib: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filemode: typing.Optional[typing.Any] = 9,
    display_type: typing.Optional[typing.Any] = "DEFAULT",
    sort_method: typing.Optional[typing.Union[str, int, typing.Any]] = "",
):
    """Add a directory to be used by the Asset Browser as source of assets

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param directory: Directory, Directory of the file
        :type directory: typing.Union[str, typing.Any]
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: typing.Optional[typing.Union[bool, typing.Any]]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_blender: Filter .blend files
        :type filter_blender: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_backup: Filter .blend files
        :type filter_backup: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_image: Filter image files
        :type filter_image: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_movie: Filter movie files
        :type filter_movie: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_python: Filter Python files
        :type filter_python: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_font: Filter font files
        :type filter_font: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_sound: Filter sound files
        :type filter_sound: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_text: Filter text files
        :type filter_text: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_archive: Filter archive files
        :type filter_archive: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_btx: Filter btx files
        :type filter_btx: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_collada: Filter COLLADA files
        :type filter_collada: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_usd: Filter USD files
        :type filter_usd: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_obj: Filter OBJ files
        :type filter_obj: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_folder: Filter folders
        :type filter_folder: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: typing.Optional[typing.Union[bool, typing.Any]]
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Optional[typing.Any]
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: typing.Optional[typing.Any]
        :param sort_method: File sorting mode
        :type sort_method: typing.Optional[typing.Union[str, int, typing.Any]]
    """

    ...

def asset_library_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    index: typing.Optional[typing.Any] = 0,
):
    """Remove a path to a .blend file, so the Asset Browser will not attempt to show it anymore

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param index: Index
    :type index: typing.Optional[typing.Any]
    """

    ...

def associate_blend(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Use this installation for .blend files and to display thumbnails

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def autoexec_path_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add path to exclude from auto-execution

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def autoexec_path_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    index: typing.Optional[typing.Any] = 0,
):
    """Remove path to exclude from auto-execution

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param index: Index
    :type index: typing.Optional[typing.Any]
    """

    ...

def copy_prev(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Copy settings from previous version

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def extension_repo_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    name: typing.Union[str, typing.Any] = "",
    remote_path: typing.Union[str, typing.Any] = "",
    use_custom_directory: typing.Optional[typing.Union[bool, typing.Any]] = False,
    custom_directory: typing.Union[str, typing.Any] = "",
    type: typing.Optional[typing.Any] = "REMOTE",
):
    """Add a new repository used to store extensions

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param name: Name, Unique repository name
        :type name: typing.Union[str, typing.Any]
        :param remote_path: URL, Remote URL or path for extension repository
        :type remote_path: typing.Union[str, typing.Any]
        :param use_custom_directory: Custom Directory, Manually set the path for extensions to be stored. When disabled a user's extensions directory is created
        :type use_custom_directory: typing.Optional[typing.Union[bool, typing.Any]]
        :param custom_directory: Custom Directory, The local directory containing extensions
        :type custom_directory: typing.Union[str, typing.Any]
        :param type: Type, The kind of repository to add

    REMOTE
    Add Remote Repository -- Add a repository referencing an remote repository with support for listing and updating extensions.

    LOCAL
    Add Local Repository -- Add a repository managed manually without referencing an external repository.
        :type type: typing.Optional[typing.Any]
    """

    ...

def extension_repo_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    index: typing.Optional[typing.Any] = 0,
    type: typing.Optional[typing.Any] = "REPO_ONLY",
):
    """Remove an extension repository

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param index: Index
        :type index: typing.Optional[typing.Any]
        :param type: Type, Method for removing the repository

    REPO_ONLY
    Remove Repository.

    REPO_AND_DIRECTORY
    Remove Repository & Files -- Delete all associated local files when removing.
        :type type: typing.Optional[typing.Any]
    """

    ...

def extension_repo_sync(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Synchronize the active extension repository with its remote URL

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def extension_repo_upgrade(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Update any outdated extensions for the active extension repository

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def extension_url_drop(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    url: typing.Union[str, typing.Any] = "",
):
    """Handle dropping an extension URL

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param url: URL, Location of the extension to install
    :type url: typing.Union[str, typing.Any]
    """

    ...

def keyconfig_activate(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filepath: typing.Union[str, typing.Any] = "",
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    """

    ...

def keyconfig_export(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    all: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filepath: typing.Union[str, typing.Any] = "",
    filter_folder: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_text: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_python: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Export key configuration to a Python script

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param all: All Keymaps, Write all keymaps (not just user modified)
    :type all: typing.Optional[typing.Union[bool, typing.Any]]
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    :param filter_folder: Filter folders
    :type filter_folder: typing.Optional[typing.Union[bool, typing.Any]]
    :param filter_text: Filter text
    :type filter_text: typing.Optional[typing.Union[bool, typing.Any]]
    :param filter_python: Filter Python
    :type filter_python: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def keyconfig_import(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filepath: typing.Union[str, typing.Any] = "keymap.py",
    filter_folder: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_text: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_python: typing.Optional[typing.Union[bool, typing.Any]] = True,
    keep_original: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Import key configuration from a Python script

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    :param filter_folder: Filter folders
    :type filter_folder: typing.Optional[typing.Union[bool, typing.Any]]
    :param filter_text: Filter text
    :type filter_text: typing.Optional[typing.Union[bool, typing.Any]]
    :param filter_python: Filter Python
    :type filter_python: typing.Optional[typing.Union[bool, typing.Any]]
    :param keep_original: Keep Original, Keep original file after copying to configuration folder
    :type keep_original: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def keyconfig_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove key config

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def keyconfig_test(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Test key configuration for conflicts

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def keyitem_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add key map item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def keyitem_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    item_id: typing.Optional[typing.Any] = 0,
):
    """Remove key map item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param item_id: Item Identifier, Identifier of the item to remove
    :type item_id: typing.Optional[typing.Any]
    """

    ...

def keyitem_restore(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    item_id: typing.Optional[typing.Any] = 0,
):
    """Restore key map item

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param item_id: Item Identifier, Identifier of the item to restore
    :type item_id: typing.Optional[typing.Any]
    """

    ...

def keymap_restore(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    all: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Restore key map(s)

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param all: All Keymaps, Restore all keymaps to default
    :type all: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def reset_default_theme(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Reset to the default theme colors

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def script_directory_add(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    directory: typing.Union[str, typing.Any] = "",
    filter_folder: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param directory: directory
    :type directory: typing.Union[str, typing.Any]
    :param filter_folder: Filter Folders
    :type filter_folder: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def script_directory_remove(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    index: typing.Optional[typing.Any] = 0,
):
    """Undocumented, consider contributing.

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param index: Index, Index of the script directory to remove
    :type index: typing.Optional[typing.Any]
    """

    ...

def studiolight_copy_settings(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    index: typing.Optional[typing.Any] = 0,
):
    """Copy Studio Light settings to the Studio Light editor

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param index: index
    :type index: typing.Optional[typing.Any]
    """

    ...

def studiolight_install(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    files: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    ] = None,
    directory: typing.Union[str, typing.Any] = "",
    filter_folder: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_glob: typing.Union[str, typing.Any] = "*.png;*.jpg;*.hdr;*.exr",
    type: typing.Optional[typing.Any] = "MATCAP",
):
    """Install a user defined light

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param files: File Path
        :type files: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]]
        :param directory: directory
        :type directory: typing.Union[str, typing.Any]
        :param filter_folder: Filter Folders
        :type filter_folder: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_glob: filter_glob
        :type filter_glob: typing.Union[str, typing.Any]
        :param type: Type

    MATCAP
    MatCap -- Install custom MatCaps.

    WORLD
    World -- Install custom HDRIs.

    STUDIO
    Studio -- Install custom Studio Lights.
        :type type: typing.Optional[typing.Any]
    """

    ...

def studiolight_new(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filename: typing.Union[str, typing.Any] = "StudioLight",
):
    """Save custom studio light from the studio light editor settings

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param filename: Name
    :type filename: typing.Union[str, typing.Any]
    """

    ...

def studiolight_show(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Show light preferences

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def studiolight_uninstall(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    index: typing.Optional[typing.Any] = 0,
):
    """Delete Studio Light

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param index: index
    :type index: typing.Optional[typing.Any]
    """

    ...

def theme_install(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    overwrite: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filepath: typing.Union[str, typing.Any] = "",
    filter_folder: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_glob: typing.Union[str, typing.Any] = "*.xml",
):
    """Load and apply a Blender XML theme file

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param overwrite: Overwrite, Remove existing theme file if exists
    :type overwrite: typing.Optional[typing.Union[bool, typing.Any]]
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    :param filter_folder: Filter folders
    :type filter_folder: typing.Optional[typing.Union[bool, typing.Any]]
    :param filter_glob: filter_glob
    :type filter_glob: typing.Union[str, typing.Any]
    """

    ...

def unassociate_blend(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove this installation's associations with .blend files

    :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...
