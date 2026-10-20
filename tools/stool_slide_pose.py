"""Right-hand pull, one compact boarding step, occupied slide, hands on desk.

Blender pose targets in metres: +Z up, front -Y, anatomical Right is local -X.
Source character needs the independently prepared right arm; do not use fused rig.
"""
import math
from mathutils import Vector
import stool_interaction_pose as b
from character3d_fit import _elbow

FPS=20
DURATION=8.8
KEY_TIMES=(0.,1.6,2.4,3.4,3.8,4.25,4.7,5.5,6.3,6.85,7.4,8.8)
PHASE_BOUNDARIES=((1.6,'Approach the left side'),(2.4,'Right hand takes the seat'),
 (3.4,'Pull the stool'),(3.8,'Release and rise'),(4.7,'Move directly to sit'),
 (5.8,'Sit down'),(6.3,'Right hand grips the seat'),(7.4,'Slide toward the desk'),
 (8.8,'Rest both hands on the desk'))
START=Vector((-1.6,-.7,0))
APPROACH=Vector((-.32,.55,0))
PULL_ROOT=Vector((-.44,.52,0))
# One planted adjustment clears the near stool leg without adding a shuffle.
PULL_FOOT_OFFSET=Vector((.29,.04,0))
# A small mid-pull rise keeps the satchel clear; root compensation retains reach.
PULL_HEIGHT_BUMP=.018
PULL_ROOT_BUMP=Vector((-.02,0,0))
RELEASE_ROOT=Vector((-.25,.50,0))
STOOL_PULLED=Vector((-.24,.20,0))
SLIDE=Vector((.26,-.18,0))
YAW=135.
SIT_BACK=.23
STAND=STOOL_PULLED-b._q(YAW)@Vector((.005,SIT_BACK,0))
PULL_GRIP=Vector((-.14707,.17975,.590))
SEATED_GRIP=b._q(YAW)@Vector((-.18697,-.22851,.590))
DESK_Z=.93
# Hand-bone landmarks above tabletop; evaluated palm skin determines final fit.
DESK_HANDS={'Left':Vector((.10,.30,.999)), 'Right':Vector((.38,-.20,.985))}
SLIDE_INTERVAL=(6.3,7.4)
SEAT_HEIGHT=.568
SEATED_PELVIS_HEIGHT=.698
GAIT_PHASES=('approach',)
DESK_GEOMETRY=True
REVIEW_DESCRIPTION='Maziss pulls with his right hand, makes one compact move to sit, slides forward with the stool and rests both hands on the desk.'
FINAL_LABEL='Seated with both hands on the desk'
CONTACT_SPECIFICATION={'pullInterval':[2.4,3.4],'pullGrip':list(PULL_GRIP),
 'slideInterval':list(SLIDE_INTERVAL),'seatedGrip':list(SEATED_GRIP),
 'localSeatMarker':[.005,SIT_BACK,SEAT_HEIGHT],'deskHeight':DESK_Z,
 'finalHandBoneTips':{side:list(p) for side,p in DESK_HANDS.items()},
 'landmarkNote':'Bone tips are above support; independently inspect evaluated skin contact.'} 


def arm(out,side,tip,direction,amount=1,elbow_drop=0):
    upper,lower,hand=(side+x for x in ('UpperArm','ForeArm','Hand'))
    shoulder=out[upper][0];old_wrist,old_tip=out[hand]
    direction=direction.normalized();desired=tip-direction*b.LENGTHS[hand]
    wrist=old_wrist.lerp(desired,amount)
    maximum=(b.LENGTHS[upper]+b.LENGTHS[lower])*.999
    if (wrist-shoulder).length>maximum:
        wrist=shoulder+(wrist-shoulder).normalized()*maximum
    minimum=abs(b.LENGTHS[upper]-b.LENGTHS[lower])+.003
    if (wrist-shoulder).length<minimum:
        wrist=shoulder+(wrist-shoulder).normalized()*minimum
    sign=1 if side=='Left' else -1
    pole=b._q(YAW)@Vector((sign*.7,.30,-.15)).lerp(Vector((sign*.12,.05,-.8)),elbow_drop)
    elbow=_elbow(shoulder,wrist,b.LENGTHS[upper],b.LENGTHS[lower],pole)
    handdir=(old_tip-old_wrist).normalized().lerp(direction,amount).normalized()
    out[upper]=(shoulder,elbow);out[lower]=(elbow,wrist)
    out[hand]=(wrist,wrist+handdir*b.LENGTHS[hand])


def seated(root,feet,lean=15):
    return b._posture(root,YAW,SEATED_PELVIS_HEIGHT,lean,SIT_BACK,feet)


def state_at(seconds):
    t=max(0.,min(DURATION,float(seconds)));stool=Vector((0,0,0));yaw=YAW
    initial=b._feet(APPROACH,YAW)
    pulled={side:tuple(p+PULL_FOOT_OFFSET if side=='Right' else p.copy() for p in pair) for side,pair in initial.items()}
    planted={side:tuple(STAND+b._q(YAW)@(p+Vector((.07 if side=='Left' else -.07,-.04,0))) for p in b.REST[side+'Foot']) for side in ('Left','Right')}
    seated_feet={}
    for side,sign in (('Left',1),('Right',-1)):
        ankle=STOOL_PULLED+b._q(YAW)@Vector((sign*.29,-.44,.225))
        seated_feet[side]=(ankle,ankle+b._q(YAW)@(b.REST[side+'Foot'][1]-b.REST[side+'Foot'][0]))
    if t<1.6:
        u=t/1.6;s=b._ease(u);root=START.lerp(APPROACH,s)+Vector((-.15,.18,0))*math.sin(math.pi*u)**2
        travel_yaw=math.degrees(math.atan2(APPROACH.x-START.x,-(APPROACH.y-START.y)))
        yaw=travel_yaw+(YAW-travel_yaw)*b._ease((u-.65)/.35)
        out=b._posture(root,yaw)
        gait_time=(root-START).length/b._stride_metres()*b._motion()['cycleSeconds']
        gait,shift=b._gait(gait_time,b._ease(u/.12)*(1-b._ease((u-.55)/.25)))
        out={name:tuple(v+shift for v in pair) for name,pair in out.items()}
        for name,pair in gait.items():out[name]=tuple(root+b._q(yaw)@v for v in pair)
        phase='approach'
    elif t<2.4:
        u=b._ease((t-1.6)/.8);root=APPROACH.copy()
        out=b._posture(root,YAW,.91-.202*u,0)
        arm(out,'Right',PULL_GRIP,Vector((0,0,-1)),u);phase='right_reach'
    elif t<3.4:
        raw=t-2.4;u=b._ease((raw-.22)/.78);foot_u=b._ease(raw/.32);stool=STOOL_PULLED*u;root=APPROACH.lerp(PULL_ROOT,u)+PULL_ROOT_BUMP*math.sin(math.pi*u)
        feet={side:tuple(a.lerp(c,foot_u)+Vector((0,0,.075*math.sin(math.pi*min(1.,raw/.32))**2 if side=='Right' else 0)) for a,c in zip(initial[side],pulled[side])) for side in ('Left','Right')}
        out=b._posture(root,YAW,.708+.015*u+PULL_HEIGHT_BUMP*math.sin(math.pi*u),0,feet=feet)
        arm(out,'Right',stool+PULL_GRIP,Vector((0,0,-1)));phase='right_pull'
    elif t<3.8:
        u=b._ease((t-3.4)/.4);stool=STOOL_PULLED.copy();root=PULL_ROOT.lerp(RELEASE_ROOT,u)
        out=b._posture(root,YAW,.723+.107*u,0,feet=pulled)
        arm(out,'Right',stool+PULL_GRIP,Vector((0,0,-1)),1-u);phase='release'
    elif t<4.7:
        u=(t-3.8)/.9
        ramp=.10
        def path_progress(v):
            if v<ramp:return (v/2-ramp/(2*math.pi)*math.sin(math.pi*v/ramp))/(1-ramp)
            if v>1-ramp:return 1-path_progress(1-v)
            return (v-ramp/2)/(1-ramp)
        s=path_progress(u);root=RELEASE_ROOT.lerp(STAND,s);stool=STOOL_PULLED.copy()
        feet=b._step_feet(pulled,planted,u,lead='Right')
        out=b._posture(root,YAW,.83+.055*s-.03*math.sin(math.pi*u)**2,feet=feet)
        phase='compact_step'
    elif t<5.8:
        u=(t-4.7)/1.1;s=b._ease(u);root=STAND.copy();stool=STOOL_PULLED.copy()
        feet={side:tuple(a.lerp(c,s) for a,c in zip(planted[side],seated_feet[side])) for side in ('Left','Right')}
        out=b._posture(root,YAW,.885+(SEATED_PELVIS_HEIGHT-.885)*s,15*s,SIT_BACK*s,feet)
        phase='sit'
    elif t<6.3:
        u=b._ease((t-5.8)/.5);root=STAND.copy();stool=STOOL_PULLED.copy()
        out=seated(root,seated_feet)
        arm(out,'Right',stool+SEATED_GRIP,Vector((0,0,-1)),u);phase='seat_grip'
    elif t<7.4:
        u=b._ease((t-6.3)/1.1);shift=SLIDE*u;root=STAND+shift;stool=STOOL_PULLED+shift
        # Supported boots travel with the seated scoot, clear of the footrest.
        feet={side:tuple(p+shift for p in pair) for side,pair in seated_feet.items()}
        out=seated(root,feet,15+4*math.sin(math.pi*u)**2)
        arm(out,'Right',stool+SEATED_GRIP,Vector((0,0,-1)));phase='occupied_slide'
    else:
        u=b._ease((t-7.4)/1.4);root=STAND+SLIDE;stool=STOOL_PULLED+SLIDE
        feet={side:tuple(p+SLIDE for p in pair) for side,pair in seated_feet.items()}
        out=seated(root,feet)
        arm(out,'Right',stool+SEATED_GRIP,Vector((0,0,-1)))
        forward=b._q(YAW)@Vector((0,-1,0));raw=(t-7.4)/1.4
        for side in ('Left','Right'):
            old_wrist,old_tip=out[side+'Hand'];old_direction=(old_tip-old_wrist).normalized()
            lift_offset=Vector((0,-.24,0)) if side=='Left' else Vector((-.18,-.12,0))
            lifted=old_tip+Vector((0,0,.46))+b._q(YAW)@lift_offset;above=DESK_HANDS[side]+Vector((0,0,.10))
            if raw<.30:
                tip=old_tip.lerp(lifted,b._ease(raw/.30));direction=old_direction
            elif raw<.75:
                progress=b._ease((raw-.30)/.45);tip=lifted.lerp(above,progress)
                direction=old_direction.lerp(forward,progress).normalized()
            else:
                tip=above.lerp(DESK_HANDS[side],b._ease((raw-.75)/.25));direction=forward
            arm(out,side,tip,direction,elbow_drop=b._ease(raw/.75))
        phase='desktop_reach' if t<DURATION else 'hands_on_desk'
    return {'targets':{name:{'head':list(a),'tail':list(c)} for name,(a,c) in out.items()},
      'stool_position':list(stool),'phase':phase,'root':{'position':list(root),'yaw_degrees':yaw},'seconds':t}
