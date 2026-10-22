extends SceneTree
## Exercise the supplied rig through Godot's actual glTF importer, privately.

func _initialize() -> void:
	call_deferred("check_model")

func check_model() -> void:
	var args := OS.get_cmdline_user_args()
	assert(args.size() == 2, "Expected private GLB input and JSON report output")
	var state := GLTFState.new()
	var document := GLTFDocument.new()
	GLTFDocument.register_gltf_document_extension(GLTFDocumentExtensionConvertImporterMesh.new())
	assert(document.append_from_file(args[0], state) == OK, "glTF import failed")
	var scene := document.generate_scene(state)
	assert(scene != null, "No imported scene")
	root.add_child(scene)
	var skeletons: Array[Node] = scene.find_children("*", "Skeleton3D", true, false)
	var players: Array[Node] = scene.find_children("*", "AnimationPlayer", true, false)
	var meshes: Array[Node] = scene.find_children("*", "MeshInstance3D", true, false)
	assert(skeletons.size() == 1 and players.size() == 1)
	assert(meshes.size() >= 17, "Source body and modeled facial parts must import as runtime meshes")
	var skeleton: Skeleton3D = skeletons[0]
	var player: AnimationPlayer = players[0]
	assert(skeleton.get_bone_count() == 14)
	var clips := player.get_animation_list()
	var walk := ""
	for clip in clips:
		if clip != "RESET": walk = clip
	assert(not walk.is_empty(), "No walk imported")
	var animation := player.get_animation(walk)
	assert(animation.length > 1.0 and animation.length < 1.3)
	var coloured_surfaces := 0
	for mesh: MeshInstance3D in meshes:
		assert(mesh.mesh != null and mesh.skin != null)
		for surface in mesh.mesh.get_surface_count():
			var material := mesh.get_active_material(surface)
			assert(material != null)
			if material is BaseMaterial3D and material.vertex_color_use_as_albedo:
				coloured_surfaces += 1
	assert(coloured_surfaces > 0, "Continuous body colours were lost on import")
	var bone := skeleton.find_bone("LeftShin")
	assert(bone >= 0)
	var poses: Array[Quaternion] = []
	player.play(walk)
	for phase in [0.0, 0.25, 0.5, 0.75]:
		player.seek(phase * animation.length, true)
		skeleton.force_update_all_bone_transforms()
		for index in skeleton.get_bone_count():
			assert(skeleton.get_bone_global_pose(index).is_finite())
		poses.append(skeleton.get_bone_pose_rotation(bone))
	assert(poses[0].angle_to(poses[1]) > 0.02, "Walk did not move the skeleton")
	var report := {"input_sha256": FileAccess.get_sha256(args[0]),
		"engine": Engine.get_version_info().string, "skeletons": skeletons.size(),
		"bones": skeleton.get_bone_count(), "mesh_instances": meshes.size(),
		"colour_surfaces": coloured_surfaces, "animation": walk,
		"duration_seconds": animation.length, "sampled_phases": 4,
		"finite_bone_transforms": true, "animated_shin": true,
		"scope": "Actual Godot glTF import and animation evaluation; no game integration or final art approval"}
	var file := FileAccess.open(args[1], FileAccess.WRITE)
	assert(file != null)
	file.store_string(JSON.stringify(report, "  ") + "\n")
	print(JSON.stringify(report))
	quit(0)
