#!/usr/bin/env python3
"""Render the actual rig for visual review, with no projected image materials."""
from pathlib import Path
import hashlib,json,math,sys
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from build_supplied_character import pose
OUT=ROOT/'build/checks/supplied-character';RENDERS=OUT/'renders';RENDERS.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'maziss-supplied-rig.blend'))
rig=bpy.data.objects['MazissRig'];rig.animation_data_clear()
movement=json.loads((OUT/'motion-private.json').read_text());scene=bpy.context.scene
scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=480;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast' if False else 'None'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='VERTEX';scene.display.shading.show_specular_highlight=False;scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH';scene.display.shading.curvature_ridge_factor=.7;scene.display.shading.curvature_valley_factor=.7;scene.display.shading.show_shadows=True;scene.display.shading.show_object_outline=True;scene.display.shading.object_outline_color=(.06,.04,.025)
scene.world=bpy.data.worlds.new('ReviewWorld');scene.world.color=(.2,.22,.23)
bpy.ops.object.camera_add();camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=2.23;scene.camera=camera
angles=[0,45,90,135,180,225,270,315];frames=24
model_hash=hashlib.sha256((OUT/'maziss-supplied-rig.glb').read_bytes()).hexdigest()
manifest={'views':[],'cycleSeconds':movement['cycleSeconds'],'modelSHA256':model_hash,'source':'actual supplied-model rig renders; no sprite projection'}
for angle in angles:
    a=math.radians(angle);camera.location=(4*math.sin(a),-4*math.cos(a),1.09);camera.rotation_euler=(Vector((0,0,1.0))-camera.location).to_track_quat('-Z','Y').to_euler()
    pose(rig,movement['idle']);name=f'idle-{angle}.png';scene.render.filepath=str(RENDERS/name);bpy.ops.render.render(write_still=True)
    record={'angle':angle,'idle':name,'frames':[]}
    view_frames=frames if angle in (0,90,180,270) else 4
    for number in range(view_frames):
        # Continuous reference poses, sampled through their actual target bone
        # endpoints. Linear interpolation preserves the retained reference timing.
        t=number/view_frames*(len(movement['frames'])-1);index=int(t);u=t-index
        first=movement['frames'][index];second=movement['frames'][(index+1)%(len(movement['frames'])-1)]
        targets={name:{end:list(Vector(first[name][end]).lerp(Vector(second[name][end]),u)) for end in ('head','tail')} for name in first}
        pose(rig,targets);name=f'walk-{angle}-{number:02}.png';scene.render.filepath=str(RENDERS/name);bpy.ops.render.render(write_still=True);record['frames'].append(name)
    manifest['views'].append(record);print('CAPTURED',angle,flush=True)
assert hashlib.sha256((OUT/'maziss-supplied-rig.glb').read_bytes()).hexdigest()==model_hash,'Model changed during capture'
(OUT/'render-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
