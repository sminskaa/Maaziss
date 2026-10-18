'use strict';
const assert=require('node:assert/strict');
const {Gait}=require('../walking/gait.js');
let checks=0;
const check=(value,message)=>{assert.ok(value,message);checks++;};
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
const gait=new Gait();let position={x:0,y:500},pose=gait.reset(position,400);
const contacts=[],ahead={left:[],right:[]};let previous=pose,maxLift=0;
for(let i=0;i<600;i++) {
  position={x:position.x+400/60,y:500};pose=gait.update(position,400,1/60,true,{x:1,y:0});
  for(const leg of pose.legs) {
    const old=previous.legs.find(l=>l.id===leg.id);
    if(leg.stance&&old.stance&&leg.contactId===old.contactId)check(distance(leg.ground,old.ground)<1e-9,'stance contact must be fixed in world space');
    if(leg.stance&&leg.contactId!==old.contactId)contacts.push(leg.id);
    ahead[leg.id].push(leg.ground.x-position.x);maxLift=Math.max(maxLift,leg.lift);
    check(distance(leg.hip,leg.knee)<91,'thigh bounded');
    check(distance(leg.knee,leg.ankle)<91,'shin bounded');
    check([leg.hip,leg.knee,leg.ankle,leg.ground].every(p=>Number.isFinite(p.x)&&Number.isFinite(p.y)),'finite joints');
  }
  check(pose.legs.filter(l=>!l.stance).length===1,'one support leg while walking');
  previous=pose;
}
check(contacts.length>20,'many actual contacts observed');
check(contacts.every((id,i)=>i===0||id!==contacts[i-1]),'left/right contact sequence alternates');
for(const id of ['left','right'])check(Math.min(...ahead[id])<-55&&Math.max(...ahead[id])>55,`${id} actually crosses behind to ahead`);
check(maxLift>14,'swing boot lifts above floor');
let frozen=JSON.stringify(gait.getPose());
for(let i=0;i<30;i++)gait.update(position,400,0,false,{x:1,y:0});
check(JSON.stringify(gait.getPose())===frozen,'pause freezes complete pose');
const phase=gait.getPose().phase;
for(let i=0;i<60;i++)gait.update(position,400,1/60,false,{x:1,y:0});
check(gait.getPose().phase===phase,'idle does not advance gait phase');
check(gait.getPose().legs.every(l=>l.stance&&l.lift===0),'stopping gently lowers swing boot');
frozen=JSON.stringify(gait.getPose());
gait.update(position,400,1,false,{x:1,y:0});
check(JSON.stringify(gait.getPose())===frozen,'settled idle does not drift');
gait.update(position,400,1,true,{x:1,y:0});
check(JSON.stringify(gait.getPose())===frozen,'a clock tick without travel is not a walking step');
// Identical body travel has identical timing despite different frame rates.
const a=new Gait(),b=new Gait();a.reset({x:0,y:500},400);b.reset({x:0,y:500},400);
for(let i=1;i<=60;i++)a.update({x:i*4,y:500},400,1/60,true,{x:1,y:0});
for(let i=1;i<=30;i++)b.update({x:i*8,y:500},400,1/30,true,{x:1,y:0});
check(Math.abs(a.getPose().phase-b.getPose().phase)<1e-10,'phase follows distance, not wall clock');
for(const vector of [{x:-1,y:0},{x:0,y:1},{x:0,y:-1},{x:.7071,y:.7071},{x:-.7071,y:-.7071}]) {
  for(let i=0;i<90;i++) {
    position={x:position.x+vector.x*5,y:position.y+vector.y*5};pose=gait.update(position,400,1/60,true,vector);
    for(const leg of pose.legs) {
      check([leg.hip,leg.knee,leg.ankle].every(p=>Number.isFinite(p.x)&&Number.isFinite(p.y)),'turns and all directions stay finite');
      check(distance(leg.hip,leg.knee)<91&&distance(leg.knee,leg.ankle)<96,'joint lengths bounded on abrupt turns');
    }
    check(Math.abs(pose.torso.angle)<Math.PI/90,'torso lean under two degrees');
  }
}
for(const h of [370,425,480]) {
  const size=new Gait();let p={x:0,y:500};size.reset(p,h);
  for(let i=0;i<200;i++) {
    const theta=i*.021,v={x:Math.cos(theta),y:Math.sin(theta)};
    p={x:p.x+v.x*6,y:p.y+v.y*6};const result=size.update(p,h,1/60,true,v);
    check(result.legs.every(l=>distance(l.hip,l.knee)<h*.226&&distance(l.knee,l.ankle)<h*.226),'physical bone lengths preserved across sizes and curved travel');
  }
}
const edge=new Gait({isWalkable:p=>p.x>=0&&p.x<=300&&p.y>=0&&p.y<=700});
edge.reset({x:250,y:500},400);
for(let i=1;i<=40;i++) {
  pose=edge.update({x:250+i,y:500},400,1/60,true,{x:1,y:0});
  check(pose.legs.every(l=>l.ground.x>=0&&l.ground.x<=300),'contact projection cannot plant outside allowed geometry');
}
// Real concave room corners: both planted contacts and airborne projections
// respect the navigation buffer, which is stricter than solid collision.
const {Navigation}=require('../walking/navigation.js');
const room=require('../walking/room.json'),navigation=new Navigation(room);
const roomGait=new Gait({isWalkable:p=>navigation.isWalkable(p)});
let roomPosition={...room.start},roomPrevious=roomGait.reset(roomPosition,420),roomSamples=0,maxAirborneDelta=0;
const destinations=navigation.nodes.filter((_,i)=>i%61===0);
for(const destination of destinations) {
  const route=navigation.findPath(roomPosition,destination);
  check(route.path.length>0,'room route can be built');
  for(const endpoint of route.path.slice(1)) {
    while(distance(roomPosition,endpoint)>1e-7) {
      const d=distance(roomPosition,endpoint),step=Math.min(5,d);
      const direction={x:(endpoint.x-roomPosition.x)/d,y:(endpoint.y-roomPosition.y)/d};
      roomPosition={x:roomPosition.x+direction.x*step,y:roomPosition.y+direction.y*step};
      const current=roomGait.update(roomPosition,420,1/60,true,direction);roomSamples++;
      for(const leg of current.legs) {
        check(navigation.isWalkable(leg.ground),`${leg.stance?'stance':'airborne'} projection retains 32px room clearance`);
        check(distance(leg.hip,leg.knee)<420*.226&&distance(leg.knee,leg.ankle)<420*.226,'corner-shortened steps preserve both bone lengths');
        const previousLeg=roomPrevious.legs.find(l=>l.id===leg.id);
        if(leg.stance&&previousLeg.stance&&leg.contactId===previousLeg.contactId)check(distance(leg.ground,previousLeg.ground)<1e-9,'corner correction never moves a planted foot');
        if(!leg.stance&&!previousLeg.stance)maxAirborneDelta=Math.max(maxAirborneDelta,distance(leg.ground,previousLeg.ground));
      }
      roomPrevious=current;
    }
  }
}
check(roomSamples>1000,'substantial real-room traversal including corners');
check(maxAirborneDelta<420*.12,'corner constraints do not create large airborne position jumps');
console.log(`Gait checks passed: ${checks}. Physical contact/IK checks do not certify perceived naturalness.`);
console.log(`Room traversal: ${roomSamples} poses; largest airborne projection movement per 5px root step: ${maxAirborneDelta.toFixed(2)}px.`);
