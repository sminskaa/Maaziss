# Sharing visual reviews from this workspace

## Current delivery checks

The owner reports that direct image tool output and links to the original screenshot
and newer HTML page did not display in the chat. Local browser rendering alone did
not demonstrate delivery through the owner's interface.

A concrete filesystem inconsistency was found: the newer review HTML was mode 0600,
while the older HTML page was mode 0644. Original screenshot directories also used
0700. These modes can prevent a file service running as another account from reading
or traversing them. This is a possible cause, not a confirmed diagnosis of the chat
backend, which is not available to the agent.

The public-to-review files under `visual-preview/` now use 0644 with a 0755 directory
and traversable parent directories. Private voice references, caches, and original
recordings are not made broadly readable as part of this fix. New preview generation
sets these modes explicitly instead of inheriting the restrictive process umask.

`tools/build_visual_review.py` writes JPEG delivery copies without changing the source
PNG images or their dimensions. Both images are embedded in a self-contained HTML
page, reduced from about 3.4 MB to about 657 KB. The main entry is
`visual-preview/index.html`; the named `maziss-style-review.html` remains available.
`apartment-cartoon.jpg` and `game-controls.jpg` are direct image alternatives.

Validation: both embedded JPEGs decode and render in Chromium, the HTML responds with
HTTP 200 in an internal test, there are no external network requests, files have the
expected read bits, and all parent directories have traversal bits. Actual rendering
in the owner's chat interface still requires owner confirmation. Do not report that
UI delivery is fixed on the strength of local browser checks alone.

## Updating the review

After producing a new art proposal or running the actual browser walkthrough:

```sh
python3 tools/build_visual_review.py
```

This optional delivery helper uses Pillow, already installed in this workspace. It is
not needed to run the game. Preview pages are excluded from both playable exports and
source bundles; no public website or external upload has been created.

Share the new index link or the direct JPEG. If the owner reports another failure,
record that evidence and investigate the file-delivery service or an explicitly agreed
hosting route; do not keep repeating unchanged links or assert that the owner can see
what the agent sees through an internal image tool.


## Continued owner feedback

The owner subsequently reported that images still do not appear. Inline chat image
delivery therefore remains unresolved. The owner clarified that the self-contained HTML page works and only images embedded
directly in chat fail. Use the HTML preview for subsequent visual reviews. Correct file
permissions and local rendering must not be presented as proof that chat rendering
works. The host chat interface is outside this game repository.

The revision-2 composition with Maziss has a distinct named HTML page to avoid
confusing it with a previously opened revision; the stable index is also updated.
