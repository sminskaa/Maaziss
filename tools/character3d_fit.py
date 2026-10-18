"""Organic construction refinements and geometric satchel-side arm clearance.

No source painting is changed. This module works on complete Blender surfaces,
before the caller assigns projected painting coordinates. The pose solver moves
the arm around the actual satchel, rather than masking or hiding its triangles.
"""
import math
import bpy
import bmesh
from mathutils import Vector
from character3d_body import union, bind, constant, jacket_weights, JOINTS


def _apply(obj, modifier):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=modifier.name)


def _subdivide(obj, levels=1):
    """Bake round interpolation into geometry before the exported skin."""
    mod = obj.modifiers.new('Rounded illustrated silhouette', 'SUBSURF')
    mod.subdivision_type = 'CATMULL_CLARK'
    mod.levels = levels
    # Evaluate in rest space. Existing skin modifiers have identity rest pose.
    _apply(obj, mod)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True


def apply_art_geometry(armature, objects):
    objects = list(objects)
    names = {'Head', 'Jaw', 'Chin', 'Cheek-1', 'Cheek1',
             'Nose bridge', 'Nose tip'}
    face = [obj for obj in objects if obj.name in names]
    if face:
        # Remove component armatures before joining. Rebind the united surface
        # once, so no duplicate skin modifier transforms it a second time.
        for obj in face:
            for mod in list(obj.modifiers):
                if mod.type == 'ARMATURE':
                    obj.modifiers.remove(mod)
        objects = [obj for obj in objects if obj not in face]
        # Keep Head as the surviving name, regardless of construction ordering.
        face.sort(key=lambda obj: obj.name != 'Head')
        head = union('Head', face, .0055)
        head.vertex_groups.clear()
        head['part_group'] = 'Head and neck'
        bind(head, armature, constant('Head'))
        _subdivide(head)
        objects.append(head)
    for obj in objects:
        if obj.get('part_group') == 'Eyes':
            sign = -1 if obj.name.endswith('-1') else 1
            center = Vector((sign*.065, -.187, 1.791))
            # Every eye, iris, lid, highlight and brow shares one transform.
            # Moving only the sclera leaves floating lid and pupil rings.
            for vertex in obj.data.vertices:
                world = obj.matrix_world @ vertex.co
                local = world-center
                target = center+Vector((local.x*.64, local.y*.64+.002,
                                        local.z*.75))
                vertex.co = obj.matrix_world.inverted() @ target
        if obj.name.startswith(('Hair tuft', 'Fringe', 'Sideburn')):
            _subdivide(obj)
        if obj.get('part_group') == 'Hair':
            inverse = obj.matrix_world.inverted()
            for vertex in obj.data.vertices:
                world = obj.matrix_world @ vertex.co
                excess = max(0, world.z-1.925)
                # Keep a messy silhouette, but compress the spikes beyond the
                # rounded scalp. Quadratic onset avoids a horizontal hard seam.
                world.z -= .52*excess*excess/(excess+.018)
                vertex.co = inverse @ world
        if obj.name.startswith(('Ear', 'Ear inset')):
            inverse = obj.matrix_world.inverted()
            sign = -1 if obj.name.endswith('-1') else 1
            center = Vector((sign*.151,-.047,1.755))
            for vertex in obj.data.vertices:
                world = obj.matrix_world @ vertex.co
                offset = world-center
                world = center+Vector((offset.x*.72-sign*.005,
                                       offset.y*.88,offset.z*.92))
                vertex.co = inverse @ world
        if obj.name == 'Neck':
            inverse = obj.matrix_world.inverted()
            center = Vector((0,-.055,1.535))
            for vertex in obj.data.vertices:
                world = obj.matrix_world @ vertex.co
                offset = world-center
                # A softer, broader throat keeps the head attached to a real
                # neck rather than a narrow straight stem. Height is unchanged.
                shoulder_blend = max(0, min(1, (1.58-world.z)/.13))
                offset.x *= 1.12+.12*shoulder_blend
                offset.y *= 1.10+.08*shoulder_blend
                vertex.co = inverse @ (center+offset)
        if obj.name == 'Jacket':
            inverse = obj.matrix_world.inverted()
            for vertex in obj.data.vertices:
                world = obj.matrix_world @ vertex.co
                side = max(0, min(1, (abs(world.x)-.13)/.13))
                top = max(0, min(1, (world.z-1.36)/.15))
                # Sleeve caps previously formed pointed shoulder epaulettes.
                world.z -= .020*side*side*(3-2*side)*top*top*(3-2*top)
                vertex.co = inverse @ world
            soften = obj.modifiers.new('Soft jacket tailoring', 'SMOOTH')
            soften.factor = .5
            soften.iterations = 6
            _apply(obj, soften)
            _subdivide(obj)
        if obj.name in ('Shirt', 'BodyCore', 'Belt'):
            _subdivide(obj)
        obj['rounded_art_fit'] = True
    # Projected portrait already contains the stubble. Tiny separate sphere
    # specks would hover in front of that original painted expression.
    for obj in list(objects):
        if obj.name.startswith('Stubble '):
            objects.remove(obj)
            bpy.data.objects.remove(obj, do_unlink=True)
    for side in ('Left', 'Right'):
        elbow = Vector(JOINTS[side+'elbow'])
        shoulder = Vector(JOINTS[side+'shoulder'])
        axis = (elbow-shoulder).normalized()
        bpy.ops.mesh.primitive_torus_add(major_radius=.064, minor_radius=.012,
                                        major_segments=32, minor_segments=10,
                                        location=elbow+axis*.008)
        cuff = bpy.context.object
        cuff.name = side+'RolledCuff'
        cuff.rotation_mode = 'QUATERNION'
        cuff.rotation_quaternion = Vector((0,0,1)).rotation_difference(axis)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        cuff.data.materials.append(bpy.data.materials['JacketTeal'])
        for polygon in cuff.data.polygons:
            polygon.use_smooth = True
        cuff['part_group'] = 'Jacket'
        bind(cuff, armature, jacket_weights)
        objects.append(cuff)
    for obj in objects:
        # Blender's converted beveled curves have coincident, separate cap
        # rings. Weld their seams without deleting any visible surface.
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=.000001)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(obj.data)
        bm.free()
        if not any(mod.type == 'ARMATURE' for mod in obj.modifiers):
            mod = obj.modifiers.new('Complete part anatomical skin', 'ARMATURE')
            mod.object = armature
            mod.use_deform_preserve_volume = True
    return objects


def _elbow(shoulder, wrist, length_a, length_b, preferred):
    axis = wrist-shoulder
    distance = axis.length
    if distance < 1e-8:
        return shoulder+Vector((0, 0, -length_a))
    axis /= distance
    axial = (length_a*length_a-length_b*length_b+distance*distance)/(2*distance)
    radius = math.sqrt(max(0, length_a*length_a-axial*axial))
    bend = preferred-axis*preferred.dot(axis)
    if bend.length < 1e-7:
        bend = Vector((0, -1, 0))-axis*Vector((0, -1, 0)).dot(axis)
    return shoulder+axis*axial+bend.normalized()*radius


def adjust_arm_targets(targets, rest, objects):
    """Fixed-length two-bone IK around the right-hip tool satchel.

    A broad, smooth outward bias replaces phase-local wrist clamping. The
    forearm, palm and fingers keep their own geometry and remain visible.
    The actual model-wide bag extent determines the protected X plane.
    """
    if 'RightHand' not in targets:
        return targets
    bag = [obj for obj in objects if obj.get('part_group') == 'Bag'
           and obj.name != 'Shoulder strap']
    min_x = min((float((obj.matrix_world @ vertex.co).x)
                 for obj in bag for vertex in obj.data.vertices), default=-.326)
    shoulder = targets['RightUpperArm'][0].copy()
    original_elbow = targets['RightUpperArm'][1].copy()
    original_wrist = targets['RightForeArm'][1].copy()
    length_a = (rest['RightUpperArm'][1]-rest['RightUpperArm'][0]).length
    length_b = (rest['RightForeArm'][1]-rest['RightForeArm'][0]).length
    hand_length = (rest['RightHand'][1]-rest['RightHand'][0]).length
    # The palm radius is .038m. Add 12mm leather/hand clearance.
    safe_x = min_x-.050
    # Soft minimum, continuous in value and derivative through the whole walk.
    softness = .014
    wrist = original_wrist.copy()
    delta = original_wrist.x-safe_x
    wrist.x = safe_x-.5*(math.sqrt(delta*delta+softness*softness)-delta)
    # Preserve length without a stretched arm at the lowest original wrist.
    direction = wrist-shoulder
    reach = (length_a+length_b)*.975
    if direction.length > reach:
        # Keep protected lateral clearance while lifting the wrist naturally.
        transverse = (wrist.x-shoulder.x)**2+(wrist.y-shoulder.y)**2
        wrist.z = shoulder.z-math.sqrt(max(.0001, reach*reach-transverse))
    # Bend slightly outward and forward, away from tool handles at the bag top.
    # The circular IK locus preserves BOTH original bone lengths exactly.
    elbow = _elbow(shoulder, wrist, length_a, length_b, Vector((-.7,-.6,.1)))
    hand_direction = (wrist-elbow).normalized()
    # Fingers hang mostly down instead of curling back into the satchel.
    hand_direction = (hand_direction+Vector((-.15,0,-.35))).normalized()
    targets['RightUpperArm'] = (shoulder, elbow)
    targets['RightForeArm'] = (elbow, wrist)
    targets['RightHand'] = (wrist, wrist+hand_direction*hand_length)
    return targets
