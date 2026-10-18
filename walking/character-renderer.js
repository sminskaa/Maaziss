/* Complete clothing/equipment layers, with original heads and articulated arms.
 * Torso coverage is never obtained by subtracting moving arms from a screenshot.
 * Both trousers end at the actual skeletal cuff, including in depth views. */
(function(root){
'use strict';
const profiles={
 Side:{height:421,hip:[267,237],body:[[170,5],[345,5],[345,110],[307,135],[307,190],[309,219],[295,246],[270,258],[253,251],[243,269],[174,269],[174,218],[191,188],[181,145],[190,111]],
  arms:[{pivot:[225,133],neutral:-.325,poly:[[215,117],[237,130],[229,161],[216,184],[209,210],[207,228],[202,246],[195,255],[185,255],[176,248],[182,231],[184,210],[190,181],[189,160],[202,138]]},
        {pivot:[286,137],neutral:.555,poly:[[279,126],[295,139],[307,170],[323,196],[341,216],[361,232],[357,249],[342,251],[326,237],[308,226],[297,209],[285,184],[278,160]]}],
  pants:{a:[270,240],b:[302,312],c:[326,380],poly:[[246,224],[281,227],[296,263],[321,298],[326,323],[337,355],[341,379],[331,388],[309,386],[305,366],[295,343],[286,320],[277,297],[259,272],[246,254]]},
  boot:{top:[713,386],sole:[729,432],poly:[[690,385],[735,383],[744,399],[769,403],[777,411],[777,429],[760,435],[693,434],[684,422],[684,405]]}},
 Front:{height:428,hip:[258,239],body:[[165,8],[344,8],[344,164],[326,200],[316,232],[302,249],[286,252],[275,274],[255,274],[239,255],[211,260],[180,239],[171,200]],
  arms:[{pivot:[202,143],neutral:0,poly:[[192,125],[214,138],[207,185],[201,218],[199,247],[198,281],[176,290],[164,279],[168,249],[171,214],[172,192],[180,154]]},
        {pivot:[313,140],neutral:0,poly:[[299,123],[321,131],[333,168],[338,201],[337,227],[344,270],[330,287],[313,285],[308,263],[307,225],[304,193],[294,157]]}],
  pants:{a:[235,247],b:[225,319],c:[216,383],poly:[[210,233],[255,237],[247,315],[241,353],[240,385],[222,393],[197,388],[198,355],[204,308]]},
  boot:{top:[215,391],sole:[215,434],poly:[[196,390],[240,390],[244,411],[242,437],[172,440],[173,414],[188,402]]}},
 Back:{height:413,hip:[252,665],body:[[163,447],[340,447],[340,600],[327,637],[319,659],[302,678],[277,684],[268,700],[247,700],[234,679],[210,681],[186,662],[167,630]],
  arms:[{pivot:[202,573],neutral:0,poly:[[187,552],[211,563],[203,606],[198,641],[198,672],[197,704],[175,710],[161,696],[167,665],[170,637],[168,615],[177,580]]},
        {pivot:[315,574],neutral:0,poly:[[300,551],[325,561],[334,602],[340,640],[338,673],[338,703],[316,708],[306,691],[310,662],[308,639],[300,599],[294,573]]}],
  pants:{a:[226,673],b:[219,744],c:[211,809],poly:[[207,653],[252,653],[245,722],[237,780],[234,812],[213,821],[191,815],[191,787],[198,729]]},
  boot:{top:[210,821],sole:[208,857],poly:[[190,820],[233,821],[236,840],[233,859],[161,863],[161,840],[181,829]]}}
};
// Generated repair assets contain complete cloth hidden by arms and complete
// bags. Mapping preserves the first character's anchors and proportions; the
// original atlases, face and approved room remain untouched.
const equipment={
 Side:{head:[[238,5],[345,5],[345,103],[311,103],[299,110],[292,122],[280,117],[274,108],[275,100],[261,96],[238,94]],
  details:[[265,90],[294,95],[307,128],[303,175],[308,219],[294,246],[264,253],[239,249],[218,236],[215,214],[214,187],[217,157],[217,130],[236,111]],
  torso:{src:[108,100,360,444],dst:[182,101,132,154],poly:[[239,102],[284,102],[310,132],[309,191],[308,223],[294,250],[252,255],[214,248],[207,217],[207,171],[192,165],[189,143],[212,115]]},
  bag:{src:[190,685,226,271],dst:[203,196,59,76],poly:[[203,196],[262,196],[262,272],[203,272]]},
  pelvis:[[249,231],[282,231],[299,258],[279,272],[251,260]],
 },
 Front:{head:[[200,5],[321,5],[321,100],[288,101],[282,117],[254,117],[246,100],[200,99]],
  details:[[236,108],[285,108],[312,126],[312,166],[310,197],[309,230],[302,248],[280,247],[267,251],[253,245],[226,250],[207,240],[206,207],[205,179],[204,153],[209,130]],
  torso:{src:[527,100,465,444],dst:[173,106,165,145],poly:[[236,107],[284,107],[319,128],[334,165],[317,189],[316,226],[304,249],[267,247],[226,251],[199,241],[192,205],[184,183],[174,171],[176,142],[208,119]]},
  bag:{src:[614,685,310,273],dst:[187,204,57,79],poly:[[187,204],[244,204],[244,283],[187,283]]},
  pelvis:[[210,235],[303,235],[305,272],[283,282],[259,273],[239,283],[211,276]],
  otherPants:{a:[283,247],b:[289,319],c:[299,383],poly:[[261,234],[301,233],[306,274],[312,315],[314,350],[321,385],[298,393],[275,386],[272,349],[269,311],[261,277]]},
  otherBoot:{top:[301,391],sole:[305,434],poly:[[278,390],[321,389],[329,409],[342,421],[341,434],[316,440],[268,436],[269,417]]}
 },
 Back:{head:[[195,445],[314,445],[314,525],[286,535],[282,550],[231,550],[225,535],[195,530]],
  details:[[226,535],[280,535],[312,555],[316,600],[312,643],[305,669],[282,677],[244,677],[212,677],[198,662],[197,631],[199,595],[198,563]],
  torso:{src:[1024,115,446,423],dst:[167,532,174,143],poly:[[222,533],[279,533],[309,543],[332,565],[341,609],[324,633],[316,663],[295,675],[253,675],[207,676],[190,660],[183,633],[166,621],[169,581],[193,549]]},
  bag:{src:[1118,686,294,270],dst:[272,627,51,78],poly:[[272,627],[323,627],[323,705],[272,705]]},
  pelvis:[[205,650],[296,650],[301,688],[278,704],[254,693],[232,705],[207,690]],
  otherPants:{a:[277,673],b:[283,744],c:[292,809],poly:[[257,653],[296,653],[303,704],[309,747],[314,790],[316,813],[295,822],[272,816],[270,784],[265,739],[260,701]]},
  otherBoot:{top:[293,821],sole:[302,857],poly:[[273,820],[315,820],[319,834],[337,844],[337,858],[308,864],[267,859],[266,838]]}
 }
};
function path(ctx,p){ctx.beginPath();p.forEach((v,i)=>i?ctx.lineTo(...v):ctx.moveTo(...v));ctx.closePath();}
function layer(image,poly,holes=[]){
 const x=Math.floor(Math.min(...poly.map(p=>p[0])))-2,y=Math.floor(Math.min(...poly.map(p=>p[1])))-2;
 const w=Math.ceil(Math.max(...poly.map(p=>p[0])))-x+3,h=Math.ceil(Math.max(...poly.map(p=>p[1])))-y+3;
 const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;const c=canvas.getContext('2d',{willReadFrequently:true});
 c.save();c.translate(-x,-y);path(c,poly);c.clip();c.drawImage(image,0,0);c.restore();
 c.save();c.translate(-x,-y);c.globalCompositeOperation='destination-out';for(const p of holes){path(c,p);c.fill();}c.restore();
 const pixels=c.getImageData(0,0,w,h),data=pixels.data,labels=new Int32Array(w*h),queue=new Int32Array(w*h);let next=0,best=0,bestSize=0,removed=0;
 for(let k=0;k<w*h;k++)if(!labels[k]&&data[k*4+3]>24){
  const label=++next;let head=0,tail=0;queue[tail++]=k;labels[k]=label;
  while(head<tail){const v=queue[head++],vx=v%w;for(const n of [vx?v-1:-1,vx<w-1?v+1:-1,v-w,v+w])if(n>=0&&n<w*h&&!labels[n]&&data[n*4+3]>24){labels[n]=label;queue[tail++]=n;}}
  if(tail>bestSize){best=label;bestSize=tail;}
 }
 for(let k=0;k<w*h;k++)if(labels[k]!==best){if(data[k*4+3])removed++;data[k*4+3]=0;}
 c.putImageData(pixels,0,0);return {canvas,x,y,w,h,removed,components:next};
}
function drawLayer(ctx,L){ctx.drawImage(L.canvas,L.x,L.y);}
function mergeLayers(a,b){
 const x=Math.min(a.x,b.x),y=Math.min(a.y,b.y),w=Math.max(a.x+a.w,b.x+b.w)-x,h=Math.max(a.y+a.h,b.y+b.h)-y;
 const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;const c=canvas.getContext('2d');c.translate(-x,-y);drawLayer(c,a);drawLayer(c,b);
 return {canvas,x,y,w,h,removed:a.removed+b.removed,components:1};
}
function mappedLayer(image,part){
 const canvas=document.createElement('canvas');canvas.width=512;canvas.height=900;
 const c=canvas.getContext('2d');c.drawImage(image,...part.src,...part.dst);
 return layer(canvas,part.poly);
}
function triangle(ctx,L,a,b,c,A,B,C){
 const det=(b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]);if(Math.abs(det)<1e-8)return;
 const u={x:(B.x-A.x),y:(B.y-A.y)},v={x:(C.x-A.x),y:(C.y-A.y)};
 const aa=(u.x*(c[1]-a[1])-v.x*(b[1]-a[1]))/det,cc=(v.x*(b[0]-a[0])-u.x*(c[0]-a[0]))/det;
 const bb=(u.y*(c[1]-a[1])-v.y*(b[1]-a[1]))/det,dd=(v.y*(b[0]-a[0])-u.y*(c[0]-a[0]))/det;
 // Adjacent texture triangles share vertices but independent antialias clips
 // leave translucent cracks. A subpixel edge overlap closes the cloth surface.
 const points=[A,B,C],centre={x:(A.x+B.x+C.x)/3,y:(A.y+B.y+C.y)/3};
 const normals=points.map((p,i)=>{const q=points[(i+1)%3],dx=q.x-p.x,dy=q.y-p.y,n=Math.hypot(dx,dy)||1;let nx=-dy/n,ny=dx/n;if(nx*(centre.x-p.x)+ny*(centre.y-p.y)>0){nx=-nx;ny=-ny;}return {x:nx,y:ny};});
 const expanded=points.flatMap((p,i)=>[normals[(i+2)%3],normals[i]].map(n=>[p.x+n.x*.45,p.y+n.y*.45]));
 ctx.save();path(ctx,expanded);ctx.clip();ctx.transform(aa,bb,cc,dd,A.x-aa*a[0]-cc*a[1],A.y-bb*a[0]-dd*a[1]);drawLayer(ctx,L);ctx.restore();
}
function skin(ctx,L,p,a,b,c,scale){
 function bone(s,t,A,B,q){const dx=t[0]-s[0],dy=t[1]-s[1],ls=Math.hypot(dx,dy),tx=(B.x-A.x),ty=(B.y-A.y),lt=Math.hypot(tx,ty),u=((q[0]-s[0])*dx+(q[1]-s[1])*dy)/ls,v=(-(q[0]-s[0])*dy+(q[1]-s[1])*dx)/ls;return {x:A.x+tx/ls*u-ty/lt*v*scale,y:A.y+ty/ls*u+tx/lt*v*scale};}
 const rows=[];
 for(let k=0;k<=18;k++){const t=k/18,first=t<=.5,local=first?t*2:(t-.5)*2,s=first?p.a:p.b,e=first?p.b:p.c,dx=e[0]-s[0],dy=e[1]-s[1],n=Math.hypot(dx,dy),mid=[s[0]+dx*local,s[1]+dy*local],r=23-3*t;
  const points=[-1,1].map(sign=>[mid[0]-dy/n*r*sign,mid[1]+dx/n*r*sign]);
  const weight=Math.max(0,Math.min(1,(t-.35)/.30)),w=weight*weight*(3-2*weight);
  rows.push(points.map(q=>{const u=bone(p.a,p.b,a,b,q),v=bone(p.b,p.c,b,c,q);return {source:q,target:{x:u.x+(v.x-u.x)*w,y:u.y+(v.y-u.y)*w}};}));
 }
 for(let k=0;k<rows.length-1;k++){const [a,b]=rows[k],[c,d]=rows[k+1];triangle(ctx,L,a.source,b.source,c.source,a.target,b.target,c.target);triangle(ctx,L,b.source,d.source,c.source,b.target,d.target,c.target);}
}
class Character{
 constructor(side,depth,clothing){this.cache={};this.debug=[];for(const [name,p]of Object.entries(profiles)){const image=name==='Side'?side:depth,e=equipment[name];
  const backing=mappedLayer(clothing,e.torso),details=layer(image,e.details);
  // Retain the original collar/neck and tailoring over complete hidden cloth.
  // This is an opaque torso core, not an arm-shaped subtractive cutout.
  const body=mergeLayers(backing,details);
  this.cache[name]={head:layer(image,e.head),body,bag:mappedLayer(clothing,e.bag),pelvis:layer(image,e.pelvis),arms:p.arms.map(a=>layer(image,a.poly)),pants:layer(image,p.pants.poly),boot:layer(image,p.boot.poly)};
  if(e.otherPants){this.cache[name].otherPants=layer(image,e.otherPants.poly);this.cache[name].otherBoot=layer(image,e.otherBoot.poly);}
 }}
 draw(output,pose,h){
  if(!this.frame){this.frame=document.createElement('canvas');this.frame.width=this.frame.height=640;this.frameCtx=this.frame.getContext('2d',{willReadFrequently:true});this.labels=new Int32Array(640*640);this.queue=new Int32Array(640*640);}
  // Integer framebuffer placement avoids a second bilinear resample separating
  // a cleaned edge into a floating pixel island. Joint positions stay fractional.
  const ctx=this.frameCtx,width=Math.min(640,Math.ceil(h*1.2)),height=Math.min(640,Math.ceil(h*1.12)),origin={x:Math.floor(pose.pelvis.x-width/2),y:Math.floor(pose.pelvis.y-h*.60)};
  ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,640,640);ctx.translate(-origin.x,-origin.y);
  const metrics=this.drawParts(ctx,pose,h);
  ctx.setTransform(1,0,0,1,0,0);
  // Cleaning individual cutouts cannot catch a clipped hand/bag sliver that
  // separates only after deformation. Remove tiny orphan components from the
  // assembled transparent silhouette before it is composited over the room.
  const pixels=ctx.getImageData(0,0,width,height),d=pixels.data,labels=this.labels,queue=this.queue;labels.fill(0,0,width*height);let id=0,removed=0;
  const small=new Set(),limit=Math.ceil(110*(h/421)**2);
  for(let k=0;k<width*height;k++)if(!labels[k]&&d[k*4+3]>64){let head=0,tail=0;queue[tail++]=k;labels[k]=++id;
   while(head<tail){const v=queue[head++],x=v%width;for(let j=0;j<4;j++){const n=j===0?(x?v-1:-1):j===1?(x<width-1?v+1:-1):j===2?v-width:v+width;if(n>=0&&n<width*height&&!labels[n]&&d[n*4+3]>64){labels[n]=id;queue[tail++]=n;}}}
   if(tail<=limit)small.add(id);
  }
  for(let k=0;k<width*height;k++){
   let keep=labels[k]&&!small.has(labels[k]);
   if(!labels[k]&&d[k*4+3]>8){
    // Retain an antialiased fringe only next to a substantial opaque core.
    // A faint bridge must not attach an otherwise floating hand/bag sliver.
    const x=k%width,y=Math.floor(k/width);
    for(let yy=Math.max(0,y-1);yy<=Math.min(height-1,y+1)&&!keep;yy++)for(let xx=Math.max(0,x-1);xx<=Math.min(width-1,x+1);xx++){const id=labels[yy*width+xx];if(id&&!small.has(id)){keep=true;break;}}
   }
   if(!keep){if(d[k*4+3])removed++;d[k*4+3]=0;}
  }
  ctx.putImageData(pixels,0,0);output.drawImage(this.frame,0,0,width,height,origin.x,origin.y,width,height);
  metrics.orphanPixelsRemoved=removed;return metrics;
 }
 drawParts(ctx,pose,h){
  const side=Math.abs(pose.yaw.x)>.65,name=side?'Side':pose.yaw.y<0?'Back':'Front',p=profiles[name],cache=this.cache[name],scale=h/p.height,face=pose.yaw.x>=0?1:-1;
  const joints=[],layers=[],feet=[];
  const armOrder=[...pose.arms].sort((a,b)=>a.depth-b.depth),screenArms=[...pose.arms].sort((a,b)=>a.shoulder.x-b.shoulder.x);
  const arm=(a,near)=>{
   const index=side?(near?0:1):screenArms.indexOf(a),src=p.arms[index];
   const angle=side?src.neutral-a.forwardAngle:(src.neutral-a.screenAngle*.5);
   ctx.save();ctx.translate(pose.pelvis.x,pose.pelvis.y);ctx.rotate(pose.torso.angle);if(side)ctx.scale(face,1);ctx.scale(scale,scale);ctx.translate(-p.hip[0],-p.hip[1]);ctx.translate(...src.pivot);ctx.rotate(angle);ctx.translate(-src.pivot[0],-src.pivot[1]);drawLayer(ctx,cache.arms[index]);ctx.restore();layers.push(near?'near-arm':'far-arm');
  };
  arm(armOrder[0],false);
  const rigid=L=>{ctx.save();ctx.translate(pose.pelvis.x,pose.pelvis.y);ctx.rotate(pose.torso.angle);if(side)ctx.scale(face,1);ctx.scale(scale,scale);ctx.translate(-p.hip[0],-p.hip[1]);drawLayer(ctx,L);ctx.restore();};
  rigid(cache.pelvis);
  for(const leg of [...pose.legs].sort((a,b)=>a.depth-b.depth)){
   let cuff,sole;let pant=p.pants,pantLayer=cache.pants;
   if(side){
    const roll=leg.bootAngle,c=Math.cos(roll),s=Math.sin(roll);cuff=leg.cuff;
    ctx.save();ctx.translate(cuff.x,cuff.y);ctx.transform(pose.yaw.x*c*scale,(pose.yaw.y*.36*c+s)*scale,-pose.yaw.x*s*scale,(-pose.yaw.y*.36*s+c)*scale,0,0);ctx.translate(-p.boot.top[0],-p.boot.top[1]);drawLayer(ctx,cache.boot);ctx.restore();
    const point=q=>{const x=(q[0]-p.boot.top[0])*scale,y=(q[1]-p.boot.top[1])*scale,f=c*x-s*y,v=s*x+c*y;return {x:cuff.x+pose.yaw.x*f,y:cuff.y+pose.yaw.y*.36*f+v};};
    sole=point(p.boot.sole);feet.push({id:leg.id,heel:point([695,432]),toe:point([763,432]),rotation:roll});
   }else{
    // Select the actual observer-left/right artwork, rather than rendering the
    // same left-facing foot twice. The cuff stays on the skeletal ankle; only
    // shoe foreshortening is projected, never an extra shift of the trouser end.
    const rightOnScreen=leg.hip.x>pose.pelvis.x,other=rightOnScreen;
    const boot=other?equipment[name].otherBoot:p.boot,bootLayer=other?cache.otherBoot:cache.boot;
    pant=other?equipment[name].otherPants:p.pants;pantLayer=other?cache.otherPants:cache.pants;
    cuff=leg.cuff;sole=leg.sole;
    const ys=(sole.y-cuff.y)/(boot.sole[1]-boot.top[1]);
    ctx.save();ctx.translate(cuff.x,cuff.y);ctx.scale(scale,ys);ctx.translate(-boot.top[0],-boot.top[1]);drawLayer(ctx,bootLayer);ctx.restore();
    feet.push({id:leg.id,heel:{x:sole.x-16*scale,y:sole.y},toe:{x:sole.x+16*scale,y:sole.y},rotation:0,artwork:other?'observer-right':'observer-left'});
   }
   // The entire grey cuff is in this same connected cloth mesh, never a shoe.
   skin(ctx,pantLayer,pant,leg.hip,leg.knee,cuff,scale);
   layers.push('leg-'+leg.id);joints.push({id:leg.id,shinEnd:cuff,bootCuff:cuff,paintedContact:sole,pantContinuous:true});
  }
  rigid(cache.body);layers.push('body');rigid(cache.head);rigid(cache.bag);layers.push('bag');
  arm(armOrder[1],true);
  return {source:'first-proposal',baseHeight:h,view:name,joins:joints,layers,feet,farArm:armOrder[0].id,nearArm:armOrder[1].id,
   maskCleanup:Object.fromEntries(Object.entries(cache).filter(([k])=>k!=='arms').map(([k,L])=>[k,{removed:L.removed,components:L.components}])),continuousPants:true,completeTorso:true,independentBag:true};
 }
}
root.MazissPaintedCharacter={Character,profiles,equipment};
})(globalThis);
