/* Retarget the actual bilateral FBX skeleton onto fixed original-art proportions.
 * The image-study class supplies only route/start/stop state, not walking poses. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory(require('./image-gait.js'));else root.MazissFbxGait=factory(root.MazissImageGait);})(typeof globalThis!=='undefined'?globalThis:this,function(base){
'use strict';
const mix=(a,b,t)=>a+(b-a)*t,TAU=Math.PI*2;
const sub=(a,b)=>a.map((x,i)=>x-b[i]);
const unit=v=>{const n=Math.hypot(...v)||1;return v.map(x=>x/n);};
const blendDir=(a,b,t)=>unit(a.map((v,i)=>mix(v,b[i],t)));
const sum=(a,b)=>a.map((x,i)=>x+b[i]);
const mul=(a,k)=>a.map(x=>x*k);
class Gait extends base.Gait{
 constructor(data){
  const stride=data.inferredStrideBodyHeights*(.355/.504);
  super({cycle_seconds:data.cycleSeconds,stride_height_ratio:stride});
  this.data=data;this.frames=data.samples.slice(0,-1);this.reference.stride_height_ratio=stride;
 }
 sampleFbx(phase){
  const n=this.frames.length,t=((phase%1)+1)%1*n,i=Math.floor(t),u=t-i;
  const f=[-1,0,1,2].map(d=>this.frames[(i+d+n)%n]);
  const cubic=(a,b,c,d)=>.5*((2*b)+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u);
  const joints={};for(const key of Object.keys(f[1].joints))joints[key]=[0,1,2].map(k=>cubic(...f.map(x=>x.joints[key][k])));
  const pitch={};for(const key of ['left','right'])pitch[key]=cubic(...f.map(x=>x.footPitchDeg[key]));
  return {joints,pitch,pelvisUp:cubic(...f.map(x=>x.pelvisUp))};
 }
 getPose(){
  if(!this.data)return null;
  const h=this.h,w=this.weight,phase=((this.cycle%1)+1)%1,source=this.sampleFbx(phase);
  const L1=.187*h,L2=.168*h,B=46/421*h,heelF=-18/421*h,toeF=50/421*h,soleOffset=(heelF+toeF)/2;
  // A neutral sole centred under the hip, with a small relaxed knee bend.
  const cuffF=-soleOffset,kneeF=.012*h;
  const idleThigh=unit([kneeF,0,-Math.sqrt(L1*L1-kneeF*kneeF)]);
  const idleShin=unit([cuffF-kneeF,0,-Math.sqrt(L2*L2-(cuffF-kneeF)**2)]);
  const parts=[];let floor=-Infinity;
  for(const [i,id] of ['left','right'].entries()){
   const j=source.joints,thigh=blendDir(idleThigh,unit(sub(j[id+'Knee'],j[id+'Hip'])),w);
   const shin=blendDir(idleShin,unit(sub(j[id+'Ankle'],j[id+'Knee'])),w);
   const hip=[0,(i?-.045:.045)*h,j[id+'Hip'][2]*h*w],knee=sum(hip,mul(thigh,L1)),cuff=sum(knee,mul(shin,L2));
   const roll=.60*Math.tanh(-source.pitch[id]*Math.PI/180/.60)*w;
   const key=(f)=>[cuff[0]+f*Math.cos(roll)+B*Math.sin(roll),cuff[1],cuff[2]+f*-Math.sin(roll)-B*Math.cos(roll)];
   const heel=key(heelF),toe=key(toeF),sole=mul(sum(heel,toe),.5);
   const need=-Math.min(heel[2],toe[2]);
   floor=floor===-Infinity?need:Math.max(floor,need)+h*.0015*Math.log1p(Math.exp(-Math.abs(floor-need)/(h*.0015)));
   parts.push({id,index:i,hip,knee,cuff,heel,toe,sole,roll,thigh,shin});
  }
  const pelvisHeight=floor,pelvis=this.project(0,0,pelvisHeight),legs=[];
  const world=v=>this.project(v[0],v[1],v[2]+pelvisHeight);
  for(const p of parts){
   const hip=world(p.hip),knee=world(p.knee),cuff=world(p.cuff),heel=world(p.heel),toe=world(p.toe),sole=world(p.sole);
   const base=this.project(p.sole[0],p.sole[1],0),lift=Math.max(0,Math.min(p.heel[2],p.toe[2])+pelvisHeight);
   legs.push({id:p.id,phase:(phase+p.index*.5)%1,hip,knee,cuff,ankle:cuff,heel,toe,sole,base,ground:base,baseUp:lift,lift,
    pad:0,shift:0,bootAngle:p.roll,stance:lift<h*.008,contactId:Math.floor(this.cycle+p.index*.5)*2+p.index,
    thigh:Math.atan2(p.thigh[0],-p.thigh[2]),shin:Math.atan2(p.shin[0],-p.shin[2]),
    depth:this.yaw.y*p.sole[0]-this.yaw.x*p.sole[1],local:{hip:p.hip,knee:p.knee,cuff:p.cuff,sole:p.sole},
    sagittal:{forward:p.cuff[0],kneeForward:p.knee[0],kneeDown:-p.knee[2],ankleUp:p.cuff[2]+pelvisHeight,pelvisHeight,thighLength:L1,shinLength:L2}});
  }
  const arms=['left','right'].map(id=>{
   const j=source.joints,d=blendDir([0,0,-1],unit(sub(j[id+'Wrist'],j[id+'Shoulder'])),w);
   const shoulder=[-.015*h,j[id+'Shoulder'][1]*h*.80,.25*h],wrist=sum(shoulder,mul(d,.29*h));
   const a=world(shoulder),b=world(wrist);
   return {id,shoulder:a,wrist:b,forwardAngle:Math.atan2(d[0],-d[2]),screenAngle:Math.atan2(b.x-a.x,b.y-a.y),depth:this.yaw.y*wrist[0]-this.yaw.x*wrist[1]};
  });
  const c=source.joints.chest,n=this.data.neutral.joints.chest;
  const torsoAngle=(Math.atan2(this.yaw.x*c[0]+this.yaw.y*c[1],c[2])-Math.atan2(this.yaw.x*n[0]+this.yaw.y*n[1],n[2]))*.18*w;
  this.pose={phase,blend:w,mode:this.mode,pelvis,pelvisHeight,bob:h*.46-pelvisHeight,legs,arms,yaw:{...this.yaw},travel:this.travel,
   torso:{x:pelvis.x,y:pelvis.y,angle:torsoAngle},motionSource:this.data.source.filename,sourcePhase:phase,cycleSeconds:this.data.cycleSeconds};
  return this.pose;
 }
}
return {Gait};
});
