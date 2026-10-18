# Open Maziss on Windows

This runs the existing apartment prototype in the free Godot editor. It is not a
standalone `.exe` installer. You do not need Python, Node, AI models, an API key or
an AI subscription to run this project.

## 1. Download Godot once

Use the standard **Godot 4.6.3 Windows 64-bit editor** for an Intel/AMD PC:

https://github.com/godotengine/godot-builds/releases/tag/4.6.3-stable

Under Assets, download `Godot_v4.6.3-stable_win64.exe.zip` and choose **Extract all**
in Windows File Explorer. Use the standard build, not the .NET/C# build. Keep the
extracted editor; Godot does not require an installer.

## 2. Download the project

Repository: https://github.com/sminskaa/Maaziss

Click **Code → Download ZIP**, then **Extract all**. A direct source download is:

https://github.com/sminskaa/Maaziss/archive/refs/heads/main.zip

Put the extracted folder somewhere convenient, such as Documents. Open it to find
`project.godot`, `scripts`, `assets` and `scenes`. Do not try to run inside the ZIP.
The workspace-produced source ZIP has an outer `Maziss` folder instead of GitHub's
`Maaziss-main`; both contain the same project entry point.

## 3. Import and play

1. Start the Godot editor executable from step 1.
2. In Project Manager, click **Import** and select the project's `project.godot` file.
3. Click **Import & Edit** (the wording can vary slightly) and allow resource import.
4. Press **F5**, or click **Run Project** in the upper right. F6 runs only a scene;
   F5 is the intended button here.

The project already selects Godot's Compatibility renderer. Once the editor and
source are downloaded, the game runs locally without an internet connection.

## What you should see

A placeholder illustrated apartment, Maziss, nine verb buttons and an inventory.
This runnable Godot room still uses the older SVG art and simple movement. The
approved painted artwork is under `art/proposals/`; the experimental painted walking
study is separate and has not been integrated or approved. No voice clips or music
are included yet. See [current status](PROJECT_STATUS.md).

Try clicking the floor, examining objects with right-click, searching the sofa with
Pick up, using the metal strip on the window, opening it and collecting the leaflet.
Read the leaflet and desk notice, then use Notebook to consider the Morgrave lead.
Save and Load use a local save slot. Esc closes an in-game panel; use the game
window's close button or Godot's Stop button to stop the running project.

## First check on your PC

- Confirm that the room opens and text/buttons fit the window.
- Walk, collect an item, save, close the game, run again and load it.
- After downloading everything, repeat a short play with internet disconnected.

Record issues at https://github.com/sminskaa/Maaziss/issues, using the bug template
or describe them in the project chat. Report the Windows version, Godot version,
what you clicked, expected behavior and what happened. Godot's Debugger/Output panel
can help if there is an error. You can attach a screenshot if useful.

Cloud checks use Linux Godot. Native Windows rendering, audio/device behavior and
this first-PC walkthrough still require your Windows test. A standalone Windows
export/installer is a later task, not part of this source handoff.

## Updating later

Download the new GitHub ZIP to a new folder to keep an easy fallback. For convenient
updates and branch review, the free GitHub Desktop app is optional; it is not needed
for this first run. Do not edit `.godot`, which Godot regenerates automatically.
