"""ART-012 authored world-space stool pull/sit targets; import has no scene edits.

Blender Python module. +Z up, front -Y, root yaw about +Z in degrees.
The retained sculpt/rig and bone lengths are unchanged. Right hand remains
rigid relative to the torso because its surface is joined to the source bag.
"""
import json
import math
from functools import lru_cache
from pathlib import Path
from mathutils import Vector, Quaternion
from build_supplied_character import JOINTS
from character3d_fit import _elbow

DURATION = 7.8
FPS = 20
KEY_TIMES = (0., 1.2, 2.5, 4., 4.6, 5.8, 7.8)
SEAT_HEIGHT = .568
SEATED_PELVIS_HEIGHT = .698
REST = {n: tuple(Vector(p) for p in pair) for n, pair in JOINTS.items()}
LENGTHS = {n: (p[1]-p[0]).length for n,p in REST.items()}
START = Vector((-1.7,-.9,0))
APPROACH = Vector((-.63,-.55,0))
PULL_END = Vector((-.88,-.72,0))
STOOL_END = Vector((-.38,-.32,0))
FINAL_YAW = 25.
# Seat marker (.005,.365,.568) must stay centered on the moved stool.
FINAL = STOOL_END - Quaternion((0,0,1),math.radians(FINAL_YAW)) @ Vector((.005,.365,0))
RIM = Vector((-.17,-.12,.56))


def _ease(t):
    t=max(0.,min(1.,t))
    return t*t*t*(10+t*(-15+6*t))


def _q(yaw):
    return Quaternion((0,0,1), math.radians(yaw))


@lru_cache(maxsize=1)
def _motion():
    return json.loads((Path(__file__).resolve().parents[1]/'build/checks/supplied-character/motion-private.json').read_text())


@lru_cache(maxsize=1)
def _stride_metres():
    frames=_motion()['frames']
    return sum(max(f[side+'Foot']['head'][1] for f in frames)-
               min(f[side+'Foot']['head'][1] for f in frames)
               for side in ('Left','Right'))


def _gait(seconds, amount):
    """Interpolate retained FBX directions without interpolating bone lengths."""
    motion=_motion(); frames=motion['frames']; f=seconds/motion['cycleSeconds']*len(frames)
    a,b=frames[int(f)%len(frames)],frames[(int(f)+1)%len(frames)]
    result={}
    for side in ('Left','Right'):
        parent=None
        for part in ('Thigh','Shin','Foot'):
            name=side+part
            va=Vector(a[name]['tail'])-Vector(a[name]['head'])
            vb=Vector(b[name]['tail'])-Vector(b[name]['head'])
            direction=(REST[name][1]-REST[name][0]).normalized().lerp(va.normalized().lerp(vb.normalized(),f%1).normalized(),amount).normalized()
            head=REST[name][0] if parent is None else parent
            tail=head+direction*LENGTHS[name]; result[name]=(head,tail); parent=tail
    shift=Vector((0,0,(a['Spine']['head'][2]*(1-f%1)+b['Spine']['head'][2]*(f%1)-REST['Spine'][0].z)*amount))
    return {n:tuple(v+shift for v in pair) for n,pair in result.items()},shift


def _posture(root,yaw,pelvis_z=.91,lean=0.,back=0.,feet=None):
    q=_q(yaw); tilt=Quaternion((1,0,0),math.radians(lean)); pivot=REST['Spine'][0]
    hip=Vector((pivot.x,pivot.y+back,pelvis_z))
    def torso(p): return root+q@(hip+tilt@(p-pivot))
    out={name:tuple(torso(p) for p in REST[name]) for name in ('Spine','Head','RightUpperArm','RightForeArm','RightHand','LeftUpperArm','LeftForeArm','LeftHand')}
    for side,sign in (('Left',1),('Right',-1)):
        thigh=side+'Thigh'; shin=side+'Shin'; foot=side+'Foot'
        h=root+q@(REST[thigh][0]+hip-pivot)
        ankle,toe=feet[side] if feet else tuple(root+q@p for p in REST[foot])
        bend=q@Vector((sign*.08,-1,.02))
        knee=_elbow(h,ankle,LENGTHS[thigh],LENGTHS[shin],bend)
        out[thigh]=(h,knee); out[shin]=(knee,ankle);out[foot]=(ankle,toe)
    return out


def _feet(root,yaw):
    q=_q(yaw)
    return {side:tuple(root+q@p for p in REST[side+'Foot']) for side in ('Left','Right')}


def _step_feet(old,new,t,lead='Left'):
    trail='Right' if lead=='Left' else 'Left'
    out={}
    for side,start,end in ((lead,0.,.52),(trail,.48,1.)):
        raw=max(0.,min(1.,(t-start)/(end-start)));s=_ease(raw)
        a,b=old[side],new[side];ankle=a[0].lerp(b[0],s)
        ankle.z+=.065*math.sin(math.pi*raw)**2
        # Interpolate heading about Z, preserving the boot's planted pitch.
        before=a[1]-a[0];after=b[1]-b[0]
        angle=math.atan2(before.x*after.y-before.y*after.x,
                         before.x*after.x+before.y*after.y)
        direction=(Quaternion((0,0,1),angle*s)@before).normalized()
        out[side]=(ankle,ankle+direction*LENGTHS[side+'Foot'])
    return out


def _reach(out,tip,amount):
    shoulder=out['LeftUpperArm'][0]
    old_wrist,old_tip=out['LeftHand']
    # Fingertips follow the exact rim while contact is held. Wrist is above
    # fingertips, with a lightly curled/downward hand rather than a long spear.
    direction=Vector((.12,.03,-1)).normalized()
    desired=tip-direction*LENGTHS['LeftHand']
    wrist=old_wrist.lerp(desired,amount)
    maximum=(LENGTHS['LeftUpperArm']+LENGTHS['LeftForeArm'])*.998
    if (wrist-shoulder).length>maximum:
        wrist=shoulder+(wrist-shoulder).normalized()*maximum
    elbow=_elbow(shoulder,wrist,LENGTHS['LeftUpperArm'],LENGTHS['LeftForeArm'],Vector((-.4,-.6,-.3)))
    handdir=(old_tip-old_wrist).normalized().lerp(direction,amount).normalized()
    out['LeftUpperArm']=(shoulder,elbow);out['LeftForeArm']=(elbow,wrist)
    out['LeftHand']=(wrist,wrist+handdir*LENGTHS['LeftHand'])


def state_at(seconds):
    """Return all 14 targets, stool_position, phase and root metadata.

    Targets already include root translation/heading. Do not transform twice.
    Final sit feet stay fixed from 5.8 seconds onward; pelvis travels back .365m.
    """
    t=max(0.,min(DURATION,float(seconds)));stool=Vector((0,0,0));yaw=80.
    if t<1.2:
        u=t/1.2;s=_ease(u);root=START.lerp(APPROACH,s)
        yaw=math.degrees(math.atan2(APPROACH.x-START.x,-(APPROACH.y-START.y)))
        yaw=yaw+(80-yaw)*_ease((u-.70)/.30)
        out=_posture(root,yaw)
        gait_time=(root-START).length/_stride_metres()*_motion()['cycleSeconds']
        gait,shift=_gait(gait_time,_ease(u/.14)*(1-_ease((u-.72)/.28)))
        out={n:tuple(v+shift for v in pair) for n,pair in out.items()}
        for n,p in gait.items():out[n]=tuple(root+_q(yaw)@v for v in p)
        phase='approach'
    elif t<2.5:
        u=_ease((t-1.2)/1.3);root=APPROACH.copy()
        out=_posture(root,yaw,.91-.25*u,32*u)
        _reach(out,RIM,u);phase='reach'
    elif t<4.:
        u=_ease((t-2.5)/1.5);root=APPROACH.lerp(PULL_END,u);stool=STOOL_END*u
        # A rear step follows the pull; the opposite boot remains planted.
        feet=_step_feet(_feet(APPROACH,yaw),_feet(PULL_END,yaw),(t-2.5)/1.5)
        out=_posture(root,yaw,.66,32,feet=feet)
        _reach(out,RIM+stool,1);phase='pull'
    elif t<4.6:
        u=_ease((t-4.)/.6);root=PULL_END.copy();stool=STOOL_END.copy()
        out=_posture(root,yaw,.66+.25*u,32*(1-u))
        _reach(out,RIM+stool,1-u);phase='release'
    elif t<5.8:
        u=(t-4.6)/1.2;s=_ease(u);root=PULL_END.lerp(FINAL,s);stool=STOOL_END.copy();yaw=80+(FINAL_YAW-80)*s
        feet=_step_feet(_feet(PULL_END,80),_feet(FINAL,FINAL_YAW),u,lead='Right')
        out=_posture(root,yaw,.91-.15*math.sin(math.pi*u)**2,feet=feet)
        phase='align'
    else:
        u=(t-5.8)/2.;travel=_ease((u-.12)/.80)
        prepare=_ease(u/.30);recover=_ease((u-.48)/.49)
        root=FINAL.copy();stool=STOOL_END.copy();yaw=FINAL_YAW
        out=_posture(root,yaw,.91+(SEATED_PELVIS_HEIGHT-.91)*travel,21*prepare-16*recover,.365*travel)
        # Quiet free hand resting above near thigh after releasing the stool.
        _reach(out,root+Vector((.34,-.08,.73)),.55*travel)
        phase='sit' if t<DURATION else 'seated'
    return {'targets':{n:{'head':list(a),'tail':list(b)} for n,(a,b) in out.items()},
            'stool_position':list(stool),'phase':phase,
            'root':{'position':list(root),'yaw_degrees':yaw},'seconds':t}
