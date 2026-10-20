#!/usr/bin/env python3
"""Render a few real owner-feedback poses from the preserved scene, plus probes.
Run in Blender; does not overwrite the retained model/scene/action.
"""
from pathlib import Path
import sys,json,hashlib,math
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
import stool_feedback_pose as p
from render_stool_interaction import apply_sample
OUT=ROOT/'build/checks/stool-feedback';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'build/checks/stool-slide/stool-interaction.blend'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene=bpy.context.scene
# Isolated study copy: correct known free-left-arm binding, matching the source
# region used to prepare the independent right arm. Geometry is unchanged.
body=bpy.data.objects['Maziss supplied sculpt'];rebound=[]
def smooth(a,b,v):
 u=max(0.,min(1.,(v-a)/(b-a)));return u*u*(3-2*u)
for v in body.data.vertices:
 x,y,z=v.co
 if not (x>.24 and .69<z<1.475):continue
 factor=smooth(.24,.28,x)*(1-smooth(1.35,1.475,z))
 if not factor:continue
 upper=smooth(1.07,1.23,z);hand=1-smooth(.865,.985,z)
 target={'LeftUpperArm':upper,'LeftForeArm':(1-upper)*(1-hand),'LeftHand':(1-upper)*hand}
 original={body.vertex_groups[g.group].name:g.weight for g in v.groups}
 for name in set(original)|set(target):
  group=body.vertex_groups.get(name) or body.vertex_groups.new(name=name)
  weight=(1-factor)*original.get(name,0)+factor*target.get(name,0)
  if weight>1e-8:group.add([v.index],weight,'REPLACE')
  else:group.remove([v.index])
 rebound.append(v.index)
(OUT/'left-arm-binding.json').write_text(json.dumps({'sourceSceneSHA256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'verticesRebound':len(rebound),'vertexIndices':rebound,'scope':'Private study copy only; rest geometry unchanged; free-arm region with shoulder blend'},indent=2))
for obj in scene.objects:
 if obj.animation_data:obj.animation_data_clear()
rig=bpy.data.objects['MazissRig'];actor=bpy.data.objects['Maziss world heading and position'];stool=bpy.data.objects['Movable complete stool']
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.cycles.samples=32;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.use_freestyle=False
records=[]
# Measure actual hand-weighted vertices against the finite desktop slab, not just
# against an infinite Z plane. Source surface winding is not used for containment.
from mathutils.geometry import tessellate_polygon
from stool_desk_geometry import world_at,TOP_PIXELS
poly=[Vector(world_at(v,.93)) for v in TOP_PIXELS]
def on_desk(v):
 x,y=v.x,v.y;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a.y>y)!=(b.y>y) and x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x:inside=not inside
 return inside
meshes=[o for o in scene.objects if o.type=='MESH' and o.vertex_groups and any(g.name.endswith('Hand') for g in o.vertex_groups)]
def hands():
 result={s:[] for s in ('Left','Right','LeftForearm','RightForearm')};dg=bpy.context.evaluated_depsgraph_get()
 for obj in meshes:
  ev=obj.evaluated_get(dg)
  indices={g.index:g.name for g in obj.vertex_groups}
  for v in ev.data.vertices:
   for weight in v.groups:
    name=indices.get(weight.group,'')
    if weight.weight>.65 and name in ('LeftHand','RightHand','LeftForeArm','RightForeArm'):
     label={'LeftHand':'Left','RightHand':'Right','LeftForeArm':'LeftForearm','RightForeArm':'RightForearm'}[name];result[label].append(ev.matrix_world@v.co)
 return result
for n in range(121):
 t=n/20;sample=p.state_at(t);apply_sample(rig,actor,stool,sample,());bpy.context.view_layer.update()
 hs=hands();records.append({'seconds':t,'phase':sample['phase'],'hands':{side:{'vertices':len(vs),'insideDesktopSlab':sum(on_desk(v) and .8705<v.z<.9295 for v in vs),'minimumZ':min(v.z for v in vs) if vs else None,'minimumZOverDesktop':min((v.z for v in vs if on_desk(v)),default=None)}for side,vs in hs.items()}})
(OUT/'hand-probe.json').write_text(json.dumps(records,indent=2))
if '--probe-only' in sys.argv:
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'probe-scene.blend'))
 print('HAND SLAB HITS',[(r['seconds'],s,v['insideDesktopSlab'])for r in records for s,v in r['hands'].items()if v['insideDesktopSlab']],flush=True)
 raise SystemExit(0)
manifest={'poseSHA256':hashlib.sha256((ROOT/'tools/stool_feedback_pose.py').read_bytes()).hexdigest(),'sourceSceneSHA256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'renders':[],'scope':'Isolated poses; no full animation or Godot integration; model art unfinished','cameraPosition':list(scene.camera.location),'cameraTarget':[-.8,-.28,.85],'orthoScale':2.9,'roomFloorAnchor':[1445,744],'roomPixelsPerMetre':200}
from bpy_extras.object_utils import world_to_camera_view
ground=world_to_camera_view(scene,scene.camera,Vector((0,0,0)));manifest['groundPixel']=[ground.x*640,(1-ground.y)*640]
for t in (0.,.65,1.45,2.4,3.05,3.7,4.5,5.4,6.):
 sample=p.state_at(t);apply_sample(rig,actor,stool,sample,());bpy.context.view_layer.update()
 name=f'pose-{round(t*100):03}.png';scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
 manifest['renders'].append({'name':name,'seconds':t,'phase':sample['phase']});(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2));print('RENDERED',name,flush=True)
# A second, visibly separate studio camera exposes the seated feet and hand path.
# Neutral desk shading is diagnostic only; room painting and model are untouched.
cam=scene.camera;cam_location=cam.location.copy();cam_rotation=cam.rotation_euler.copy();cam_scale=cam.data.ortho_scale
neutral=bpy.data.materials.new('Diagnostic desk surface only');neutral.diffuse_color=(.22,.19,.15,1)
replaced=[]
for obj in scene.objects:
 if obj.name.startswith('Desk /') or obj.name.startswith('Desk item /'):
  replaced.append((obj,list(obj.data.materials)));obj.data.materials.clear();obj.data.materials.append(neutral)
for t in (0.,.65,1.45,2.4,3.05,3.7,4.5,5.4,6.):
 sample=p.state_at(t);apply_sample(rig,actor,stool,sample,());bpy.context.view_layer.update()
 focus=Vector((.1,.2,.75));cam.location=focus+Vector((1.8,-4.,2.2));cam.rotation_euler=(focus-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=2.2
 name=f'diagnostic-{round(t*100):03}.png';scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
for obj,materials in replaced:
 obj.data.materials.clear()
 for mat in materials:obj.data.materials.append(mat)
cam.location=cam_location;cam.rotation_euler=cam_rotation;cam.data.ortho_scale=cam_scale
# Save separate diagnostic scene for independent evaluated-surface QA/review.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'pose-test.blend'))
print('HAND SLAB HITS',[(r['seconds'],s,v['insideDesktopSlab'])for r in records for s,v in r['hands'].items()if v['insideDesktopSlab']],flush=True)
