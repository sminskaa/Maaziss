/* Human reference poses are evaluated in the forward/vertical plane, then
 * projected into the room. A camera-facing knee is never solved sideways. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.MazissReferenceGait=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),mix=(a,b,t)=>a+(b-a)*t,TAU=Math.PI*2;
const copy=p=>({x:p.x,y:p.y}),length=p=>Math.hypot(p.x,p.y),dot=(a,b)=>a.x*b.x+a.y*b.y;
class Gait{
 constructor(reference,options={}){this.reference={cycleSeconds:reference.cycle_seconds,strideHeightRatio:reference.estimated_stride_body_heights,stanceFraction:reference.contact_window[1],
   curve:reference.samples.filter(p=>p.phase<1).map(p=>({phase:p.phase,thigh:p.thigh_deg*Math.PI/180,shin:p.shin_deg*Math.PI/180,foot:p.fitted_foot_pitch_deg*Math.PI/180,lift:0,arm:p.thigh_deg*Math.PI/180}))};this.safe=options.isWalkable||(()=>true);this.cycle=0;this.blend=0;this.contacts=0;this.ready=false;}
 reset(p,h){this.p=copy(p);this.h=h;this.cycle=0;this.travel=0;this.blend=0;this.yaw={x:1,y:0};this.yawAngle=0;this.heading={x:1,y:0};this.records={};this.ready=true;return this.getPose();}
 sample(phase){
  const poses=this.reference.curve,phase0=((phase%1)+1)%1;
  let i=poses.findIndex((p,j)=>j+1<poses.length&&p.phase<=phase0&&poses[j+1].phase>phase0);if(i<0)i=poses.length-1;
  const a=poses[i],b=poses[(i+1)%poses.length],start=a.phase,end=i===poses.length-1?1: b.phase,t=clamp((phase0-start)/(end-start),0,1);
  const result={};for(const key of ['thigh','shin','foot','lift','arm'])result[key]=mix(a[key],b[key],t);return result;
 }
 update(p,h,dt,moving,direction,study=false){
  if(!this.ready)return this.reset(p,h);
  const distance=Math.hypot(p.x-this.p.x,p.y-this.p.y);
  if(distance>h*.75)return this.reset(p,h);
  this.h=h;
  if(direction&&length(direction)>.0001){
   // Undo the room's depth foreshortening before obtaining world heading.
   const world={x:direction.x,y:direction.y/.36},n=length(world);this.heading={x:world.x/n,y:world.y/n};
   const targetAngle=Math.atan2(this.heading.y,this.heading.x);
   const delta=Math.atan2(Math.sin(targetAngle-this.yawAngle),Math.cos(targetAngle-this.yawAngle));
   this.yawAngle+=clamp(delta,-dt*12,dt*12);
   this.yaw={x:Math.cos(this.yawAngle),y:Math.sin(this.yawAngle)};
  }
  const stride=this.reference.strideHeightRatio*h;
  if(study&&dt>0){this.cycle+=dt/this.reference.cycleSeconds;this.travel+=stride*dt/this.reference.cycleSeconds;}
  else if(distance>0.0001){this.cycle+=distance/(stride*Math.max(.36,Math.hypot(this.yaw.x,this.yaw.y*.36)));this.travel+=distance;}
  if(dt>0)this.blend+=clamp(Number(moving||study)-this.blend,-dt*7,dt*7);
  this.p=copy(p);this.study=study;return this.getPose();
 }
 project(forward,side,up){const d=this.yaw;return {x:this.p.x+d.x*forward+d.y*side,y:this.p.y+d.y*.36*forward-d.x*.36*side-up};}
 getPose(){
  if(!this.ready)return null;
  const h=this.h,blend=this.blend,phase=((this.cycle%1)+1)%1;
  const limb=h*.2025,ankleHeight=h*.065,toeLength=h*.16;
  let pelvisHeight=h*.467;
  const prepared=[];
  for(let i=0;i<2;i++){
   const id=i?'right':'left',legPhase=(phase+i*.5)%1,s=this.sample(legPhase),side=(i?-.052:.052)*h;
   const thigh=s.thigh*blend,shin=s.shin*blend;
   const f=limb*(Math.sin(thigh)+Math.sin(shin)),down=limb*(Math.cos(thigh)+Math.cos(shin));
   const stance=legPhase<this.reference.stanceFraction||blend<.02;
   // The recording's foot pitch is unreliable on blur. Keep a flat loaded foot;
   // use its measured heel-rise interval for a bounded toe pivot before lift-off.
   const push=clamp((legPhase-.48)/(.69-.48),0,1);
   let pitch=stance?-push*35*Math.PI/180:clamp(s.foot,-35*Math.PI/180,8*Math.PI/180);
   pitch*=blend;
   let ankleUp=Math.max(ankleHeight,pelvisHeight-down,ankleHeight+toeLength*Math.max(0,-Math.sin(pitch)));
   let ground=this.project(f,side,0),ankle=this.project(f,side,ankleUp);
   const prev=this.records[id],step=Math.floor(this.cycle+i*.5),turned=prev&&dot(prev.yaw,this.yaw)<.985;
   let toe;
   if(stance){
    if(!this.study&&blend>.95&&prev&&prev.stance&&prev.step===step&&!turned)toe=copy(prev.toe);
    else {toe=this.project(f+toeLength*Math.cos(pitch),side,0);}
    if(!this.safe(toe)&&!this.study){
     for(let t=.95;t>=0;t-=.05){const q={x:mix(this.p.x,toe.x,t),y:mix(this.p.y,toe.y,t)};if(this.safe(q)){toe=q;break;}}
    }
    ground={x:toe.x-this.yaw.x*toeLength*Math.cos(pitch),y:toe.y-this.yaw.y*.36*toeLength*Math.cos(pitch)};
    ankleUp=ankleHeight+toeLength*Math.max(0,-Math.sin(pitch));
    ankle={x:ground.x,y:ground.y-ankleUp};
    const df=dot({x:ground.x-this.p.x,y:(ground.y-this.p.y)/.36},this.yaw);
    const reachUp=Math.sqrt(Math.max(0,(2*limb*.995)**2-df*df));
    pelvisHeight=Math.min(pelvisHeight,reachUp+ankleUp);
   } else toe=this.project(f+toeLength*Math.cos(pitch),side,0);
   prepared.push({id,phase:legPhase,thigh,shin,foot:pitch,arm:s.arm*blend,f,down,side,stance,ankleUp,ankle,ground,toe,prev,step});
  }
  // Retarget contact extension for a human standing leg; literal oblique-camera
  // joint angles would reproduce measurement bias as a crouch.
  pelvisHeight=clamp(pelvisHeight,h*.405,h*.467);
  const pelvis=this.project(0,0,pelvisHeight),results=[];
  for(const leg of prepared){
   if(!leg.stance){leg.ankleUp=Math.max(ankleHeight,pelvisHeight-leg.down,ankleHeight+toeLength*Math.max(0,-Math.sin(leg.foot)));leg.ankle={x:leg.ground.x,y:leg.ground.y-leg.ankleUp};}
   const df=dot({x:leg.ground.x-this.p.x,y:(leg.ground.y-this.p.y)/.36},this.yaw);
   const vertical=pelvisHeight-leg.ankleUp,reach=Math.hypot(df,vertical),bounded=Math.min(reach,2*limb-.001);
   const half=bounded/2,bend=Math.sqrt(Math.max(0,limb*limb-half*half));
   const kf=df/Math.max(reach,.001)*half+vertical/Math.max(reach,.001)*bend;
   const kd=vertical/Math.max(reach,.001)*half-df/Math.max(reach,.001)*bend;
   const hip=this.project(0,leg.side,pelvisHeight),knee=this.project(kf,leg.side,pelvisHeight-kd);
   const contactId=leg.prev&&leg.prev.step===leg.step?leg.prev.contactId:++this.contacts;
   const result={id:leg.id,phase:leg.phase,thigh:leg.thigh,shin:leg.shin,side:leg.side,arm:leg.arm,stance:leg.stance,
    hip,knee,ankle:leg.ankle,ground:leg.ground,toe:leg.toe,lift:Math.max(0,leg.ankleUp-ankleHeight),bootAngle:leg.foot,contactId,
    sagittal:{forward:df,kneeForward:kf,kneeDown:kd,ankleUp:leg.ankleUp,pelvisHeight,limb}};
   this.records[leg.id]={stance:leg.stance,step:leg.step,toe:copy(leg.toe),yaw:{...this.yaw},contactId};results.push(result);
  }
  return {phase,blend,pelvis,pelvisHeight,bob:h*.467-pelvisHeight,legs:results,yaw:{...this.yaw},travel:this.travel,torso:{x:pelvis.x,y:pelvis.y,angle:0}};
 }
}
return {Gait};
});
