#!/usr/bin/env python3
"""Build a complete 3D construction study, not a replacement painted-art approval.

blender -b --python tools/build_character_3d.py
The model/preview geometry and private FBX-derived poses remain in ignored build/.
"""
from pathlib import Path
import sys,json,math,random,hashlib
import bpy
from mathutils import Vector,Quaternion,Matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
OUT=ROOT/'build/checks/painted-character';OUT.mkdir(parents=True,exist_ok=True)
from character3d_fit import apply_art_geometry,adjust_arm_targets
from character3d_textures import paint_coordinates,assign_blender_paint
random.seed(19)

def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.85
 return m

def finish(obj,name,mat,bone='Head',group=None):
 obj.name=name;obj.data.materials.clear();obj.data.materials.append(mat)
 for p in obj.data.polygons:p.use_smooth=True
 if bone:
  vg=obj.vertex_groups.new(name=bone);vg.add(list(range(len(obj.data.vertices))),1,'REPLACE')
  mod=obj.modifiers.new('Shared skeleton','ARMATURE');mod.object=ARM
 obj['part_group']=group or name;OBJECTS.append(obj);return obj

def sphere(name,loc,scale,mat,bone='Head',group=None,segments=20,rings=12):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc)
 o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 return finish(o,name,mat,bone,group)

def box(name,loc,scale,mat,bone='Spine',group=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 be=o.modifiers.new('Rounded edges','BEVEL');be.width=bevel;be.segments=3;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=be.name)
 return finish(o,name,mat,bone,group)

def tube(name,points,radius,mat,bone='Head',group=None):
 bpy.ops.object.select_all(action='DESELECT')
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=10;cu.bevel_depth=radius;cu.bevel_resolution=2;cu.use_fill_caps=True
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,xyz in zip(sp.bezier_points,points):p.co=xyz;p.handle_left_type=p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);bpy.context.view_layer.objects.active=o;o.select_set(True)
 bpy.ops.object.convert(target='MESH');o=bpy.context.object
 for selected in bpy.context.selected_objects:selected.select_set(False)
 return finish(o,name,mat,bone,group)

def tuft(name,start,end,width,mat):
 a,b=Vector(start),Vector(end);axis=(b-a).normalized();u=axis.cross(Vector((0,1,0)))
 if u.length<.01:u=axis.cross(Vector((1,0,0)))
 u.normalize();v=axis.cross(u);verts=[];faces=[]
 for j,(t,r) in enumerate([(0,.7),(.25,1),(.70,.6),(1,.025)]):
  mid=a.lerp(b,t)+Vector((.015*math.sin(t*math.pi),0,0))
  for k in range(8):verts.append(tuple(mid+width*r*(math.cos(k*math.tau/8)*u+math.sin(k*math.tau/8)*v*.65)))
 for j in range(3):
  for k in range(8):n=(k+1)%8;faces.append((j*8+k,j*8+n,(j+1)*8+n,(j+1)*8+k))
 faces += [tuple(reversed(range(8))),tuple(24+k for k in range(8))]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);finish(o,name,mat,'Head','Hair')

def head():
 skin=material('Warm skin',(.58,.34,.20));skinlight=material('Skin light',(.70,.43,.25));inner=material('Ear and lip',(.39,.16,.12));hair=material('Untidy dark brown hair',(.065,.035,.020));brow=material('Eyebrow and stubble',(.055,.027,.017));white=material('Warm eye white',(.88,.86,.71));iris=material('Grey green iris',(.13,.24,.23));black=material('Pupils and mouth',(.018,.012,.010))
 sphere('Neck',(0,-.055,1.535),(.064,.060,.115),skin,'Head','Head and neck')
 sphere('Head',(0,-.074,1.78),(.148,.125,.224),skin,'Head','Head and neck',28,20)
 sphere('Jaw',(0,-.109,1.637),(.101,.085,.077),skin,'Head','Head and neck')
 sphere('Chin',(0,-.170,1.624),(.060,.033,.031),skinlight,'Head','Head and neck')
 for sign in [-1,1]:
  sphere('Cheek'+str(sign),(sign*.097,-.168,1.711),(.049,.032,.055),skin,'Head','Head and neck')
  sphere('Ear'+str(sign),(sign*.151,-.047,1.755),(.029,.025,.051),skinlight,'Head','Head and neck')
  sphere('Ear inset'+str(sign),(sign*.167,-.063,1.755),(.010,.012,.027),inner,'Head','Head and neck',12,8)
  x=sign*.065
  sphere('Eye white'+str(sign),(x,-.187,1.791),(.047,.025,.057),white,'Head','Eyes',24,16)
  sphere('Iris'+str(sign),(x,-.211,1.786),(.023,.006,.031),iris,'Head','Eyes')
  sphere('Pupil'+str(sign),(x,-.217,1.786),(.011,.003,.021),black,'Head','Eyes',16,10)
  sphere('Eye glint'+str(sign),(x-.005,-.221,1.799),(.005,.002,.006),white,'Head','Eyes',12,8)
  # Actual lid rims, not painted floating eye rectangles.
  tube('Upper lid'+str(sign),[(x-.044,-.193,1.800),(x-.025,-.209,1.840),(x+.015,-.209,1.843),(x+.044,-.192,1.802)],.006,skinlight,'Head','Eyes')
  tube('Lower lid'+str(sign),[(x-.044,-.191,1.788),(x,-.205,1.736),(x+.043,-.191,1.789)],.004,skin,'Head','Eyes')
  tube('Brow'+str(sign),[(x-.045,-.180,1.856),(x-.016,-.201,1.875),(x+.023,-.194,1.865),(x+.047,-.169,1.849)],.010,brow,'Head','Eyes')
 sphere('Nose bridge',(0,-.198,1.761),(.028,.039,.064),skinlight,'Head','Head and neck')
 sphere('Nose tip',(0,-.231,1.711),(.035,.037,.026),skinlight,'Head','Head and neck')
 for s in [-1,1]:sphere('Nostril'+str(s),(s*.019,-.247,1.704),(.009,.005,.006),inner,'Head','Head and neck',12,8)
 tube('Mouth',[(-.049,-.186,1.646),(-.018,-.199,1.657),(.017,-.199,1.658),(.049,-.184,1.645)],.0045,black,'Head','Mouth')
 tube('Lower lip',[(-.038,-.188,1.640),(0,-.199,1.643),(.037,-.187,1.639)],.004,inner,'Head','Mouth')
 # Closed brown cap; tufts break the outline without relying on alpha cards.
 sphere('Hair cap',(0,-.034,1.893),(.154,.133,.142),hair,'Head','Hair',24,16)
 for i in range(34):
  a=random.uniform(0,math.tau);z=random.uniform(1.91,2.005);r=.12*math.sqrt(max(.08,1-((z-1.89)/.15)**2));start=(r*math.cos(a),-.04+r*.83*math.sin(a),z)
  end=(start[0]+random.uniform(-.075,.075),start[1]+random.uniform(-.06,.06),start[2]+random.uniform(.04,.095));tuft('Hair tuft %02d'%i,start,end,random.uniform(.023,.038),hair)
 for s in [-1,1]:
  tuft('Sideburn'+str(s),(s*.139,-.079,1.859),(s*.137,-.107,1.760),.024,hair)
 # A swept fringe; keep eyes unobstructed.
 for i in range(7):tuft('Fringe'+str(i),(-.11+i*.032,-.13,1.951),(-.14+i*.031,-.170,1.872+abs(i-3)*.006),.029,hair)
 for i in range(28):
  x=random.uniform(-.075,.075);z=random.uniform(1.63,1.687);y=-.17-.023*(1-abs(x)/.09)
  sphere('Stubble %02d'%i,(x,y,z),(.002,.002,.003),brow,'Head','Head and neck',8,6)

def bag():
 leather=material('Worn russet leather',(.24,.095,.025));edge=material('Leather seams',(.09,.035,.011));gold=material('Dull brass',(.45,.27,.055));steel=material('Dark steel',(.19,.23,.22));wood=material('Tool handles',(.11,.047,.020))
 box('Bag shell',(-.244,-.040,.866),(.163,.090,.194),leather,'Spine','Bag',.025)
 box('Bag flap',(-.244,-.091,.900),(.159,.019,.095),leather,'Spine','Bag',.018)
 box('Bag fastening',(-.244,-.106,.866),(.024,.009,.068),edge,'Spine','Bag',.004)
 box('Bag buckle',(-.244,-.114,.863),(.036,.011,.029),gold,'Spine','Bag',.004)
 for dx in [-.069,.069]:tube('Bag stitch'+str(dx),[(-.244+dx,-.096,.936),(-.244+dx,-.096,.795),(-.244+dx*.8,-.094,.782)],.0028,gold,'Spine','Bag')
 # A flat, closed leather loop follows the torso rather than a hovering rope.
 points=[(.13,-.025,1.513),(.115,-.108,1.45),(.07,-.135,1.36),(-.05,-.142,1.18),(-.18,-.100,1.01),(-.24,-.038,.955),(-.20,.085,1.02),(-.05,.120,1.23),(.08,.105,1.43),(.13,.045,1.49)]
 # Fit the band to actual outer clothing, including the closed jacket back.
 # Hand-authored rear coordinates previously buried the strap inside the coat.
 deps=bpy.context.evaluated_depsgraph_get();surfaces=[o.evaluated_get(deps) for o in OBJECTS if o.name in ('Jacket','Shirt')];fitted=[]
 for x,y,z in points:
  if abs(y)>.04 and z>1:
   sign=1 if y>0 else -1;hits=[]
   for surface in surfaces:
    hit,location,normal,face=surface.ray_cast(Vector((x,sign*.6,z)),Vector((0,-sign,0)),distance=1.2)
    if hit:hits.append(location.y)
   if hits:y=(max(hits) if sign>0 else min(hits))+sign*.012
  fitted.append((x,y,z))
 points=fitted
 verts=[];faces=[]
 for i,p in enumerate(points):
  p=Vector(p);t=(Vector(points[(i+1)%len(points)])-Vector(points[(i-1)%len(points)])).normalized();n=Vector((p.x*.3,p.y*4,.02)).normalized();u=t.cross(n).normalized();n=u.cross(t).normalized()
  for sign,depth in [(-1,-1),(1,-1),(1,1),(-1,1)]:verts.append(tuple(p+u*.014*sign+n*.0035*depth))
 for i in range(len(points)):
  for k in range(4):faces.append((i*4+k,i*4+(k+1)%4,((i+1)%len(points))*4+(k+1)%4,((i+1)%len(points))*4+k))
 mesh=bpy.data.meshes.new('Flat shoulder strap');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Shoulder strap',mesh);bpy.context.collection.objects.link(o);finish(o,'Shoulder strap',leather,'Spine','Bag')
 for i in range(3):
  x=-.29+i*.044
  box('Tool handle'+str(i),(x,-.025,1.002),(.019,.022,.095),wood,'Spine','Bag',.006)
  box('Tool shaft'+str(i),(x,-.025,1.065),(.009,.011,.060),steel,'Spine','Bag',.003)
  if i==1:
   # Wrench ring is real closed geometry with a deliberate opening.
   bpy.ops.mesh.primitive_torus_add(major_radius=.019,minor_radius=.005,major_segments=16,minor_segments=6,location=(x,-.025,1.099),rotation=(math.pi/2,0,0));finish(bpy.context.object,'Spanner ring',steel,'Spine','Bag')

def category(o):
 if o.get('part_group'):return o['part_group']
 n=o.name.lower()
 for key,value in [('jacket','Jacket'),('shirt','Shirt'),('pants','Pants'),('trouser','Pants'),('boot','Boots'),('belt','Belt'),('upperarm','Upper arms'),('forearm','Lower arms'),('hand','Hands'),('thigh','Upper legs'),('shin','Lower legs'),('foot','Feet'),('torso','Body'),('pelvis','Body'),('elbow','Lower arms'),('knee','Lower legs')]:
  if key in n.replace('_','').replace(' ',''):return value
 return 'Body'

def export():
 deps=bpy.context.evaluated_depsgraph_get();names=[b.name for b in ARM.data.bones];index={n:i for i,n in enumerate(names)}
 bones=[{'name':b.name,'head':list(b.head_local),'tail':list(b.tail_local),'matrix':list(v for col in b.matrix_local.transposed() for v in col)} for b in ARM.data.bones]
 # Blender matrices serialize column-major for Three.js Matrix4.fromArray.
 objects=[]
 for o in OBJECTS:
  if o.type!='MESH':continue
  ob=o.evaluated_get(deps);mesh=ob.to_mesh();mesh.calc_loop_triangles();matrix=o.matrix_world
  pos=[];normals=[];ids=[];weights=[]
  for v in mesh.vertices:
   pos.extend(round(x,6) for x in matrix@v.co);normals.extend(round(x,6) for x in (matrix.to_3x3()@v.normal).normalized())
   groups=sorted([(index[o.vertex_groups[g.group].name],g.weight) for g in v.groups if o.vertex_groups[g.group].name in index],key=lambda x:-x[1])[:4]
   if not groups:groups=[(index['Spine'],1)]
   total=sum(v for _,v in groups);groups += [(0,0)]*(4-len(groups));ids.extend(i for i,_ in groups);weights.extend(round(w/total,6) for _,w in groups)
  mat=o.data.materials[0] if o.data.materials else None;color=list(mat.diffuse_color[:3]) if mat else [.4,.4,.4]
  item={'name':o.name,'group':category(o),'positions':pos,'normals':normals,'indices':[i for tri in mesh.loop_triangles for i in tri.vertices],'skinIndices':ids,'skinWeights':weights,'color':color}
  item.update(paint_coordinates(item));objects.append(item)
  ob.to_mesh_clear()
 data={'version':2,'purpose':'Original-art surface mapping study on complete geometry; likeness still under review','bones':bones,'objects':objects,'motion':motion(bones)}
 (OUT/'model-private.json').write_text(json.dumps(data,separators=(',',':')))
 # Keep a usable animated authoring file as well as the offline viewer export.
 # The FBX-derived action stays in ignored build output, never the public source.
 for pb in ARM.pose.bones:pb.rotation_mode='QUATERNION'
 bpy.context.scene.render.fps=30;bpy.context.scene.frame_start=1;bpy.context.scene.frame_end=len(data['motion']['frames'])-1
 for frame,targets in enumerate(data['motion']['frames'],1):
  bpy.context.scene.frame_set(frame)
  for bone,target in zip(ARM.data.bones,targets):
   a,b=Vector(target['head']),Vector(target['tail']);rest_dir=(bone.tail_local-bone.head_local).normalized();delta=rest_dir.rotation_difference((b-a).normalized());rotation=delta@bone.matrix_local.to_quaternion()
   pb=ARM.pose.bones[bone.name];pb.matrix=Matrix.LocRotScale(a,rotation,Vector((1,1,1)));bpy.context.view_layer.update()
   pb.keyframe_insert(data_path='location',frame=frame);pb.keyframe_insert(data_path='rotation_quaternion',frame=frame)
 if ARM.animation_data and ARM.animation_data.action:ARM.animation_data.action.name='Private FBX walking reference'
 bpy.context.scene.frame_set(1)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'maziss-construction.blend'))
 print('EXPORTED',len(objects),'objects',sum(len(o['positions'])//3 for o in objects),'vertices')


def motion(bones):
 data=json.loads((ROOT/'private/motion/fbx-motion.json').read_text());rest={b['name']:(Vector(b['head']),Vector(b['tail'])) for b in bones}
 frames=[]
 # Grounding uses the actual rigid boot/sole surfaces that the viewer renders.
 boot_points={side:[o.matrix_world@v.co for o in OBJECTS if side.lower() in o.name.lower() and 'boot' in o.name.lower() for v in o.data.vertices] for side in ['Left','Right']}
 def canonical(v):return Vector((v[1],-v[0],v[2]))
 for sample in data['samples']:
  j=sample['joints'];targets={};lowest=1e9
  for side in ['Left','Right']:
   k=side.lower();hip=rest[side+'Thigh'][0].copy();th=(canonical(j[k+'Knee'])-canonical(j[k+'Hip'])).normalized();sh=(canonical(j[k+'Ankle'])-canonical(j[k+'Knee'])).normalized()
   knee=hip+th*(rest[side+'Thigh'][1]-rest[side+'Thigh'][0]).length;ankle=knee+sh*(rest[side+'Shin'][1]-rest[side+'Shin'][0]).length
   a=-.65*math.tanh(math.radians(sample['footPitchDeg'][k])/.65);q=Quaternion((1,0,0),a);foot=ankle+q@(rest[side+'Foot'][1]-rest[side+'Foot'][0]);targets[side+'Thigh']=(hip,knee);targets[side+'Shin']=(knee,ankle);targets[side+'Foot']=(ankle,foot)
   r=rest[side+'Foot'][0]
   for point in boot_points[side]:lowest=min(lowest,(ankle+q@(point-r)).z)
  dz=.004-lowest;shift=Vector((0,0,dz))
  targets={n:(a+shift,b+shift) for n,(a,b) in targets.items()}
  for name in ['Spine','Head']:targets[name]=tuple(v+shift for v in rest[name])
  for side in ['Left','Right']:
   k=side.lower();shoulder=rest[side+'UpperArm'][0]+shift
   u=(canonical(j[k+'Elbow'])-canonical(j[k+'Shoulder'])).normalized();v=(canonical(j[k+'Wrist'])-canonical(j[k+'Elbow'])).normalized()
   elbow=shoulder+u*(rest[side+'UpperArm'][1]-rest[side+'UpperArm'][0]).length;wrist=elbow+v*(rest[side+'ForeArm'][1]-rest[side+'ForeArm'][0]).length
   targets[side+'UpperArm']=(shoulder,elbow);targets[side+'ForeArm']=(elbow,wrist);targets[side+'Hand']=(wrist,wrist+v*(rest[side+'Hand'][1]-rest[side+'Hand'][0]).length)
  targets=adjust_arm_targets(targets,rest,OBJECTS)
  frames.append([{'head':list(targets[b['name']][0]),'tail':list(targets[b['name']][1])} for b in bones])
 idle_shift=Vector((0,0,-.014))
 idle=adjust_arm_targets({b['name']:(Vector(b['head'])+idle_shift,Vector(b['tail'])+idle_shift) for b in bones},rest,OBJECTS)
 return {'cycleSeconds':data['cycleSeconds'],'source':data['source']['filename'],'frames':frames,'idle':[{'head':list(idle[b['name']][0]),'tail':list(idle[b['name']][1])} for b in bones]}

bpy.ops.wm.read_factory_settings(use_empty=True)
from character3d_body import build_body
built=build_body();ARM=built['armature'];OBJECTS=list(built['objects'])
head();bag();OBJECTS=apply_art_geometry(ARM,OBJECTS)
# Seat the complete portrait closer to the collar. This is a rest-surface fit,
# not bone scaling; every head part and its painting registration move together.
for obj in OBJECTS:
 obj['part_group']=category(obj)
 if obj.get('part_group') in ('Head and neck','Eyes','Mouth','Hair'):
  for vertex in obj.data.vertices:
   point=obj.matrix_world@vertex.co;point.z-=.055
   vertex.co=obj.matrix_world.inverted()@point
 if obj.name.startswith(('Tool handle','Tool shaft','Spanner ring')):
  for vertex in obj.data.vertices:
   point=obj.matrix_world@vertex.co;point.z=.963+(point.z-.963)*.55
   vertex.co=obj.matrix_world.inverted()@point
assign_blender_paint(OBJECTS,ROOT);export()
