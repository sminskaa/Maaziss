"""ART-014: preserve accepted pull, circle behind stool, sit toward right desk.

Import-safe Blender world-space pose API. Source models and accepted action stay
unchanged. +Z up; local front -Y; yaw135 faces world +X,+Y (the right desk).
"""
import math
from mathutils import Vector
import stool_interaction_pose as baseline

FPS = baseline.FPS
SEAT_HEIGHT = baseline.SEAT_HEIGHT
SEATED_PELVIS_HEIGHT = baseline.SEATED_PELVIS_HEIGHT
FINAL_YAW = 135.
STOOL_END = baseline.STOOL_END.copy()
FINAL = STOOL_END-baseline._q(FINAL_YAW)@Vector((.005,.365,0))
# Modest paired steps keep both boots outside the seat/leg footprint. The
# west/north detour passes behind the stool before the final desk-facing pivot.
ROUTE = (
    (4.6, baseline.PULL_END.copy(), 80.),
    (5.3, Vector((-1.01,-.52,0)), 100.),
    (6.0, Vector((-1.08,-.20,0)), 135.),
    (6.7, Vector((-.98,.13,0)), 155.),
    (7.4, Vector((-.72,.37,0)), 145.),
    (8.1, Vector((-.39,.44,0)), 120.),
    (8.8, Vector((-.12,.30,0)), 110.),
    (9.5, FINAL.copy(), FINAL_YAW),
)
SIT_START = ROUTE[-1][0]
DURATION = SIT_START+2.
KEY_TIMES = (0.,1.2,2.5,4.,4.6,5.3,6.,6.7,7.4,8.1,8.8,9.5,10.5,11.5)
PHASE_BOUNDARIES = ((1.2,'Approach'),(2.5,'Reach'),(4.,'Pull'),
                    (4.6,'Release'),(8.1,'Pass behind stool'),
                    (9.5,'Face the desk'),(11.5,'Sit at desk'))


def state_at(seconds):
    t=max(0.,min(DURATION,float(seconds)))
    if t < 4.6:
        return baseline.state_at(t)
    if t < SIT_START:
        index=next(i for i in range(len(ROUTE)-1) if t<ROUTE[i+1][0])
        start,old,heading=ROUTE[index];end,new,new_heading=ROUTE[index+1]
        u=(t-start)/(end-start);s=baseline._ease(u)
        root=old.lerp(new,s);yaw=heading+(new_heading-heading)*s
        feet=baseline._step_feet(baseline._feet(old,heading),
                                 baseline._feet(new,new_heading),u,
                                 lead='Right' if index<3 else 'Left')
        out=baseline._posture(root,yaw,.91-.035*math.sin(math.pi*u)**2,feet=feet)
        phase='circle_back' if t<8.1 else 'desk_align'
    else:
        u=(t-SIT_START)/2.;travel=baseline._ease((u-.12)/.80)
        prepare=baseline._ease(u/.30);recover=baseline._ease((u-.48)/.49)
        root=FINAL.copy();yaw=FINAL_YAW
        out=baseline._posture(root,yaw,.91+(SEATED_PELVIS_HEIGHT-.91)*travel,
                             21*prepare-16*recover,.365*travel)
        # Keep the free arm relaxed in its local frame; the bag-side Right arm
        # follows the unchanged torso transform throughout the entire action.
        tip=root+baseline._q(yaw)@Vector((.34,-.08,.73))
        baseline._reach(out,tip,.55*travel)
        phase='sit' if t<DURATION else 'seated'
    return {'targets':{name:{'head':list(a),'tail':list(b)} for name,(a,b) in out.items()},
            'stool_position':list(STOOL_END),'phase':phase,
            'root':{'position':list(root),'yaw_degrees':yaw},'seconds':t}
