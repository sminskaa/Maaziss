(function () {
  'use strict';
  const canvas=document.getElementById('room'),ctx=canvas.getContext('2d');
  const status=document.getElementById('status'),pauseButton=document.getElementById('pause');
  const nav=new MazissNavigation.Navigation(ROOM),background=new Image(),atlas=new Image(),depthAtlas=new Image();
  const gait=new MazissGait.Gait({isWalkable:p=>nav.isWalkable(p)});
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  let pos={...ROOM.start},waypoints=[],target=null,requested=null,speed=0,travel=0,facing=1;
  let paused=false,debug=false,showFeet=false,lastTime=null,ready=false,moving=false,direction='right';
  let travelDirection={x:1,y:0},pose=null,upperMotion=0,renderMetrics=null;
  const samples=[{...pos,time:0}],commands=[],gaitSamples=[];
  const baseHeightAt=()=>370+110*Math.max(0,Math.min(1,(pos.y-530)/240));
  const heightAt=()=>baseHeightAt();
  gait.reset(pos,heightAt());
  function say(text){status.textContent=text;}
  function record(){samples.push({...pos,time:performance.now(),speed});if(samples.length>12000)samples.splice(0,2000);}
  function recordPose(){gaitSamples.push({time:performance.now(),position:{...pos},height:heightAt(),speed,moving,paused,direction,pose,render:renderMetrics});if(gaitSamples.length>6000)gaitSamples.splice(0,1000);}
  function goTo(x,y) {
    if(!ready)return {status:'loading',path:[]};
    const result=nav.findPath(pos,{x,y});
    commands.push({x,y,status:result.status,time:performance.now()});if(commands.length>100)commands.shift();
    if(!result.target){say('That spot is out of reach. Choose the room floor.');return result;}
    waypoints=result.path.slice(1).map(p=>({...p}));target={...result.target};requested={x,y};
    if(MazissNavigation.distance(pos,target)<1){waypoints=[];speed=0;moving=false;say('Already here.');}
    else say(result.status==='adjusted'?'Walking to the nearest clear floor beside that spot.':'Walking…');
    return result;
  }
  function reset(){pos={...ROOM.start};waypoints=[];target=null;requested=null;speed=0;travel=0;moving=false;facing=1;direction='right';travelDirection={x:1,y:0};pose=gait.reset(pos,heightAt());record();recordPose();say('Reset. Click an open patch of floor.');}
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
    const desired=Math.min((350+90*perspective)*projection,Math.sqrt(2*1100*remaining));
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
  // No replacement character artwork, body scaling, posture or shoulder rig.
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
    const sole={x:leg.ground.x,y:leg.ground.y-leg.lift},angle=leg.bootAngle;
    const dx=(part.cuff[0]-part.sole[0])*scale*(side?facing:1),dy=(part.cuff[1]-part.sole[1])*scale;
    const cuff={x:sole.x+Math.cos(angle)*dx-Math.sin(angle)*dy,y:sole.y+Math.sin(angle)*dx+Math.cos(angle)*dy};
    return {cuff,draw:()=>{
      ctx.save();ctx.translate(sole.x,sole.y);ctx.rotate(angle);ctx.scale((side?facing:1)*scale,scale);ctx.translate(-part.sole[0],-part.sole[1]);
      clipSource(part.poly);ctx.drawImage(image,0,0);ctx.restore();
    }};
  }
  function originalUpper(image,f,h,side,index){
    const scale=h/f.h,width=f.w*scale;
    ctx.save();ctx.translate(pos.x,pos.y);if(side)ctx.scale(facing,1);

    // Clip only the old trousers/feet. Keep the actual original head, jacket,
    // bag, arms and their existing painted frame-to-frame acting.
    let poly=side?[[0,0],[1,0],[1,.62],[.77,.62],[.69,.545],[.58,.60],[.44,.545],[.40,.62],[0,.62]]:
      direction==='up'?[[0,0],[1,0],[1,.66],[.60,.66],[.60,.55],[.56,.63],[.45,.63],[.35,.55],[.20,.55],[.18,.66],[0,.66]]:
      [[0,0],[1,0],[1,.66],[.82,.66],[.79,.55],[.64,.55],[.56,.63],[.46,.63],[.40,.55],[.40,.66],[0,.66]];
    clipSource(poly.map(p=>[-width*f.footX+p[0]*width,-h+p[1]*h]));
    ctx.drawImage(image,f.x,f.y,f.w,f.h,-width*f.footX,-h,width,h);ctx.restore();
  }
  function character(){
    const h=heightAt(),initial=travel===0,side=!initial&&(direction==='left'||direction==='right');
    const suffix=side?'Side':direction==='up'?'Back':'Front',image=side?atlas:depthAtlas;
    const active=speed>0||pose.legs.some(l=>!l.stance),sequence=direction==='up'?[5,6,7,6]:[1,2,3,2];
    const index=side?(active?Math.floor(travel/24)%8:0):(active?sequence[Math.floor(travel/24)%4]:(direction==='up'?4:0));
    const f=(side?SPRITES.frames:SPRITES.depthFrames)[index];
    ctx.save();ctx.translate(pos.x,pos.y);ctx.fillStyle='#140f1b66';ctx.beginPath();ctx.ellipse(0,-2,h*.14,11,0,0,Math.PI*2);ctx.fill();ctx.restore();
    if(initial){
      // The starting character is byte-for-byte the original atlas frame,
      // drawn with the first proposal's exact size and anchoring.
      ctx.drawImage(depthAtlas,f.x,f.y,f.w,f.h,pos.x-f.w*h/f.h*f.footX,pos.y-h,f.w*h/f.h,h);
      renderMetrics={source:'first-proposal',originalFrame:index,initial:true};
    }else{
      const source=originalLegs[suffix],reference=side?SPRITES.frames[0]:SPRITES.depthFrames[suffix==='Back'?4:0],scale=h/reference.h,joins=[];
      for(const leg of [...pose.legs].sort((a,b)=>a.ground.y-b.ground.y)){
        const boot=originalBoot(image,source.boot,leg,scale,side);
        sourcePart(image,source.thigh,leg.hip,leg.knee,scale);
        sourcePart(image,source.shin,leg.knee,boot.cuff,scale);
        boot.draw();joins.push({id:leg.id,shinEnd:boot.cuff,bootCuff:boot.cuff});
      }
      originalUpper(image,f,h,side,index);
      renderMetrics={source:'first-proposal',originalFrame:index,joins,baseHeight:h};
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
  }
  function tick(now){
    const dt=lastTime===null?0:Math.min(0.04,Math.max(0,(now-lastTime)/1000));lastTime=now;
    if(ready){const previous={...pos};update(dt);const moved=Math.hypot(pos.x-previous.x,pos.y-previous.y)>1e-6;
      pose=gait.update(pos,heightAt(),paused?0:dt,moved,travelDirection);
      if(!paused)upperMotion+=(Number(moved)-upperMotion)*Math.min(1,dt*9);
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
  pauseButton.addEventListener('click',()=>setPaused(!paused));
  document.getElementById('debug').addEventListener('change',event=>{debug=event.target.checked;});
  document.getElementById('feet').addEventListener('change',event=>{showFeet=event.target.checked;});
  document.addEventListener('visibilitychange',()=>{lastTime=null;});
  window.mazissWalk={goTo,reset,nav,navigation:nav,geometry:ROOM,
    getState:()=>({ready,position:{...pos},speed,moving,paused,facing,direction,travel,pose:gait.getPose(),render:renderMetrics,target:target?{...target}:null,requested:requested?{...requested}:null,path:waypoints.map(p=>({...p})),samples:samples.map(p=>({...p})),commands:commands.map(p=>({...p}))}),
    getGaitSamples:()=>JSON.parse(JSON.stringify(gaitSamples))};
  let loaded=0;function load(){if(++loaded===3){ready=true;pose=gait.getPose();document.getElementById('room-fallback').hidden=true;document.getElementById('room-fallback').style.display='none';canvas.style.display='block';say('Ready. Click an open patch of floor.');}}
  background.onload=atlas.onload=depthAtlas.onload=load;background.onerror=atlas.onerror=depthAtlas.onerror=()=>say('The embedded artwork could not be loaded. Please report this preview error.');
  background.src=BACKGROUND_URL;atlas.src=ATLAS_URL;depthAtlas.src=DEPTH_ATLAS_URL;requestAnimationFrame(tick);
})();
