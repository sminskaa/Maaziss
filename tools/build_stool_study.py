#!/usr/bin/env python3
"""Build/save a complete reference-guided stool, then render three actual views.

blender -b --python tools/build_stool_study.py
Private outputs stay in build/checks/stool-study/. No room or character edits.
"""
from pathlib import Path
import hashlib
import json
import math
import sys

import bpy
import bmesh
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/checks/stool-study'
OUT.mkdir(parents=True, exist_ok=True)


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    node = mat.node_tree.nodes.get('Principled BSDF')
    node.inputs['Base Color'].default_value = (*color, 1)
    node.inputs['Roughness'].default_value = .82
    return mat


def finish(obj, mat, bevel=.006):
    obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new('Rounded worn edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        mod = obj.modifiers.new('Weighted corner normals', 'WEIGHTED_NORMAL')
        mod.keep_sharp = True
    return obj


def seat(mat, edge_mat):
    # A closed lathed mesh: actual seat top, bevel profile and underside.
    count = 64
    profile = [(.205, .508), (.216, .512), (.223, .525),
               (.223, .550), (.217, .563), (.198, .568)]
    vertices = []
    for radius, z in profile:
        for i in range(count):
            a = 2 * math.pi * i / count
            irregular = 1 + .009 * math.sin(3*a) + .004 * math.cos(7*a)
            vertices.append((radius*math.cos(a)*irregular,
                             radius*math.sin(a)*irregular, z))
    faces = [tuple(reversed(range(count)))]
    for j in range(len(profile)-1):
        for i in range(count):
            n = (i+1) % count
            faces.append((j*count+i, j*count+n, (j+1)*count+n, (j+1)*count+i))
    faces.append(tuple((len(profile)-1)*count+i for i in range(count)))
    mesh = bpy.data.meshes.new('Closed solid seat geometry')
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('Stool / solid rounded seat', mesh)
    bpy.context.collection.objects.link(obj)
    mesh.materials.append(edge_mat)
    mesh.materials.append(mat)
    mesh.polygons[-1].material_index = 1
    for poly in mesh.polygons[1:-1]:
        poly.use_smooth = True
    return obj


def leg(name, x, y, mat):
    bottom = Vector((x*.182, y*.182, .03))
    top = Vector((x*.103, y*.103, .521))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(bottom+top)/2)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = (.048, .045, (top-bottom).length)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    # Slight taper: narrower at the floor, all four legs remain solid parts.
    for v in obj.data.vertices:
        if v.co.z < 0:
            v.co.x *= .80
            v.co.y *= .80
    obj.rotation_euler = (top-bottom).to_track_quat('Z', 'Y').to_euler()
    finish(obj, mat, .006)
    bpy.context.view_layer.update()
    # Flatten only the foot end. Translating the entire leg to ground lowered
    # its top too, leaving a visible gap beneath the seat in the first export.
    inverse = obj.matrix_world.inverted()
    for vertex in obj.data.vertices:
        if vertex.co.z < 0:
            point = obj.matrix_world @ vertex.co
            point.z = 0
            vertex.co = inverse @ point
    obj.data.update()
    return obj


def foot_ring(mat):
    # Closed rectangular-section hoop, not a painted ellipse or flat card.
    count = 64
    vertices = []
    for radius, z in [(.202, .177), (.222, .177), (.222, .198), (.202, .198)]:
        for i in range(count):
            a = 2 * math.pi * i/count
            vertices.append((radius*math.cos(a), radius*math.sin(a), z))
    faces = []
    for j in range(4):
        for i in range(count):
            n = (i+1) % count
            faces.append((j*count+i, j*count+n, ((j+1)%4)*count+n, ((j+1)%4)*count+i))
    mesh = bpy.data.meshes.new('Closed solid footrest hoop')
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('Stool / circular bracing footrest', mesh)
    bpy.context.collection.objects.link(obj)
    return finish(obj, mat, .003)


def light(name, location, color, power, size):
    data = bpy.data.lights.new(name, 'AREA')
    data.energy, data.color, data.size = power, color, size
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector((0, 0, .3))-obj.location).to_track_quat('-Z','Y').to_euler()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    top = material('Seat / warm worn wood base', (.37, .145, .047))
    edge = material('Seat / dark chestnut edge', (.18, .065, .031))
    legs = material('Legs / muted weathered brown', (.135, .077, .050))
    brace = material('Footrest / dark wood', (.17, .095, .040))
    parts = [seat(top, edge)]
    for x, y in [(-1,-1),(1,-1),(1,1),(-1,1)]:
        parts.append(leg(f'Stool / leg {len(parts)}', x, y, legs))
    parts.append(foot_ring(brace))
    # Object-local UV coordinates are prepared for a later dedicated painting pass.
    for obj in parts:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.uv.smart_project(island_margin=.035)
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    glb = OUT/'maziss-stool.glb'
    bpy.ops.export_scene.gltf(filepath=str(glb), export_format='GLB',
                              use_selection=True, export_apply=True, export_yup=True)
    audit = []
    for obj in parts:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        audit.append({'name':obj.name,'vertices':len(bm.verts),'faces':len(bm.faces),
                      'nonManifoldEdges':sum(not e.is_manifold for e in bm.edges),
                      'uvLayers':list(obj.data.uv_layers.keys())})
        bm.free()
    assert len(parts) == 6 and all(p['nonManifoldEdges']==0 for p in audit)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 48
    scene.cycles.use_denoising = False
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 4
    scene.render.resolution_x = scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.view_settings.view_transform = 'Standard'
    scene.world.color = (.10,.08,.13)
    floor_mat = material('Studio ground / muted violet', (.105,.085,.125))
    bpy.ops.mesh.primitive_plane_add(size=200)
    floor = bpy.context.object
    floor.name = 'Review studio floor (excluded from GLB)'
    floor.data.materials.append(floor_mat)
    light('Warm left key', (-2,-3,4), (1,.67,.35), 400, 2.5)
    light('Cool right fill', (3,0,2.5), (.43,.65,1), 130, 3)
    scene.render.use_freestyle = True
    style = bpy.data.linestyles.new('Fine brown cartoon contour')
    style.color, style.thickness = (.045,.02,.012), .9
    line = scene.view_layers[0].freestyle_settings.linesets[0]
    line.linestyle = style
    line.select_crease = False
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = .86
    scene.camera = camera
    target = Vector((0,0,.285))
    def aim(azimuth, elevation):
        a,e = math.radians(azimuth), math.radians(elevation)
        camera.location = target + Vector((math.sin(a)*math.cos(e), -math.cos(a)*math.cos(e), math.sin(e)))*3
        camera.rotation_euler = (target-camera.location).to_track_quat('-Z','Y').to_euler()
    aim(20,23)
    scene.render.filepath = str(OUT/'room-angle.png')
    blend = OUT/'maziss-stool.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))  # save before rendering
    manifest = {'scope':'Geometry-only stool candidate, no room replacement or character animation',
                'sourceRoomSHA256':digest(ROOT/'build/checks/room-cutaway/room-reframed-source.png'),
                'sourceCrop':[1368,592,1513,767], 'seatTopMetres':.568,
                'dimensionsAssumed':True,'parts':audit,'modelSHA256':digest(glb),
                'blendSHA256':digest(blend),'scriptSHA256':digest(Path(__file__)),
                'views':[], 'limits':['Base colours only; painted wood/wear not finished.',
                                    'Camera angle is a local reference estimate, not a recovered room camera.',
                                    'No clean background, room replacement, moving stool or sitting character.']}
    (OUT/'model-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('MODEL SAVED',glb,blend,flush=True)
    for name, azimuth, elevation in [('room-angle',20,23),('rear-angle',155,25),('underside',220,-16)]:
        aim(azimuth,elevation)
        floor.hide_render = elevation < 0
        scene.render.filepath = str(OUT/(name+'.png'))
        bpy.ops.render.render(write_still=True)
        manifest['views'].append({'name':name,'azimuth':azimuth,'elevation':elevation,
                                  'imageSHA256':digest(OUT/(name+'.png'))})
        (OUT/'model-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE',len(manifest['views']),'actual views',flush=True)


if __name__ == '__main__':
    main()
