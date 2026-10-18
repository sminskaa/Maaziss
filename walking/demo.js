(function () {
  'use strict';
  const canvas=document.getElementById('room'),ctx=canvas.getContext('2d');
  const detail=document.getElementById('detail'),detailContext=detail.getContext('2d');
  const status=document.getElementById('status'),pauseButton=document.getElementById('pause');
  const nav=new MazissNavigation.Navigation(ROOM),background=new Image(),atlas=new Image(),depthAtlas=new Image(),clothingAtlas=new Image();
  const gait=new MazissFbxGait.Gait(FBX_MOTION);
  let painted=null;
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
    const pace=heightAt()*gait.reference.stride_height_ratio/gait.reference.cycle_seconds;
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
  function character(){
    const h=heightAt();facing=pose.yaw.x>=0?1:-1;direction=Math.abs(pose.yaw.x)>.65?(facing<0?'left':'right'):(pose.yaw.y<0?'up':'down');
    ctx.save();ctx.fillStyle='#140f1b66';ctx.beginPath();ctx.ellipse(pos.x,pos.y-2,h*.14,11,0,0,Math.PI*2);ctx.fill();ctx.restore();
    renderMetrics=painted.draw(ctx,pose,h);
    if(showFeet)for(const leg of pose.legs){ctx.strokeStyle=leg.id==='left'?'#79dfff':'#ffb38c';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(leg.ground.x,leg.ground.y,9,4,0,0,Math.PI*2);ctx.stroke();}
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
    renderPose:(context,pose,height)=>painted.draw(context,pose,height),getPainter:()=>painted,
    getState:()=>({ready,position:{...pos},speed,moving,paused,facing,direction,travel,study,pose,render:renderMetrics,target:target?{...target}:null,requested:requested?{...requested}:null,path:waypoints.map(p=>({...p})),samples:samples.map(p=>({...p})),commands:commands.map(p=>({...p}))}),
    getGaitSamples:()=>JSON.parse(JSON.stringify(gaitSamples))};
  let loaded=0;function load(){if(++loaded===4){painted=new MazissPaintedCharacter.Character(atlas,depthAtlas,clothingAtlas);ready=true;pose=gait.getPose();document.getElementById('room-fallback').hidden=true;document.getElementById('room-fallback').style.display='none';canvas.style.display='block';say('Ready. Click an open patch of floor.');}}
  background.onload=atlas.onload=depthAtlas.onload=clothingAtlas.onload=load;background.onerror=atlas.onerror=depthAtlas.onerror=clothingAtlas.onerror=()=>say('The embedded artwork could not be loaded. Please report this preview error.');
  background.src=BACKGROUND_URL;atlas.src=ATLAS_URL;depthAtlas.src=DEPTH_ATLAS_URL;clothingAtlas.src=CLOTHING_ATLAS_URL;requestAnimationFrame(tick);
})();
