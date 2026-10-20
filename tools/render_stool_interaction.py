#!/usr/bin/env python3
"""Bake and render actual Maziss + stool geometry with one fixed room camera.

blender -b --python tools/render_stool_interaction.py -- --keys
blender -b --python tools/render_stool_interaction.py
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector, Quaternion, Matrix

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_supplied_character import pose
from render_character_style import toon_materials, add_light
from stool_interaction_pose import state_at, DURATION, FPS

OUT = ROOT/'build/checks/stool-interaction'
SOURCE = ROOT/'build/checks/supplied-character/maziss-supplied-rig.blend'
STOOL = ROOT/'build/checks/stool-study/maziss-stool.blend'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--keys',action='store_true')
    parser.add_argument('--only',type=float,nargs='*')
    parser.add_argument('--size',type=int,default=448)
    parser.add_argument('--samples',type=int,default=32)
    parser.add_argument('--reuse-approach-before-foot-fix',action='store_true',
                        help='Reuse explicitly unchanged approach captures from the retained pre-foot-roll manifest')
    parser.add_argument('--reuse-verified-prefix',type=Path,
                        help='Prior render manifest paired with art/prefix-equivalence.json')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    OUT.mkdir(exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    rig=bpy.data.objects['MazissRig'];rig.animation_data_clear()
    body=bpy.data.objects['Maziss supplied sculpt']
    scene=bpy.context.scene
    for obj in list(scene.objects):
        if obj.type in {'CAMERA','LIGHT'}:
            bpy.data.objects.remove(obj,do_unlink=True)
    actor=bpy.data.objects.new('Maziss world heading and position',None)
    bpy.context.collection.objects.link(actor);actor.rotation_mode='QUATERNION'
    for obj in list(scene.objects):
        if obj.type in {'MESH','ARMATURE'} and obj.parent is None:
            obj.parent=actor
    toon_materials()  # character palette only; props keep their real base materials
    with bpy.data.libraries.load(str(STOOL),link=False) as (available,loaded):
        loaded.objects=[n for n in available.objects if n.startswith('Stool /')]
    stool=bpy.data.objects.new('Movable complete stool',None)
    bpy.context.collection.objects.link(stool)
    for obj in loaded.objects:
        bpy.context.collection.objects.link(obj);obj.parent=stool
    assert len(loaded.objects)==6
    scene.render.engine='CYCLES';scene.cycles.device='CPU'
    scene.cycles.samples=args.samples;scene.cycles.use_denoising=False
    scene.cycles.use_adaptive_sampling=True
    scene.cycles.adaptive_threshold=.05;scene.cycles.adaptive_min_samples=8
    scene.cycles.max_bounces=3;scene.cycles.diffuse_bounces=2
    scene.render.threads_mode='FIXED';scene.render.threads=4
    scene.render.resolution_x=scene.render.resolution_y=args.size
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
    scene.world=bpy.data.worlds.new('Painted room ambient');scene.world.use_nodes=True
    ambient=scene.world.node_tree.nodes.get('Background')
    ambient.inputs['Color'].default_value=(.28,.22,.36,1)
    ambient.inputs['Strength'].default_value=.34
    add_light('Warm room key',(-3,-4,5),680,(1,.66,.33),2)
    add_light('Window fill',(3,1,3),240,(.30,.75,1),2.5)
    add_light('Soft room bounce',(0,-4,2),80,(1,.84,.62),4)
    bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.002))
    floor=bpy.context.object;floor.name='Real floor shadow catcher'
    floor.is_shadow_catcher=True
    floor_mat=bpy.data.materials.new('Shadow floor');floor_mat.use_nodes=True
    node=floor_mat.node_tree.nodes.get('Principled BSDF')
    node.inputs['Base Color'].default_value=(.3,.2,.13,1)
    node.inputs['Roughness'].default_value=1
    floor.data.materials.append(floor_mat)
    scene.render.use_freestyle=True
    line=bpy.data.linestyles.new('Brown toon contour')
    line.color=(.045,.021,.012);line.thickness=.9
    lineset=scene.view_layers[0].freestyle_settings.linesets[0]
    lineset.linestyle=line;lineset.select_crease=False
    bpy.ops.object.camera_add()
    camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=2.9
    target=Vector((-.8,-.28,.85))
    camera.location=target+Vector((0,-5,5*math.tan(math.radians(23))))
    camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.camera=camera
    scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=round(DURATION*FPS)+1
    for bone in rig.pose.bones:
        bone.rotation_mode='QUATERNION'
    def apply(sample):
        position=Vector(sample['root']['position'])
        heading=Quaternion((0,0,1),math.radians(sample['root']['yaw_degrees']))
        local={name:{end:list(heading.inverted()@(Vector(point)-position))
                     for end,point in pair.items()} for name,pair in sample['targets'].items()}
        # Bone direction alone cannot encode twist about a near-vertical spine.
        # The real root carries heading; bones receive only actor-local poses.
        actor.location=position;actor.rotation_quaternion=heading
        pose(rig,local)
        if sample['phase']!='approach':
            # Head/tail direction does not specify roll. During a planted pivot,
            # preserve the entire sole's orientation with an exact Z rotation.
            for side in ('Left','Right'):
                name=side+'Foot';bone=rig.data.bones[name]
                a=Vector(local[name]['head']);b=Vector(local[name]['tail'])
                original=bone.tail_local-bone.head_local;direction=b-a
                angle=math.atan2(direction.y,direction.x)-math.atan2(original.y,original.x)
                rotation=Quaternion((0,0,1),angle)@bone.matrix_local.to_quaternion()
                rig.pose.bones[name].matrix=Matrix.LocRotScale(a,rotation,Vector((1,1,1)))
                bpy.context.view_layer.update()
        stool.location=sample['stool_position']
    # Bake one editable action and the stool track before expensive rendering.
    states=[]
    for number in range(scene.frame_end):
        scene.frame_set(number+1)
        sample=state_at(number/FPS)
        apply(sample)
        for bone in rig.pose.bones:
            bone.keyframe_insert(data_path='location',frame=number+1)
            bone.keyframe_insert(data_path='rotation_quaternion',frame=number+1)
        stool.keyframe_insert(data_path='location',frame=number+1)
        actor.keyframe_insert(data_path='location',frame=number+1)
        actor.keyframe_insert(data_path='rotation_quaternion',frame=number+1)
        states.append({'seconds':number/FPS,'phase':sample['phase'],
                       'stoolPosition':list(sample['stool_position']), 'root':sample['root']})
    for obj in (rig,stool,actor):
        for curve in obj.animation_data.action.fcurves:
            for point in curve.keyframe_points:point.interpolation='LINEAR'
    scene.frame_set(1);bpy.context.view_layer.update()
    ground=world_to_camera_view(scene,camera,Vector((0,0,0)))
    manifest={'sourceBlendSHA256':digest(SOURCE),'stoolBlendSHA256':digest(STOOL),
              'poseScriptSHA256':digest(ROOT/'tools/stool_interaction_pose.py'),
              'rendererSHA256':digest(Path(__file__)), 'width':args.size,'height':args.size,
              'samples':args.samples,
              'orthoScale':2.9,'cameraPosition':list(camera.location),'cameraTarget':list(target),
              'groundPixel':[ground.x*args.size,(1-ground.y)*args.size],
              'roomFloorAnchor':[1445,744],'roomPixelsPerMetre':200,
              'fps':FPS,'duration':DURATION,'states':states,'renders':[],
              'realGeometry':['supplied character rig','six-part stool','floor shadow catcher'],
              'scope':'One authored approach/pull/sit action over a repaired painted background'}
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'stool-interaction.blend'))
    manifest['sceneSHA256']=digest(OUT/'stool-interaction.blend')
    file=OUT/('key-manifest.json' if args.keys or args.only else 'render-manifest.json')
    file.write_text(json.dumps(manifest,indent=2)+'\n')
    times=args.only if args.only else [0,1.2,2.5,3.25,4,5.2,5.8,6.8,7.8] if args.keys else [n/FPS for n in range(scene.frame_end)]
    previous={}
    if args.reuse_approach_before_foot_fix:
        old=json.loads((OUT/'render-before-foot-roll.json').read_text())
        for field in ('sourceBlendSHA256','stoolBlendSHA256','poseScriptSHA256','width','height','samples','cameraPosition','cameraTarget','fps'):
            assert old[field]==manifest[field], 'Cannot reuse incompatible approach: '+field
        previous={round(r['seconds']*FPS):dict(r,reusedFromRendererSHA256=old['rendererSHA256'])
                  for r in old['renders'] if r['phase']=='approach' and digest(OUT/r['name'])==r['sha256']}
    if args.reuse_verified_prefix:
        old=json.loads(args.reuse_verified_prefix.read_text())
        proof=json.loads((OUT/'art/prefix-equivalence.json').read_text())
        assert proof['oldPoseSHA256']==old['poseScriptSHA256']
        assert proof['newPoseSHA256']==manifest['poseScriptSHA256']
        assert proof['exactStateEqual'] and proof['sampleCount']>=460
        for field in ('sourceBlendSHA256','stoolBlendSHA256','width','height','samples','cameraPosition','cameraTarget','fps'):
            assert old[field]==manifest[field], 'Incompatible prefix render: '+field
        previous={round(r['seconds']*FPS):dict(r,reusedFromPoseScriptSHA256=old['poseScriptSHA256'],
                                             prefixEquivalenceSHA256=digest(OUT/'art/prefix-equivalence.json'))
                  for r in old['renders'] if r['seconds']<proof['untilSecondsExclusive']
                  and digest(OUT/r['name'])==r['sha256']}
    for t in times:
        number=round(t*FPS);scene.frame_set(number+1)
        if number in previous:
            manifest['renders'].append(previous[number])
            file.write_text(json.dumps(manifest,indent=2)+'\n')
            print('REUSED UNCHANGED APPROACH',number,flush=True)
            continue
        # Exact authored target at each sampled frame; no frame-bound resizing.
        sample=state_at(number/FPS);apply(sample)
        bpy.context.view_layer.update()
        evaluated=body.evaluated_get(bpy.context.evaluated_depsgraph_get())
        vertices=[evaluated.matrix_world@v.co for v in evaluated.data.vertices]
        name=f'key-{number:03}.png' if args.keys or args.only else f'frame-{number:03}.png'
        scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
        manifest['renders'].append({'name':name,'seconds':number/FPS,'phase':sample['phase'],
                                    'bodyMinimumZ':min(v.z for v in vertices),
                                    'bodyVertices':len(vertices),
                                    'finite':all(math.isfinite(c) for v in vertices for c in v),
                                    'sha256':digest(OUT/name)})
        file.write_text(json.dumps(manifest,indent=2)+'\n')
        print('CAPTURE',name,sample['phase'],flush=True)
    assert digest(SOURCE)==manifest['sourceBlendSHA256']
    assert digest(STOOL)==manifest['stoolBlendSHA256']
    print('COMPLETE',len(manifest['renders']),flush=True)


if __name__=='__main__':
    main()
