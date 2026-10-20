"""Fitted 3D support/occlusion desk and item volumes for the painted room.

These meshes provide contact/depth, while original painted appearance remains
visible through camera holdouts. Not a complete textured export-ready desk asset.
"""
import math
import bpy
from mathutils import Vector

DESK_Z=.93
TOP_PIXELS=((1382,501),(1568,488),(1672,536),(1672,633),(1496,600))


def world_at(pixel,z):
    x,y=pixel
    return ((x-1445)/200,(744-y-200*math.cos(math.radians(23))*z)/(200*math.sin(math.radians(23))),z)


def build(scene):
    collection=bpy.data.collections.new('Fitted painted desk contact geometry')
    scene.collection.children.link(collection)
    hold=bpy.data.materials.new('Painted desk camera holdout');hold.use_nodes=True
    nodes=hold.node_tree.nodes;nodes.clear();h=nodes.new('ShaderNodeHoldout');out=nodes.new('ShaderNodeOutputMaterial')
    hold.node_tree.links.new(h.outputs[0],out.inputs['Surface'])
    objects=[]
    def adopt(obj,name):
        obj.name=name
        for c in list(obj.users_collection):c.objects.unlink(obj)
        collection.objects.link(obj);obj.data.materials.append(hold)
        obj.visible_shadow=False;obj.visible_diffuse=False;obj.visible_glossy=False
        obj['purpose']='Fitted 3D contact and depth; original painted appearance retained'
        objects.append(obj);return obj
    def box(name,location,scale):
        bpy.ops.mesh.primitive_cube_add(size=1,location=location);obj=bpy.context.object;obj.scale=scale
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        return adopt(obj,name)
    top=[Vector(world_at(p,DESK_Z)) for p in TOP_PIXELS]
    vertices=[tuple(p) for p in top]+[tuple(p-Vector((0,0,.06))) for p in top];n=len(top)
    faces=[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh=bpy.data.meshes.new('Fitted desk slab closed surface');mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new('Desk / solid fitted tabletop',mesh);collection.objects.link(obj);obj.data.materials.append(hold)
    obj.visible_shadow=False;obj.visible_diffuse=False;obj.visible_glossy=False;objects.append(obj)
    # Cabinet/far support are behind the active stool/hand approach corridor.
    box('Desk / right cabinet',world_at((1610,725),.40),(.42,.60,.80))
    box('Desk / far leg',world_at((1414,631),.40),(.085,.10,.80))
    box('Desk item / radio housing',world_at((1580,517),1.15),(.36,.22,.43))
    # Thin paper remains painted; this is its separately addressable support plane.
    paper=box('Desk item / paper',world_at((1500,551),.932),(.29,.22,.004))
    paper.hide_render=True
    for name,pixel,radius,height in [('pencil cup',(1473,518),.055,.13),('mug',(1510,513),.045,.085),('lamp base',(1640,601),.08,.025),('bowl',(1589,596),.065,.055)]:
        center=world_at(pixel,DESK_Z+height/2)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=radius,depth=height,location=center)
        adopt(bpy.context.object,'Desk item / '+name)
    pen=box('Desk item / pen',world_at((1535,573),.944),(.29,.018,.018));pen.rotation_euler[2]=math.radians(25)
    return {'supportHeight':DESK_Z,'topPixelPolygon':[list(p) for p in TOP_PIXELS],
      'topWorldPolygon':[list(p) for p in top],'objects':[o.name for o in objects],
      'appearance':'Original painted room retained; fitted 3D holdouts provide depth/contact, coarse item collision shapes'}
