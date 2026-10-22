/* Image-guided walk: continuous foot curves and painted cuff geometry are
 * evaluated together, before two-link leg fitting and camera projection. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.MazissImageGait=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),mix=(a,b,t)=>a+(b-a)*t,TAU=Math.PI*2;
const ease=t=>{t=clamp(t,0,1);return t*t*t*(10+t*(-15+6*t));};
const cp=p=>({x:p.x,y:p.y});
const softmin=(a,b,k)=>Math.min(a,b)-k*Math.log1p(Math.exp(-Math.abs(a-b)/k));
class Gait{
 constructor(reference,options={}){this.reference=reference;this.safe=options.isWalkable||(()=>true);this.ready=false;}
 reset(p,h){this.p=cp(p);this.h=h;this.cycle=.30;this.travel=0;this.weight=0;this.elapsed=0;this.mode='idle';this.settle=null;this.records={};this.yawAngle=0;this.yaw={x:1,y:0};this.heading={...this.yaw};this.contacts=0;this.ready=true;return this.getPose();}
 project(f,side,up){return {x:this.p.x+this.yaw.x*f+this.yaw.y*side,y:this.p.y+this.yaw.y*.36*f-this.yaw.x*.36*side-up};}
 forward(p){return (p.x-this.p.x)*this.yaw.x+(p.y-this.p.y)/.36*this.yaw.y;}
 update(p,h,dt,moving,direction,study=false){
  if(!this.ready)return this.reset(p,h);
  dt=Math.max(0,dt);const distance=Math.hypot(p.x-this.p.x,p.y-this.p.y);
  if(distance>h*.75)return this.reset(p,h);
  if(dt===0){this.p=cp(p);this.h=h;return this.getPose();}
  const active=moving||study;
  if(direction&&Math.hypot(direction.x,direction.y)>1e-6&&(active||this.mode!=='idle')){
   const x=direction.x,y=direction.y/.36,n=Math.hypot(x,y);this.heading={x:x/n,y:y/n};
   const wanted=Math.atan2(this.heading.y,this.heading.x),delta=Math.atan2(Math.sin(wanted-this.yawAngle),Math.cos(wanted-this.yawAngle));
   this.yawAngle+=delta*(1-Math.exp(-dt*12));this.yaw={x:Math.cos(this.yawAngle),y:Math.sin(this.yawAngle)};
  }
  if(active){
   if(this.mode==='idle'||this.mode==='settling'||study!==this.study){this.mode='starting';this.elapsed=0;this.startWeight=this.weight;this.startFeet=this.pose?this.pose.legs.map(l=>({base:cp(l.base),up:l.baseUp,roll:l.bootAngle,pad:l.pad,shift:l.shift})):null;this.records={};this.settle=null;}
   this.elapsed+=dt;this.weight=mix(this.startWeight,1,ease(this.elapsed/.28));if(this.elapsed>=.28)this.mode='walking';
   this.cycle+=study?dt/this.reference.cycle_seconds:distance/(this.reference.stride_height_ratio*h*Math.max(.36,Math.hypot(this.yaw.x,this.yaw.y*.36)));
   this.travel+=distance;
  }else if(this.mode==='walking'||this.mode==='starting'){
   this.mode='settling';this.elapsed=0;this.settle={legs:this.pose.legs.map(l=>({base:cp(l.base),up:l.baseUp,roll:l.bootAngle,pad:l.pad,shift:l.shift})),weight:this.weight};this.records={};
  }else if(this.mode==='settling'){
   this.elapsed+=dt;this.weight=this.settle.weight*(1-ease(this.elapsed/.46));
   if(this.elapsed>=.46){this.mode='idle';this.weight=0;this.settle=null;}
  }
  this.p=cp(p);this.h=h;this.study=study;return this.getPose();
 }
 roll(phase){const keys=this.reference.key_poses;for(let i=0;i<keys.length-1;i++){const a=keys[i],b=keys[i+1];if(phase<=b.phase)return mix(a.roll_degrees,b.roll_degrees,ease((phase-a.phase)/(b.phase-a.phase)))*Math.PI/180;}return keys[0].roll_degrees*Math.PI/180;}
 getPose(){
  const h=this.h,phase=((this.cycle%1)+1)%1,w=this.weight,stanceEnd=this.reference.stance_fraction,S=this.reference.stride_height_ratio*h;
  const neutralRotation=this.reference.source_foot.neutral_rotation_radians,scale=h/this.reference.source_foot.height;
  const source=this.reference.source_foot,soleSource=[(source.heel[0]+source.ball[0])/2,(source.heel[1]+source.ball[1])/2];
  const dx=source.cuff[0]-soleSource[0],dy=source.cuff[1]-soleSource[1];
  const cuffF=(dx*Math.cos(neutralRotation)-dy*Math.sin(neutralRotation))*scale;
  const cuffUp=-(dx*Math.sin(neutralRotation)+dy*Math.cos(neutralRotation))*scale;
  const halfSole=Math.hypot(source.ball[0]-source.heel[0],source.ball[1]-source.heel[1])*scale/2;
  const l1=h*Math.hypot(32,72)/421,l2=h*Math.hypot(24,61)/421,total=l1+l2;
  const sway=Math.sin(TAU*phase)*h*.005*w,prepared=[];
  let pelvisHeight=h*(.474-.010*w+.003*w*Math.cos(2*TAU*(phase-.24)));
  for(let i=0;i<2;i++){
   const id=i?'right':'left',p=(phase+i*.5)%1,side=(i?-.044:.044)*h,neutralF=(i?-.012:.012)*h;
   const neutral=this.project(neutralF,side,0);let base=cp(neutral),baseUp=0,roll=0,pad=0,shift=0,stance=true;
   if(this.mode==='walking'||this.mode==='starting'){
    const q=clamp((p-stanceEnd)/(1-stanceEnd),0,1);stance=p<stanceEnd;
    let f;
    if(stance)f=S*(stanceEnd/2-p);
    else {const a=-S*stanceEnd/2,b=S*stanceEnd/2,m=-S*(1-stanceEnd);f=a+m*q+(b-a-m)*ease(q);}
    // Fold early in swing, then extend over the longer remaining interval.
    // A late symmetric lift made an otherwise continuous knee straighten fast.
    const lift=q<.30?ease(q/.30):1-ease((q-.30)/.70);
    base=this.project(f,side,0);baseUp=stance?0:h*this.reference.swing_clearance_height_ratio*lift;roll=this.roll(p);
    if(stance){pad=halfSole*Math.abs(Math.sin(roll));shift=Math.sign(roll)*halfSole*(1-Math.cos(roll));}
    else {
     // In the air, interpolate the sole height independently of foot roll.
     // Applying a ground-support abs(sin(angle)) here creates a sharp cusp
     // precisely when a swinging shoe passes through flat.
     const rise=32*Math.PI/180,land=12*Math.PI/180;
     pad=q<.40?halfSole*Math.sin(rise)*(1-ease(q/.40)):halfSole*Math.sin(land)*ease((q-.40)/.60);
     shift=mix(halfSole*(1-Math.cos(rise)),-halfSole*(1-Math.cos(land)),ease(q));
    }
    const previous=this.records[id],step=Math.floor(this.cycle+i*.5);
    if(stance&&this.mode==='walking'&&!this.study){
     if(previous&&previous.stance&&previous.step===step){base=cp(previous.base);}
    }else if(!stance&&!this.study&&previous&&previous.release){
     const gain=1-ease(q);base.x+=previous.release.x*gain;base.y+=previous.release.y*gain;
    }
    let release=previous&&previous.release;
    if(!stance&&!this.study&&previous&&previous.stance){const nominal=this.project(-S*stanceEnd/2,side,0);release={x:previous.base.x-nominal.x,y:previous.base.y-nominal.y};base.x+=release.x*(1-ease(q));base.y+=release.y*(1-ease(q));}
    if(this.mode==='starting'&&this.startFeet){const t=ease(this.elapsed/.28),start=this.startFeet[i];base={x:mix(start.base.x,base.x,t),y:mix(start.base.y,base.y,t)};baseUp=mix(start.up,baseUp,t)+h*.012*Math.sin(Math.PI*t)**2;roll=mix(start.roll,roll,t);pad=mix(start.pad,pad,t);shift=mix(start.shift,shift,t);}
    this.records[id]={base:cp(base),stance,step,release:stance?null:release};
   }else if(this.mode==='settling'&&this.settle){
    const start=this.settle.legs[i],q=clamp((this.elapsed-(i?.08:0))/.38,0,1),t=ease(q);
    base={x:mix(start.base.x,neutral.x,t),y:mix(start.base.y,neutral.y,t)};baseUp=mix(start.up,0,t)+h*.025*Math.sin(Math.PI*q)**4;roll=mix(start.roll,0,t);pad=mix(start.pad,0,t);shift=mix(start.shift,0,t);stance=q===0||q===1;
   }
   const f=this.forward(base)+shift,up=baseUp+pad;
   const localCuffF=cuffF*Math.cos(roll)+cuffUp*Math.sin(roll),localCuffUp=cuffUp*Math.cos(roll)-cuffF*Math.sin(roll);
   // Retain the locked ground anchor's lateral coordinate in turning steps.
   const lateral=(base.x-this.p.x)*this.yaw.y-(base.y-this.p.y)/.36*this.yaw.x;
   const actualCuff=this.project(f+localCuffF,lateral,up+localCuffUp),actualSole=this.project(f,lateral,up);
   const df=f+localCuffF,cu=up+localCuffUp,maxReach=total*.995;
   const allowance=cu+Math.sqrt(Math.max((total*.10)**2,maxReach*maxReach-df*df));
   pelvisHeight=softmin(pelvisHeight,allowance,h*.0045);
   const contactId=Math.floor(this.cycle+i*.5)*2+i;
   prepared.push({id,index:i,phase:p,side,base,baseUp,roll,pad,shift,stance,cuff:actualCuff,sole:actualSole,df,cu,lateral,contactId,footF:f,footUp:up});
  }
  const pelvis=this.project(0,sway,pelvisHeight),legs=[];
  for(const leg of prepared){
   const df=leg.df,down=pelvisHeight-leg.cu,reach=Math.hypot(df,down),along=(l1*l1-l2*l2+reach*reach)/(2*Math.max(1e-6,reach));
   const bend=Math.sqrt(Math.max(0,l1*l1-along*along)),kf=df/reach*along+down/reach*bend,kd=down/reach*along-df/reach*bend;
   const hip=this.project(0,leg.lateral+sway,pelvisHeight),knee=this.project(kf,leg.lateral+sway*.5,pelvisHeight-kd);
   const heel=this.project(leg.footF-halfSole*Math.cos(leg.roll),leg.lateral,leg.footUp+halfSole*Math.sin(leg.roll));
   const toe=this.project(leg.footF+halfSole*Math.cos(leg.roll),leg.lateral,leg.footUp-halfSole*Math.sin(leg.roll));
   legs.push({...leg,hip,knee,ankle:leg.cuff,ground:cp(leg.base),toe,heel,bootAngle:leg.roll,lift:leg.baseUp,
    thigh:Math.atan2(kf,kd),shin:Math.atan2(df-kf,down-kd),arm:.18*Math.cos(TAU*leg.phase),
    sagittal:{forward:df,kneeForward:kf,kneeDown:kd,ankleUp:leg.cu,pelvisHeight,thighLength:l1,shinLength:l2,reachRatio:reach/(l1+l2)}});
  }
  this.pose={phase,blend:w,mode:this.mode,pelvis,pelvisHeight,bob:h*.474-pelvisHeight,legs,yaw:{...this.yaw},travel:this.travel,
   torso:{x:pelvis.x,y:pelvis.y,angle:.008*Math.sin(TAU*phase)*w},sourceFoot:source};return this.pose;
 }
}
return {Gait};
});
