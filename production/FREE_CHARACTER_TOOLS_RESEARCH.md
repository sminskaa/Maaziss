# Free tools for rebuilding Maziss from the approved drawings

Research date: 18 October 2026. Assignment: RESEARCH-003. This is a source review,
not an installation or quality benchmark. Official READMEs, licenses and public
documentation were fetched and read. No model weights were downloaded, no hosted
generation was submitted, no account was created, and no training videos were
watched. Access results and source copies are retained privately under
`build/checks/character-rebuild/research/free-tools-sources.json` and adjacent files.

## Recommendation for this workspace

Use Blender to **model the recognizable design first**, then unwrap and paint
materials for that geometry. Preserve the approved drawings as visual references.
An existing generic body and a repeated image projection do not establish likeness.
Image-to-3D tools can provide a rough volume proposal, but their generation claim
does not establish that Maziss's face, clothing construction, joints or unseen
surfaces will be correct.

The present workspace exposes five logical CPUs and approximately 33.3 GiB RAM.
It has Blender 4.3.2, but no `nvidia-smi`, `/dev/nvidia*` or `/dev/dri` devices.
This is evidence that an accessible CUDA GPU was not found; it is not a benchmark.
Blender CPU modeling/rendering and scripting are already usable. GPU-dependent
image-to-3D stacks are not a practical prerequisite for the next likeness study.

| Tool | Free use and access actually checked | Hardware and practical value here |
| --- | --- | --- |
| Blender | Existing installation. Core modeling, sculpting, UV editing, texture painting, rigging and rendering require no paid add-on or hosted account. | CPU-capable. Best immediate tool for a deliberately designed, editable model. New head/body proportions and recognizable features must be established before applying paint. |
| [MPFB / MakeHuman](https://github.com/makehumancommunity/mpfb2) | Free Blender human generator. GPLv3 source; bundled base meshes, targets, clothes, rigs and textures are CC0. The project explicitly disclaims ownership over combined output. Individually downloaded community assets may have their own terms. | MPFB 2.x requires Blender >=4.2, compatible with this 4.3.2 installation by version. Useful anatomical/topological starting point, not a likeness converter. A realistic default human would still need substantial Maziss-specific stylization. Not installed in this assignment. |
| [TripoSR](https://github.com/VAST-AI-Research/TripoSR) | Official README explicitly says MIT covers source code, pretrained models and demo. This is distinct from any separately offered commercial Tripo service. No hosted account is needed for the repository's local workflow. | README states default single-image inference uses approximately 6 GB VRAM. Official `run.py` explicitly falls back to CPU when CUDA is unavailable. A CPU experiment is technically possible, but runtime and quality are unmeasured here. Output would require inspection, topology work, separate clothing and rigging; not a guaranteed replacement for modeling. |
| [Stable Fast 3D](https://github.com/Stability-AI/stable-fast-3d) | Community License, not MIT. Free research/hobby evaluation; commercial use includes registration and an annual revenue threshold of US $1 million. Weights are gated: official instructions require Hugging Face login, access request and a read token. Direct model-card request returned HTTP 401 in this workspace. | Official README explicitly supports CPU and automatic fallback; GPU default is approximately 6 GB VRAM. Predicts UV-unwrapped textured meshes and materials, an actual reconstruction alternative to our rejected projection. CPU feasibility in principle, but no runtime/likeness benchmark performed. Not selected as a dependency because it adds gated access and setup before any demonstrated identity benefit. |
| [TRELLIS](https://github.com/microsoft/TRELLIS) | Main models and most code MIT; README lists separately licensed renderer/FlexiCubes components. Repository access is free; that does not supply free GPU hosting. | Official requirements: NVIDIA GPU with at least 16 GB memory and CUDA toolkit; Linux verified. No suitable GPU found here. Not selected for this workspace. |
| [Hunyuan3D 2.0](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) | The specific fetched 2.0 Community License explicitly excludes the EU, UK and South Korea, including use/display of outputs outside its territory. This cannot be described as unrestricted free use for a European project. Other versions would need their own license review. | Official README states 6 GB VRAM for shape, 16 GB for shape plus texture. Hardware and this version's territory restrictions make it unsuitable for this project. Not downloaded or used. |
| [Instant Meshes](https://github.com/wjakob/instant-meshes) | Free source and Windows/macOS/Linux binaries. Actual `LICENSE.txt` is a BSD-style three-clause license. | Surface remesher, **not** image-to-3D or a character designer. Useful after a sculpt for cleaner surface flow; joint/face loops still need deliberate review. CPU application; no generative GPU inference requirement documented. |
| [QuadriFlow](https://github.com/hjwdzh/QuadriFlow) | Free source. README calls the license MIT, but the linked `LICENSE.txt` actually contains BSD-style three-clause conditions; use the license text rather than repeating that README label. Blender also has a QuadriFlow remesh workflow. | Remeshes existing geometry. Does not create missing likeness, UVs or articulation automatically. Do not remesh a finished skinned character expecting rig, texture layout and facial edge loops to survive unchanged. |
| [Krita](https://krita.org/en/about/license/) | GPLv3 application; official license page expressly allows creation of commercial work. No paid subscription required for the direct application. | Optional companion for deliberately painting UV islands, turnarounds and reference sheets. It does not infer a complete rigged model from one picture. Not installed in this assignment. |

## Useful public learning material, with the access limits made clear

[Blender Studio: Stylized Character Workflow](https://studio.blender.org/training/stylized-character-workflow/)
has a public course overview and some explicitly marked free introductory lessons.
The overview describes design, sculpting and retopology, followed by UV unwrapping,
shading and presentation. It lists a subscription price for full course access.
Therefore the full course is **not** a zero-budget resource to promise the owner.
The public outline nevertheless confirms the geometry-first production stages.
Only the public overview was read; paid lessons and their videos were not accessed.

[Blender Studio: Snow](https://studio.blender.org/characters/snow/) is listed as a
free stylized character rig with a CC-BY license. Its public page describes it as a
resource for learning and practicing animation. The page is useful for studying
what a finished, coherent stylized rig looks like; it is not Maziss and should not
replace his design. The download was not fetched or incorporated. The generic
character page worked; a direct `/v2/` request returned HTTP 403. Attribution would
be required if this asset were used, under the exact attached license version.

## Proposed production sequence and visual acceptance checks

1. **Design registration.** Put front, side and three-quarter references next to
   orthographic cameras. Establish matching head, chin, eyes, shoulders, belt, knees
   and sole heights. A sprite's pose and painterly perspective are references, not
   automatically consistent engineering drawings; resolve disagreement explicitly.
2. **Recognizable geometry without projected art.** Build skull, cheeks, jaw,
   nose, ear placement, eyelids, brows and hair silhouette to match Maziss. Match
   his head/body ratio, narrow shoulders, slight stoop and large work boots. Compare
   neutral-color front, profile and three-quarter renders against the original.
   Face identity and silhouette must read before texture detail can help.
3. **Complete clothing construction.** Make shirt, jacket, continuous trousers,
   boots, belt, strap and bag coherent surfaces with modeled thickness or seam
   overlaps. Hidden cloth and body regions must exist where animation reveals
   them. Preserve useful existing FBX motion separately from the rejected material.
4. **Animation topology and weights.** Put edge loops and enough geometry around
   knees, hips, elbows and shoulders to bend predictably. A generic remesher cannot
   choose all animation loops. Review rest pose, contact, passing and maximum bend;
   keep bag clearance and correct front/back ordering under the actual camera.
5. **Deliberate UV layout.** Place seams in low-visibility areas and unwrap the
   actual head and garments into separate named material regions. The face belongs
   once on the face region. It must not wrap onto ears, temples, hair or the back
   of the head. Keep enough area for eyes/mouth and avoid uncontrolled mirrored
   overlap where asymmetry matters.
6. **Paint for the model.** Recreate the approved palette, ink, cloth texture,
   folds and scuffs on those UV regions, using the original as art direction.
   Controlled single-view projection can seed a matching visible region, followed
   by seam cleanup and painting hidden areas. Projecting a complete dressed sprite
   repeatedly over a mismatched body is not a substitute for these steps.
7. **Shading and delivery.** Tune outlines, soft bands/highlights and surface detail
   against the approved room. Render real model turntables and short FBX-driven
   walks into compact HTML reviews with still/video fallback. Owner approval of
   likeness remains a visual decision, separate from geometric tests passing.

This is an achievable direction, not a claim that a first reconstruction already
matches the drawings. No internet resource makes a faithful multi-angle character
automatic, and no downloaded tool was run in this research assignment.

## Source evidence excerpts

All following sources were actually fetched on the research date; line references
refer to those retained snapshots, not immutable upstream versions.

- [TripoSR README](https://raw.githubusercontent.com/VAST-AI-Research/TripoSR/main/README.md),
  line 27: “The model is released under the MIT license, which includes the source
  code, pretrained models, and an interactive online demo.” Line 41: “6GB VRAM”.
  [Official runner](https://raw.githubusercontent.com/VAST-AI-Research/TripoSR/main/run.py),
  lines 117–119: when `torch.cuda.is_available()` is false, `device = "cpu"`.
- [SF3D README](https://raw.githubusercontent.com/Stability-AI/stable-fast-3d/main/README.md),
  lines 41–47 explain gated access/login; lines 69–73 explain CPU support;
  line 80 states 6 GB VRAM. [License](https://raw.githubusercontent.com/Stability-AI/stable-fast-3d/main/LICENSE.md),
  Section III requires registration for commercial use and sets the revenue
  threshold. Output ownership and derivative models are separately defined.
- [TRELLIS README](https://raw.githubusercontent.com/microsoft/TRELLIS/main/README.md),
  line 41: “An NVIDIA GPU with at least 16GB of memory is necessary.” Lines 329–334
  distinguish MIT models/main code from separately licensed submodules.
- [Hunyuan3D 2.0 license](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE),
  line 3: “THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED
  KINGDOM AND SOUTH KOREA”. Section 5(c) covers outputs outside its territory.
  [README](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/README.md),
  line 126 states 6 GB / 16 GB VRAM.
- [MPFB README](https://raw.githubusercontent.com/makehumancommunity/mpfb2/master/README.md)
  requires Blender >=4.2. [License](https://raw.githubusercontent.com/makehumancommunity/mpfb2/master/LICENSE.md),
  sections C/D: bundled output-contributing assets are CC0; combined output is
  unrestricted by those assets. [Full CC0 asset license](https://raw.githubusercontent.com/makehumancommunity/mpfb2/master/LICENSE.ASSETS.md).
- [Instant Meshes license text](https://raw.githubusercontent.com/wjakob/instant-meshes/master/LICENSE.txt)
  and [QuadriFlow license text](https://raw.githubusercontent.com/hjwdzh/QuadriFlow/master/LICENSE.txt)
  contain redistribution conditions. The first attempted Instant Meshes `/LICENSE`
  URL was a 404; `/LICENSE.txt` was successfully read.

No service's “free trial” or changing demo quota is counted as a permanent free
production resource. Model sizes, runtimes and licensing have not been inferred
from marketing videos. Recheck upstream versions before adopting a new dependency.
