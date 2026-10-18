# Complete clothing repair layers

`maziss-clothing-repair.png` was generated on 18 October 2026 using OpenAI image
editing, referencing the original `maziss-side-atlas.png` and
`maziss-depth-atlas.png`. It supplies complete painted torso backing and separate
intact tool satchels in side/front/back views. Original atlases and the approved
room PNG remain unchanged. The generated master is retained in the workspace's
image-generation output; this file is a copied original output, not a repainted
or alpha-processed PNG.

Runtime mappings in `walking/character-renderer.js` select jacket backing and the
three standalone satchels. The generated top-row torsos also contain attached
bag details despite the separation prompt; mappings limit their use to torso
coverage, with the intact separate bag layered over the attachment area. The
original opaque torso core preserves collar, neck and tailoring detail. Original
head/face and arm drawings remain in use. No complete arm-shaped hole is cut out
of the jacket, and no hand-shaped hole is cut out of the bag.

These are painted 2D layer repairs, not 3D clothing, cloth simulation or a complete
production character model. Cloth follows the animated leg bones; the bag is a
single rigid layer attached to the torso. Full turns, independent fabric physics
and production-ready disassembled garment art remain future work.
