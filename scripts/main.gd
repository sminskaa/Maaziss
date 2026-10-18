extends Control
## Presentation only: all puzzle and narrative rules live in OpeningState.

const INK := Color("18232b")
const CREAM := Color("f5e7c9")
const GOLD := Color("efbf69")
const MUTED := Color("aebbb9")
const TEAL := Color("315c62")
const VERBS: Array[Dictionary] = [
	{"id": "give", "label": "Give"}, {"id": "pick_up", "label": "Pick up"}, {"id": "use", "label": "Use"},
	{"id": "inspect", "label": "Look at"}, {"id": "talk", "label": "Talk to"}, {"id": "pull", "label": "Pull"},
	{"id": "push", "label": "Push"}, {"id": "close", "label": "Close"}, {"id": "open", "label": "Open"},
]
const HOTSPOTS: Array[Dictionary] = [
	{"id": "sofa", "name": "The sofa", "rect": Rect2(55, 300, 350, 170)},
	{"id": "window", "name": "Painted window", "rect": Rect2(790, 70, 210, 210)},
	{"id": "desk", "name": "Desk & official notice", "rect": Rect2(1010, 280, 230, 170)},
	{"id": "front_door", "name": "Front door", "rect": Rect2(490, 75, 145, 290)},
	{"id": "sink", "name": "The washbasin", "rect": Rect2(40, 90, 180, 190)},
	{"id": "noticeboard", "name": "Odd-job noticeboard", "rect": Rect2(245, 65, 200, 175)},
]

var state := OpeningState.new()
var active_verb: String = "inspect"
var selected_item: String = ""
var show_hotspots: bool = false
var overlay: Control
var modal_previous_focus: Control
var narration: RichTextLabel
var action_label: Label
var location_note: Label
var inspect_button: Button
var verb_buttons: Dictionary = {}
var inventory_slots: Array[Button] = []
var inventory_pictures: Array[TextureRect] = []
var inventory_labels: Array[Label] = []
var walk_tween: Tween
var leaflet_button: Button
var strip_button: Button
var hotspots_button: Button
var hotspot_buttons: Array[Button] = []
var room_buttons: Array[Button] = []
var goal_label: Label
var narrator_text: String = ""
var completion_presented: bool = false
var actor: TextureRect
var status_markers: Control


func _ready() -> void:
	_build_theme()
	_build_room()
	_build_hud()
	_refresh()
	var opening: String = "They saw me. All three of them. I watched a man die by the bridge stairs and they let me walk away. I don't intend to be here when they reconsider. First: a way out. And that damned travel restriction."
	if FileAccess.file_exists("res://data/dialogue.json"):
		var content: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://data/dialogue.json"))
		if content is Dictionary and content.get("opening") is String:
			opening = content.opening
	_say(opening)
	inspect_button.grab_focus()


func _build_theme() -> void:
	var ui_theme := Theme.new()
	ui_theme.default_font_size = 18
	ui_theme.set_color("font_color", "Label", CREAM)
	ui_theme.set_color("default_color", "RichTextLabel", CREAM)
	ui_theme.set_color("font_color", "Button", CREAM)
	ui_theme.set_color("font_hover_color", "Button", Color.WHITE)
	ui_theme.set_color("font_focus_color", "Button", Color.WHITE)
	ui_theme.set_color("font_pressed_color", "Button", GOLD)
	ui_theme.set_stylebox("normal", "Button", _style(Color("263940"), Color("506166"), 1, 6))
	ui_theme.set_stylebox("hover", "Button", _style(Color("3b5559"), GOLD, 1, 6))
	ui_theme.set_stylebox("pressed", "Button", _style(Color("17363e"), GOLD, 2, 6))
	ui_theme.set_stylebox("focus", "Button", _style(Color.TRANSPARENT, GOLD, 3, 6))
	theme = ui_theme


func _build_room() -> void:
	var background := ColorRect.new()
	background.color = Color("39444c")
	_place(background, Rect2(0, 0, 1280, 540), self)
	if ResourceLoader.exists("res://assets/room.svg"):
		var room := TextureRect.new()
		room.texture = load("res://assets/room.svg")
		room.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		room.stretch_mode = TextureRect.STRETCH_SCALE
		room.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_place(room, Rect2(0, 0, 1280, 540), self)
	else:
		_build_fallback_room()
	var floor_target := Control.new()
	floor_target.name = "WalkableFloor"
	floor_target.mouse_default_cursor_shape = Control.CURSOR_CROSS
	_place(floor_target, Rect2(0, 350, 1280, 190), self)
	floor_target.gui_input.connect(_floor_input)
	floor_target.mouse_entered.connect(_show_walk_action)
	if ResourceLoader.exists("res://assets/maziss.svg"):
		actor = TextureRect.new()
		actor.texture = load("res://assets/maziss.svg")
		actor.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		actor.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		actor.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_place(actor, Rect2(565, 290, 150, 225), self)
	for index: int in HOTSPOTS.size():
		var spot: Dictionary = HOTSPOTS[index]
		var target := Button.new()
		target.name = "Hotspot_" + spot.id
		target.tooltip_text = "%s — click to %s; right-click to inspect" % [spot.name, active_verb]
		target.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		target.add_theme_stylebox_override("normal", StyleBoxEmpty.new())
		target.add_theme_stylebox_override("hover", _style(Color(0.95, 0.8, 0.43, 0.08), Color(0.95, 0.8, 0.43, 0.55), 2, 8))
		target.add_theme_stylebox_override("pressed", _style(Color(0.95, 0.8, 0.43, 0.12), GOLD, 2, 8))
		target.add_theme_font_size_override("font_size", 19)
		_place(target, spot.rect, self)
		target.pressed.connect(_on_hotspot.bind(spot.id))
		target.mouse_entered.connect(_show_action.bind(spot.name))
		target.mouse_exited.connect(_show_action.bind(""))
		target.focus_entered.connect(_show_action.bind(spot.name))
		target.gui_input.connect(_hotspot_input.bind(spot.id))
		hotspot_buttons.append(target)
		room_buttons.append(target)
	strip_button = _make_loose_hotspot("loose_strip", "Loose metal strip", Rect2(120, 423, 100, 35))
	leaflet_button = _make_loose_hotspot("leaflet", "Folded leaflet", Rect2(850, 241, 90, 43))
	status_markers = Control.new()
	status_markers.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_place(status_markers, Rect2(0, 0, 1280, 540), self)
	var location := Panel.new()
	location.add_theme_stylebox_override("panel", _style(Color(0.07, 0.12, 0.15, 0.94), Color("657268"), 1, 8))
	_place(location, Rect2(20, 14, 430, 45), self)
	_label("MAZISS'S APARTMENT", Rect2(14, 5, 295, 32), location, 20, CREAM)
	location_note = _label("The morning after", Rect2(462, 20, 500, 32), self, 18, CREAM)
	hotspots_button = _button("[H] Hotspots", Rect2(1056, 16, 200, 40), self, _toggle_hotspots)
	hotspots_button.tooltip_text = "Reveal every interactive area. Keyboard: H."


func _build_fallback_room() -> void:
	# Native import can start while optional art is still being prepared.
	for spot: Dictionary in HOTSPOTS:
		var object := Panel.new()
		object.add_theme_stylebox_override("panel", _style(Color("58646a"), Color("24323b"), 4, 6))
		_place(object, spot.rect, self)
		_label(spot.name, Rect2(8, 8, spot.rect.size.x - 16, 40), object, 20, CREAM)
	var floor_rect := ColorRect.new()
	floor_rect.color = Color("725c50")
	floor_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_place(floor_rect, Rect2(0, 474, 1280, 66), self)


func _build_hud() -> void:
	var hud := Panel.new()
	hud.add_theme_stylebox_override("panel", _style(INK, Color("b2915f"), 2, 0))
	_place(hud, Rect2(0, 540, 1280, 180), self)
	action_label = _label("LOOK AT", Rect2(22, 7, 1000, 27), hud, 18, GOLD)
	for index: int in VERBS.size():
		var entry: Dictionary = VERBS[index]
		var button := _button(entry.label, Rect2(20 + (index % 3) * 114, 42 + (index / 3) * 38, 108, 32), hud, _set_verb.bind(entry.id))
		verb_buttons[entry.id] = button
	inspect_button = verb_buttons.inspect
	for index: int in 3:
		var slot := _button("", Rect2(380 + index * 113, 42, 105, 79), hud, _inventory_click.bind(index))
		slot.name = "InventorySlot%d" % index
		slot.gui_input.connect(_inventory_input.bind(index))
		var picture := TextureRect.new()
		picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_place(picture, Rect2(16, 4, 73, 49), slot)
		var caption := _label("Empty", Rect2(2, 53, 101, 23), slot, 12, MUTED)
		caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		inventory_slots.append(slot)
		inventory_pictures.append(picture)
		inventory_labels.append(caption)
	_button("Bag", Rect2(380, 132, 61, 32), hud, _open_inventory)
	_button("Notebook", Rect2(447, 132, 107, 32), hud, _open_journal)
	_button("Save", Rect2(560, 132, 66, 32), hud, _save)
	_button("Load", Rect2(632, 132, 66, 32), hud, _load)
	_button("?", Rect2(706, 7, 32, 28), hud, _open_help)
	_button("Reset", Rect2(1119, 7, 137, 28), hud, _confirm_reset)
	goal_label = _label("FIND A WAY OUT", Rect2(22, 156, 335, 19), hud, 12, MUTED)
	narration = RichTextLabel.new()
	narration.name = "Narration"
	narration.bbcode_enabled = false
	narration.add_theme_font_size_override("normal_font_size", 19)
	narration.scroll_active = true
	narration.selection_enabled = true
	narration.mouse_filter = Control.MOUSE_FILTER_STOP
	_place(narration, Rect2(757, 43, 496, 122), hud)


func _make_loose_hotspot(id: String, title: String, rect: Rect2) -> Button:
	var button := _button("", rect, self, _on_hotspot.bind(id))
	button.name = "Hotspot_" + id
	button.add_theme_stylebox_override("normal", StyleBoxEmpty.new())
	button.tooltip_text = title
	button.gui_input.connect(_hotspot_input.bind(id))
	button.mouse_entered.connect(_show_action.bind(title))
	return button


func _verb_label(id: String) -> String:
	for entry: Dictionary in VERBS:
		if entry.id == id:
			return entry.label
	return id


func _inventory_input(event: InputEvent, index: int) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_RIGHT and index < state.inventory.size():
		_read_item(state.inventory[index])
		get_viewport().set_input_as_handled()


func _inventory_click(index: int) -> void:
	if index >= state.inventory.size():
		return
	var id: String = state.inventory[index]
	if active_verb == "inspect":
		_read_item(id)
	elif active_verb == "use" and not selected_item.is_empty():
		_say(state.combine_items(selected_item, id))
		selected_item = ""
		_refresh()
	elif active_verb == "give" or active_verb == "use":
		selected_item = id
		_refresh()
	else:
		_say("Choose Look at to examine this, or Use / Give to select it.")


func _show_walk_action() -> void:
	if action_label != null:
		action_label.text = "Walk to"


func _floor_input(event: InputEvent) -> void:
	if is_instance_valid(overlay):
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if is_instance_valid(actor):
			if walk_tween != null and walk_tween.is_valid():
				walk_tween.kill()
			var feet := Vector2(clampf(event.position.x, 75, 1205), clampf(event.position.y + 350, 495, 530))
			var destination := feet - Vector2(75, 225)
			actor.flip_h = destination.x < actor.position.x
			walk_tween = create_tween()
			walk_tween.tween_property(actor, "position", destination, actor.position.distance_to(destination) / 250.0)
			_show_walk_action()
		get_viewport().set_input_as_handled()


func _place(control: Control, rect: Rect2, parent: Node) -> void:
	parent.add_child(control)
	control.position = rect.position
	control.size = rect.size


func _style(fill: Color, border: Color, width: int, radius: int) -> StyleBoxFlat:
	var box := StyleBoxFlat.new()
	box.bg_color = fill
	box.border_color = border
	box.set_border_width_all(width)
	box.set_corner_radius_all(radius)
	box.content_margin_left = 12
	box.content_margin_right = 12
	box.content_margin_top = 7
	box.content_margin_bottom = 7
	return box


func _label(value: String, rect: Rect2, parent: Node, font_size: int = 20, color: Color = CREAM) -> Label:
	var control := Label.new()
	control.text = value
	control.add_theme_font_size_override("font_size", font_size)
	control.add_theme_color_override("font_color", color)
	control.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_place(control, rect, parent)
	return control


func _button(value: String, rect: Rect2, parent: Node, callback: Callable) -> Button:
	var control := Button.new()
	control.text = value
	control.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_place(control, rect, parent)
	control.pressed.connect(callback)
	if overlay == null:
		room_buttons.append(control)
	return control


func _show_action(target: String) -> void:
	if action_label == null:
		return
	var prefix: String = _verb_label(active_verb)
	if not selected_item.is_empty() and active_verb in ["use", "give"]:
		prefix = "%s %s %s" % [_verb_label(active_verb), OpeningState.item_name(selected_item), "to" if active_verb == "give" else "with"]
	action_label.text = prefix + ("  ›  " + target if not target.is_empty() else "  ·  MAZISS")


func _set_verb(verb: String) -> void:
	active_verb = verb
	if not verb in ["use", "give"]:
		selected_item = ""
	_refresh()


func _hotspot_input(event: InputEvent, id: String) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_RIGHT:
		_say(state.interact(id, "inspect"))
		_refresh()
		get_viewport().set_input_as_handled()


func _on_hotspot(id: String) -> void:
	_say(state.interact(id, active_verb, selected_item))
	if active_verb in ["use", "give"]:
		selected_item = ""
	_refresh()


func _say(value: String) -> void:
	narrator_text = value
	if narration != null:
		narration.text = value
		narration.scroll_to_line(0)


func _refresh() -> void:
	if inspect_button == null:
		return
	for id: String in verb_buttons:
		var button: Button = verb_buttons[id]
		button.add_theme_stylebox_override("normal", _style(TEAL if active_verb == id else Color("263940"), GOLD if active_verb == id else Color("506166"), 2 if active_verb == id else 1, 6))
	for index: int in inventory_slots.size():
		var slot: Button = inventory_slots[index]
		var filled: bool = index < state.inventory.size()
		slot.disabled = not filled
		var id: String = state.inventory[index] if filled else ""
		inventory_pictures[index].texture = load("res://assets/items/" + id + ".svg") if filled else null
		inventory_labels[index].text = OpeningState.item_name(id) if filled else "Empty"
		slot.tooltip_text = OpeningState.item_name(id) + " — right-click to look at" if filled else "Empty inventory slot"
		slot.add_theme_stylebox_override("normal", _style(TEAL if filled and selected_item == id else Color("263940"), GOLD if filled and selected_item == id else Color("506166"), 2, 6))
	strip_button.visible = not state.flags.strip_found
	leaflet_button.visible = state.flags.window_open and not state.flags.leaflet_collected
	hotspots_button.text = "[H] Hide hotspots" if show_hotspots else "[H] Hotspots"
	for index: int in hotspot_buttons.size():
		var target: Button = hotspot_buttons[index]
		target.text = HOTSPOTS[index].name if show_hotspots else ""
		target.add_theme_stylebox_override("normal", _style(Color(0.04, 0.08, 0.10, 0.35), Color(0.94, 0.75, 0.41, 0.7), 2, 8) if show_hotspots else StyleBoxEmpty.new())
		target.tooltip_text = "%s — click to %s; right-click to inspect" % [HOTSPOTS[index].name, active_verb]
	location_note.text = "A provisional plan. No guarantees." if state.flags.plan_formed else "The morning after  ·  Northeast district"
	goal_label.text = "PLAN FORMED · OPEN NOTEBOOK" if state.flags.plan_formed else "READ · RECOVER · THINK IT THROUGH"
	_show_action("")
	_refresh_markers()


func _refresh_markers() -> void:
	if status_markers == null:
		return
	for child: Node in status_markers.get_children():
		child.queue_free()
	if state.flags.window_open:
		var wind := _label("OPEN", Rect2(824, 83, 90, 26), status_markers, 14, Color("e9d7a8"))
		wind.add_theme_color_override("font_shadow_color", INK)
		wind.add_theme_constant_override("shadow_offset_x", 2)
		wind.add_theme_constant_override("shadow_offset_y", 2)
	if state.flags.window_open and not state.flags.leaflet_collected:
		var paper := Panel.new()
		paper.add_theme_stylebox_override("panel", _style(Color("f1d6a2"), Color("8a6546"), 2, 2))
		paper.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_place(paper, Rect2(854, 248, 76, 29), status_markers)
		_label("LEAFLET", Rect2(4, 4, 68, 20), paper, 12, INK)


func _toggle_hotspots() -> void:
	show_hotspots = not show_hotspots
	_refresh()


func _make_overlay(title: String) -> VBoxContainer:
	if walk_tween != null and walk_tween.is_valid():
		walk_tween.kill()
	var previous_focus: Control = modal_previous_focus if is_instance_valid(overlay) else get_viewport().gui_get_focus_owner()
	_close_overlay()
	modal_previous_focus = previous_focus
	overlay = Control.new()
	_place(overlay, Rect2(0, 0, 1280, 720), self)
	overlay.z_index = 20
	for button: Button in room_buttons:
		button.focus_mode = Control.FOCUS_NONE
	var shade := ColorRect.new()
	shade.color = Color(0.02, 0.04, 0.06, 0.82)
	_place(shade, Rect2(0, 0, 1280, 720), overlay)
	var panel := Panel.new()
	panel.add_theme_stylebox_override("panel", _style(INK, GOLD, 2, 12))
	_place(panel, Rect2(130, 65, 1020, 590), overlay)
	_label(title, Rect2(32, 19, 850, 46), panel, 29, GOLD)
	var close := _button("Close · Esc", Rect2(828, 24, 160, 37), panel, _close_overlay)
	close.grab_focus()
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.follow_focus = true
	_place(scroll, Rect2(32, 83, 956, 477), panel)
	var body := VBoxContainer.new()
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation", 15)
	scroll.add_child(body)
	_configure_modal_focus.call_deferred()
	return body


func _configure_modal_focus() -> void:
	if not is_instance_valid(overlay):
		return
	var focusable: Array[Button] = []
	for candidate: Node in overlay.find_children("*", "Button", true, false):
		if candidate is Button and candidate.focus_mode != Control.FOCUS_NONE:
			focusable.append(candidate)
	for index: int in focusable.size():
		var button: Button = focusable[index]
		button.focus_next = button.get_path_to(focusable[(index + 1) % focusable.size()])
		button.focus_previous = button.get_path_to(focusable[(index - 1 + focusable.size()) % focusable.size()])


func _body_text(body: VBoxContainer, value: String, font_size: int = 20, color: Color = CREAM) -> Label:
	var text_label := Label.new()
	text_label.text = value
	text_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text_label.add_theme_font_size_override("font_size", font_size)
	text_label.add_theme_color_override("font_color", color)
	text_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_child(text_label)
	return text_label


func _body_button(body: VBoxContainer, value: String, callback: Callable) -> Button:
	var control := Button.new()
	control.text = value
	control.custom_minimum_size.y = 46
	control.alignment = HORIZONTAL_ALIGNMENT_LEFT
	control.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	control.pressed.connect(callback)
	body.add_child(control)
	return control


func _close_overlay() -> void:
	if is_instance_valid(overlay):
		overlay.queue_free()
	overlay = null
	for button: Button in room_buttons:
		button.focus_mode = Control.FOCUS_ALL
	if is_instance_valid(modal_previous_focus) and modal_previous_focus in room_buttons:
		modal_previous_focus.grab_focus()
	elif is_instance_valid(inspect_button):
		inspect_button.grab_focus()
	modal_previous_focus = null


func _open_inventory() -> void:
	var body: VBoxContainer = _make_overlay("INVENTORY")
	_body_text(body, "Read an item, or select it to use on something in the room.", 18, MUTED)
	if state.inventory.is_empty():
		_body_text(body, "Empty pockets. The traditional beginning of a promising career.")
	for id: String in state.inventory:
		_body_text(body, OpeningState.item_name(id), 24, GOLD)
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 12)
		body.add_child(row)
		var read_button := Button.new()
		read_button.text = "Read / inspect"
		read_button.custom_minimum_size = Vector2(230, 42)
		row.add_child(read_button)
		read_button.pressed.connect(_read_item.bind(id))
		var select_button := Button.new()
		select_button.text = "Use this item"
		select_button.custom_minimum_size = Vector2(230, 42)
		row.add_child(select_button)
		select_button.pressed.connect(_select_item.bind(id))
	if not selected_item.is_empty():
		_body_button(body, "Put away selected item", _clear_selected_item)


func _read_item(id: String) -> void:
	var value: String = state.inspect_item(id)
	_say(value)
	_refresh()
	var body: VBoxContainer = _make_overlay(OpeningState.item_name(id).to_upper())
	_body_text(body, value)
	_body_button(body, "Back to inventory", _open_inventory)
	if id == "leaflet" or id == "travel_notice":
		_body_button(body, "Think it through in the notebook", _open_journal)


func _select_item(id: String) -> void:
	selected_item = id
	active_verb = "use"
	_close_overlay()
	_say("Selected: %s. Click an object or another inventory item to use it. Choose another verb to put it away." % OpeningState.item_name(id))
	_refresh()


func _clear_selected_item() -> void:
	selected_item = ""
	_refresh()
	_open_inventory()


func _open_journal() -> void:
	var body: VBoxContainer = _make_overlay("NOTEBOOK · FACTS BEFORE PANIC")
	_body_text(body, state.journal_text(), 19)
	if state.flags.plan_formed:
		_body_button(body, "View the end of this prototype", _open_completion)
	else:
		var choices: Array[Dictionary] = state.thought_choices()
		if choices.is_empty():
			_body_text(body, "Read the desk notice and recover/read the window leaflet. Then compare them here.", 19, GOLD)
		else:
			_body_text(body, "THINK IT THROUGH", 17, GOLD)
			for choice: Dictionary in choices:
				_body_button(body, choice.text, _choose_thought.bind(choice.id))


func _choose_thought(id: String) -> void:
	var value: String = state.choose_thought(id)
	_say(value)
	_refresh()
	if state.flags.plan_formed:
		_open_completion()
		return
	var body: VBoxContainer = _make_overlay("MAZISS · THINKING ALOUD")
	_body_text(body, value, 21)
	_body_button(body, "Keep thinking", _open_journal)


func _open_completion() -> void:
	completion_presented = true
	var body: VBoxContainer = _make_overlay("A DIRECTION. THAT WILL HAVE TO DO.")
	_body_text(body, "END OF THE FIRST-ROOM PROTOTYPE", 18, GOLD)
	_body_text(body, "The Morgrave job fair advertises paid work outside the city, transport included. Maziss plans to find where it leaves, learn what the guards check, and work out how to get aboard despite his pending scrap case.\n\nThe leaflet hasn't lifted his restriction. The killers are still out there. But he now has somewhere to begin.", 22)
	_body_text(body, "This playable slice ends inside the apartment. The wider city and the next part of the story are still to be built.", 18, MUTED)
	_body_button(body, "Keep exploring the apartment", _close_overlay)
	_body_button(body, "Save this progress", _save_from_overlay)
	_body_button(body, "Start again", _confirm_reset)


func _save() -> void:
	_say(OpeningSaveStore.save_game(state))


func _save_from_overlay() -> void:
	_close_overlay()
	_save()


func _load() -> void:
	_say(OpeningSaveStore.load_game(state))
	selected_item = ""
	_refresh()


func _confirm_reset() -> void:
	var body: VBoxContainer = _make_overlay("START THE ROOM AGAIN?")
	_body_text(body, "This resets the current room. Your stored save stays available until you explicitly save over it.")
	_body_button(body, "Start again from empty pockets", _reset)
	_body_button(body, "Keep my current progress", _close_overlay)


func _reset() -> void:
	state = OpeningState.new()
	selected_item = ""
	active_verb = "inspect"
	completion_presented = false
	_close_overlay()
	_refresh()
	_say("Last night's murder is not going to un-witness itself. Read the notice on the desk, find out what is caught in the window, and make a plan in the notebook.")


func _open_help() -> void:
	var body: VBoxContainer = _make_overlay("HOW TO PLAY")
	_body_text(body, "Choose a verb, then left-click an object. Right-click looks at an object without changing your selected verb. Click empty floor to walk there.\n\nUse Pick up for the loose metal beneath the sofa cushion. Use the metal strip with the window to free its catch; Open the window; Pick up the leaflet. Look at inventory items to read them.\n\nYour bag is shown as icons below the room. Choose Use or Give, then an item, then its target. Use one inventory item with another to try a combination. There are no NPCs in this room yet; Talk to and Give will be used in later scenes.\n\nThe notebook records what Maziss knows and offers thoughts when both documents have been read.", 20)
	_body_text(body, "KEYBOARD\nTab / Shift+Tab: move between buttons. Enter / Space: activate. I: inventory. J: notebook. H: reveal hotspots. Esc: close a panel. F1: this help.\n\nSave / Load use one local slot with a backup. Your game is not sent to a server. No sound or voices are included in this slice.", 18, MUTED)


func _unhandled_key_input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo:
		return
	match event.keycode:
		KEY_ESCAPE:
			_close_overlay()
		KEY_I:
			_open_inventory()
		KEY_J:
			_open_journal()
		KEY_H:
			_toggle_hotspots()
		KEY_F1:
			_open_help()
		_:
			return
	get_viewport().set_input_as_handled()
