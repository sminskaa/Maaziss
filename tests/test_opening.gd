extends SceneTree
## Standalone, dependency-free checks for the apartment's puzzle and save contract.
## Run after importing the project; see tests/README.md.

const StateScript = preload("res://scripts/game_state.gd")
const FLAG_NAMES: Array[String] = [
	"sofa_examined", "strip_found", "window_examined", "window_unjammed",
	"window_open", "leaflet_collected", "leaflet_read", "restriction_read",
	"plan_formed", "notice_collected", "plan_started", "route_questioned",
]
const ITEM_IDS: Array[String] = ["metal_strip", "leaflet", "travel_notice"]

var assertions := 0
var failures: Array[String] = []


func _initialize() -> void:
	_test_initial_state()
	_test_complete_walkthrough()
	_test_shortcuts_and_wrong_actions()
	_test_alternative_order_and_repeated_actions()
	_test_explicit_verbs()
	_test_save_roundtrips()
	_test_hostile_save_data()
	_test_deterministic_action_sequences()
	print("Opening tests: %d assertions, %d failures." % [assertions, failures.size()])
	for failure in failures:
		printerr("FAIL: " + failure)
	quit(0 if failures.is_empty() else 1)


func _check(condition: bool, label: String) -> void:
	assertions += 1
	if not condition:
		failures.append(label)


func _unchanged(state, before: Dictionary, label: String) -> void:
	_check(state.to_dict() == before, label)


func _fresh():
	return StateScript.new()


func _get_leaflet(state) -> void:
	state.interact("sofa", "pick_up")
	state.interact("window", "inspect")
	state.interact("window", "use", "metal_strip")
	state.interact("window", "open")
	state.interact("window", "pick_up")


func _read_documents(state) -> void:
	_get_leaflet(state)
	state.inspect_item("leaflet")
	state.interact("desk", "inspect")


func _finish_plan(state) -> void:
	_read_documents(state)
	state.choose_thought("compare_documents")
	state.choose_thought("check_restriction")
	state.choose_thought("investigate_morgrave")


func _test_initial_state() -> void:
	var state = _fresh()
	_check(state.inventory.is_empty(), "New game starts without puzzle items")
	_check(state.flags.size() == FLAG_NAMES.size(), "New game exposes the documented flags")
	for flag in FLAG_NAMES:
		_check(state.flags.has(flag) and state.flags[flag] == false,
			"New game flag is false: " + flag)
	_check(state.to_dict().get("version") == 1, "Save schema has an explicit version")


func _test_complete_walkthrough() -> void:
	var state = _fresh()
	_check(not state.interact("sofa", "inspect").is_empty(), "Looking at the sofa gives feedback")
	_check(state.flags.sofa_examined, "Looking marks sofa examined")
	_check(state.inventory.is_empty(), "Looking alone does not collect the strip")
	state.interact("sofa", "pick_up")
	_check(state.flags.strip_found and state.inventory.has("metal_strip"), "Searching sofa finds strip")
	state.interact("window", "inspect")
	_check(state.flags.window_examined, "Looking identifies the jammed window")
	state.interact("window", "use", "metal_strip")
	_check(state.flags.window_unjammed, "Owned strip releases window")
	_check(not state.flags.window_open, "Releasing window and opening it are separate actions")
	state.interact("window", "open")
	_check(state.flags.window_open, "Released window can be opened")
	_check(not state.inventory.has("leaflet"), "Opening window does not silently collect the leaflet")
	state.interact("window", "pick_up")
	_check(state.flags.leaflet_collected and state.inventory.has("leaflet"), "Visible leaflet can be collected")
	_check(not state.flags.leaflet_read, "Collecting the leaflet does not read it")
	state.inspect_item("leaflet")
	_check(state.flags.leaflet_read, "Inventory inspection reads the leaflet")
	_check(not state.flags.plan_formed, "Job advertisement alone is not an escape plan")
	state.interact("desk", "inspect")
	_check(state.flags.restriction_read, "Desk notice reveals the travel restriction")
	_check(not state.flags.plan_formed, "Reading both documents still requires the notebook reasoning")
	state.choose_thought("compare_documents")
	_check(state.flags.plan_started and not state.flags.plan_formed, "First thought compares the documents")
	state.choose_thought("check_restriction")
	_check(state.flags.route_questioned and not state.flags.plan_formed, "Second thought questions the restriction")
	_check(not state.choose_thought("investigate_morgrave").is_empty(), "Final thought explains the next lead")
	_check(state.flags.plan_formed, "Reasoning establishes Morgrave as a lead")
	var before: Dictionary = state.to_dict().duplicate(true)
	state.interact("front_door", "use")
	_unchanged(state, before, "Planning does not remove the restriction or leave the apartment")


func _test_shortcuts_and_wrong_actions() -> void:
	var state = _fresh()
	var before: Dictionary = state.to_dict().duplicate(true)
	for item in ITEM_IDS:
		state.inspect_item(item)
		_unchanged(state, before, "An unowned item cannot be read: " + item)
	for thought in ["compare_documents", "check_restriction", "investigate_morgrave"]:
		state.choose_thought(thought)
		_unchanged(state, before, "New game cannot skip directly to thought: " + thought)
	state.interact("window", "use")
	_check(not state.flags.window_unjammed and not state.flags.window_open,
		"Bare hands cannot bypass the jam")
	state.interact("window", "use", "metal_strip")
	_check(not state.flags.window_unjammed and state.inventory.is_empty(),
		"Naming an unowned strip cannot release the window")
	state.interact("sofa", "pick_up")
	before = state.to_dict().duplicate(true)
	for hotspot in ["sofa", "sink", "desk", "noticeboard", "front_door"]:
		state.interact(hotspot, "use", "metal_strip")
		_unchanged(state, before, "Wrong strip use is recoverable: " + hotspot)
	for thought in ["trust_leaflet", "buy_ticket", "wait_here", "ignore_case", "missing_thought"]:
		state.choose_thought(thought)
		_unchanged(state, before, "Wrong notebook choice preserves progress: " + thought)
	for action in [["missing_hotspot", "use", ""], ["sofa", "dance", ""],
		["window", "use", "res://scripts/game_state.gd"], ["sofa", "inspect", "unknown_item"]]:
		state.interact(action[0], action[1], action[2])
		_unchanged(state, before, "Unknown interaction cannot change puzzle data: " + str(action))
	_read_documents(state)
	before = state.to_dict().duplicate(true)
	state.choose_thought("investigate_morgrave")
	_unchanged(state, before, "Reading documents cannot skip the reasoning sequence")
	state.choose_thought("check_restriction")
	_unchanged(state, before, "Second thought requires the first thought")
	state.choose_thought("compare_documents")
	before = state.to_dict().duplicate(true)
	state.choose_thought("investigate_morgrave")
	_unchanged(state, before, "Final thought requires questioning the route first")


func _test_alternative_order_and_repeated_actions() -> void:
	var state = _fresh()
	state.interact("desk", "pick_up")
	_check(state.flags.notice_collected and state.flags.restriction_read,
		"Taking the desk notice also reveals its restriction")
	_check(state.inventory.has("travel_notice"), "Travel notice remains inspectable in inventory")
	state.choose_thought("compare_documents")
	_check(not state.flags.plan_started, "Restriction alone cannot start the plan")
	_get_leaflet(state)
	state.choose_thought("compare_documents")
	_check(not state.flags.plan_started, "An unread collected leaflet cannot start the plan")
	state.inspect_item("leaflet")
	state.choose_thought("compare_documents")
	state.choose_thought("check_restriction")
	state.choose_thought("investigate_morgrave")
	_check(state.flags.plan_formed, "Reading restriction before leaflet also completes the plan")
	# Finish optional observations before checking that repeats are idempotent.
	state.interact("sofa", "inspect")
	var before: Dictionary = state.to_dict().duplicate(true)
	for i in range(5):
		state.interact("sofa", "inspect")
		state.interact("sofa", "pick_up")
		state.interact("window", "inspect")
		state.interact("window", "use")
		state.interact("window", "use", "metal_strip")
		state.interact("desk", "inspect")
		state.interact("desk", "pick_up")
		for item in ITEM_IDS:
			state.inspect_item(item)
		for thought in ["compare_documents", "check_restriction", "investigate_morgrave"]:
			state.choose_thought(thought)
	_unchanged(state, before, "Repeated collection, inspection and thoughts do not reset or duplicate progress")
	_check(state.inventory.size() == 3, "Each of the three items appears exactly once")


func _test_explicit_verbs() -> void:
	var state = _fresh()
	state.interact("sofa", "use")
	_check(state.inventory.is_empty(), "Use does not silently pick up the metal strip")
	state.interact("loose_strip", "pick_up")
	state.interact("window", "use", "metal_strip")
	state.interact("window", "pick_up")
	_check(not state.flags.leaflet_collected, "Pick up cannot bypass opening the window")
	state.interact("window", "open")
	state.interact("window", "close")
	_check(state.flags.window_open, "Loose leaflet must be collected before closing the window")
	state.interact("leaflet", "pick_up")
	state.interact("window", "close")
	_check(not state.flags.window_open and state.inventory.has("leaflet"), "Close really shuts the window and preserves its collected paper")
	var restored = _fresh()
	_check(restored.load_dict(state.to_dict()), "Closed-window state with recovered leaflet is a valid save")
	state.interact("window", "open")
	state.interact("leaflet", "pick_up")
	_check(state.inventory.count("leaflet") == 1, "Reopening cannot duplicate the leaflet")
	var before: Dictionary = state.to_dict().duplicate(true)
	for verb in ["give", "talk", "push", "pull"]:
		state.interact("desk", verb, "metal_strip" if verb == "give" else "")
		_unchanged(state, before, "Unsupported room action remains safe: " + verb)
	state.combine_items("metal_strip", "leaflet")
	_unchanged(state, before, "Unhelpful inventory combination keeps both items")
	state.combine_items("metal_strip", "unknown")
	_unchanged(state, before, "Unowned inventory target cannot affect progress")


func _test_save_roundtrips() -> void:
	var state = _fresh()
	var snapshots: Array[Dictionary] = [state.to_dict().duplicate(true)]
	var actions: Array = [
		["sofa", "inspect", ""], ["sofa", "pick_up", ""],
		["window", "inspect", ""], ["window", "use", "metal_strip"],
		["window", "open", ""], ["window", "pick_up", ""], ["desk", "pick_up", ""],
	]
	for action in actions:
		state.interact(action[0], action[1], action[2])
		snapshots.append(state.to_dict().duplicate(true))
	state.inspect_item("leaflet")
	snapshots.append(state.to_dict().duplicate(true))
	for thought in ["compare_documents", "check_restriction", "investigate_morgrave"]:
		state.choose_thought(thought)
		snapshots.append(state.to_dict().duplicate(true))
	for i in range(snapshots.size()):
		var restored = _fresh()
		# The file format is JSON: this also checks JSON's numeric representation.
		var payload: Variant = JSON.parse_string(JSON.stringify(snapshots[i]))
		_check(restored.load_dict(payload), "Valid JSON save restores checkpoint %d" % i)
		_check(restored.to_dict() == snapshots[i], "Checkpoint %d survives a full save roundtrip" % i)
	var exported: Dictionary = state.to_dict()
	exported["flags"]["plan_formed"] = false
	exported["inventory"].clear()
	_check(state.flags.plan_formed and not state.inventory.is_empty(), "Exported save is a detached copy")
	var source: Dictionary = state.to_dict()
	var restored = _fresh()
	_check(restored.load_dict(source), "Valid source save is accepted")
	source["flags"]["plan_formed"] = false
	source["inventory"].clear()
	_check(restored.flags.plan_formed and not restored.inventory.is_empty(), "Loaded state does not alias the source payload")
	var resumed = _fresh()
	var midgame = _fresh()
	_get_leaflet(midgame)
	_check(resumed.load_dict(midgame.to_dict()), "A mid-puzzle save can be resumed")
	resumed.inspect_item("leaflet")
	resumed.interact("desk", "inspect")
	resumed.choose_thought("compare_documents")
	resumed.choose_thought("check_restriction")
	resumed.choose_thought("investigate_morgrave")
	_check(resumed.flags.plan_formed, "Resuming an intermediate save leaves the puzzle solvable")


func _reject_without_mutation(state, payload: Variant, label: String) -> void:
	var before: Dictionary = state.to_dict().duplicate(true)
	_check(not state.load_dict(payload), "Reject malformed save: " + label)
	_unchanged(state, before, "Rejected save preserves current progress: " + label)


func _test_hostile_save_data() -> void:
	var state = _fresh()
	_finish_plan(state)
	for payload in [null, true, 17, "not a dictionary", [], {}]:
		_reject_without_mutation(state, payload, "invalid root " + str(payload))
	for key in ["version", "flags", "inventory"]:
		var payload: Dictionary = state.to_dict().duplicate(true)
		payload.erase(key)
		_reject_without_mutation(state, payload, "missing field " + key)
	for version in [0, -1, 2, "1", true, 1.5]:
		var payload: Dictionary = state.to_dict().duplicate(true)
		payload.version = version
		_reject_without_mutation(state, payload, "unsupported version " + str(version))
	var extra: Dictionary = state.to_dict().duplicate(true)
	extra["script"] = "res://scripts/game_state.gd"
	_reject_without_mutation(state, extra, "unexpected top-level executable path")
	for invalid_flags in [null, [], "flags"]:
		var payload: Dictionary = state.to_dict().duplicate(true)
		payload.flags = invalid_flags
		_reject_without_mutation(state, payload, "flags must be a dictionary")
	for flag in FLAG_NAMES:
		var missing: Dictionary = state.to_dict().duplicate(true)
		missing.flags.erase(flag)
		_reject_without_mutation(state, missing, "missing flag " + flag)
		var bad_type: Dictionary = state.to_dict().duplicate(true)
		bad_type.flags[flag] = 1
		_reject_without_mutation(state, bad_type, "nonboolean flag " + flag)
	var unknown_flag: Dictionary = state.to_dict().duplicate(true)
	unknown_flag.flags["restriction_waived"] = true
	_reject_without_mutation(state, unknown_flag, "unknown flag cannot grant travel permission")
	for invalid_inventory in [null, {}, "metal_strip", ["unknown_item"], [17], [null],
		["metal_strip", "metal_strip"], ["res://scripts/game_state.gd"], ["../outside"],
		["x".repeat(65536)], ["leaflet"].duplicate() + ["leaflet"].duplicate()]:
		var payload: Dictionary = state.to_dict().duplicate(true)
		payload.inventory = invalid_inventory
		_reject_without_mutation(state, payload, "invalid or duplicate inventory entry")
	var oversized: Dictionary = state.to_dict().duplicate(true)
	oversized.inventory = []
	for i in range(256):
		oversized.inventory.append("metal_strip")
	_reject_without_mutation(state, oversized, "oversized inventory")
	# These contradictions would bypass prerequisites or make a legitimate item disappear.
	var contradictions: Array = [
		["strip_found", false], ["window_unjammed", false],
		["leaflet_collected", false], ["leaflet_read", false], ["restriction_read", false],
		["plan_started", false], ["route_questioned", false],
	]
	for contradiction in contradictions:
		var payload: Dictionary = state.to_dict().duplicate(true)
		payload.flags[contradiction[0]] = contradiction[1]
		_reject_without_mutation(state, payload, "inconsistent prerequisite " + contradiction[0])
	for item in ["metal_strip", "leaflet"]:
		var payload: Dictionary = state.to_dict().duplicate(true)
		payload.inventory.erase(item)
		_reject_without_mutation(state, payload, "collected item missing from inventory " + item)
	var forged_item: Dictionary = _fresh().to_dict()
	forged_item.inventory = ["leaflet"]
	_reject_without_mutation(state, forged_item, "inventory item without collected flag")
	var forged_plan: Dictionary = _fresh().to_dict()
	forged_plan.flags.plan_formed = true
	_reject_without_mutation(state, forged_plan, "completed plan without its evidence")


func _test_deterministic_action_sequences() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 41853
	var state = _fresh()
	var hotspots: Array[String] = ["sofa", "window", "desk", "sink", "noticeboard", "front_door", "unknown"]
	var thoughts: Array[String] = ["compare_documents", "check_restriction", "investigate_morgrave",
		"trust_leaflet", "buy_ticket", "wait_here", "ignore_case", "unknown"]
	for step in range(160):
		var before: Dictionary = state.to_dict().duplicate(true)
		match rng.randi_range(0, 3):
			0:
				state.interact(hotspots[rng.randi_range(0, hotspots.size() - 1)], "inspect")
			1:
				var item := "" if rng.randi_range(0, 1) == 0 else ITEM_IDS[rng.randi_range(0, 2)]
				var verbs: Array[String] = ["use", "pick_up", "open", "close", "give", "talk", "push", "pull"]
				state.interact(hotspots[rng.randi_range(0, hotspots.size() - 1)], verbs[rng.randi_range(0, verbs.size() - 1)], item)
			2:
				state.inspect_item(ITEM_IDS[rng.randi_range(0, 2)])
			3:
				state.choose_thought(thoughts[rng.randi_range(0, thoughts.size() - 1)])
		for flag in FLAG_NAMES:
			_check(flag == "window_open" or not before.flags[flag] or state.flags[flag], "Progress never reverses at action %d: %s" % [step, flag])
		for item in before.inventory:
			_check(state.inventory.has(item), "Actions cannot strand a collected item at step %d" % step)
		var restored = _fresh()
		_check(restored.load_dict(state.to_dict()), "Action sequence always produces a valid save at step %d" % step)
		_check(restored.to_dict() == state.to_dict(), "Action sequence state roundtrips at step %d" % step)
