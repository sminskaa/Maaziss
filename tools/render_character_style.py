#!/usr/bin/env python3
"""Actual Blender Cycles toon-light study; preserve the supplied sculpt and motion.

Run: blender -b --python tools/render_character_style.py -- --test
Omit --test for three idle views plus a 24-frame side-walk cycle. No sprite projection.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys
import time

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build_supplied_character import pose

SOURCE = ROOT / 'build/checks/supplied-character'
OUTPUT = ROOT / 'build/checks/style-match/character'


def add_light(name, position, power, color, size):
    data = bpy.data.lights.new(name, 'AREA')
    data.energy = power
    data.color = color
    data.shape = 'DISK'
    data.size = size
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = position
    obj.rotation_euler = (Vector((0, 0, 1)) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def toon_materials():
    """Use the retained continuous surface colours with a bounded rough toon BSDF."""
    for material in bpy.data.materials:
        if not material.use_nodes:
            continue
        tree = material.node_tree
        base = material.diffuse_color[:]
        tree.nodes.clear()
        output = tree.nodes.new('ShaderNodeOutputMaterial')
        toon = tree.nodes.new('ShaderNodeBsdfToon')
        toon.component = 'DIFFUSE'
        toon.inputs['Size'].default_value = .72
        toon.inputs['Smooth'].default_value = .16
        color = tree.nodes.new('ShaderNodeVertexColor')
        color.layer_name = 'MazissPalette'
        # The palette is a complete continuous vertex field, not a photograph
        # or repeated portrait. All facial meshes also retain this attribute.
        noise = tree.nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 56
        noise.inputs['Detail'].default_value = 2
        ramp = tree.nodes.new('ShaderNodeMapRange')
        ramp.inputs['From Min'].default_value = 0
        ramp.inputs['From Max'].default_value = 1
        ramp.inputs['To Min'].default_value = .88
        ramp.inputs['To Max'].default_value = 1.10
        multiply = tree.nodes.new('ShaderNodeMixRGB')
        multiply.blend_type = 'MULTIPLY'
        multiply.inputs[0].default_value = 1
        tree.links.new(color.outputs['Color'], multiply.inputs[1])
        tree.links.new(noise.outputs['Fac'], ramp.inputs['Value'])
        tree.links.new(ramp.outputs['Result'], multiply.inputs[2])
        tree.links.new(multiply.outputs[0], toon.inputs['Color'])
        tree.links.new(toon.outputs[0], output.inputs['Surface'])
        material.diffuse_color = base


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--test', action='store_true')
    args.add_argument('--walk-frames', type=int, default=24)
    opts = args.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source_hash = hashlib.sha256((SOURCE / 'maziss-supplied-rig.blend').read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE / 'maziss-supplied-rig.blend'))
    rig = bpy.data.objects['MazissRig']
    rig.animation_data_clear()
    movement = json.loads((SOURCE / 'motion-private.json').read_text())
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 128
    scene.cycles.use_denoising = False
    scene.cycles.max_bounces = 3
    scene.cycles.diffuse_bounces = 2
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 4
    scene.render.resolution_x = 480
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.world = bpy.data.worlds.new('Room purple ambient')
    scene.world.use_nodes = True
    world = scene.world.node_tree.nodes.get('Background')
    world.inputs['Color'].default_value = (.28, .22, .36, 1)
    world.inputs['Strength'].default_value = .34
    # The warm source is left of the camera, matching the room lamps; the
    # weaker window source cools the shadow-side edge without bleaching it.
    add_light('Amber room key', (-3, -4, 5), 680, (1, .66, .33), 2)
    add_light('Cool window fill', (3, 1, 3), 240, (.30, .75, 1), 2.5)
    add_light('Quiet frontal bounce', (0, -4, 2), 80, (1, .84, .62), 4)
    toon_materials()
    scene.render.use_freestyle = True
    line = bpy.data.linestyles.new('Maziss thin brown contour')
    scene.view_layers[0].freestyle_settings.linesets[0].linestyle = line
    line.color = (.045, .021, .012)
    line.thickness = 1.15
    lineset = scene.view_layers[0].freestyle_settings.linesets[0]
    lineset.select_crease = False
    lineset.select_border = True
    lineset.select_silhouette = True
    lineset.select_contour = True
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 2.23
    scene.camera = camera
    camera.location = (0, -4, 1.09)
    camera.rotation_euler = (Vector((0, 0, 1)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
    # A game character turns under the room's fixed lights. Rotating a review
    # camera instead would change screen-space light direction in composites.
    stage = bpy.data.objects.new('Character heading presentation only', None)
    bpy.context.collection.objects.link(stage)
    for obj in list(scene.objects):
        if obj.type in {'MESH', 'ARMATURE'} and obj.parent is None:
            obj.parent = stage
    views = [0] if opts.test else [0, 45, 90]
    manifest = {'sourceBlendSHA256': source_hash, 'source': 'Actual supplied rig rendered in Blender Cycles CPU',
                'sourceMotionSHA256': hashlib.sha256((SOURCE / 'motion-private.json').read_bytes()).hexdigest(),
                'geometryChanged': False, 'motionChanged': False, 'imageProjectionUsed': False,
                'cycleSeconds': movement['cycleSeconds'], 'engine': 'Cycles CPU, diffuse toon BSDF, Freestyle',
                'width': 480, 'height': 640, 'cameraOrthoScale': camera.data.ortho_scale,
                'projectionConvention': 'PNG pixels, origin top-left; ground point is world (0,0,0)',
                'headingConvention': 'Fixed camera and room lights; character stage rotates -angle about world Z',
                'characterRestHeightWorld': 2.0, 'walkHeading': 90, 'views': [], 'walk': []}
    started = time.monotonic()
    def render(name):
        scene.render.filepath = str(OUTPUT / name)
        bpy.ops.render.render(write_still=True)
    for angle in views:
        stage.rotation_euler.z = -math.radians(angle)
        pose(rig, movement['idle'])
        name = f'idle-{angle}.png'
        render(name)
        ground = world_to_camera_view(scene, camera, Vector((0, 0, 0)))
        manifest['views'].append({'angle': angle, 'idle': name,
                                 'groundPixel': [ground.x * 480, (1 - ground.y) * 640]})
    if not opts.test:
        for number in range(max(1, opts.walk_frames)):
            t = number / max(1, opts.walk_frames) * (len(movement['frames']) - 1)
            index = int(t)
            u = t - index
            first = movement['frames'][index]
            second = movement['frames'][(index + 1) % (len(movement['frames']) - 1)]
            targets = {name: {end: list(Vector(first[name][end]).lerp(Vector(second[name][end]), u))
                             for end in ('head', 'tail')} for name in first}
            pose(rig, targets)
            name = f'walk-90-{number:02}.png'
            render(name)
            manifest['walk'].append(name)
    manifest['renderSeconds'] = round(time.monotonic() - started, 2)
    manifest['renderScriptSHA256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUTPUT / ('test-manifest.json' if opts.test else 'manifest.json')).write_text(json.dumps(manifest, indent=2) + '\n')
    assert hashlib.sha256((SOURCE / 'maziss-supplied-rig.blend').read_bytes()).hexdigest() == source_hash
    print('STYLE_STUDY', json.dumps(manifest), flush=True)


if __name__ == '__main__':
    main()
