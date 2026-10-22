"""Fixed-spot, planted-foot sitting study for the supplied Maziss skeleton.

Run inside Blender; importing this module does not alter a scene. Coordinate
convention follows build_supplied_character: front is -Y, up is +Z. Seat and
floor are real world landmarks, never inferred from a changing image bound.
"""
import math
from mathutils import Vector, Quaternion
from build_supplied_character import JOINTS
from character3d_fit import _elbow

SEAT_HEIGHT = .43
SEATED_PELVIS_HEIGHT = .56
SEATED_PELVIS_BACK = .365
SIT_SECONDS = 2.0
SEAT_CONTACT = (0.005, .365, SEAT_HEIGHT)
FOOT_CONTACTS = {side: (sign * .25, -.13, 0.0)
                 for side, sign in [('Left', 1), ('Right', -1)]}


def _ease(value):
    value = max(0.0, min(1.0, value))
    return value * value * value * (10 + value * (-15 + 6 * value))


def targets_at(t):
    """Return complete head/tail targets for stand (0) through seated (1).

    Feet remain in the same floor-supported pose. Hip travel is solved through
    fixed-length two-bone leg IK, so knees bend continuously rather than popping
    or shortening the trousers. An early forward lean prepares the descent;
    the chest returns close to upright as weight arrives on the seat.
    """
    t = max(0.0, min(1.0, float(t)))
    rest = {name: tuple(Vector(p) for p in pair) for name, pair in JOINTS.items()}
    travel = _ease((t - .12) / .80)
    prepare = _ease(t / .30)
    recover = _ease((t - .48) / .49)
    lean = math.radians(21 * prepare - 16 * recover)
    rotation = Quaternion((1, 0, 0), lean)
    pivot = rest['Spine'][0]
    hip = Vector((pivot.x,
                  pivot.y + (SEATED_PELVIS_BACK - pivot.y) * travel,
                  pivot.z + (SEATED_PELVIS_HEIGHT - pivot.z) * travel))

    def torso_point(point):
        return hip + rotation @ (point - pivot)

    targets = {}
    for name in ('Spine', 'Head'):
        targets[name] = tuple(torso_point(p) for p in rest[name])
    for side, sign in [('Left', 1), ('Right', -1)]:
        original_hip, original_knee = rest[side + 'Thigh']
        original_ankle = rest[side + 'Shin'][1]
        # Pelvis translates without shrinking its width. Legs flex in their
        # forward plane while ankles/complete boots remain unrotated.
        leg_hip = original_hip + hip - pivot
        rest_bend = original_knee - (original_hip + original_ankle) * .5
        bend_direction = rest_bend.normalized().lerp(Vector((sign * .08, -1, .02)).normalized(), travel).normalized()
        knee = _elbow(leg_hip, original_ankle,
                      (original_knee - original_hip).length,
                      (original_ankle - original_knee).length,
                      bend_direction)
        targets[side + 'Thigh'] = (leg_hip, knee)
        targets[side + 'Shin'] = (knee, original_ankle)
        targets[side + 'Foot'] = rest[side + 'Foot']
        if side == 'Right':
            # Hand and satchel share source triangles. Preserve their common
            # torso transform rather than tearing this known fused junction.
            for part in ('UpperArm', 'ForeArm', 'Hand'):
                targets[side + part] = tuple(torso_point(p) for p in rest[side + part])
            continue
        shoulder = torso_point(rest[side + 'UpperArm'][0])
        arm_up = (rest[side + 'UpperArm'][1] - rest[side + 'UpperArm'][0]).length
        arm_low = (rest[side + 'ForeArm'][1] - rest[side + 'ForeArm'][0]).length
        hand_length = (rest[side + 'Hand'][1] - rest[side + 'Hand'][0]).length
        arm_blend = _ease((t - .13) / .72)
        original_wrist = torso_point(rest[side + 'ForeArm'][1])
        # The free hand eases ahead, above the near thigh, without flailing.
        seated_wrist = Vector((.33, -.055, .70))
        wrist = original_wrist.lerp(seated_wrist, arm_blend)
        maximum = (arm_up + arm_low) * .998
        if (wrist - shoulder).length > maximum:
            wrist = shoulder + (wrist - shoulder).normalized() * maximum
        elbow = _elbow(shoulder, wrist, arm_up, arm_low,
                       Vector((.35, .10, -.9)))
        hand_direction = (rotation @ (rest[side + 'Hand'][1] - rest[side + 'Hand'][0])).normalized()
        hand_direction = hand_direction.lerp(Vector((-.12, -.93, -.35)).normalized(), arm_blend).normalized()
        hand = wrist + hand_direction * hand_length
        targets[side + 'UpperArm'] = (shoulder, elbow)
        targets[side + 'ForeArm'] = (elbow, wrist)
        targets[side + 'Hand'] = (wrist, hand)
    return {name: {'head': list(pair[0]), 'tail': list(pair[1])}
            for name, pair in targets.items()}
