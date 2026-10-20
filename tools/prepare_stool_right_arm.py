#!/usr/bin/env python3
"""Private local right-arm separation for the stool study; original sculpt untouched.
Run with Blender. The free supplied left arm supplies the mirrored closed arm.
"""
from pathlib import Path
import sys,json,hashlib,math
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_supplied_character import weights,bind,rgb,pose,bag_influence,smooth
SOURCE=ROOT/'build/checks/supplied-character/maziss-supplied-rig.blend'
OUT=ROOT/'build/checks/stool-slide'

def cap(bm):
    edges=[e for e in bm.edges if e.is_boundary]
    if edges:bmesh.ops.holes_fill(bm,edges=edges,sides=0)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))

def main():
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'art').mkdir(exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    rig=bpy.data.objects['MazissRig'];rig.animation_data_clear()
    for p in rig.pose.bones:p.matrix_basis.identity()
    body=bpy.data.objects['Maziss supplied sculpt']
    arm=body.copy();arm.data=body.data.copy();arm.name='Right arm';bpy.context.collection.objects.link(arm)
    bm=bmesh.new();bm.from_mesh(arm.data)
    # Two clean planes isolate the supplied free arm without inventing a hand.
    for point,normal in [((.26,0,0),(1,0,0)),((0,0,1.475),(0,0,-1)),((0,0,.69),(0,0,1))]:
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=point,plane_no=normal,clear_inner=True,clear_outer=False)
    cap(bm)
    for v in bm.verts:v.co.x=-v.co.x
    bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(arm.data);bm.free()
    arm.vertex_groups.clear();arm.modifiers.clear()
    def right_weights(p):
        z=p.z;u=max(0,min(1,(z-1.07)/.16));u=u*u*(3-2*u)
        h=max(0,min(1,(.985-z)/.12));h=h*h*(3-2*h)
        return {'RightUpperArm':u,'RightForeArm':(1-u)*(1-h),'RightHand':(1-u)*h}
    bind(arm,rig,right_weights)
    # Retire the fused outer arm, preserving the original satchel's inner shell.
    # Closing the local boundary produces a real bag side/torso, not a hidden hole.
    bm=bmesh.new();bm.from_mesh(body.data)
    def remove(p):
        x,y,z=p
        if not .69<z<1.485:return False
        cutoff=.305 if z<1.11 else .305-(min(z,1.46)-1.11)*.10
        return x < -cutoff
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if remove(v.co)],context='VERTS')
    bmesh.ops.delete(bm,geom=[e for e in bm.edges if not e.link_faces],context='EDGES')
    cap(bm)
    colors=bm.verts.layers.float_color.get('MazissPalette')
    if colors:
        for v in bm.verts:
            if v.co.x<-.265 and .69<v.co.z<1.115:v[colors]=(*rgb('986133'),1)
    bm.to_mesh(body.data);bm.free()
    # The remaining satchel and old junction never receive right-arm movement.
    for name in ('RightUpperArm','RightForeArm','RightHand'):
        group=body.vertex_groups.get(name)
        if group:
            spine=body.vertex_groups.get('Spine') or body.vertex_groups.new(name='Spine')
            for v in body.data.vertices:
                amount=sum(g.weight for g in v.groups if g.group==group.index)
                if amount:
                    old=sum(g.weight for g in v.groups if g.group==spine.index)
                    spine.add([v.index],old+amount,'REPLACE')
            body.vertex_groups.remove(group)
    # Retain continuous supplied satchel/strap geometry, but hang its shell
    # farther outboard so a seated pelvis does not drive it into the seat.
    # The original smooth bag field tapers to zero at the hip and strap.
    bag_shift=[]
    for v in body.data.vertices:
        amount=bag_influence(v.co)
        if amount>0:
            displacement=.10*amount*(1-smooth(.99,1.23,v.co.z))
            v.co.x-=displacement
            bag_shift.append(displacement)
    for obj in (body,arm):
        for p in obj.data.polygons:p.use_smooth=True
        obj.data.update()
    report={'source':str(SOURCE.relative_to(ROOT)),'sourceSHA256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'method':'locally cap retired fused outer arm and original bag shell; mirror supplied free left arm; bind mirrored closed mesh only to actual Right bones','bagLateralShiftMaximum':max(bag_shift),'bagShiftVertexCount':len(bag_shift),'meshes':{}}
    for obj in (body,arm):
        bm=bmesh.new();bm.from_mesh(obj.data)
        report['meshes'][obj.name]={'vertices':len(bm.verts),'faces':len(bm.faces),'boundaryEdges':sum(e.is_boundary for e in bm.edges),'nonManifoldEdges':sum(not e.is_manifold for e in bm.edges)};bm.free()
    target=OUT/'character-right-arm.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(target))
    report['outputSHA256']=hashlib.sha256(target.read_bytes()).hexdigest()
    (OUT/'art/right-arm-topology.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
