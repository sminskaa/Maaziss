#!/usr/bin/env python3
"""Extract a private, bilateral FBX walk reference using Blender.

Run: blender -b --python tools/extract_fbx_walk.py -- --intake private/motion/fbx-intake.json
Animation arrays and source files must remain outside version control. The selected
source uses recorded walking takes, not a ready-made exact seamless loop.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

import bpy
from mathutils import Vector


def smoothstep(x):
    return x * x * (3 - 2 * x)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intake', type=Path, required=True)
    parser.add_argument('--source', default='02-walkforward.fbx')
    parser.add_argument('--start', type=int, default=234)
    parser.add_argument('--end', type=int, default=269)
    parser.add_argument('--output', type=Path, default=Path('private/motion/fbx-motion.json'))
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    source = next(f for f in json.loads(args.intake.read_text())['files'] if f['name'] == args.source)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=source['path'], use_anim=True)
    armature = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    bones = {b.name.split(':')[-1]: b for b in armature.pose.bones}
    mixamo = 'LeftUpLeg' in bones
    suffixes = {'Hip': 'UpLeg' if mixamo else 'Thigh',
                'Knee': 'Leg' if mixamo else 'Shin', 'Ankle': 'Foot',
                'Toe': 'ToeBase' if mixamo else 'Toe',
                'Shoulder': 'Arm', 'Elbow': 'ForeArm', 'Wrist': 'Hand'}
    mapping = {side.lower() + joint: side + suffix for side in ['Left', 'Right'] for joint, suffix in suffixes.items()}
    mapping.update(head='Head', neck='Neck', chest='Spine2' if mixamo else 'Spine4')
    fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
    period = args.end - args.start

    def capture(frame):
        bpy.context.scene.frame_set(frame)
        world = lambda n: armature.matrix_world @ bones[n].head
        origin = (world(mapping['leftHip']) + world(mapping['rightHip'])) / 2
        side = world(mapping['leftHip']) - world(mapping['rightHip'])
        side.z = 0
        side.normalize()
        forward = side.cross(Vector((0, 0, 1)))
        canonical = lambda p: [p.dot(forward), p.dot(side), p.z]
        joints = {key: canonical(world(name) - origin) for key, name in mapping.items()}
        foot_axes = {}
        for side_name in ['left', 'right']:
            matrix = (armature.matrix_world @ bones[mapping[side_name + 'Ankle']].matrix).to_3x3()
            foot_axes[side_name] = [canonical(matrix.col[k].normalized()) for k in range(3)]
        return {'joints': joints, 'root': list(origin), 'footAxes': foot_axes}

    rest = capture(1)  # Supplied setup T-pose: foot calibration only, not an idle animation.
    # Some imported head-bone tails point back toward the neck. Estimate crown
    # from head joint + neck-to-head distance rather than trusting those tails.
    head_z = (armature.matrix_world @ bones['Head'].head).z
    neck_z = (armature.matrix_world @ bones['Neck'].head).z
    rest_height = head_z + (head_z - neck_z) - min((armature.matrix_world @ b.head).z for b in armature.pose.bones)
    raw = [capture(frame) for frame in range(args.start - 1, args.end + 2)]
    cycle = raw[1:-1]
    mean_pelvis = statistics.mean(x['root'][2] for x in cycle[:-1])
    ground_z = min((x['joints'][side + 'Toe'][2] + x['root'][2]) for x in cycle for side in ['left', 'right'])

    def flatten(record):
        values = {}
        for joint, xyz in record['joints'].items():
            for k, value in enumerate(xyz):
                values[f'joints/{joint}/{k}'] = value / rest_height
        values['pelvisUp'] = (record['root'][2] - mean_pelvis) / rest_height
        for side in ['left', 'right']:
            ankle, toe = (record['joints'][side + part] for part in ['Ankle', 'Toe'])
            rest_ankle, rest_toe = (rest['joints'][side + part] for part in ['Ankle', 'Toe'])
            pitch = math.degrees(math.atan2(toe[2] - ankle[2], toe[0] - ankle[0]))
            neutral = math.degrees(math.atan2(rest_toe[2] - rest_ankle[2], rest_toe[0] - rest_ankle[0]))
            values[f'footPitchDeg/{side}'] = ((pitch - neutral + 180) % 360) - 180
            for axis, vector in enumerate(record['footAxes'][side]):
                for k, value in enumerate(vector):
                    values[f'footAxes/{side}/{axis}/{k}'] = value
        return values

    flat = [flatten(x) for x in raw]
    start, end = flat[1], flat[-2]
    deltas = {k: end[k] - start[k] for k in start}
    # Cubic correction closes position and first derivative at original timing.
    # Centered derivatives use actual samples just outside the chosen cycle.
    derivative_mismatch = {k: ((flat[-1][k] - flat[-3][k]) - (flat[2][k] - flat[0][k])) * period / 2 for k in start}
    samples = []
    corrections = []
    for i in range(period + 1):
        phase = i / period
        corrected = {k: flat[i + 1][k] - deltas[k] * smoothstep(phase) - derivative_mismatch[k] * (phase ** 3 - phase ** 2) for k in start}
        sample = {'phase': phase, 'sourceFrame': args.start + i, 'time': i / fps, 'joints': {},
                  'footPitchDeg': {}, 'footAxes': {}, 'pelvisUp': corrected['pelvisUp']}
        for joint in mapping:
            sample['joints'][joint] = [round(corrected[f'joints/{joint}/{k}'], 7) for k in range(3)]
        for side in ['left', 'right']:
            sample['footPitchDeg'][side] = round(corrected[f'footPitchDeg/{side}'], 5)
            sample['footAxes'][side] = [[round(corrected[f'footAxes/{side}/{axis}/{k}'], 7) for k in range(3)] for axis in range(3)]
        samples.append(sample)
        corrections.extend(abs(corrected[k] - flat[i + 1][k]) for k in corrected if k.startswith('joints/'))
    # Infer stride from backward movement of the low foot during stance. Root
    # translation itself is near zero in this particular FBX and cannot give speed.
    speeds = []
    for side in ['left', 'right']:
        floor = min(s['joints'][side + 'Toe'][2] + s['pelvisUp'] for s in samples[:-1])
        for a, b in zip(samples[:-1], samples[1:]):
            toe_up = a['joints'][side + 'Toe'][2] + a['pelvisUp']
            backward_speed = (a['joints'][side + 'Ankle'][0] - b['joints'][side + 'Ankle'][0]) * fps
            if toe_up < floor + .018 and backward_speed > .05:
                speeds.append(backward_speed)
    inferred_stride = statistics.median(speeds) * period / fps
    result = {
        'version': 1, 'purpose': 'Private bilateral FBX retargeting reference; do not publish source animation arrays.',
        'source': {'filename': source['name'], 'sha256': hashlib.sha256(Path(source['path']).read_bytes()).hexdigest(),
                   'frames': [args.start, args.end], 'fps': fps, 'blender': bpy.app.version_string,
                   'bothLegsExtractedIndependently': True, 'containsOriginalMesh': False},
        'coordinates': {'order': ['forward', 'left', 'up'], 'units': 'standing skeleton body heights',
                        'origin': 'per-frame midpoint of left/right hip joints',
                        'heading': 'per-frame horizontal left-minus-right hip axis; forward=left cross world-up',
                        'footPitchDeg': 'toe-axis elevation relative to setup-frame flat-foot calibration; positive toe-up',
                        'footAxes': 'foot-bone local X/Y/Z basis vectors expressed in canonical forward/left/up; renormalize after interpolation'},
        'cycleSeconds': period / fps, 'cadenceStepsPerMinute': 120 * fps / period,
        'bodyHeightMeters': rest_height, 'bodyHeightMethod': 'setup-frame head height + neck-to-head vertical length - lowest toe joint', 'meanPelvisHeight': (mean_pelvis - ground_z) / rest_height,
        'inferredStrideBodyHeights': inferred_stride,
        'rootMotion': {'actualDisplacementMeters': math.dist(cycle[0]['root'], cycle[-1]['root']),
                       'speedIsInferredFromLoadedFoot': True},
        'loopFit': {'method': 'Cubic endpoint and centered-velocity mismatch removal over the complete selected bilateral cycle.',
                    'maxJointCorrectionBodyHeights': max(corrections),
                    'rawEndpointJointRmsBodyHeights': math.sqrt(statistics.mean(v*v for k,v in deltas.items() if k.startswith('joints/'))),
                    'timingAltered': False},
        'neutral': {'sourceFrame': 1, 'isAuthoredIdle': False, 'description': 'Supplied T-pose setup: foot alignment calibration only; do not use its outstretched arms for idle.',
                    'joints': {k: [v / rest_height for v in xyz] for k, xyz in rest['joints'].items()}},
        'limitations': ['No authored idle clip supplied.', 'In-place mocap; travel stride inferred from low-foot backward velocity.',
                       'Hip-derived heading includes a little natural pelvic yaw.', 'Cubic loop closure slightly adjusts measured trajectories.'],
        'samples': samples}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['source','cycleSeconds','bodyHeightMeters','meanPelvisHeight','inferredStrideBodyHeights','rootMotion','loopFit']}, indent=2))

if __name__ == '__main__':
    main()
