"""Closed, skinned Maziss construction study for Blender 4.3+.

This is original procedural geometry, not a reconstruction of unseen sprite pixels.
Call build_body() in an empty scene. Coordinates are X anatomical left, Y rear,
Z up. Every exported mesh uses world/rest coordinates and normalized bone groups.
"""
import math
import bpy
from mathutils import Vector

JOINTS = {
    'pelvis': (0, 0, .90), 'shoulders': (0, -.025, 1.48),
    'head_base': (0, -.06, 1.52), 'head_top': (0, -.08, 1.90),
}
for _side, _sign in [('Left', 1), ('Right', -1)]:
    for _part, _point in {'hip': (.095, 0, .90), 'knee': (.10, -.018, .54),
                         'ankle': (.10, 0, .19), 'toe': (.10, -.16, .07),
                         'shoulder': (.20, -.025, 1.48), 'elbow': (.25, -.045, 1.18),
                         'wrist': (.27, -.075, .94), 'hand': (.275, -.095, .84)}.items():
        JOINTS[_side + _part] = (_point[0] * _sign, _point[1], _point[2])


def material(name, color):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = .82
    return mat


def mesh(name, vertices, faces, mat):
    data = bpy.data.meshes.new(name + 'Mesh')
    data.from_pydata(vertices, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    for poly in data.polygons:
        poly.use_smooth = True
    return obj


def loft(name, rings, mat, segments=20):
    """Closed horizontal elliptical rings [(cx,cy,z,rx,ry), ...]."""
    vertices = []
    for x, y, z, rx, ry in rings:
        vertices.extend((x + rx * math.cos(2 * math.pi * i / segments),
                         y + ry * math.sin(2 * math.pi * i / segments), z)
                        for i in range(segments))
    faces = []
    for row in range(len(rings) - 1):
        a, b = row * segments, (row + 1) * segments
        faces.extend((a + i, a + (i + 1) % segments,
                      b + (i + 1) % segments, b + i) for i in range(segments))
    faces.append(tuple(reversed(range(segments))))
    faces.append(tuple((len(rings) - 1) * segments + i for i in range(segments)))
    return mesh(name, vertices, faces, mat)


def limb(name, start, end, r0, r1, mat, sides=16, rings=9, depth=.84):
    a, b = Vector(start), Vector(end)
    axis = (b - a).normalized()
    a -= axis * .012
    b += axis * .012
    u = axis.cross(Vector((0, 1, 0))).normalized()
    v = axis.cross(u).normalized()
    vertices = []
    for row in range(rings):
        t = row / (rings - 1)
        center = a.lerp(b, t)
        radius = r0 * (1 - t) + r1 * t
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            vertices.append(tuple(center + radius * math.cos(angle) * u +
                                  radius * depth * math.sin(angle) * v))
    faces = []
    for row in range(rings - 1):
        a0, b0 = row * sides, (row + 1) * sides
        faces.extend((a0 + i, a0 + (i + 1) % sides,
                      b0 + (i + 1) % sides, b0 + i) for i in range(sides))
    faces.extend([tuple(reversed(range(sides))),
                  tuple((rings - 1) * sides + i for i in range(sides))])
    return mesh(name, vertices, faces, mat)


def ellipsoid(name, center, scale, mat, segments=20, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings,
                                       location=center)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.data.materials.append(mat)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


def union(name, parts, voxel=.012):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = name
    remesh = obj.modifiers.new('Closed garment union', 'REMESH')
    remesh.mode = 'VOXEL'
    remesh.voxel_size = voxel
    remesh.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    smooth = obj.modifiers.new('Soft construction edges', 'SMOOTH')
    smooth.factor = .30
    smooth.iterations = 2
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    return obj


def make_armature():
    data = bpy.data.armatures.new('MazissConstructionSkeleton')
    armature = bpy.data.objects.new('MazissConstructionRig', data)
    bpy.context.collection.objects.link(armature)
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    def bone(name, head, tail, parent=None):
        item = data.edit_bones.new(name)
        item.head, item.tail = head, tail
        if parent:
            item.parent = data.edit_bones[parent]
        return item
    bone('Spine', JOINTS['pelvis'], JOINTS['shoulders'])
    bone('Head', JOINTS['head_base'], JOINTS['head_top'], 'Spine')
    for side in ('Left', 'Right'):
        bone(side + 'Thigh', JOINTS[side+'hip'], JOINTS[side+'knee'], 'Spine')
        bone(side + 'Shin', JOINTS[side+'knee'], JOINTS[side+'ankle'], side+'Thigh')
        bone(side + 'Foot', JOINTS[side+'ankle'], JOINTS[side+'toe'], side+'Shin')
        bone(side + 'UpperArm', JOINTS[side+'shoulder'], JOINTS[side+'elbow'], 'Spine')
        bone(side + 'ForeArm', JOINTS[side+'elbow'], JOINTS[side+'wrist'], side+'UpperArm')
        bone(side + 'Hand', JOINTS[side+'wrist'], JOINTS[side+'hand'], side+'ForeArm')
    bpy.ops.object.mode_set(mode='OBJECT')
    armature.select_set(False)
    return armature


def smoothstep(a, b, value):
    t = max(0, min(1, (value-a)/(b-a)))
    return t*t*(3-2*t)


def bind(obj, armature, weight_function):
    groups = {}
    for vertex in obj.data.vertices:
        weights = {name: max(0, weight) for name, weight in weight_function(vertex.co).items()
                   if weight > 1e-7}
        total = sum(weights.values())
        if total <= 0:
            weights, total = {'Spine': 1}, 1
        for name, value in weights.items():
            if name not in groups:
                groups[name] = obj.vertex_groups.new(name=name)
            groups[name].add([vertex.index], value / total, 'REPLACE')
    mod = obj.modifiers.new('Anatomical skin', 'ARMATURE')
    mod.object = armature
    mod.use_deform_preserve_volume = True
    obj['construction_part'] = True
    return obj


def constant(name):
    return lambda point: {name: 1}


def leg_weights(point):
    x, y, z = point
    side = 'Left' if x >= 0 else 'Right'
    # The complete waist belongs to the pelvis. Letting the thighs tug vertices
    # as high as the belt folds the upper shell through the rigid shirt/belt.
    pelvis = smoothstep(.73, .86, z)
    upper = smoothstep(.44, .64, z)
    return {'Spine': pelvis, side+'Thigh': (1-pelvis)*upper,
            side+'Shin': (1-pelvis)*(1-upper)}


def jacket_weights(point):
    x, y, z = point
    side = 'Left' if x >= 0 else 'Right'
    arm = smoothstep(.145, .225, abs(x))
    # Underarm and shoulder form a continuous skinned transition.
    arm *= 1-smoothstep(1.47, 1.56, z)
    forearm = 1-smoothstep(1.12, 1.24, z)
    return {'Spine': 1-arm, side+'UpperArm': arm*(1-forearm), side+'ForeArm': arm*forearm}


def jacket_shell(mat):
    """Thick closed C-section coat; shirt remains visible through front opening."""
    profile = [(.925,.151,.109,.020), (1.01,.153,.113,.015),
               (1.15,.171,.121,.002), (1.32,.204,.131,-.015),
               (1.43,.226,.118,-.025), (1.49,.198,.097,-.025)]
    segments = 28
    vertices = []
    # Arc excludes the center-front: -Y front, +Y rear.
    start, end = -math.pi*.34, math.pi*1.34
    for inner in (False, True):
        for z, rx, ry, cy in profile:
            ry += .025  # Clearance around the complete underlying shirt.
            for i in range(segments):
                a = start + (end-start)*i/(segments-1)
                vertices.append(((rx-(.028 if inner else 0))*math.cos(a),
                                 cy+(ry-(.028 if inner else 0))*math.sin(a), z))
    rows = len(profile)
    n = rows*segments
    faces = []
    for inside in (0,1):
        offset = inside*n
        for row in range(rows-1):
            for i in range(segments-1):
                quad = (offset+row*segments+i, offset+row*segments+i+1,
                        offset+(row+1)*segments+i+1, offset+(row+1)*segments+i)
                faces.append(tuple(reversed(quad)) if inside else quad)
    for row in (0,rows-1):
        for i in range(segments-1):
            a = row*segments+i
            faces.append((a,a+1,a+1+n,a+n))
    for i in (0,segments-1):
        for row in range(rows-1):
            a = row*segments+i
            faces.append((a,a+segments,a+segments+n,a+n))
    return mesh('JacketCore', vertices, faces, mat)


def build_body():
    mats = {name: material(name, color) for name,color in {
        'Skin': (.55,.29,.16), 'JacketTeal': (.075,.18,.16),
        'ShirtMustard': (.57,.32,.095), 'PantsUmber': (.17,.145,.105),
        'BootLeather': (.20,.09,.035), 'BootSole': (.075,.045,.024),
        'BeltLeather': (.18,.085,.03), 'BuckleBrass': (.47,.30,.09),
    }.items()}
    armature = make_armature()
    objects = []
    def add(obj, weights):
        objects.append(bind(obj, armature, weights))
        return obj
    # Closed anatomy stays present beneath clothing and can be isolated in review.
    add(loft('BodyCore', [(0,0,.79,.12,.08),(0,0,.95,.14,.09),
                         (0,-.008,1.13,.14,.085),(0,-.02,1.34,.185,.095),
                         (0,-.025,1.46,.16,.078)], mats['Skin']), constant('Spine'))
    for side, sign in [('Left',1),('Right',-1)]:
        add(limb(side+'UpperArm', JOINTS[side+'shoulder'], JOINTS[side+'elbow'],
                 .057,.043,mats['Skin']), jacket_weights)
        add(limb(side+'ForeArm', JOINTS[side+'elbow'], JOINTS[side+'wrist'],
                 .043,.030,mats['Skin']), constant(side+'ForeArm'))
        palm = ellipsoid(side+'Hand', (sign*.274,-.079,.898), (.038,.032,.066), mats['Skin'])
        thumb = ellipsoid(side+'Thumb', (sign*.247,-.103,.915), (.022,.023,.039), mats['Skin'])
        add(union(side+'Hand',[palm,thumb],.007), constant(side+'Hand'))
        add(limb(side+'Thigh',JOINTS[side+'hip'],JOINTS[side+'knee'],.063,.052,mats['Skin']), leg_weights)
        # Match the surrounding trouser knee blend. A rigid shin below a blended
        # trouser knee protruded through the fabric during knee flexion.
        add(limb(side+'Shin',JOINTS[side+'knee'],JOINTS[side+'ankle'],.052,.033,mats['Skin']), leg_weights)
        add(ellipsoid(side+'Foot',(sign*.10,-.055,.091),(.050,.114,.069),mats['Skin']),constant(side+'Foot'))
    add(loft('Shirt',[(0,0,.91,.149,.102),(0,0,1.04,.151,.104),
                      (0,-.012,1.20,.166,.109),(0,-.025,1.39,.198,.110),
                      (0,-.035,1.47,.165,.093)],mats['ShirtMustard']),constant('Spine'))
    # Trousers are ONE welded shell across waist, hips and both legs.
    pants_parts=[loft('PantsWaist',[(0,0,.77,.161,.109),(0,.004,.87,.17,.114),
                                   (0,.002,.96,.156,.105)],mats['PantsUmber'])]
    for side,sign in [('Left',1),('Right',-1)]:
        pants_parts.append(loft(side+'PantsLeg',[
            (sign*.10,0,.205,.056,.057),(sign*.10,0,.26,.059,.060),
            (sign*.10,-.009,.42,.065,.066),(sign*.10,-.018,.54,.068,.065),
            (sign*.10,-.008,.68,.080,.079),(sign*.095,0,.82,.090,.091),
            (sign*.086,0,.89,.085,.093)],mats['PantsUmber']))
    add(union('Pants',pants_parts,.012),leg_weights)
    jacket_parts=[jacket_shell(mats['JacketTeal'])]
    for side,sign in [('Left',1),('Right',-1)]:
        jacket_parts.append(limb(side+'Sleeve',
            (sign*.18,-.025,1.49),(sign*.255,-.045,1.16),.084,.062,mats['JacketTeal'],rings=10))
    # Fine voxel size retains the open coat's continuous thick fabric.
    add(union('Jacket',jacket_parts,.012),jacket_weights)
    # Belt is a closed thick elliptical ring, not a cap covering the shirt.
    belt_rings=[(0,0,.913,.159,.108),(0,0,.955,.159,.108)]
    belt=loft('Belt',belt_rings,mats['BeltLeather'])
    # A belt may overlap trousers; its continuity does not depend on alpha masks.
    add(belt,constant('Spine'))
    add(ellipsoid('BeltBuckle',(0,-.111,.934),(.035,.012,.029),mats['BuckleBrass'],16,8),constant('Spine'))
    for side,sign in [('Left',1),('Right',-1)]:
        x=sign*.10
        shaft=loft(side+'BootShaft',[(x,.005,.06,.063,.070),(x,.005,.12,.065,.075),
                                  (x,.006,.22,.055,.059),(x,.006,.28,.060,.063)],mats['BootLeather'])
        toe=ellipsoid(side+'BootToe',(x,-.085,.095),(.072,.145,.069),mats['BootLeather'])
        boot=union(side+'Boot',[shaft,toe],.009)
        add(boot,constant(side+'Foot'))
        sole=loft(side+'BootSole',[(x,-.067,.018,.074,.150),(x,-.067,.042,.076,.151),
                                 (x,-.067,.055,.073,.147)],mats['BootSole'],24)
        add(sole,constant(side+'Foot'))
    for obj in objects:
        obj['representation']='Closed 3D construction study; original approved painted art retained separately'
        obj['category']='anatomy' if obj.name in ['BodyCore'] or any(obj.name==s+p for s in ('Left','Right') for p in ('UpperArm','ForeArm','Hand','Thigh','Shin','Foot')) else 'clothing'
    return {'armature':armature,'objects':objects}


def validate_body(result):
    """Read-only topology/weight facts for the construction acceptance report."""
    import bmesh
    items=[]
    for obj in result['objects']:
        bm=bmesh.new(); bm.from_mesh(obj.data)
        bad=sum(not edge.is_manifold for edge in bm.edges)
        unseen=set(bm.verts)
        components=[]
        while unseen:
            seed=unseen.pop(); frontier=[seed]; count=0
            while frontier:
                current=frontier.pop(); count+=1
                for edge in current.link_edges:
                    other=edge.other_vert(current)
                    if other in unseen:
                        unseen.remove(other); frontier.append(other)
            components.append(count)
        bm.free()
        sums=[sum(group.weight for group in vertex.groups) for vertex in obj.data.vertices]
        items.append({'name':obj.name,'vertices':len(obj.data.vertices),'nonManifoldEdges':bad,'connectedComponents':len(components),
                      'unweightedVertices':sum(value<.999 or value>1.001 for value in sums),
                      'armatureModifiers':sum(mod.type=='ARMATURE' for mod in obj.modifiers)})
    return {'vertices':sum(item['vertices'] for item in items),'objects':items,
            'pass':all(item['nonManifoldEdges']==0 and item['connectedComponents']==1 and item['unweightedVertices']==0 and item['armatureModifiers']==1 for item in items)}
