"""Isolated owner-corrected seated turn / desk-reach pose study.

Two separate tests, not the full stool action. Existing pose/model sources stay
unchanged. +Z up; camera screen-right is world +X. Anatomical Right is rig Right.
"""
import math
from mathutils import Vector, Quaternion
import stool_slide_pose as old
b=old.b
DURATION=6.0
FPS=20
FINAL_YAW=90.
KEY_TIMES=(0.,.65,1.45,2.4,3.,3.5,4.0,4.7,5.4,6.)
GAIT_PHASES=()
DESK_GEOMETRY=True
REVIEW_DESCRIPTION='Two isolated pose tests: right foot, left foot, then seated torso/head turn; separately lift hands, travel above the desk edge and place on top.'
FINAL_LABEL='Hand-placement candidate, unfinished model'
PHASE_BOUNDARIES=((.65,'Move right foot'),(1.45,'Move left foot'),(2.4,'Turn torso and head'),(3.,'Hold; then separate test cut'),(3.69,'Withdraw hands below desk edge'),(4.5,'Lift outside desk'),(5.49,'Reach above tabletop'),(6.,'Lower onto tabletop'))
BASE=old.state_at(5.8)
ROOT=Vector(BASE['root']['position'])
PIVOT=Vector(BASE['targets']['Spine']['head'])
FEET={s:tuple(Vector(BASE['targets'][s+'Foot'][k]) for k in ('head','tail')) for s in ('Left','Right')}
# Move the right boot genuinely toward screen right, rather than merely rotating
# it leftward around the hip. The left boot follows to its own separated stance.
FINAL_FEET={}
for side,sign in (('Left',1),('Right',-1)):
    before=FEET[side][1]-FEET[side][0]
    direction=b._q(FINAL_YAW-old.YAW)@before
    x=.12 if side=='Left' else FEET['Right'][0].x+.030
    ankle=Vector((x,PIVOT.y+sign*.16,FEET[side][0].z))
    FINAL_FEET[side]=(ankle,ankle+direction)


def foot_move(side,raw):
    u=b._ease(raw);a,c=FEET[side],FINAL_FEET[side]
    ankle=a[0].lerp(c[0],u);ankle.z+=.035*math.sin(math.pi*max(0.,min(1.,raw)))**2
    before=a[1]-a[0];after=c[1]-c[0]
    angle=math.atan2(before.x*after.y-before.y*after.x,before.x*after.x+before.y*after.y)
    direction=Quaternion((0,0,1),angle*u)@before
    return ankle,ankle+direction


def seated(yaw,feet,shift=Vector((0,0,0)),lean=15):
    hip=Vector((b.REST['Spine'][0].x,b.REST['Spine'][0].y+old.SIT_BACK,0))
    root=Vector((PIVOT.x,PIVOT.y,0))-b._q(yaw)@hip+shift
    root.x+=.08*(old.YAW-yaw)/(old.YAW-FINAL_YAW)
    targets=b._posture(root,yaw,old.SEATED_PELVIS_HEIGHT,lean,old.SIT_BACK,feet)
    return root,targets


def state_at(seconds):
    t=max(0.,min(DURATION,float(seconds)))
    if t<=3.:
        feet={'Right':foot_move('Right',t/.65),'Left':foot_move('Left',(t-.80)/.65)}
        yaw=old.YAW+(FINAL_YAW-old.YAW)*b._ease((t-1.65)/.75)
        root,out=seated(yaw,feet);stool=old.STOOL_PULLED.copy()
        # Keep the idle far hand near the lap as the seated torso turns, so
        # the hanging forearm does not sweep through the desk edge.
        old.arm(out,'Left',Vector((-.26,.34,.66)),Vector((0,0,-1)),b._ease((t-1.65)/.75))
        phase='right_foot' if t<.65 else 'left_foot' if t<1.45 else 'torso_turn' if t<2.4 else 'turn_hold'
    else:
        # Separate final-desk-position test; no intervening slide is claimed.
        shift=old.SLIDE+Vector((-.28,0,0));feet={s:tuple(v+shift for v in pair) for s,pair in FINAL_FEET.items()}
        yaw=FINAL_YAW;root,out=seated(yaw,feet,shift,lean=5);stool=old.STOOL_PULLED+shift
        raw=(t-3.)/3.
        for side in ('Left','Right'):
            wrist,tip=out[side+'Hand'];direction=(tip-wrist).normalized()
            # Lift vertically on the character side of the desk before traversing
            # the leading edge. Real evaluated skin clearance is checked separately.
            target=Vector((.38,.25,.994)) if side=='Left' else Vector((.38,-.16,.994))
            withdrawn=tip.copy();withdrawn.x=-.22 if side=='Left' else tip.x-.03
            lifted=withdrawn.copy();lifted.z=1.10;above=target+Vector((0,0,.10))
            if raw<.23:
                u=b._ease(raw/.23);desired=tip.lerp(withdrawn,u);aim=direction;phase='withdraw_below_edge'
            elif raw<.5:
                u=b._ease((raw-.23)/.27);desired=withdrawn.lerp(lifted,u);aim=direction.lerp(Vector((1,0,0)),u).normalized();phase='lift_outside_edge'
            elif raw<.83:
                u=b._ease((raw-.5)/.33);desired=lifted.lerp(above,u);aim=Vector((1,0,0)).lerp(Vector((1,0,-.28)).normalized(),u).normalized();phase='over_edge'
            else:
                u=b._ease((raw-.83)/.17);desired=above.lerp(target,u);aim=Vector((1,0,-.28)).normalized();phase='place_hands'
            old.arm(out,side,desired,aim,elbow_drop=0)
            shoulder=out[side+'UpperArm'][0];wrist=out[side+'Hand'][0]
            sign=1 if side=='Left' else -1
            pole=Vector((-.4,sign*.25,-1)).lerp(Vector((0,sign*.25,1)),b._ease((raw-.54)/.16))
            elbow=old._elbow(shoulder,wrist,b.LENGTHS[side+'UpperArm'],b.LENGTHS[side+'ForeArm'],pole)
            out[side+'UpperArm']=(shoulder,elbow);out[side+'ForeArm']=(elbow,wrist)
    return {'targets':{n:{'head':list(a),'tail':list(c)} for n,(a,c) in out.items()},'stool_position':list(stool),'root':{'position':list(root),'yaw_degrees':yaw},'phase':phase,'seconds':t}
