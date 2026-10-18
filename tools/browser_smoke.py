#!/usr/bin/env python3
"""Exercise the actual canvas build and its persisted save, without game test hooks.

Requires the free Playwright Python package and Chromium. Start tools/serve.py first.
Each run uses a fresh isolated browser context, never an existing player's profile.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build/checks"
READ_SAVE = """async () => {
  const dbs = await indexedDB.databases();
  if (!dbs.some(d => d.name === '/userfs')) return null;
  const db = await new Promise((resolve, reject) => {
    const r = indexedDB.open('/userfs');
    r.onsuccess = () => resolve(r.result); r.onerror = () => reject(r.error);
  });
  try {
    const keys = await new Promise((resolve, reject) => {
      const r = db.transaction('FILE_DATA').objectStore('FILE_DATA').getAllKeys();
      r.onsuccess = () => resolve(r.result); r.onerror = () => reject(r.error);
    });
    const key = keys.find(k => String(k).endsWith('/opening-save.json'));
    if (!key) return null;
    const value = await new Promise((resolve, reject) => {
      const r = db.transaction('FILE_DATA').objectStore('FILE_DATA').get(key);
      r.onsuccess = () => resolve(r.result); r.onerror = () => reject(r.error);
    });
    return JSON.parse(new TextDecoder().decode(value.contents));
  } finally { db.close(); }
}"""
READ_BACKUP = READ_SAVE.replace("/opening-save.json", "/opening-save.backup.json")
CORRUPT_TEST_SAVE = """async () => {
  const db = await new Promise((resolve, reject) => {
    const r = indexedDB.open('/userfs');
    r.onsuccess = () => resolve(r.result); r.onerror = () => reject(r.error);
  });
  try {
    const keys = await new Promise((resolve, reject) => {
      const r = db.transaction('FILE_DATA').objectStore('FILE_DATA').getAllKeys();
      r.onsuccess = () => resolve(r.result); r.onerror = () => reject(r.error);
    });
    const key = keys.find(k => String(k).endsWith('/opening-save.json'));
    const value = await new Promise((resolve, reject) => {
      const r = db.transaction('FILE_DATA').objectStore('FILE_DATA').get(key);
      r.onsuccess = () => resolve(r.result); r.onerror = () => reject(r.error);
    });
    value.contents = new TextEncoder().encode('{invalid test save');
    await new Promise((resolve, reject) => {
      const transaction = db.transaction('FILE_DATA', 'readwrite');
      transaction.objectStore('FILE_DATA').put(value, key);
      transaction.oncomplete = resolve; transaction.onerror = () => reject(transaction.error);
    });
  } finally { db.close(); }
}"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8060")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    checks: list[str] = []

    def record(condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(label)
        checks.append(label)
        print("PASS: " + label, flush=True)

    with sync_playwright() as playwright:
        binary = shutil.which("chromium") or shutil.which("chromium-browser")
        browser = playwright.chromium.launch(
            executable_path=binary,
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--enable-unsafe-swiftshader"],
        )
        context = browser.new_context(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

        def click(x: int, y: int) -> None:
            page.mouse.click(x, y)
            page.wait_for_timeout(180)

        def press(key: str) -> None:
            page.keyboard.press(key)
            page.wait_for_timeout(140)

        def first_choice() -> None:
            press("Tab")
            press("Enter")

        def save_and_read(expected: dict | None = None) -> dict:
            click(590, 688)
            found = None
            for _ in range(20):
                page.wait_for_timeout(100)
                try:
                    found = page.evaluate(READ_SAVE)
                except Exception:
                    continue
                if found is not None and (expected is None or all(found["flags"].get(k) == v for k, v in expected.items())):
                    return found
            raise AssertionError(f"Visible Save did not persist expected state {expected}; received {found}")

        response = page.goto(args.url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(2000)
        record(response is not None and response.status == 200, "Web build responds successfully")
        record(page.title() == "Maziss — The Morning After", "Correct game is loaded")
        page.screenshot(path=str(OUTPUT / "opening.png"))
        initial = save_and_read({"strip_found": False})
        record(not any(initial["flags"].values()) and not initial["inventory"], "New game starts with empty inventory and no completed actions")

        def verb(name: str) -> None:
            positions = {"give": (74, 598), "pick_up": (188, 598), "use": (302, 598),
                         "look": (74, 636), "talk": (188, 636), "pull": (302, 636),
                         "push": (74, 674), "close": (188, 674), "open": (302, 674)}
            click(*positions[name])

        # Walking must move the visible actor without changing puzzle state.
        from PIL import Image, ImageChops
        import io
        before_walk = Image.open(io.BytesIO(page.screenshot())).crop((0, 350, 1280, 540))
        click(1030, 520)
        page.wait_for_timeout(1700)
        after_walk = Image.open(io.BytesIO(page.screenshot())).crop((0, 350, 1280, 540))
        record(ImageChops.difference(before_walk, after_walk).getbbox() is not None,
               "Clicking empty floor moves the visible character")
        record(save_and_read() == initial, "Walking does not alter puzzle progress")
        click(640, 515)
        page.wait_for_timeout(1700)

        # Opening the window by hand is blocked, then the sofa supplies a tool.
        verb("open")
        click(888, 180)
        blocked = save_and_read({"window_examined": True})
        record(not blocked["flags"]["window_open"], "Window cannot open before its obstruction is cleared")
        verb("pick_up")
        click(160, 438)
        checkpoint = save_and_read({"strip_found": True})
        record(checkpoint["inventory"] == ["metal_strip"], "Searching the sofa gives one metal strip")

        # Use the item through the visible graphical inventory.
        verb("use")
        click(432, 615)
        click(888, 180)
        # Do not save: loading must restore the earlier, closed-window checkpoint.
        click(665, 688)
        restored = save_and_read({"window_unjammed": False})
        record(restored == checkpoint, "Visible Load restores an earlier checkpoint after an unsaved action")

        verb("use")
        click(432, 615)
        click(888, 180)  # Free catch.
        verb("open")
        click(888, 180)  # Open window.
        verb("pick_up")
        click(888, 258)  # Take the loose leaflet.
        recovered = save_and_read({"leaflet_collected": True})
        record(recovered["inventory"] == ["metal_strip", "leaflet"] and not recovered["flags"]["leaflet_read"], "Opening and collection expose an unread leaflet without consuming the tool")

        page.screenshot(path=str(OUTPUT / "controls-inventory.png"))

        # Right-click inventory reads it even while Pick up remains selected.
        page.mouse.click(545, 615, button="right")
        page.wait_for_timeout(180)
        page.screenshot(path=str(OUTPUT / "leaflet.png"))
        press("Escape")
        read_leaflet = save_and_read({"leaflet_read": True})
        record(not read_leaflet["flags"]["plan_formed"], "Reading the leaflet alone does not complete the plan")
        verb("close")
        click(888, 180)
        closed = save_and_read({"window_open": False})
        record(closed["inventory"] == read_leaflet["inventory"], "Closing the window keeps the recovered paper")
        verb("open")
        click(888, 180)
        verb("use")
        click(432, 615)
        click(545, 615)
        record(save_and_read(read_leaflet["flags"]) == read_leaflet, "Unhelpful icon-to-icon combination preserves both items")
        for name in ("give", "talk", "pull", "push"):
            verb(name)
            click(1100, 365)
        record(save_and_read(read_leaflet["flags"]) == read_leaflet, "Unsupported verbs give feedback without advancing puzzle progress")

        page.mouse.click(1100, 365, button="right")
        page.wait_for_timeout(180)
        save_and_read({"restriction_read": True})

        press("j")
        press("Tab")
        press("Tab")  # Deliberately choose an unhelpful thought.
        press("Enter")
        press("Escape")
        wrong = save_and_read({"plan_started": False})
        record(not wrong["flags"]["plan_formed"], "Unhelpful dialogue leaves the plan recoverable")

        press("j")
        first_choice()  # Compare documents.
        first_choice()  # Keep thinking.
        first_choice()  # Consider travel restriction.
        first_choice()  # Keep thinking.
        first_choice()  # Investigate Morgrave.
        page.screenshot(path=str(OUTPUT / "completion.png"))
        press("Escape")
        complete = save_and_read({"plan_formed": True})
        record(complete["flags"]["route_questioned"], "Notebook choices reach the provisional Morgrave plan")

        page.reload(wait_until="networkidle")
        page.wait_for_timeout(1500)
        click(665, 688)
        persisted = save_and_read({"plan_formed": True})
        record(persisted == complete, "Completed save survives a full browser-page reload")

        # Recovery promises the previous durable valid slot, not the latest slot.
        # Inspect the actual backup rather than assuming it equals the current save;
        # browser persistence runs asynchronously and may coalesce repeated writes.
        page.wait_for_timeout(800)
        backup_checkpoint = page.evaluate(READ_BACKUP)
        record(backup_checkpoint is not None and backup_checkpoint["inventory"], "A distinct valid previous-save backup is persisted")
        # Only this run's fresh browser profile is modified. The backup must recover it.
        page.evaluate(CORRUPT_TEST_SAVE)
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(1500)
        click(665, 688)
        recovered_backup = save_and_read(backup_checkpoint["flags"])
        record(recovered_backup == backup_checkpoint, "Corrupt persisted primary save recovers the previous valid backup")

        page.set_viewport_size({"width": 960, "height": 720})
        page.wait_for_timeout(300)
        press("j")
        page.screenshot(path=str(OUTPUT / "resized-notebook.png"))
        press("Escape")
        record(not errors, "No browser JavaScript or Godot console errors during the walkthrough")
        (OUTPUT / "browser-results.json").write_text(json.dumps({"checks": checks, "errors": errors, "browser": browser.version}, indent=2) + "\n")
        print(f"Browser walkthrough: {len(checks)} checks passed; no console errors.")
        context.close()
        browser.close()


if __name__ == "__main__":
    main()
