class_name OpeningState
extends RefCounted
## Authoritative, deterministic state for the apartment opening.
## Content never supplies paths, expressions, or executable instructions.

const SCHEMA_VERSION: int = 1
const FLAG_NAMES: Array[String] = [
	"sofa_examined", "strip_found", "window_examined", "window_unjammed",
	"window_open", "leaflet_collected", "leaflet_read", "restriction_read",
	"plan_formed", "notice_collected", "plan_started", "route_questioned",
]
const ITEM_NAMES: Array[String] = ["metal_strip", "leaflet", "travel_notice"]
const HOTSPOT_NAMES: Array[String] = [
	"sofa", "window", "desk", "sink", "noticeboard", "front_door", "loose_strip", "leaflet",
]

var flags: Dictionary = {}
var inventory: Array[String] = []


func _init() -> void:
	for flag: String in FLAG_NAMES:
		flags[flag] = false


func interact(hotspot: String, verb: String, selected_item: String = "") -> String:
	if not hotspot in HOTSPOT_NAMES or not verb in ["inspect", "use", "give", "pick_up", "talk", "pull", "push", "close", "open"]:
		return "There is nothing useful to do that way."
	if not selected_item.is_empty() and not selected_item in inventory:
		return "I should acquire that before developing ambitions for it."
	if verb == "give":
		return "Choose something from my inventory first." if selected_item.is_empty() else "There's nobody there to give it to."
	if verb == "talk":
		return "Nobody there. I can supply both sides of the conversation, but it rarely gets me anywhere."
	if verb == "use" and not selected_item.is_empty():
		if hotspot == "window" and selected_item == "metal_strip":
			if not flags.window_unjammed:
				flags.window_examined = true
				flags.window_unjammed = true
				return "The strip slips under the catch. A crack of old paint, and it moves. Now I can open the window."
			return "The catch is already free. I can open the window by hand."
		return "I can't see a useful way to apply the %s to that." % item_name(selected_item).to_lower()
	if verb == "pick_up":
		match hotspot:
			"sofa", "loose_strip":
				flags.sofa_examined = true
				if flags.strip_found:
					return "Only crumbs left. I'll leave those for the next tenant."
				flags.strip_found = true
				inventory.append("metal_strip")
				return "A metal strip under the cushion. That explains my back."
			"window", "leaflet":
				if flags.leaflet_collected:
					return "The leaflet's already in my bag."
				if not flags.window_open:
					return "The paper is trapped in the window frame. I need to open it first."
				flags.leaflet_collected = true
				inventory.append("leaflet")
				return "Morgrave. Better read the rest."
			"desk":
				flags.restriction_read = true
				if not flags.notice_collected:
					flags.notice_collected = true
					inventory.append("travel_notice")
				return restriction_text()
		return "That can stay where it is."
	if verb == "open" or (verb == "use" and hotspot == "window"):
		if hotspot == "window":
			flags.window_examined = true
			if not flags.window_unjammed:
				return "The catch is painted stuck. Something thin and stiff might get under it."
			if flags.window_open:
				return "Already open."
			flags.window_open = true
			return "I open the window. A folded leaflet drops onto the inside sill." if not flags.leaflet_collected else "The window opens again."
		if hotspot == "front_door":
			return "The next part of the city isn't built yet. For now, I need a lead from this room." if not flags.plan_formed else "The Morgrave fair is my next lead. This prototype ends here."
		return "There's nothing there to open."
	if verb == "close":
		if hotspot == "window":
			if not flags.window_open:
				return "Already shut."
			if not flags.leaflet_collected:
				return "I'll pick up the loose leaflet first. No point trapping it again."
			flags.window_open = false
			return "I close the window. The city can manage without my attention for a minute."
		return "Already shut." if hotspot == "front_door" else "There's nothing there to close."
	if verb == "push" or verb == "pull":
		return "The window has a catch. Open it once the paint is cleared." if hotspot == "window" else "Nothing useful moves."
	match hotspot:
		"sofa", "loose_strip":
			flags.sofa_examined = true
			if flags.strip_found:
				return "Still lumpy. Apparently the metal wasn't its only problem."
			return "Something metallic under the cushion. That would explain my back."
		"window", "leaflet":
			flags.window_examined = true
			if flags.window_open:
				return "Fresh air. And a leaflet on the sill." if not flags.leaflet_collected else "Open. Nothing between me and the city except a regrettable drop."
			if flags.leaflet_collected:
				return "Closed again. The leaflet is in my bag."
			if flags.window_unjammed:
				return "The catch is free. Opening it should loosen that paper."
			return "Paint has sealed the catch. There's a folded leaflet trapped in the frame."
		"desk":
			flags.restriction_read = true
			return restriction_text()
		"noticeboard":
			return "Shelves, hinges, leaks. Payment in actual money preferred. Someone has added 'sober' beneath 'reliable'. I recognise the handwriting."
		"sink":
			return "I splash water on my face. Now I'm awake enough to appreciate the situation." if verb == "use" else "A washbasin and last night's cup. Neither smells particularly encouraging."
		"front_door":
			return "Three men saw me witness a murder. They didn't chase me. I'd prefer to be elsewhere if they change their minds."
	return "Nothing changes."


func combine_items(first: String, second: String) -> String:
	if first not in inventory or second not in inventory:
		return "I don't have both of those."
	if first == second:
		return "One is quite enough."
	return "Those don't fit together in any useful way. I'll keep them separate."


func inspect_item(id: String) -> String:
	if not id in inventory:
		return "I don't have that."
	match id:
		"metal_strip":
			return "A narrow, stiff metal strip with one blunt end. Useful for easing catches without breaking them. Less useful for paying rent."
		"leaflet":
			flags.leaflet_read = true
			return "MORGRAVE JOB FAIR\nPAID WORK OUTSIDE THE CITY. TRANSPORT INCLUDED. Early applicants welcome.\n\nOutside the city. Precisely where I'd like to be. It says nothing about travel restrictions or what the guards check. Compare it with the notice in my notebook."
		"travel_notice":
			flags.restriction_read = true
			return restriction_text()
	return "Nothing useful."


func choose_thought(choice_id: String) -> String:
	if flags.plan_formed:
		return "Find the Morgrave job fair. Learn where the transport leaves, what the guards check, and whether I can get aboard despite the restriction. No guarantees. Better than waiting here."
	if not flags.leaflet_read or not flags.restriction_read:
		return "I need to read both the leaflet and the travel notice before I can compare them."
	match choice_id:
		"compare_documents":
			flags.plan_started = true
			return "The notice says I have to stay in the city. The leaflet offers paid work outside it, with transport included. I need to find that transport. Preferably before three murderers find me."
		"check_restriction":
			if not flags.plan_started:
				return "First, put the two documents together. Wishful thinking is how I acquired the scrap case."
			flags.route_questioned = true
			return "The leaflet doesn't cancel the restriction. Fine. I need to know where the transport leaves and what anyone checks. A fine or a cell would be inconvenient; a knife would be conclusive."
		"investigate_morgrave":
			if not flags.route_questioned:
				return "Before deciding, I need to consider what the travel restriction means for this lead."
			flags.plan_formed = true
			return "Find the Morgrave job fair. Paid work outside the city, transport included: that could be my way out. Learn where it leaves, what the guards check, and how to get aboard despite the scrap case. No guarantee. But it's a plan, which is more than my sofa offered."
		"trust_leaflet":
			return "An advertisement can't cancel the case. If attractive printing did that, I'd have wallpapered the court by now. I need an actual way onto the transport."
		"buy_ticket":
			return "With what money? And a ticket would not answer the restriction. Start with information. It's occasionally free."
		"ignore_case":
			return "I'd happily ignore it. The guards may be less accommodating. Find out what they check before trusting my life to their inattention."
		"wait_here":
			return "The killers saw my face and let me walk away. Waiting for a knock would put an unpleasant amount of faith in their manners."
	return "That thought goes nowhere. Try putting the facts together."


func thought_choices() -> Array[Dictionary]:
	if flags.plan_formed:
		return []
	if not flags.leaflet_read or not flags.restriction_read:
		return []
	if not flags.plan_started:
		return [
			{"id": "compare_documents", "text": "Compare the leaflet with the travel notice."},
			{"id": "trust_leaflet", "text": "Surely an advertisement is permission enough?"},
			{"id": "buy_ticket", "text": "Buy a ticket and worry later."},
		]
	if not flags.route_questioned:
		return [
			{"id": "check_restriction", "text": "The ban still exists. What might stop me boarding?"},
			{"id": "ignore_case", "text": "Ignore the restriction. What's one more problem?"},
		]
	return [
		{"id": "investigate_morgrave", "text": "Find the Morgrave fair. Learn how to get onto that transport."},
		{"id": "wait_here", "text": "Stay in bed until this becomes someone else's problem."},
	]


func journal_text() -> String:
	var entries: Array[String] = [
		"LAST NIGHT\nThe bar threw me out. Across the street, by the bridge stairs, three men killed someone. They saw me. They let me go. Now it's morning. I need a way out before they change their minds.",
	]
	if flags.restriction_read:
		entries.append("THE PROBLEM\nThe illegal-scrapping administrative case is still pending. The notice says I have to stay in the city. I care rather more about staying alive.")
	else:
		entries.append("FIRST THINGS FIRST\nThere's an official notice on the desk. I ought to read it before choosing my next mistake.")
	if flags.leaflet_read:
		entries.append("A LEAD\nThe Morgrave job fair advertises paid work outside the city, transport included. It says nothing about my restriction. Find out where the transport leaves and what gets checked.")
	elif flags.leaflet_collected:
		entries.append("UNREAD\nThe leaflet is in my inventory. Advertising works better when opened. Allegedly.")
	elif flags.window_open:
		entries.append("ON THE SILL\nThe leaflet fell inside when I opened the window. Pick it up.")
	elif flags.window_unjammed:
		entries.append("THE WINDOW\nThe catch is free. Open it by hand to loosen the paper above the frame.")
	elif flags.window_examined:
		entries.append("THE WINDOW\nA leaflet is caught above the frame. The painted catch needs a thin, stiff tool.")
	if flags.plan_formed:
		entries.append("PROVISIONAL PLAN\nFind the Morgrave job fair. Learn where its transport leaves, what the guards check, and how to get aboard despite the pending scrap case. The advertisement is a lead, not a guarantee.")
	return "\n\n".join(entries)


func to_dict() -> Dictionary:
	return {"version": SCHEMA_VERSION, "flags": flags.duplicate(true), "inventory": inventory.duplicate()}


func load_dict(data: Variant) -> bool:
	# Validate into temporary values; any rejection leaves this object unchanged.
	if not data is Dictionary or data.size() != 3:
		return false
	if not data.has_all(["version", "flags", "inventory"]):
		return false
	if typeof(data.version) not in [TYPE_INT, TYPE_FLOAT] or data.version != SCHEMA_VERSION:
		return false
	if not data.flags is Dictionary or data.flags.size() != FLAG_NAMES.size():
		return false
	for name: String in FLAG_NAMES:
		if not data.flags.has(name) or typeof(data.flags[name]) != TYPE_BOOL:
			return false
	if not data.inventory is Array or data.inventory.size() > ITEM_NAMES.size():
		return false
	var next_inventory: Array[String] = []
	for value: Variant in data.inventory:
		if not value is String or not value in ITEM_NAMES or value in next_inventory:
			return false
		next_inventory.append(value)
	var next_flags: Dictionary = data.flags
	if next_flags.strip_found != ("metal_strip" in next_inventory):
		return false
	if next_flags.leaflet_collected != ("leaflet" in next_inventory):
		return false
	if next_flags.notice_collected != ("travel_notice" in next_inventory):
		return false
	if next_flags.strip_found and not next_flags.sofa_examined:
		return false
	if next_flags.window_unjammed and (not next_flags.strip_found or not next_flags.window_examined):
		return false
	if next_flags.window_open and not next_flags.window_unjammed:
		return false
	if next_flags.leaflet_collected and not next_flags.window_unjammed:
		return false
	if next_flags.leaflet_read and not next_flags.leaflet_collected:
		return false
	if next_flags.notice_collected and not next_flags.restriction_read:
		return false
	if next_flags.plan_started and (not next_flags.leaflet_read or not next_flags.restriction_read):
		return false
	if next_flags.route_questioned and not next_flags.plan_started:
		return false
	if next_flags.plan_formed and not next_flags.route_questioned:
		return false
	flags = next_flags.duplicate(true)
	inventory = next_inventory
	return true


static func item_name(id: String) -> String:
	match id:
		"metal_strip":
			return "Metal strip"
		"leaflet":
			return "Morgrave leaflet"
		"travel_notice":
			return "Travel notice"
	return "Unknown item"


static func restriction_text() -> String:
	return "NOTICE OF TRAVEL RESTRICTION\nPending administrative case: illegal scrapping. The subject must remain within the city pending resolution of the case.\n\nStill pending. Of course. A person can die waiting for a form; the form itself enjoys excellent health."
