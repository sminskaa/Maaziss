# Embedded-media delivery report for ChatGPT/Codex support

## Confirmed compact HTML workaround — 18 October 2026

The owner reported that the new painted model review opened as literal HTML
source, while the separate web preview displayed a generic visualization error.
They confirmed older HTML reviews still displayed correctly. The new files were
about 10 MB (rendered frames) and 18 MB (live model), compared with roughly
2–2.5 MB for earlier working construction reviews. File size or content
compatibility is a hypothesis; the host's actual error and limit are unknown.

A compact alternative now packages the same verified rendered frames into a
307 KB H.264 video, with an embedded still comparison and native media controls.
The complete HTML is 850,346 bytes and requires no page scripts or WebGL. The
owner explicitly confirmed that this version displays correctly. This establishes
a working delivery route, not a repair of the platform's image renderer.

Current local review: `visual-preview/maziss-review-small.html`. A separate
image-only fallback, `visual-preview/maziss-review-picture.html`, is 79,016 bytes.
`python3 tools/build_compact_character_review.py` reproduces the compact video
review from retained `maziss-painted-rendered.html` frames. It needs installed
Playwright/Chromium and FFmpeg. Generated reviews and intermediate frames remain
private and ignored; original character art and motion are unchanged.

Browser checks confirmed video playback and seeking with page JavaScript enabled
and disabled, plus offline still decoding. These checks are separate from the
owner's successful panel check. Prefer compact reviews near or below 1 MB for
future delivery, while treating that target as a tested practice rather than an
official maximum. Larger live models can remain optional inspection artifacts.

## Observed behaviour

In this Codex conversation, images posted by the assistant appear as placeholders or
fail to display in chat. Workspace audio preview also previously reported unavailable,
and an archive preview reported unable to load. The user can view the same visual work
and use interactive examples through self-contained HTML files in the HTML panel.

The user reproduced the embedded-image failure in both Brave and Google Chrome,
reported as the latest versions. Exact version numbers and operating system have not
been supplied. The user currently has only this Codex conversation, so other Codex
sessions have not been tested. Brave and Chrome both use Chromium; this does not
constitute an independent browser-engine comparison.

## Reproduction and expected result

1. In the affected conversation, open an assistant-posted image or workspace image link.
2. Observe that the embedded image does not appear.
3. Open the HTML review containing the image: that route works for the user.

Expected: supported assistant image/media output should be visible, or the interface
should clearly state that inline delivery is unsupported and offer a working route.

## Checks already made by the project assistant

- Confirmed source images exist and decode.
- Confirmed self-contained HTML images and the interactive example render in Chromium.
- Corrected public review-file read permissions and directory traversal permissions.
- Reduced review payload size and retained source images.
- Tried image tool output and direct image links; owner still reports no inline images.

These checks do not verify or repair the host chat frontend, attachment service or
artifact delivery path. No frontend error logs, account-level investigation or platform
root cause are available to the project assistant. It is unknown whether this is a
product capability limitation, session-specific delivery issue or another platform bug.

## Next diagnostic step

Try a simple generated image in a new regular ChatGPT conversation. If it works there,
report that the issue appears specific to this Codex session/delivery route. If it also
fails there, ask support to investigate a broader account or media-delivery issue.
This does not require restarting or discarding the Maziss project.

Send this description through ChatGPT Help/support with the affected conversation
reference, browser/OS details and an example screenshot if support requests one. Do
not post credentials, session cookies or unredacted network captures in the project.
The assistant has not contacted support or sent this report externally.

Until the platform route is resolved, use the confirmed-working HTML panel for visual
and interactive deliverables. Do not describe it as a repair of inline chat images.
