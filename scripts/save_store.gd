class_name OpeningSaveStore
extends RefCounted
## One fixed save slot. No save-supplied resource paths or object decoding.

const SAVE_PATH: String = "user://opening-save.json"
const BACKUP_PATH: String = "user://opening-save.backup.json"
const TEMP_PATH: String = "user://opening-save.pending.json"
const MAX_BYTES: int = 16384


static func save_game(state: OpeningState) -> String:
	var check := OpeningState.new()
	var payload: Dictionary = state.to_dict()
	if not check.load_dict(payload):
		return "Save refused: the current state did not pass validation."
	var encoded: String = JSON.stringify(payload, "\t")
	if encoded.to_utf8_buffer().size() > MAX_BYTES:
		return "Save refused: the save would exceed its size limit."
	var file := FileAccess.open(TEMP_PATH, FileAccess.WRITE)
	if file == null:
		return "Could not write the save. Your current progress is still here."
	file.store_string(encoded)
	file.flush()
	var write_error: Error = file.get_error()
	file.close()
	if write_error != OK:
		DirAccess.remove_absolute(TEMP_PATH)
		return "Could not finish writing the save. The previous save was kept."
	# Keep a verified previous slot before atomically replacing the active slot.
	if FileAccess.file_exists(SAVE_PATH):
		var previous: Dictionary = _read_validated(SAVE_PATH)
		if previous.get("ok", false):
			var backup_error: Error = DirAccess.copy_absolute(SAVE_PATH, BACKUP_PATH)
			if backup_error != OK:
				DirAccess.remove_absolute(TEMP_PATH)
				return "Could not preserve the previous save. Save cancelled."
	var rename_error: Error = DirAccess.rename_absolute(TEMP_PATH, SAVE_PATH)
	if rename_error != OK:
		DirAccess.remove_absolute(TEMP_PATH)
		return "Could not replace the save. The previous save was kept."
	return "Game saved on this device. Browser storage can be cleared; this prototype has one save slot."


static func load_game(state: OpeningState) -> String:
	var result: Dictionary = _read_validated(SAVE_PATH)
	if result.get("ok", false):
		state.load_dict(result.data)
		return "Game loaded."
	var backup: Dictionary = _read_validated(BACKUP_PATH)
	if backup.get("ok", false):
		state.load_dict(backup.data)
		return "The main save was unavailable or invalid. Restored the previous valid backup."
	return "No valid save was found. Your current progress has been kept."


static func _read_validated(path: String) -> Dictionary:
	if path not in [SAVE_PATH, BACKUP_PATH]:
		return {"ok": false}
	if not FileAccess.file_exists(path):
		return {"ok": false}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {"ok": false}
	var size: int = file.get_length()
	if size <= 0 or size > MAX_BYTES:
		file.close()
		return {"ok": false}
	var source: String = file.get_as_text()
	file.close()
	var parsed := JSON.new()
	if parsed.parse(source) != OK:
		return {"ok": false}
	var candidate := OpeningState.new()
	if not candidate.load_dict(parsed.data):
		return {"ok": false}
	return {"ok": true, "data": candidate.to_dict()}
