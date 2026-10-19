#!/usr/bin/env python3
"""Rig the owner's private sculpt with real material regions and fitted details.

blender -b --python tools/build_supplied_character.py
No source sprite is used as a character texture. Outputs remain private in build/.
"""
from pathlib import Path
import sys,math,json,hashlib
import bpy
from mathutils import Vector,Matrix,Quaternion

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
OUT=ROOT/'build/checks/supplied-character';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'private/models/white_mesh.glb'


def smooth(a,b,value):
    t=max(0,min(1,(value-a)/(b-a)));return t*t*(3-2*t)


def rgb(hexcode):
    values=[int(hexcode[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values)


def material(name,hexcode):
    mat=bpy.data.materials.new(name);color=rgb(hexcode)
    mat.diffuse_color=(*color,1);mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.85
    return mat


def import_body():
    bpy.ops.import_scene.gltf(filepath=str(SOURCE))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    if len(meshes)!=1:raise ValueError('Expected the inspected single-mesh source')
    obj=meshes[0];vertices=[obj.matrix_world@v.co for v in obj.data.vertices]
    low=Vector(tuple(min(v[i] for v in vertices) for i in range(3)));high=Vector(tuple(max(v[i] for v in vertices) for i in range(3)))
    scale=2/(high.z-low.z);center=(low+high)/2
    points=[((v.x-center.x)*scale,(v.y-center.y)*scale,(v.z-low.z)*scale) for v in vertices]
    faces=[list(p.vertices) for p in obj.data.polygons]
    # This source has one index shared by a hand fan and a tiny opposite-hand
    # patch. Restore the latter locally; merely splitting the index retains
    # five long erroneous triangles between the two hands.
    repairs=[]
    # Keep this specific source repair explicit rather than silently assuming
    # every future owner's mesh shares the same indexing.
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='209c92bbfa786d3e6e268cbb386627bbe756ee40691a4ff84b3b16bd4ca0066d':
        patch=[9433,9434,9435,9439,9440]
        neighbors={v for index in patch for v in faces[index] if v!=0}
        restored=tuple(sum(points[v][axis] for v in neighbors)/len(neighbors) for axis in range(3))
        duplicate=len(points);points.append(restored)
        for index in patch:faces[index]=[duplicate if v==0 else v for v in faces[index]]
        repairs.append({'sourceVertex':0,'newVertex':duplicate,'faces':patch,'restoredPosition':restored,'reason':'disconnected local hand patch incorrectly referenced opposite hand'})
    mesh=bpy.data.meshes.new('MazissSuppliedSurface');mesh.from_pydata(points,[],faces);mesh.update()
    old=obj.data;obj.data=mesh;bpy.data.meshes.remove(old);obj.matrix_world.identity();obj.name='Maziss supplied sculpt'
    for polygon in mesh.polygons:polygon.use_smooth=True
    return obj,repairs


JOINTS={'Spine':((.005,.025,.91),(.005,.015,1.46)),
        'Head':((.014,.025,1.51),(.014,.02,1.90))}
for side,sign in [('Left',1),('Right',-1)]:
    JOINTS[side+'Thigh']=((sign*.13,.025,.91),(sign*.175,.005,.535))
    JOINTS[side+'Shin']=((sign*.175,.005,.535),(sign*.23,.028,.225))
    JOINTS[side+'Foot']=((sign*.23,.028,.225),(sign*.25,-.13,.08))
    JOINTS[side+'UpperArm']=((sign*.255,.026,1.455),(sign*.35,.025,1.135))
    JOINTS[side+'ForeArm']=((sign*.35,.025,1.135),(sign*.39,-.003,.935))
    JOINTS[side+'Hand']=((sign*.39,-.003,.935),(sign*.40,-.008,.78))


def armature():
    data=bpy.data.armatures.new('MazissGameSkeleton');obj=bpy.data.objects.new('MazissRig',data);bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
    for name,(head,tail) in JOINTS.items():
        bone=data.edit_bones.new(name);bone.head=head;bone.tail=tail
        if name!='Spine':
            parent='Spine'
            for end,replacement in [('Shin','Thigh'),('Foot','Shin'),('ForeArm','UpperArm'),('Hand','ForeArm')]:
                if name.endswith(end):parent=name[:-len(end)]+replacement
            bone.parent=data.edit_bones[parent]
    bpy.ops.object.mode_set(mode='OBJECT');obj.select_set(False);return obj


def is_bag(point):
    x,y,z=point
    return -.36<x<-.075 and .70<z<1.105 and (y<-.095 or y>.10 or x<-.27)


def bag_influence(point):
    x,y,z=point
    # The bag joins the source body: blend its junction into the hip instead
    # of switching a shared lower-edge triangle from Spine to Thigh abruptly.
    box=smooth(-.38,-.30,x)*(1-smooth(-.11,-.05,x))*smooth(.65,.80,z)*(1-smooth(1.08,1.14,z))
    surface=max(1-smooth(-.14,-.06,y),smooth(.06,.14,y),1-smooth(-.32,-.24,x))
    return box*surface


def weights(point):
    x,y,z=point
    if z>1.52:return {'Head':1}
    if z>.95:result={'Spine':1}
    else:
        pelvis=smooth(.78,.945,z);upper=smooth(.43,.63,z);foot=1-smooth(.265,.345,z)
        left=smooth(-.035,.035,x);result={'Spine':pelvis}
        for side,factor in [('Left',left),('Right',1-left)]:
            result[side+'Thigh']=(1-pelvis)*(1-foot)*upper*factor
            result[side+'Shin']=(1-pelvis)*(1-foot)*(1-upper)*factor
            result[side+'Foot']=(1-pelvis)*foot*factor
    # Continuous influence including fingertips and the inner forearm. Hard
    # coordinate branches previously cut shared triangles at x=.27 and z=.70.
    arm=smooth(.23,.33,abs(x))*smooth(.60,.68,z)*(1-smooth(1.39,1.51,z))
    if arm:
        result={name:value*(1-arm) for name,value in result.items()}
        side='Left' if x>0 else 'Right';upper=smooth(1.07,1.23,z);hand=1-smooth(.865,.985,z)
        result.update({side+'UpperArm':arm*upper,side+'ForeArm':arm*(1-upper)*(1-hand),side+'Hand':arm*(1-upper)*hand})
    bag=bag_influence(point)
    result={name:value*(1-bag) for name,value in result.items()}
    result['Spine']=result.get('Spine',0)+bag
    return result


def bind(obj,rig,weight_function):
    groups={}
    for vertex in obj.data.vertices:
        values=sorted(((n,v) for n,v in weight_function(vertex.co).items() if v>1e-6),key=lambda item:-item[1])[:4]
        total=sum(v for _,v in values)
        for name,value in values:
            if name not in groups:groups[name]=obj.vertex_groups.new(name=name)
            groups[name].add([vertex.index],value/total,'REPLACE')
    modifier=obj.modifiers.new('Maziss normalized game skin','ARMATURE');modifier.object=rig;modifier.use_deform_preserve_volume=False
    obj.parent=rig


def assign_regions(body):
    palette={'Hair':'503522','Skin':'c49570','Jacket':'3d574e','Shirt':'b68a45','Pants':'5d5141','Boots':'704728','Soles':'332a22','Bag':'986133','Cuffs':'a98d60','Belt':'59402a','Brass':'ac8b4e'}
    mats={n:material(n,h) for n,h in palette.items()};names=list(palette)
    for mat in mats.values():body.data.materials.append(mat)
    counts={n:0 for n in names}
    for poly in body.data.polygons:
        p=sum((body.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices);x,y,z=p
        name='Jacket'
        if z>1.84 or (z>1.755 and (y>.105 or abs(x-.014)>.145)):name='Hair'
        elif z>1.615 or (z>1.515 and abs(x-.014)<.073):name='Skin'
        elif z<.055:name='Soles'
        elif z<.245:name='Boots'
        elif z<.315:name='Cuffs'
        elif is_bag(p):name='Bag'
        elif abs(x)>.31 and z<1.11:name='Skin'
        elif abs(x)>.30 and 1.11<z<1.18:name='Cuffs'
        elif z<.935:name='Pants'
        elif z<.975 and abs(x)<.20:name='Belt'
        elif y<-.09 and abs(x-.005)<(.045+max(0,z-1.15)*.19) and z<1.45:name='Shirt'
        strap=.70*(z-1.50)+.18
        if .99<z<1.50 and abs(x-strap)<.022 and (y<-.10 or y>.11):name='Bag'
        poly.material_index=names.index(name);counts[name]+=1
    # Paint a continuous color field on the actual sculpt. Interpolation across
    # vertices avoids triangle-shaped seams from hard centroid material masks.
    colors=body.data.color_attributes.new(name='MazissPalette',type='FLOAT_COLOR',domain='POINT')
    palette_rgb={name:Vector(rgb(value)) for name,value in palette.items()}
    def between(v,a,b,edge=.015):return smooth(a-edge,a+edge,v)*(1-smooth(b-edge,b+edge,v))
    for vertex in body.data.vertices:
        x,y,z=vertex.co;ax=abs(x);color=palette_rgb['Jacket'].copy()
        def paint(name,amount):
            nonlocal color
            color=color.lerp(palette_rgb[name],max(0,min(1,amount)))
        paint('Pants',1-smooth(.93,.97,z))
        paint('Belt',between(z,.927,.968,.009)*(1-smooth(.18,.22,ax)))
        front=1-smooth(-.105,-.075,y)
        shirtwidth=.045+max(0,z-1.15)*.19
        paint('Shirt',front*(1-smooth(shirtwidth-.012,shirtwidth+.012,abs(x-.005)))*between(z,.98,1.58,.025))
        paint('Cuffs',smooth(.285,.31,ax)*between(z,1.11,1.18,.018))
        paint('Skin',smooth(.29,.325,ax)*(1-smooth(1.105,1.13,z))*smooth(.70,.74,z))
        paint('Bag',bag_influence(vertex.co))
        strap=.70*(z-1.50)+.18
        paint('Bag',(1-smooth(.014,.032,abs(x-strap)))*between(z,.99,1.50,.018)*max(1-smooth(-.12,-.095,y),smooth(.10,.135,y)))
        paint('Cuffs',1-smooth(.30,.325,z))
        paint('Boots',1-smooth(.237,.26,z))
        paint('Soles',1-smooth(.045,.061,z))
        skin=max(smooth(1.60,1.63,z),smooth(1.51,1.535,z)*(1-smooth(.067,.084,abs(x-.014))))
        paint('Skin',skin)
        hair=max(smooth(1.835,1.855,z),smooth(1.755,1.79,z)*max(smooth(.10,.13,y),smooth(.14,.17,abs(x-.014))))
        paint('Hair',hair)
        colors.data[vertex.index].color=(*color,1)
    body.data.materials.clear()
    paintmat=material('Maziss continuous cartoon palette','ffffff')
    attr=paintmat.node_tree.nodes.new('ShaderNodeVertexColor');attr.layer_name='MazissPalette'
    paintmat.node_tree.links.new(attr.outputs['Color'],paintmat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
    body.data.materials.append(paintmat)
    for poly in body.data.polygons:poly.material_index=0
    return counts


def motion(rig,body):
    source=json.loads((ROOT/'private/motion/fbx-motion.json').read_text())
    rest={name:(Vector(a),Vector(b)) for name,(a,b) in JOINTS.items()};frames=[]
    boots={side:[v.co.copy() for v in body.data.vertices if v.co.z<.265 and (v.co.x>0)==(side=='Left')] for side in ['Left','Right']}
    def canonical(v):return Vector((v[1],-v[0],v[2]))
    for sample in source['samples']:
        joints=sample['joints'];targets={};lowest=1e9
        for side in ['Left','Right']:
            k=side.lower();hip=rest[side+'Thigh'][0].copy()
            thigh=(canonical(joints[k+'Knee'])-canonical(joints[k+'Hip'])).normalized()
            shin=(canonical(joints[k+'Ankle'])-canonical(joints[k+'Knee'])).normalized()
            knee=hip+thigh*(rest[side+'Thigh'][1]-rest[side+'Thigh'][0]).length
            ankle=knee+shin*(rest[side+'Shin'][1]-rest[side+'Shin'][0]).length
            pitch=-.60*math.tanh(math.radians(sample['footPitchDeg'][k])/.60);q=Quaternion((1,0,0),pitch)
            toe=ankle+q@(rest[side+'Foot'][1]-rest[side+'Foot'][0]);targets[side+'Thigh']=(hip,knee);targets[side+'Shin']=(knee,ankle);targets[side+'Foot']=(ankle,toe)
            exact=(rest[side+'Foot'][1]-rest[side+'Foot'][0]).rotation_difference(toe-ankle)
            for point in boots[side]:lowest=min(lowest,(ankle+exact@(point-rest[side+'Foot'][0])).z)
        shift=Vector((0,0,.004-lowest));targets={name:(a+shift,b+shift) for name,(a,b) in targets.items()}
        for name in ['Spine','Head']:targets[name]=tuple(p+shift for p in rest[name])
        for side in ['Left','Right']:
            k=side.lower();shoulder=rest[side+'UpperArm'][0]+shift
            if side=='Right':
                # The supplied sculpt fuses the satchel and this hand. Keep a
                # coherent bag-side resting arm until those surfaces receive
                # separate retopology; do not stretch their shared triangles.
                for part in ['UpperArm','ForeArm','Hand']:
                    targets[side+part]=tuple(p+shift for p in rest[side+part])
                continue
            upper=(canonical(joints[k+'Elbow'])-canonical(joints[k+'Shoulder'])).normalized()
            fore=(canonical(joints[k+'Wrist'])-canonical(joints[k+'Elbow'])).normalized()
            elbow=shoulder+upper*(rest[side+'UpperArm'][1]-rest[side+'UpperArm'][0]).length
            wrist=elbow+fore*(rest[side+'ForeArm'][1]-rest[side+'ForeArm'][0]).length
            hand_dir=(wrist-elbow).normalized();hand=wrist+hand_dir*(rest[side+'Hand'][1]-rest[side+'Hand'][0]).length
            targets[side+'UpperArm']=(shoulder,elbow);targets[side+'ForeArm']=(elbow,wrist);targets[side+'Hand']=(wrist,hand)
        frames.append({name:{'head':list(a),'tail':list(b)} for name,(a,b) in targets.items()})
    idle={name:{'head':list(a),'tail':list(b)} for name,(a,b) in rest.items()}
    return {'source':source['source']['filename'],'cycleSeconds':source['cycleSeconds'],'frames':frames,'idle':idle}


def pose(rig,targets):
    # World-space matrices must be set parent first. Moving Spine after its
    # children applies the root correction twice and breaks floor contact.
    for restbone in rig.data.bones:
        name=restbone.name;target=targets[name]
        bone=rig.data.bones[name];a=Vector(target['head']);b=Vector(target['tail']);delta=(bone.tail_local-bone.head_local).normalized().rotation_difference((b-a).normalized())
        rig.pose.bones[name].matrix=Matrix.LocRotScale(a,delta@bone.matrix_local.to_quaternion(),Vector((1,1,1)));bpy.context.view_layer.update()


def bake(rig,movement):
    scene=bpy.context.scene;scene.render.fps=30;scene.frame_start=1;scene.frame_end=len(movement['frames'])-1
    for pb in rig.pose.bones:pb.rotation_mode='QUATERNION'
    for number,frame in enumerate(movement['frames'],1):
        scene.frame_set(number);pose(rig,frame)
        for pb in rig.pose.bones:
            pb.keyframe_insert(data_path='location',frame=number);pb.keyframe_insert(data_path='rotation_quaternion',frame=number)
    rig.animation_data.action.name='Maziss reference walk'
    for curve in rig.animation_data.action.fcurves:
        for key in curve.keyframe_points:key.interpolation='LINEAR'
    scene.frame_set(1)


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    body,repairs=import_body();counts=assign_regions(body);rig=armature();bind(body,rig,weights)
    from character3d_sculpt import add_facial_features
    features=add_facial_features(body,rig)
    for obj in features:
        if not obj.vertex_groups:bind(obj,rig,lambda p:{'Head':1})
        colors=obj.data.color_attributes.new(name='MazissPalette',type='FLOAT_COLOR',domain='CORNER')
        for polygon in obj.data.polygons:
            for loop in polygon.loop_indices:colors.data[loop].color=obj.data.materials[polygon.material_index].diffuse_color
    movement=motion(rig,body);bake(rig,movement)
    (OUT/'motion-private.json').write_text(json.dumps(movement,separators=(',',':')))
    # UVs describe the actual surface; no image is assigned to these regions.
    rig.animation_data.action=None;pose(rig,movement['idle'])
    bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.02);bpy.ops.object.mode_set(mode='OBJECT')
    # Restore the baked action for exchange/export.
    rig.animation_data.action=bpy.data.actions['Maziss reference walk'];bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'maziss-supplied-rig.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [body,rig,*features]:obj.select_set(True)
    bpy.context.view_layer.objects.active=rig
    bpy.ops.export_scene.gltf(filepath=str(OUT/'maziss-supplied-rig.glb'),export_format='GLB',use_selection=True,export_animations=True,export_skins=True,export_normals=True,export_texcoords=True,export_yup=True)
    report={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'repairs':repairs,'body_vertices':len(body.data.vertices),'body_triangles':len(body.data.polygons),'bones':len(rig.data.bones),'features':[obj.name for obj in features],'material_regions':counts,'source_cycle_seconds':movement['cycleSeconds'],'no_image_texture_nodes':all(n.type!='TEX_IMAGE' for mat in bpy.data.materials if mat.use_nodes for n in mat.node_tree.nodes)}
    (OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n');print('REBUILT',json.dumps(report))


if __name__=='__main__':main()
