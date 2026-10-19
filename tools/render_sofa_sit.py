#!/usr/bin/env python3
"""Render actual walk/sit assets against a fixed camera and sofa contact proxy."""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from build_supplied_character import pose
from character_sitting_pose import targets_at, SEAT_HEIGHT, SEAT_CONTACT, SIT_SECONDS
from render_character_style import toon_materials, add_light
OUT=ROOT/'build/checks/sofa-sit';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'build/checks/supplied-character'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--test',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE/'maziss-supplied-rig.blend'))
    rig=bpy.data.objects['MazissRig'];rig.animation_data_clear();scene=bpy.context.scene
    body=bpy.data.objects['Maziss supplied sculpt']
    source_hash=digest(SOURCE/'maziss-supplied-rig.blend')
    movement=json.loads((SOURCE/'motion-private.json').read_text())
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=96
    scene.cycles.use_denoising=False;scene.cycles.max_bounces=3;scene.cycles.diffuse_bounces=2
    scene.render.threads_mode='FIXED';scene.render.threads=4
    scene.render.resolution_x=288;scene.render.resolution_y=360;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
    scene.world=bpy.data.worlds.new('Room ambient');scene.world.use_nodes=True
    ambient=scene.world.node_tree.nodes.get('Background');ambient.inputs['Color'].default_value=(.28,.22,.36,1);ambient.inputs['Strength'].default_value=.34
    add_light('Amber room key',(-3,-4,5),680,(1,.66,.33),2)
    add_light('Cool window fill',(3,1,3),240,(.30,.75,1),2.5)
    add_light('Frontal bounce',(0,-4,2),80,(1,.84,.62),4)
    toon_materials();scene.render.use_freestyle=True
    line=bpy.data.linestyles.new('Thin cartoon contour');line.color=(.045,.021,.012);line.thickness=.8
    lineset=scene.view_layers[0].freestyle_settings.linesets[0];lineset.linestyle=line;lineset.select_crease=False
    stage=bpy.data.objects.new('Presentation heading',None);bpy.context.collection.objects.link(stage)
    for obj in list(scene.objects):
        if obj.type in {'MESH','ARMATURE'} and obj.parent is None:obj.parent=stage
    # Real unrendered contact geometry. It guides authored hips/feet; it is not
    # a visual replacement for the painted sofa or a dynamic physics solver.
    proxies=[]
    for name,center,size in [('Seat cushion',(0,.365,.35),(.72,.60,.16)),('Floor',(0,0,-.025),(4,4,.05)),('Sofa back',(0,.70,.85),(.95,.12,.85))]:
        bpy.ops.mesh.primitive_cube_add(size=1,location=center);obj=bpy.context.object;obj.name='Contact proxy / '+name;obj.scale=size;obj.parent=stage;obj.hide_render=True;obj.display_type='WIRE';proxies.append({'name':name,'center':center,'size':size})
    bpy.ops.object.camera_add();camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=2.45
    camera.location=(0,-4.5,2.35);camera.rotation_euler=(Vector((0,0,.98))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
    bpy.context.view_layer.update()
    def project(point):
        q=world_to_camera_view(scene,camera,Vector(point));return [q.x*288,(1-q.y)*360]
    manifest={'sourceBlendSHA256':source_hash,'sourceGLBSHA256':digest(SOURCE/'maziss-supplied-rig.glb'),
              'poseScriptSHA256':digest(ROOT/'tools/character_sitting_pose.py'),'renderScriptSHA256':digest(Path(__file__)),
              'width':288,'height':360,'orthoScale':2.45,'groundPixel':project((0,0,0)),
              'cameraPosition':list(camera.location),'cameraTarget':[0,0,.98],
              'proxyGeometry':proxies,'seatHeight':SEAT_HEIGHT,'sitSeconds':SIT_SECONDS,
              'cycleSeconds':movement['cycleSeconds'],'sitHeadingDegrees':25,'walk':{},'idle':{},'turn':{},'sit':[],'contacts':[],'footShadows':{}}
    def capture(name,targets):
        pose(rig,targets);scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
        return name
    stage.rotation_euler.z=math.radians(25)
    seat_world=stage.matrix_world@Vector(SEAT_CONTACT)
    bpy.context.view_layer.update();seat_world=stage.matrix_world@Vector(SEAT_CONTACT)
    manifest['seatContactPixel']=project(seat_world)
    manifest['footShadows']['sit']=[project(stage.matrix_world@Vector((sign*.23,-.08,0))) for sign in (-1,1)]
    sit_count=3 if args.test else 41
    for number in range(sit_count):
        t=number/(sit_count-1);name=f'sit-{number:02}.png';manifest['sit'].append(capture(name,targets_at(t)))
        evaluated=body.evaluated_get(bpy.context.evaluated_depsgraph_get());points=[evaluated.matrix_world@v.co for v in evaluated.data.vertices]
        manifest['contacts'].append({'t':t,'minimumZ':min(p.z for p in points),'spineHead':list(rig.pose.bones['Spine'].head),'bodyVertices':len(points),'finite':all(math.isfinite(c) for p in points for c in p)})
    if not args.test:
        for heading in [0,45,90,135,180,225,270,315]:
            stage.rotation_euler.z=-math.radians(heading);bpy.context.view_layer.update()
            manifest['footShadows'][str(heading)]=[project(stage.matrix_world@Vector((sign*.23,-.08,0))) for sign in (-1,1)]
            manifest['idle'][str(heading)]=capture(f'idle-{heading}.png',movement['idle']);records=[]
            for number in range(24):
                t=number/24*(len(movement['frames'])-1);i=int(t);u=t-i;first=movement['frames'][i];second=movement['frames'][(i+1)%(len(movement['frames'])-1)]
                target={n:{end:list(Vector(first[n][end]).lerp(Vector(second[n][end]),u)) for end in ('head','tail')} for n in first}
                records.append(capture(f'walk-{heading}-{number:02}.png',target))
            manifest['walk'][str(heading)]=records;print('WALK',heading,flush=True)
        for heading in [22.5,67.5,112.5,157.5,202.5,247.5,292.5,337.5]:
            stage.rotation_euler.z=-math.radians(heading);bpy.context.view_layer.update()
            manifest['turn'][str(heading)]=capture(f'turn-{heading}.png',movement['idle'])
    stage.rotation_euler.z=math.radians(25);pose(rig,targets_at(1))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/('test.blend' if args.test else 'sofa-sit.blend')))
    assert digest(SOURCE/'maziss-supplied-rig.blend')==source_hash
    (OUT/('test-manifest.json' if args.test else 'render-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
    print('CAPTURED',len(manifest['sit']),'sit frames',flush=True)

if __name__=='__main__':main()
