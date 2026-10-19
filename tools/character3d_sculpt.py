"""Register restrained, real facial geometry to the supplied Maziss sculpt.

The input is the normalized 2 m owner mesh, front = -Y. No portrait projection,
replacement skull, image texture, or camera-facing face card is used here.
"""
import math
import bpy
from mathutils import Vector


def _linear(c):
    return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4


def _material(name, rgb):
    m = bpy.data.materials.new('Maziss face / ' + name)
    color = tuple(_linear(v) for v in rgb)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Roughness'].default_value = .86
    return m


def add_facial_features(body, armature=None, head_bone='Head'):
    """Return complete modeled eye/lid/brow/mouth objects fitted to ``body``.

    Features are separate objects for later facial rigging. With an armature,
    every vertex receives a normalized Head weight and one armature modifier.
    This does not claim that the source mesh has production facial edge loops.
    """
    skin = _material('lid skin', (.78, .57, .40))
    lower_skin = _material('lower lid warm shadow', (.66, .45, .31))
    white = _material('warm eye white', (.91, .88, .79))
    iris = _material('blue green iris', (.28, .45, .45))
    pupil = _material('pupil', (.065, .08, .075))
    glint = _material('small eye catchlight', (.98, .96, .87))
    brow = _material('dark brown brow', (.25, .14, .075))
    mouth = _material('closed mouth line', (.28, .16, .105))
    lip = _material('lower lip', (.58, .36, .25))
    made = []
    inverse = body.matrix_world.inverted()

    def front(x, z):
        a = inverse @ Vector((x, -1, z))
        d = inverse.to_3x3() @ Vector((0, 1, 0))
        hit, location, normal, index = body.ray_cast(a, d.normalized())
        return (body.matrix_world @ location).y if hit else -.14

    def finish(o, name, mat, group):
        o.name = 'Maziss facial ' + name
        o.data.materials.clear()
        o.data.materials.append(mat)
        for p in o.data.polygons:
            p.use_smooth = True
        o['part_group'] = group
        o['geometry_purpose'] = 'Supplied-sculpt facial feature; no image texture'
        if armature:
            vg = o.vertex_groups.new(name=head_bone)
            vg.add(list(range(len(o.data.vertices))), 1, 'REPLACE')
            mod = o.modifiers.new('Head follows shared rig', 'ARMATURE')
            mod.object = armature
        made.append(o)
        return o

    def ellipsoid(name, location, radii, mat, group='Eyes'):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=location)
        o = bpy.context.object
        o.scale = radii
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return finish(o, name, mat, group)

    def stroke(name, points, width, mat, group='Eyes'):
        bpy.ops.object.select_all(action='DESELECT')
        curve = bpy.data.curves.new(name, 'CURVE')
        curve.dimensions = '3D'
        curve.resolution_u = 12
        curve.bevel_depth = width
        curve.bevel_resolution = 3
        curve.use_fill_caps = True
        spline = curve.splines.new('BEZIER')
        spline.bezier_points.add(len(points) - 1)
        for p, location in zip(spline.bezier_points, points):
            p.co = location
            p.handle_left_type = p.handle_right_type = 'AUTO'
        o = bpy.data.objects.new(name, curve)
        bpy.context.collection.objects.link(o)
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        bpy.ops.object.convert(target='MESH')
        return finish(bpy.context.object, name, mat, group)

    center_x = .014
    eye_z = 1.773
    for sign in (-1, 1):
        label = 'right' if sign < 0 else 'left'
        x = center_x + sign * .063
        # Most of the eyeball is buried in the existing eye socket. At the
        # centre, its front lies approximately 8 mm ahead of the original skin.
        y = front(x, eye_z) + .005
        rx, ry, rz = .032, .013, .033
        eye = ellipsoid(label + ' eye white', (x, y, eye_z), (rx, ry, rz), white)
        # The white conforms to this sculpt's curved orbital surface, rather
        # than a flat frontal placement that would protrude at its outer edge.
        face_y = front(x, eye_z)
        for vertex in eye.data.vertices:
            vertex.co.z *= .78 if vertex.co.z > 0 else .90
            world = eye.matrix_world @ vertex.co
            vertex.co.y += front(world.x, world.z) - face_y
        eye.data.materials.append(skin)
        eye.data.update()
        # A real upper-lid surface covers the top of the globe; only the
        # almond-shaped exposed white remains. This is not a drawn eye ring.
        for polygon in eye.data.polygons:
            q = max(-1, min(1, polygon.center.x / rx))
            upper_edge = .013 * (1 - q*q)
            lower_edge = -.026 * (1 - q*q)
            if polygon.center.z > upper_edge or polygon.center.z < lower_edge:
                polygon.material_index = 1
        # Frontal gaze, restrained iris/pupil size. These are full ellipsoids,
        # not alpha decals and not repeated across the head's sides/back.
        ellipsoid(label + ' iris', (x, y - ry + .0012, eye_z-.002), (.013, .0015, .015), iris)
        ellipsoid(label + ' pupil', (x, y - ry - .0003, eye_z-.002), (.006, .0009, .0095), pupil)
        ellipsoid(label + ' catchlight', (x-.004, y-ry-.0014, eye_z+.004), (.0024, .0007, .0032), glint)
        # Modeled rims follow the eyeball/skin intersection rather than an
        # unrelated generic head. The inner corner sits a little higher.
        upper, lower = [], []
        for i in range(7):
            t = math.pi * i / 6
            px = x + rx * math.cos(t)
            pz = eye_z + .013 * math.sin(t)**2
            py = front(px,pz)-.002
            upper.append((px, py, pz))
            pz2 = eye_z - .026 * math.sin(t)**2
            py2 = front(px,pz2)-.0018
            lower.append((px, py2, pz2))
        stroke(label + ' upper eyelid', upper, .0015, skin)
        stroke(label + ' lower eyelid', lower[1:-1], .0007, lower_skin)
        # Frown brows rise toward the bridge, as in the accepted drawing.
        brow_points=[]
        for d, z in [(-.038,1.810),(-.018,1.820),(.008,1.832),(.030,1.827)]:
            px=x-sign*d
            brow_points.append((px,front(px,z)-.004,z))
        stroke(label + ' worried brow', brow_points, .0043, brow)

    mouth_points=[]
    for dx,z in [(-.039,1.648),(-.022,1.655),(0,1.658),(.022,1.655),(.039,1.648)]:
        x=center_x+dx
        mouth_points.append((x,front(x,z)-.0025,z))
    stroke('small closed frown',mouth_points,.0015,mouth,'Mouth')
    lip_points=[]
    for dx,z in [(-.024,1.644),(0,1.646),(.024,1.644)]:
        x=center_x+dx
        lip_points.append((x,front(x,z)-.001,z))
    stroke('lower lip',lip_points,.001,lip,'Mouth')
    return made
