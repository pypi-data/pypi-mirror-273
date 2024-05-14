import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def fbx(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filepath: typing.Union[str, typing.Any] = "",
    check_existing: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_glob: typing.Union[str, typing.Any] = "*.fbx",
    use_selection: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_visible: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_active_collection: typing.Optional[typing.Union[bool, typing.Any]] = False,
    collection: typing.Union[str, typing.Any] = "",
    global_scale: typing.Optional[typing.Any] = 1.0,
    apply_unit_scale: typing.Optional[typing.Union[bool, typing.Any]] = True,
    apply_scale_options: typing.Optional[typing.Any] = "FBX_SCALE_NONE",
    use_space_transform: typing.Optional[typing.Union[bool, typing.Any]] = True,
    bake_space_transform: typing.Optional[typing.Union[bool, typing.Any]] = False,
    object_types: typing.Optional[typing.Any] = {
        '"CAMERA"',
        '"ARMATURE"',
        '"EMPTY"',
        '"MESH"',
        '"LIGHT"',
        '"OTHER"',
    },
    use_mesh_modifiers: typing.Optional[typing.Union[bool, typing.Any]] = True,
    use_mesh_modifiers_render: typing.Optional[typing.Union[bool, typing.Any]] = True,
    mesh_smooth_type: typing.Optional[typing.Any] = "OFF",
    colors_type: typing.Optional[typing.Any] = "SRGB",
    prioritize_active_color: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_subsurf: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_mesh_edges: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_tspace: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_triangles: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_custom_props: typing.Optional[typing.Union[bool, typing.Any]] = False,
    add_leaf_bones: typing.Optional[typing.Union[bool, typing.Any]] = True,
    primary_bone_axis: typing.Optional[typing.Any] = "Y",
    secondary_bone_axis: typing.Optional[typing.Any] = "X",
    use_armature_deform_only: typing.Optional[typing.Union[bool, typing.Any]] = False,
    armature_nodetype: typing.Optional[typing.Any] = "NULL",
    bake_anim: typing.Optional[typing.Union[bool, typing.Any]] = True,
    bake_anim_use_all_bones: typing.Optional[typing.Union[bool, typing.Any]] = True,
    bake_anim_use_nla_strips: typing.Optional[typing.Union[bool, typing.Any]] = True,
    bake_anim_use_all_actions: typing.Optional[typing.Union[bool, typing.Any]] = True,
    bake_anim_force_startend_keying: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = True,
    bake_anim_step: typing.Optional[typing.Any] = 1.0,
    bake_anim_simplify_factor: typing.Optional[typing.Any] = 1.0,
    path_mode: typing.Optional[typing.Any] = "AUTO",
    embed_textures: typing.Optional[typing.Union[bool, typing.Any]] = False,
    batch_mode: typing.Optional[typing.Any] = "OFF",
    use_batch_own_dir: typing.Optional[typing.Union[bool, typing.Any]] = True,
    use_metadata: typing.Optional[typing.Union[bool, typing.Any]] = True,
    axis_forward: typing.Optional[typing.Any] = "-Z",
    axis_up: typing.Optional[typing.Any] = "Y",
):
    """Write a FBX file

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: typing.Union[str, typing.Any]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_glob: filter_glob
        :type filter_glob: typing.Union[str, typing.Any]
        :param use_selection: Selected Objects, Export selected and visible objects only
        :type use_selection: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_visible: Visible Objects, Export visible objects only
        :type use_visible: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_active_collection: Active Collection, Export only objects from the active collection (and its children)
        :type use_active_collection: typing.Optional[typing.Union[bool, typing.Any]]
        :param collection: Source Collection, Export only objects from this collection (and its children)
        :type collection: typing.Union[str, typing.Any]
        :param global_scale: Scale, Scale all data (Some importers do not support scaled armatures!)
        :type global_scale: typing.Optional[typing.Any]
        :param apply_unit_scale: Apply Unit, Take into account current Blender units settings (if unset, raw Blender Units values are used as-is)
        :type apply_unit_scale: typing.Optional[typing.Union[bool, typing.Any]]
        :param apply_scale_options: Apply Scalings, How to apply custom and units scalings in generated FBX file (Blender uses FBX scale to detect units on import, but many other applications do not handle the same way)

    FBX_SCALE_NONE
    All Local -- Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0.

    FBX_SCALE_UNITS
    FBX Units Scale -- Apply custom scaling to each object transformation, and units scaling to FBX scale.

    FBX_SCALE_CUSTOM
    FBX Custom Scale -- Apply custom scaling to FBX scale, and units scaling to each object transformation.

    FBX_SCALE_ALL
    FBX All -- Apply custom scaling and units scaling to FBX scale.
        :type apply_scale_options: typing.Optional[typing.Any]
        :param use_space_transform: Use Space Transform, Apply global space transform to the object rotations. When disabled only the axis space is written to the file and all object transforms are left as-is
        :type use_space_transform: typing.Optional[typing.Union[bool, typing.Any]]
        :param bake_space_transform: Apply Transform, Bake space transform into object data, avoids getting unwanted rotations to objects when target space is not aligned with Blender's space (WARNING! experimental option, use at own risk, known to be broken with armatures/animations)
        :type bake_space_transform: typing.Optional[typing.Union[bool, typing.Any]]
        :param object_types: Object Types, Which kind of object to export

    EMPTY
    Empty.

    CAMERA
    Camera.

    LIGHT
    Lamp.

    ARMATURE
    Armature -- WARNING: not supported in dupli/group instances.

    MESH
    Mesh.

    OTHER
    Other -- Other geometry types, like curve, metaball, etc. (converted to meshes).
        :type object_types: typing.Optional[typing.Any]
        :param use_mesh_modifiers: Apply Modifiers, Apply modifiers to mesh objects (except Armature ones) - WARNING: prevents exporting shape keys
        :type use_mesh_modifiers: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_mesh_modifiers_render: Use Modifiers Render Setting, Use render settings when applying modifiers to mesh objects (DISABLED in Blender 2.8)
        :type use_mesh_modifiers_render: typing.Optional[typing.Union[bool, typing.Any]]
        :param mesh_smooth_type: Smoothing, Export smoothing information (prefer 'Normals Only' option if your target importer understand split normals)

    OFF
    Normals Only -- Export only normals instead of writing edge or face smoothing data.

    FACE
    Face -- Write face smoothing.

    EDGE
    Edge -- Write edge smoothing.
        :type mesh_smooth_type: typing.Optional[typing.Any]
        :param colors_type: Vertex Colors, Export vertex color attributes

    NONE
    None -- Do not export color attributes.

    SRGB
    sRGB -- Export colors in sRGB color space.

    LINEAR
    Linear -- Export colors in linear color space.
        :type colors_type: typing.Optional[typing.Any]
        :param prioritize_active_color: Prioritize Active Color, Make sure active color will be exported first. Could be important since some other software can discard other color attributes besides the first one
        :type prioritize_active_color: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_subsurf: Export Subdivision Surface, Export the last Catmull-Rom subdivision modifier as FBX subdivision (does not apply the modifier even if 'Apply Modifiers' is enabled)
        :type use_subsurf: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_mesh_edges: Loose Edges, Export loose edges (as two-vertices polygons)
        :type use_mesh_edges: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_tspace: Tangent Space, Add binormal and tangent vectors, together with normal they form the tangent space (will only work correctly with tris/quads only meshes!)
        :type use_tspace: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_triangles: Triangulate Faces, Convert all faces to triangles
        :type use_triangles: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_custom_props: Custom Properties, Export custom properties
        :type use_custom_props: typing.Optional[typing.Union[bool, typing.Any]]
        :param add_leaf_bones: Add Leaf Bones, Append a final bone to the end of each chain to specify last bone length (use this when you intend to edit the armature from exported data)
        :type add_leaf_bones: typing.Optional[typing.Union[bool, typing.Any]]
        :param primary_bone_axis: Primary Bone Axis
        :type primary_bone_axis: typing.Optional[typing.Any]
        :param secondary_bone_axis: Secondary Bone Axis
        :type secondary_bone_axis: typing.Optional[typing.Any]
        :param use_armature_deform_only: Only Deform Bones, Only write deforming bones (and non-deforming ones when they have deforming children)
        :type use_armature_deform_only: typing.Optional[typing.Union[bool, typing.Any]]
        :param armature_nodetype: Armature FBXNode Type, FBX type of node (object) used to represent Blender's armatures (use the Null type unless you experience issues with the other app, as other choices may not import back perfectly into Blender...)

    NULL
    Null -- 'Null' FBX node, similar to Blender's Empty (default).

    ROOT
    Root -- 'Root' FBX node, supposed to be the root of chains of bones....

    LIMBNODE
    LimbNode -- 'LimbNode' FBX node, a regular joint between two bones....
        :type armature_nodetype: typing.Optional[typing.Any]
        :param bake_anim: Baked Animation, Export baked keyframe animation
        :type bake_anim: typing.Optional[typing.Union[bool, typing.Any]]
        :param bake_anim_use_all_bones: Key All Bones, Force exporting at least one key of animation for all bones (needed with some target applications, like UE4)
        :type bake_anim_use_all_bones: typing.Optional[typing.Union[bool, typing.Any]]
        :param bake_anim_use_nla_strips: NLA Strips, Export each non-muted NLA strip as a separated FBX's AnimStack, if any, instead of global scene animation
        :type bake_anim_use_nla_strips: typing.Optional[typing.Union[bool, typing.Any]]
        :param bake_anim_use_all_actions: All Actions, Export each action as a separated FBX's AnimStack, instead of global scene animation (note that animated objects will get all actions compatible with them, others will get no animation at all)
        :type bake_anim_use_all_actions: typing.Optional[typing.Union[bool, typing.Any]]
        :param bake_anim_force_startend_keying: Force Start/End Keying, Always add a keyframe at start and end of actions for animated channels
        :type bake_anim_force_startend_keying: typing.Optional[typing.Union[bool, typing.Any]]
        :param bake_anim_step: Sampling Rate, How often to evaluate animated values (in frames)
        :type bake_anim_step: typing.Optional[typing.Any]
        :param bake_anim_simplify_factor: Simplify, How much to simplify baked values (0.0 to disable, the higher the more simplified)
        :type bake_anim_simplify_factor: typing.Optional[typing.Any]
        :param path_mode: Path Mode, Method used to reference paths

    AUTO
    Auto -- Use relative paths with subdirectories only.

    ABSOLUTE
    Absolute -- Always write absolute paths.

    RELATIVE
    Relative -- Always write relative paths (where possible).

    MATCH
    Match -- Match absolute/relative setting with input path.

    STRIP
    Strip Path -- Filename only.

    COPY
    Copy -- Copy the file to the destination path (or subdirectory).
        :type path_mode: typing.Optional[typing.Any]
        :param embed_textures: Embed Textures, Embed textures in FBX binary file (only for "Copy" path mode!)
        :type embed_textures: typing.Optional[typing.Union[bool, typing.Any]]
        :param batch_mode: Batch Mode

    OFF
    Off -- Active scene to file.

    SCENE
    Scene -- Each scene as a file.

    COLLECTION
    Collection -- Each collection (data-block ones) as a file, does not include content of children collections.

    SCENE_COLLECTION
    Scene Collections -- Each collection (including master, non-data-block ones) of each scene as a file, including content from children collections.

    ACTIVE_SCENE_COLLECTION
    Active Scene Collections -- Each collection (including master, non-data-block one) of the active scene as a file, including content from children collections.
        :type batch_mode: typing.Optional[typing.Any]
        :param use_batch_own_dir: Batch Own Dir, Create a dir for each exported file
        :type use_batch_own_dir: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_metadata: Use Metadata
        :type use_metadata: typing.Optional[typing.Union[bool, typing.Any]]
        :param axis_forward: Forward
        :type axis_forward: typing.Optional[typing.Any]
        :param axis_up: Up
        :type axis_up: typing.Optional[typing.Any]
    """

    ...

def gltf(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filepath: typing.Union[str, typing.Any] = "",
    check_existing: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_import_convert_lighting_mode: typing.Optional[typing.Any] = "SPEC",
    gltf_export_id: typing.Union[str, typing.Any] = "",
    export_use_gltfpack: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_gltfpack_tc: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_gltfpack_tq: typing.Optional[typing.Any] = 8,
    export_gltfpack_si: typing.Optional[typing.Any] = 1.0,
    export_gltfpack_sa: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_gltfpack_slb: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_gltfpack_vp: typing.Optional[typing.Any] = 14,
    export_gltfpack_vt: typing.Optional[typing.Any] = 12,
    export_gltfpack_vn: typing.Optional[typing.Any] = 8,
    export_gltfpack_vc: typing.Optional[typing.Any] = 8,
    export_gltfpack_vpi: typing.Optional[typing.Any] = "Integer",
    export_gltfpack_noq: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_format: typing.Optional[typing.Union[str, int, typing.Any]] = "",
    ui_tab: typing.Optional[typing.Any] = "GENERAL",
    export_copyright: typing.Union[str, typing.Any] = "",
    export_image_format: typing.Optional[typing.Any] = "AUTO",
    export_image_add_webp: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_image_webp_fallback: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_texture_dir: typing.Union[str, typing.Any] = "",
    export_jpeg_quality: typing.Optional[typing.Any] = 75,
    export_image_quality: typing.Optional[typing.Any] = 75,
    export_keep_originals: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_texcoords: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_normals: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_gn_mesh: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_draco_mesh_compression_enable: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = False,
    export_draco_mesh_compression_level: typing.Optional[typing.Any] = 6,
    export_draco_position_quantization: typing.Optional[typing.Any] = 14,
    export_draco_normal_quantization: typing.Optional[typing.Any] = 10,
    export_draco_texcoord_quantization: typing.Optional[typing.Any] = 12,
    export_draco_color_quantization: typing.Optional[typing.Any] = 10,
    export_draco_generic_quantization: typing.Optional[typing.Any] = 12,
    export_tangents: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_materials: typing.Optional[typing.Any] = "EXPORT",
    export_unused_images: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_unused_textures: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_colors: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_attributes: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_mesh_edges: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_mesh_vertices: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_cameras: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_selection: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_visible: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_renderable: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_active_collection_with_nested: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = True,
    use_active_collection: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_active_scene: typing.Optional[typing.Union[bool, typing.Any]] = False,
    collection: typing.Union[str, typing.Any] = "",
    export_extras: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_yup: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_apply: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_shared_accessors: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_animations: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_frame_range: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_frame_step: typing.Optional[typing.Any] = 1,
    export_force_sampling: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_pointer_animation: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_animation_mode: typing.Optional[typing.Any] = "ACTIONS",
    export_nla_strips_merged_animation_name: typing.Union[
        str, typing.Any
    ] = "Animation",
    export_def_bones: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_hierarchy_flatten_bones: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = False,
    export_hierarchy_flatten_objs: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = False,
    export_armature_object_remove: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = False,
    export_leaf_bone: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_optimize_animation_size: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = True,
    export_optimize_animation_keep_anim_armature: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = True,
    export_optimize_animation_keep_anim_object: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = False,
    export_optimize_armature_disable_viewport: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = False,
    export_negative_frame: typing.Optional[typing.Any] = "SLIDE",
    export_anim_slide_to_zero: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_bake_animation: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_anim_single_armature: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_reset_pose_bones: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_current_frame: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_rest_position_armature: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = True,
    export_anim_scene_split_object: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = True,
    export_skins: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_influence_nb: typing.Optional[typing.Any] = 4,
    export_all_influences: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_morph: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_morph_normal: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_morph_tangent: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_morph_animation: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_morph_reset_sk_data: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_lights: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_try_sparse_sk: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_try_omit_sparse_sk: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_gpu_instances: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_action_filter: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_convert_animation_pointer: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = False,
    export_nla_strips: typing.Optional[typing.Union[bool, typing.Any]] = True,
    export_original_specular: typing.Optional[typing.Union[bool, typing.Any]] = False,
    will_save_settings: typing.Optional[typing.Union[bool, typing.Any]] = False,
    export_hierarchy_full_collections: typing.Optional[
        typing.Union[bool, typing.Any]
    ] = False,
    export_extra_animations: typing.Optional[typing.Union[bool, typing.Any]] = False,
    filter_glob: typing.Union[str, typing.Any] = "*.glb",
):
    """Export scene as glTF 2.0 file

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: typing.Union[str, typing.Any]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_import_convert_lighting_mode: Lighting Mode, Optional backwards compatibility for non-standard render engines. Applies to lights

    SPEC
    Standard -- Physically-based glTF lighting units (cd, lx, nt).

    COMPAT
    Unitless -- Non-physical, unitless lighting. Useful when exposure controls are not available.

    RAW
    Raw (Deprecated) -- Blender lighting strengths with no conversion.
        :type export_import_convert_lighting_mode: typing.Optional[typing.Any]
        :param gltf_export_id: Identifier, Identifier of caller (in case of add-on calling this exporter). Can be useful in case of Extension added by other add-ons
        :type gltf_export_id: typing.Union[str, typing.Any]
        :param export_use_gltfpack: Use Gltfpack, Use gltfpack to simplify the mesh and/or compress its textures
        :type export_use_gltfpack: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_gltfpack_tc: KTX2 Compression, Convert all textures to KTX2 with BasisU supercompression
        :type export_gltfpack_tc: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_gltfpack_tq: Texture Encoding Quality, Texture encoding quality
        :type export_gltfpack_tq: typing.Optional[typing.Any]
        :param export_gltfpack_si: Mesh Simplification Ratio, Simplify meshes targeting triangle count ratio
        :type export_gltfpack_si: typing.Optional[typing.Any]
        :param export_gltfpack_sa: Aggressive Mesh Simplification, Aggressively simplify to the target ratio disregarding quality
        :type export_gltfpack_sa: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_gltfpack_slb: Lock Mesh Border Vertices, Lock border vertices during simplification to avoid gaps on connected meshes
        :type export_gltfpack_slb: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_gltfpack_vp: Position Quantization, Use N-bit quantization for positions
        :type export_gltfpack_vp: typing.Optional[typing.Any]
        :param export_gltfpack_vt: Texture Coordinate Quantization, Use N-bit quantization for texture coordinates
        :type export_gltfpack_vt: typing.Optional[typing.Any]
        :param export_gltfpack_vn: Normal/Tangent Quantization, Use N-bit quantization for normals and tangents
        :type export_gltfpack_vn: typing.Optional[typing.Any]
        :param export_gltfpack_vc: Vertex Color Quantization, Use N-bit quantization for colors
        :type export_gltfpack_vc: typing.Optional[typing.Any]
        :param export_gltfpack_vpi: Vertex Position Attributes, Type to use for vertex position attributes

    Integer
    Integer -- Use integer attributes for positions.

    Normalized
    Normalized -- Use normalized attributes for positions.

    Floating-point
    Floating-point -- Use floating-point attributes for positions.
        :type export_gltfpack_vpi: typing.Optional[typing.Any]
        :param export_gltfpack_noq: Disable Quantization, Disable quantization; produces much larger glTF files with no extensions
        :type export_gltfpack_noq: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_format: Format, Output format. Binary is most efficient, but JSON may be easier to edit later
        :type export_format: typing.Optional[typing.Union[str, int, typing.Any]]
        :param ui_tab: ui_tab, Export setting categories

    GENERAL
    General -- General settings.

    MESHES
    Meshes -- Mesh settings.

    OBJECTS
    Objects -- Object settings.

    ANIMATION
    Animation -- Animation settings.
        :type ui_tab: typing.Optional[typing.Any]
        :param export_copyright: Copyright, Legal rights and conditions for the model
        :type export_copyright: typing.Union[str, typing.Any]
        :param export_image_format: Images, Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web applications due to the smaller file size. Alternatively they can be omitted if they are not needed

    AUTO
    Automatic -- Save PNGs as PNGs, JPEGs as JPEGs, WebPs as WebPs. For other formats, use PNG.

    JPEG
    JPEG Format (.jpg) -- Save images as JPEGs. (Images that need alpha are saved as PNGs though.) Be aware of a possible loss in quality.

    WEBP
    WebP Format -- Save images as WebPs as main image (no fallback).

    NONE
    None -- Don't export images.
        :type export_image_format: typing.Optional[typing.Any]
        :param export_image_add_webp: Create WebP, Creates WebP textures for every texture. For already WebP textures, nothing happens
        :type export_image_add_webp: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_image_webp_fallback: WebP fallback, For all WebP textures, create a PNG fallback texture
        :type export_image_webp_fallback: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_texture_dir: Textures, Folder to place texture files in. Relative to the .gltf file
        :type export_texture_dir: typing.Union[str, typing.Any]
        :param export_jpeg_quality: JPEG quality, Quality of JPEG export
        :type export_jpeg_quality: typing.Optional[typing.Any]
        :param export_image_quality: Image quality, Quality of image export
        :type export_image_quality: typing.Optional[typing.Any]
        :param export_keep_originals: Keep original, Keep original textures files if possible. WARNING: if you use more than one texture, where pbr standard requires only one, only one texture will be used. This can lead to unexpected results
        :type export_keep_originals: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_texcoords: UVs, Export UVs (texture coordinates) with meshes
        :type export_texcoords: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_normals: Normals, Export vertex normals with meshes
        :type export_normals: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_gn_mesh: Geometry Nodes Instances (Experimental), Export Geometry nodes instance meshes
        :type export_gn_mesh: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_draco_mesh_compression_enable: Draco mesh compression, Compress mesh using Draco
        :type export_draco_mesh_compression_enable: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_draco_mesh_compression_level: Compression level, Compression level (0 = most speed, 6 = most compression, higher values currently not supported)
        :type export_draco_mesh_compression_level: typing.Optional[typing.Any]
        :param export_draco_position_quantization: Position quantization bits, Quantization bits for position values (0 = no quantization)
        :type export_draco_position_quantization: typing.Optional[typing.Any]
        :param export_draco_normal_quantization: Normal quantization bits, Quantization bits for normal values (0 = no quantization)
        :type export_draco_normal_quantization: typing.Optional[typing.Any]
        :param export_draco_texcoord_quantization: Texcoord quantization bits, Quantization bits for texture coordinate values (0 = no quantization)
        :type export_draco_texcoord_quantization: typing.Optional[typing.Any]
        :param export_draco_color_quantization: Color quantization bits, Quantization bits for color values (0 = no quantization)
        :type export_draco_color_quantization: typing.Optional[typing.Any]
        :param export_draco_generic_quantization: Generic quantization bits, Quantization bits for generic values like weights or joints (0 = no quantization)
        :type export_draco_generic_quantization: typing.Optional[typing.Any]
        :param export_tangents: Tangents, Export vertex tangents with meshes
        :type export_tangents: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_materials: Materials, Export materials

    EXPORT
    Export -- Export all materials used by included objects.

    PLACEHOLDER
    Placeholder -- Do not export materials, but write multiple primitive groups per mesh, keeping material slot information.

    NONE
    No export -- Do not export materials, and combine mesh primitive groups, losing material slot information.
        :type export_materials: typing.Optional[typing.Any]
        :param export_unused_images: Unused images, Export images not assigned to any material
        :type export_unused_images: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_unused_textures: Prepare Unused textures, Export image texture nodes not assigned to any material. This feature is not standard and needs an external extension to be included in the glTF file
        :type export_unused_textures: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_colors: Dummy, Keep for compatibility only
        :type export_colors: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_attributes: Attributes, Export Attributes (when starting with underscore)
        :type export_attributes: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_mesh_edges: Loose Edges, Export loose edges as lines, using the material from the first material slot
        :type use_mesh_edges: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_mesh_vertices: Loose Points, Export loose points as glTF points, using the material from the first material slot
        :type use_mesh_vertices: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_cameras: Cameras, Export cameras
        :type export_cameras: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_selection: Selected Objects, Export selected objects only
        :type use_selection: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_visible: Visible Objects, Export visible objects only
        :type use_visible: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_renderable: Renderable Objects, Export renderable objects only
        :type use_renderable: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_active_collection_with_nested: Include Nested Collections, Include active collection and nested collections
        :type use_active_collection_with_nested: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_active_collection: Active Collection, Export objects in the active collection only
        :type use_active_collection: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_active_scene: Active Scene, Export active scene only
        :type use_active_scene: typing.Optional[typing.Union[bool, typing.Any]]
        :param collection: Source Collection, Export only objects from this collection (and its children)
        :type collection: typing.Union[str, typing.Any]
        :param export_extras: Custom Properties, Export custom properties as glTF extras
        :type export_extras: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_yup: +Y Up, Export using glTF convention, +Y up
        :type export_yup: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_apply: Apply Modifiers, Apply modifiers (excluding Armatures) to mesh objects -WARNING: prevents exporting shape keys
        :type export_apply: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_shared_accessors: Shared Accessors, Export Primitives using shared accessors for attributes
        :type export_shared_accessors: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_animations: Animations, Exports active actions and NLA tracks as glTF animations
        :type export_animations: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_frame_range: Limit to Playback Range, Clips animations to selected playback range
        :type export_frame_range: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_frame_step: Sampling Rate, How often to evaluate animated values (in frames)
        :type export_frame_step: typing.Optional[typing.Any]
        :param export_force_sampling: Always Sample Animations, Apply sampling to all animations
        :type export_force_sampling: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_pointer_animation: Export Animation Pointer (Experimental), Export material, Light & Camera animation as Animation Pointer
        :type export_pointer_animation: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_animation_mode: Animation mode, Export Animation mode

    ACTIONS
    Actions -- Export actions (actives and on NLA tracks) as separate animations.

    ACTIVE_ACTIONS
    Active actions merged -- All the currently assigned actions become one glTF animation.

    BROADCAST
    Broadcast actions -- Broadcast all compatible actions to all objects. Animated objects will get all actions compatible with them, others will get no animation at all.

    NLA_TRACKS
    NLA Tracks -- Export individual NLA Tracks as separate animation.

    SCENE
    Scene -- Export baked scene as a single animation.
        :type export_animation_mode: typing.Optional[typing.Any]
        :param export_nla_strips_merged_animation_name: Merged Animation Name, Name of single glTF animation to be exported
        :type export_nla_strips_merged_animation_name: typing.Union[str, typing.Any]
        :param export_def_bones: Export Deformation Bones Only, Export Deformation bones only
        :type export_def_bones: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_hierarchy_flatten_bones: Flatten Bone Hierarchy, Flatten Bone Hierarchy. Useful in case of non decomposable transformation matrix
        :type export_hierarchy_flatten_bones: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_hierarchy_flatten_objs: Flatten Object Hierarchy, Flatten Object Hierarchy. Useful in case of non decomposable transformation matrix
        :type export_hierarchy_flatten_objs: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_armature_object_remove: Remove Armature Object, Remove Armature object if possible. If Armature has multiple root bones, object will not be removed
        :type export_armature_object_remove: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_leaf_bone: Add Leaf Bones, Append a final bone to the end of each chain to specify last bone length (use this when you intend to edit the armature from exported data)
        :type export_leaf_bone: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_optimize_animation_size: Optimize Animation Size, Reduce exported file size by removing duplicate keyframes
        :type export_optimize_animation_size: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_optimize_animation_keep_anim_armature: Force keeping channels for bones, If all keyframes are identical in a rig, force keeping the minimal animation. When off, all possible channels for the bones will be exported, even if empty (minimal animation, 2 keyframes)
        :type export_optimize_animation_keep_anim_armature: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_optimize_animation_keep_anim_object: Force keeping channel for objects, If all keyframes are identical for object transformations, force keeping the minimal animation
        :type export_optimize_animation_keep_anim_object: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_optimize_armature_disable_viewport: Disable viewport if possible, When exporting armature, disable viewport for other objects, for performance. Drivers on shape keys for skined meshes prevent this optimization for now
        :type export_optimize_armature_disable_viewport: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_negative_frame: Negative Frames, Negative Frames are slid or cropped

    SLIDE
    Slide -- Slide animation to start at frame 0.

    CROP
    Crop -- Keep only frames above frame 0.
        :type export_negative_frame: typing.Optional[typing.Any]
        :param export_anim_slide_to_zero: Set all glTF Animation starting at 0, Set all glTF animation starting at 0.0s. Can be useful for looping animations
        :type export_anim_slide_to_zero: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_bake_animation: Bake All Objects Animations, Force exporting animation on every object. Can be useful when using constraints or driver. Also useful when exporting only selection
        :type export_bake_animation: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_anim_single_armature: Export all Armature Actions, Export all actions, bound to a single armature. WARNING: Option does not support exports including multiple armatures
        :type export_anim_single_armature: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_reset_pose_bones: Reset pose bones between actions, Reset pose bones between each action exported. This is needed when some bones are not keyed on some animations
        :type export_reset_pose_bones: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_current_frame: Use Current Frame as Object Rest Transformations, Export the scene in the current animation frame. When off, frame 0 is used as rest transformations for objects
        :type export_current_frame: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_rest_position_armature: Use Rest Position Armature, Export armatures using rest position as joints' rest pose. When off, current frame pose is used as rest pose
        :type export_rest_position_armature: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_anim_scene_split_object: Split Animation by Object, Export Scene as seen in Viewport, But split animation by Object
        :type export_anim_scene_split_object: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_skins: Skinning, Export skinning (armature) data
        :type export_skins: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_influence_nb: Bone Influences, Choose how many Bone influences to export
        :type export_influence_nb: typing.Optional[typing.Any]
        :param export_all_influences: Include All Bone Influences, Allow export of all joint vertex influences. Models may appear incorrectly in many viewers
        :type export_all_influences: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_morph: Shape Keys, Export shape keys (morph targets)
        :type export_morph: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_morph_normal: Shape Key Normals, Export vertex normals with shape keys (morph targets)
        :type export_morph_normal: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_morph_tangent: Shape Key Tangents, Export vertex tangents with shape keys (morph targets)
        :type export_morph_tangent: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_morph_animation: Shape Key Animations, Export shape keys animations (morph targets)
        :type export_morph_animation: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_morph_reset_sk_data: Reset shape keys between actions, Reset shape keys between each action exported. This is needed when some SK channels are not keyed on some animations
        :type export_morph_reset_sk_data: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_lights: Punctual Lights, Export directional, point, and spot lights. Uses "KHR_lights_punctual" glTF extension
        :type export_lights: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_try_sparse_sk: Use Sparse Accessor if better, Try using Sparse Accessor if it saves space
        :type export_try_sparse_sk: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_try_omit_sparse_sk: Omitting Sparse Accessor if data is empty, Omitting Sparse Accessor if data is empty
        :type export_try_omit_sparse_sk: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_gpu_instances: GPU Instances, Export using EXT_mesh_gpu_instancing. Limited to children of a given Empty. Multiple materials might be omitted
        :type export_gpu_instances: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_action_filter: Filter Actions, Filter Actions to be exported
        :type export_action_filter: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_convert_animation_pointer: Convert TRS/weights to Animation Pointer, Export TRS and weights as Animation Pointer. Using KHR_animation_pointer extension
        :type export_convert_animation_pointer: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_nla_strips: Group by NLA Track, When on, multiple actions become part of the same glTF animation if they're pushed onto NLA tracks with the same name. When off, all the currently assigned actions become one glTF animation
        :type export_nla_strips: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_original_specular: Export original PBR Specular, Export original glTF PBR Specular, instead of Blender Principled Shader Specular
        :type export_original_specular: typing.Optional[typing.Union[bool, typing.Any]]
        :param will_save_settings: Remember Export Settings, Store glTF export settings in the Blender project
        :type will_save_settings: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_hierarchy_full_collections: Full Collection Hierarchy, Export full hierarchy, including intermediate collections
        :type export_hierarchy_full_collections: typing.Optional[typing.Union[bool, typing.Any]]
        :param export_extra_animations: Prepare extra animations, Export additional animationsThis feature is not standard and needs an external extension to be included in the glTF file
        :type export_extra_animations: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_glob: filter_glob
        :type filter_glob: typing.Union[str, typing.Any]
    """

    ...

def x3d(
    override_context: typing.Optional[
        typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]
    ] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filepath: typing.Union[str, typing.Any] = "",
    check_existing: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_glob: typing.Union[str, typing.Any] = "*.x3d",
    use_selection: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_mesh_modifiers: typing.Optional[typing.Union[bool, typing.Any]] = True,
    use_triangulate: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_normals: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_compress: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_hierarchy: typing.Optional[typing.Union[bool, typing.Any]] = True,
    name_decorations: typing.Optional[typing.Union[bool, typing.Any]] = True,
    use_h3d: typing.Optional[typing.Union[bool, typing.Any]] = False,
    global_scale: typing.Optional[typing.Any] = 1.0,
    path_mode: typing.Optional[typing.Any] = "AUTO",
    axis_forward: typing.Optional[typing.Any] = "Z",
    axis_up: typing.Optional[typing.Any] = "Y",
):
    """Export selection to Extensible 3D file (.x3d)

        :type override_context: typing.Optional[typing.Union[typing.Dict[str, typing.Any], bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: typing.Union[str, typing.Any]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_glob: filter_glob
        :type filter_glob: typing.Union[str, typing.Any]
        :param use_selection: Selection Only, Export selected objects only
        :type use_selection: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_mesh_modifiers: Apply Modifiers, Use transformed mesh data from each object
        :type use_mesh_modifiers: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_triangulate: Triangulate, Write quads into 'IndexedTriangleSet'
        :type use_triangulate: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_normals: Normals, Write normals with geometry
        :type use_normals: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_compress: Compress, Compress the exported file
        :type use_compress: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_hierarchy: Hierarchy, Export parent child relationships
        :type use_hierarchy: typing.Optional[typing.Union[bool, typing.Any]]
        :param name_decorations: Name decorations, Add prefixes to the names of exported nodes to indicate their type
        :type name_decorations: typing.Optional[typing.Union[bool, typing.Any]]
        :param use_h3d: H3D Extensions, Export shaders for H3D
        :type use_h3d: typing.Optional[typing.Union[bool, typing.Any]]
        :param global_scale: Scale
        :type global_scale: typing.Optional[typing.Any]
        :param path_mode: Path Mode, Method used to reference paths

    AUTO
    Auto -- Use relative paths with subdirectories only.

    ABSOLUTE
    Absolute -- Always write absolute paths.

    RELATIVE
    Relative -- Always write relative paths (where possible).

    MATCH
    Match -- Match absolute/relative setting with input path.

    STRIP
    Strip Path -- Filename only.

    COPY
    Copy -- Copy the file to the destination path (or subdirectory).
        :type path_mode: typing.Optional[typing.Any]
        :param axis_forward: Forward
        :type axis_forward: typing.Optional[typing.Any]
        :param axis_up: Up
        :type axis_up: typing.Optional[typing.Any]
    """

    ...
