(function () {
  'use strict';
  const canvas=document.getElementById('room'),ctx=canvas.getContext('2d');
  const detail=document.getElementById('detail'),detailContext=detail.getContext('2d');
  const status=document.getElementById('status'),pauseButton=document.getElementById('pause');
  const nav=new MazissNavigation.Navigation(ROOM),background=new Image(),atlas=new Image(),depthAtlas=new Image();
  const gait=new MazissImageGait.Gait(IMAGE_MOTION,{isWalkable:p=>nav.isWalkable(p)});
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  let pos={...ROOM.start},waypoints=[],target=null,requested=null,speed=0,travel=0,facing=1;
  let paused=false,debug=false,showFeet=false,lastTime=null,ready=false,moving=false,direction='right';
  let travelDirection={x:1,y:0},pose=null,renderMetrics=null,study=false,studyDirection={x:1,y:0},playback=1;
  const samples=[{...pos,time:0}],commands=[],gaitSamples=[];
  const baseHeightAt=()=>370+110*Math.max(0,Math.min(1,(pos.y-530)/240));
  const heightAt=()=>baseHeightAt();
  gait.reset(pos,heightAt());
  function say(text){status.textContent=text;}
  function record(){samples.push({...pos,time:performance.now(),speed});if(samples.length>12000)samples.splice(0,2000);}
  function recordPose(){gaitSamples.push({time:performance.now(),position:{...pos},height:heightAt(),speed,moving,paused,direction,pose,render:renderMetrics});if(gaitSamples.length>6000)gaitSamples.splice(0,1000);}
  function goTo(x,y) {
    if(!ready)return {status:'loading',path:[]};
    study=false;document.getElementById('study').checked=false;const result=nav.findPath(pos,{x,y});
    commands.push({x,y,status:result.status,time:performance.now()});if(commands.length>100)commands.shift();
    if(!result.target){say('That spot is out of reach. Choose the room floor.');return result;}
    waypoints=result.path.slice(1).map(p=>({...p}));target={...result.target};requested={x,y};
    if(MazissNavigation.distance(pos,target)<1){waypoints=[];speed=0;moving=false;say('Already here.');}
    else say(result.status==='adjusted'?'Walking to the nearest clear floor beside that spot.':'Walking…');
    return result;
  }
  function reset(){study=false;document.getElementById('study').checked=false;pos={...ROOM.start};waypoints=[];target=null;requested=null;speed=0;travel=0;moving=false;facing=1;direction='right';travelDirection={x:1,y:0};pose=gait.reset(pos,heightAt());record();recordPose();say('Reset. Click an open patch of floor.');}
  function setPaused(value){paused=value;pauseButton.textContent=paused?'Resume':'Pause';pauseButton.setAttribute('aria-pressed',String(paused));lastTime=null;say(paused?'Paused.':waypoints.length?'Walking…':'Ready. Click an open patch of floor.');}
  function remainingDistance(){let total=0,previous=pos;for(const p of waypoints){total+=MazissNavigation.distance(previous,p);previous=p;}return total;}
  function update(dt){
    if(!waypoints.length||paused){moving=false;return;}
    const remaining=remainingDistance();
    const perspective=Math.max(0,Math.min(1,(pos.y-530)/240));
    const aim=waypoints[0],aimDistance=Math.hypot(aim.x-pos.x,aim.y-pos.y);
    // Depth is compressed by the room perspective. Match projected speed to
    // projected stride so walking away does not become rapid little steps.
    const projection=.4+.6*Math.abs(aim.x-pos.x)/Math.max(aimDistance,1e-6);
    const pace=heightAt()*IMAGE_MOTION.stride_height_ratio/IMAGE_MOTION.cycle_seconds;
    const desired=Math.min(pace*projection,Math.sqrt(2*1100*remaining));
    speed+=Math.max(-1250*dt,Math.min(1050*dt,desired-speed));
    let budget=Math.min(remaining,Math.max(0,speed*dt));moving=budget>0.001;
    while(budget>0&&waypoints.length){
      const next=waypoints[0],dx=next.x-pos.x,dy=next.y-pos.y,d=Math.hypot(dx,dy);
      if(d<0.001){waypoints.shift();continue;}
      const step=Math.min(d,budget,4),candidate={x:pos.x+dx/d*step,y:pos.y+dy/d*step};
      if(!nav.segmentSafe(pos,candidate)){waypoints=[];speed=0;moving=false;say('The route is blocked. Choose another floor destination.');break;}
      travelDirection={x:dx/d,y:dy/d};
      if(Math.abs(dy)>Math.abs(dx)*0.65)direction=dy<0?'up':'down';
      else {direction=dx<0?'left':'right';facing=dx<0?-1:1;}
      pos=candidate;travel+=step;budget-=step;record();
      if(step>=d-0.001)waypoints.shift();
    }
    if(!waypoints.length){speed=0;moving=false;say('Arrived. Click another patch of floor.');}
  }
  function polygon(poly){ctx.beginPath();poly.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();}
  // Source joints and masks are sampled directly from the FIRST character atlas.
  // Original character textures are retained; limbs are articulated at runtime.
  const originalLegs={
    Side:{thigh:{a:[270,240],b:[302,312],poly:[[247,225],[280,225],[324,300],[324,321],[297,331],[276,300],[246,254]]},
      shin:{a:[302,312],b:[326,373],poly:[[294,300],[321,300],[339,359],[340,381],[309,387],[295,349],[286,326]]},
      boot:{cuff:[326,373],sole:[326,429],poly:[[303,368],[337,357],[355,382],[380,382],[405,394],[405,420],[355,437],[311,429],[303,397]]}},
    Front:{thigh:{a:[235,247],b:[225,319],poly:[[211,233],[255,236],[248,317],[240,335],[207,331],[204,299]]},
      shin:{a:[225,319],b:[216,380],poly:[[207,304],[246,306],[241,354],[239,388],[199,389],[198,356]]},
      boot:{cuff:[216,380],sole:[215,434],poly:[[197,370],[240,371],[243,402],[241,434],[173,440],[174,409],[190,398]]}},
    Back:{thigh:{a:[226,673],b:[219,744],poly:[[207,652],[253,653],[246,718],[239,756],[200,757],[199,710]]},
      shin:{a:[219,744],b:[211,806],poly:[[200,730],[242,732],[237,780],[232,814],[193,815],[190,788]]},
      boot:{cuff:[211,806],sole:[208,856],poly:[[191,796],[234,799],[234,829],[230,857],[163,861],[162,834],[182,825]]}}
  };
  function clipSource(poly){ctx.beginPath();poly.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();ctx.clip();}
  function sourcePart(image,part,a,b,widthScale){
    const sa=part.a,sb=part.b,sourceLength=Math.hypot(sb[0]-sa[0],sb[1]-sa[1]);
    ctx.save();ctx.translate(a.x,a.y);ctx.rotate(Math.atan2(b.y-a.y,b.x-a.x));
    ctx.scale(Math.hypot(b.x-a.x,b.y-a.y)/sourceLength,widthScale);
    ctx.rotate(-Math.atan2(sb[1]-sa[1],sb[0]-sa[0]));ctx.translate(-sa[0],-sa[1]);
    clipSource(part.poly);ctx.drawImage(image,0,0);ctx.restore();
  }
  function originalBoot(image,part,leg,scale,side){
    // The leg was solved against THIS painted cuff, not a separate ankle that
    // is subsequently moved by shoe registration. All joins share one geometry.
    const cuff=leg.cuff,sourceContact=side?IMAGE_MOTION.source_foot.ball:part.sole;
    const angle=IMAGE_MOTION.source_foot.neutral_rotation_radians+leg.bootAngle,c=Math.cos(angle),s=Math.sin(angle);
    const transformPoint=p=>{const x=(p[0]-part.cuff[0])*scale,y=(p[1]-part.cuff[1])*scale,f=c*x-s*y,v=s*x+c*y;
      return {x:cuff.x+pose.yaw.x*f,y:cuff.y+pose.yaw.y*.36*f+v};};
    const paintedContact=side?transformPoint(sourceContact):leg.sole;
    return {cuff,paintedContact,sourceContact,draw:()=>{
      if(!side){sourcePart(image,{a:part.cuff,b:part.sole,poly:part.poly},cuff,leg.sole,scale);return;}
      ctx.save();ctx.translate(cuff.x,cuff.y);
      ctx.transform(pose.yaw.x*c*scale,(pose.yaw.y*.36*c+s)*scale,-pose.yaw.x*s*scale,(-pose.yaw.y*.36*s+c)*scale,0,0);
      ctx.translate(-part.cuff[0],-part.cuff[1]);clipSource(part.poly);ctx.drawImage(image,0,0);ctx.restore();
    }};
  }
  const armMasks={
    Side:[{pivot:[225,133],poly:[[215,116],[237,130],[229,161],[216,184],[209,210],[211,228],[207,252],[189,259],[176,250],[182,231],[184,210],[190,181],[189,160],[202,138]]},
          {pivot:[286,137],poly:[[279,126],[295,139],[307,170],[323,196],[341,216],[361,232],[357,249],[342,251],[326,237],[308,226],[297,209],[285,184],[278,160]]}],
    Front:[{pivot:[202,143],poly:[[192,125],[214,138],[207,185],[201,218],[199,247],[198,281],[176,290],[164,279],[168,249],[171,214],[172,192],[180,154]]},
           {pivot:[313,140],poly:[[299,123],[321,131],[333,168],[338,201],[337,227],[344,270],[330,287],[313,285],[308,263],[307,225],[304,193],[294,157]]}],
    Back:[{pivot:[202,573],poly:[[187,552],[211,563],[203,606],[198,641],[198,672],[197,704],[175,710],[161,696],[167,665],[170,637],[168,615],[177,580]]},
          {pivot:[315,574],poly:[[300,551],[325,561],[334,602],[340,640],[338,673],[338,703],[316,708],[306,691],[310,662],[308,639],[300,599],[294,573]]}]
  };
  function originalUpper(image,f,h,side,suffix){
    const scale=h/f.h,hip=suffix==='Side'?[267,237]:suffix==='Back'?[252,665]:[258,239];
    const masks=armMasks[suffix];
    ctx.save();ctx.translate(pose.pelvis.x,pose.pelvis.y);ctx.rotate(pose.torso.angle);if(side)ctx.scale(facing,1);ctx.scale(scale,scale);ctx.translate(-hip[0],-hip[1]);
    const body=side?[[0,0],[1,0],[1,.62],[.77,.62],[.69,.545],[.58,.60],[.44,.545],[.40,.62],[0,.62]]:
      suffix==='Back'?[[0,0],[1,0],[1,.66],[.60,.66],[.60,.55],[.56,.63],[.45,.63],[.35,.55],[.20,.55],[.18,.66],[0,.66]]:
      [[0,0],[1,0],[1,.66],[.82,.66],[.79,.55],[.64,.55],[.56,.63],[.46,.63],[.40,.55],[.40,.66],[0,.66]];
    function path(points){ctx.moveTo(...points[0]);for(const p of points.slice(1))ctx.lineTo(...p);ctx.closePath();}
    // Preserve the first painted head/jacket/bag; separate the actual original
    // arms, rather than replacing the character or cycling inconsistent bodies.
    ctx.save();ctx.beginPath();path(body.map(p=>[f.x+p[0]*f.w,f.y+p[1]*f.h]));ctx.clip();
    ctx.beginPath();ctx.rect(f.x-1,f.y-1,f.w+2,f.h+2);for(const arm of masks)path(arm.poly);ctx.clip('evenodd');
    ctx.drawImage(image,f.x,f.y,f.w,f.h,f.x,f.y,f.w,f.h);ctx.restore();
    const angles=[];
    masks.forEach((arm,i)=>{
      const leg=pose.legs[i];
      const angle=side?(i?.555:-.325)+leg.arm*pose.blend:(i?1:-1)*Math.sin((pose.phase+i*.5)*Math.PI*2)*.035*pose.blend;
      angles.push(angle);ctx.save();ctx.translate(...arm.pivot);ctx.rotate(angle);
      if(!side)ctx.scale(1,1+Math.sin((pose.phase+i*.5)*Math.PI*2)*.035*pose.blend);
      ctx.translate(-arm.pivot[0],-arm.pivot[1]);ctx.beginPath();path(arm.poly);ctx.clip();ctx.drawImage(image,f.x,f.y,f.w,f.h,f.x,f.y,f.w,f.h);ctx.restore();
    });ctx.restore();return angles;
  }
  function character(){
    const h=heightAt(),side=Math.abs(pose.yaw.x)>.65;
    facing=pose.yaw.x>=0?1:-1;direction=side?(facing<0?'left':'right'):(pose.yaw.y<0?'up':'down');
    const suffix=side?'Side':direction==='up'?'Back':'Front',image=side?atlas:depthAtlas;
    const index=suffix==='Back'?4:0,f=(side?SPRITES.frames:SPRITES.depthFrames)[index];
    ctx.save();ctx.translate(pos.x,pos.y);ctx.fillStyle='#140f1b66';ctx.beginPath();ctx.ellipse(0,-2,h*.14,11,0,0,Math.PI*2);ctx.fill();ctx.restore();
    {
      const source=originalLegs[suffix],reference=side?SPRITES.frames[0]:SPRITES.depthFrames[suffix==='Back'?4:0],scale=h/reference.h,joins=[];
      for(const leg of [...pose.legs].sort((a,b)=>a.ground.y-b.ground.y)){
        const boot=originalBoot(image,source.boot,leg,scale,side);
        sourcePart(image,source.thigh,leg.hip,leg.knee,scale);
        sourcePart(image,source.shin,leg.knee,boot.cuff,scale);
        boot.draw();joins.push({id:leg.id,shinEnd:boot.cuff,bootCuff:boot.cuff,paintedContact:boot.paintedContact,sourceContact:boot.sourceContact});
      }
      const arms=originalUpper(image,f,h,side,suffix);
      renderMetrics={source:'first-proposal',originalFrame:index,joins,baseHeight:h,view:suffix,armAngles:arms};
    }
    if(showFeet){
      for(const leg of pose.legs){
        const color=leg.id==='left'?'#79dfff':'#ffb38c';
        ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(leg.ground.x,leg.ground.y,9,4,0,0,Math.PI*2);leg.stance?ctx.fill():ctx.stroke();
        ctx.font='14px system-ui';ctx.fillText(leg.id==='left'?'L':'R',leg.ground.x+12,leg.ground.y-leg.lift-5);
        if(!leg.stance){ctx.setLineDash([3,4]);ctx.beginPath();ctx.moveTo(leg.ground.x,leg.ground.y);ctx.lineTo(leg.ground.x,leg.ground.y-leg.lift);ctx.stroke();ctx.setLineDash([]);}
      }
    }
  }
  function draw(){
    ctx.clearRect(0,0,ROOM.width,ROOM.height);ctx.drawImage(background,0,0,ROOM.width,ROOM.height);
    if(debug){
      polygon(ROOM.walkable);ctx.fillStyle='#53dfa02c';ctx.fill();ctx.strokeStyle='#7affc6';ctx.lineWidth=3;ctx.stroke();
      for(const obstacle of ROOM.obstacles){polygon(obstacle.polygon);ctx.fillStyle='#ff63487a';ctx.fill();ctx.strokeStyle='#ff947b';ctx.stroke();}
      if(waypoints.length){ctx.beginPath();ctx.moveTo(pos.x,pos.y);for(const p of waypoints)ctx.lineTo(p.x,p.y);ctx.strokeStyle='#f7efad';ctx.lineWidth=3;ctx.stroke();}
    }
    if(target){
      if(target.adjusted&&requested){ctx.save();ctx.setLineDash([6,7]);ctx.strokeStyle='#ffe0a9a0';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(requested.x,requested.y);ctx.lineTo(target.x,target.y);ctx.stroke();ctx.restore();}
      ctx.strokeStyle='#ffd978';ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(target.x,target.y,17,7,0,0,Math.PI*2);ctx.stroke();
    }
    character();
    const closeHeight=heightAt()*1.12,closeWidth=closeHeight*2/3;
    detailContext.clearRect(0,0,detail.width,detail.height);
    detailContext.drawImage(canvas,pos.x-closeWidth/2,pos.y-heightAt()*1.06,closeWidth,closeHeight,0,0,detail.width,detail.height);
  }
  function tick(now){
    const dt=lastTime===null?0:Math.min(0.04,Math.max(0,(now-lastTime)/1000))*playback;lastTime=now;
    if(ready){const previous={...pos};if(!study)update(dt);const moved=Math.hypot(pos.x-previous.x,pos.y-previous.y)>1e-6;
      pose=gait.update(pos,heightAt(),paused?0:dt,moved,study?studyDirection:travelDirection,study);
      draw();recordPose();}
    requestAnimationFrame(tick);
  }
  canvas.addEventListener('pointerdown',event=>{if(event.button!==0)return;const r=canvas.getBoundingClientRect();goTo((event.clientX-r.left)*ROOM.width/r.width,(event.clientY-r.top)*ROOM.height/r.height);canvas.focus({preventScroll:true});});
  canvas.addEventListener('keydown',event=>{
    const offsets={ArrowLeft:[-120,0],ArrowRight:[120,0],ArrowUp:[0,-70],ArrowDown:[0,70]};
    if(offsets[event.key]){event.preventDefault();const [dx,dy]=offsets[event.key];goTo(pos.x+dx,pos.y+dy);}
    else if(event.key==='Home'){event.preventDefault();reset();}
    else if(event.key==='Escape'){waypoints=[];speed=0;moving=false;target=null;say('Stopped.');}
    else if(event.code==='Space'){event.preventDefault();setPaused(!paused);}
  });
  document.getElementById('reset').addEventListener('click',reset);
  document.getElementById('stand').addEventListener('click',()=>{study=false;document.getElementById('study').checked=false;waypoints=[];target=null;speed=0;moving=false;say('Coming to rest.');});
  pauseButton.addEventListener('click',()=>setPaused(!paused));
  document.getElementById('debug').addEventListener('change',event=>{debug=event.target.checked;});
  document.getElementById('feet').addEventListener('change',event=>{showFeet=event.target.checked;});
  document.getElementById('study').addEventListener('change',event=>{study=event.target.checked;waypoints=[];speed=0;moving=false;gait.records={};say(study?'Cycle study: choose a view. The character walks in place.':'Room mode: click the floor.');});
  document.getElementById('step').addEventListener('click',()=>{study=true;document.getElementById('study').checked=true;setPaused(true);pose=gait.update(pos,heightAt(),1/30,false,studyDirection,true);draw();recordPose();});
  document.getElementById('playback').addEventListener('change',event=>{playback=Number(event.target.value);});
  for(const button of document.querySelectorAll('[data-view]'))button.addEventListener('click',()=>{
    study=true;document.getElementById('study').checked=true;studyDirection={left:{x:-1,y:0},right:{x:1,y:0},front:{x:0,y:1},back:{x:0,y:-1}}[button.dataset.view];
    const world={x:studyDirection.x,y:studyDirection.y/.36};gait.yawAngle=Math.atan2(world.y,world.x);gait.yaw={x:Math.cos(gait.yawAngle),y:Math.sin(gait.yawAngle)};
    waypoints=[];speed=0;moving=false;gait.records={};say('Cycle study: '+button.textContent+'. Click the floor to return to room movement.');
  });
  document.addEventListener('visibilitychange' ,()=>{lastTime=null;});
  window.mazissWalk={goTo,reset,nav,navigation:nav,geometry:ROOM,
    getState:()=>({ready,position:{...pos},speed,moving,paused,facing,direction,travel,study,pose,render:renderMetrics,target:target?{...target}:null,requested:requested?{...requested}:null,path:waypoints.map(p=>({...p})),samples:samples.map(p=>({...p})),commands:commands.map(p=>({...p}))}),
    getGaitSamples:()=>JSON.parse(JSON.stringify(gaitSamples))};
  let loaded=0;function load(){if(++loaded===3){ready=true;pose=gait.getPose();document.getElementById('room-fallback').hidden=true;document.getElementById('room-fallback').style.display='none';canvas.style.display='block';say('Ready. Click an open patch of floor.');}}
  background.onload=atlas.onload=depthAtlas.onload=load;background.onerror=atlas.onerror=depthAtlas.onerror=()=>say('The embedded artwork could not be loaded. Please report this preview error.');
  background.src=BACKGROUND_URL;atlas.src=ATLAS_URL;depthAtlas.src=DEPTH_ATLAS_URL;requestAnimationFrame(tick);
})();
