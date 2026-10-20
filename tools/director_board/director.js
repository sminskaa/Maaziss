'use strict';
const $=id=>document.getElementById(id), canvas=$('scene'), ctx=canvas.getContext('2d');
const KEY='maziss-director-v1', FORMAT='maziss-visual-direction', images={}, history=[];
const defaults=()=>({format:FORMAT,version:1,room:'room',coordinates:'normalized-screen-top-left',start:{x:.53,y:.83},end:{x:.65,y:.72},path:[],facing:'N',height:.39,showActor:true,intent:'',notes:[]});
let state=defaults(), mode='start', dragging=null, clipURL=null, storageOK=true;
const directions={N:[0,-1],NE:[.707,-.707],E:[1,0],SE:[.707,.707],S:[0,1],SW:[-.707,.707],W:[-1,0],NW:[-.707,-.707]};
const clone=x=>JSON.parse(JSON.stringify(x));
function validPoint(p){return p&&Number.isFinite(p.x)&&Number.isFinite(p.y)&&p.x>=0&&p.x<=1&&p.y>=0&&p.y<=1;}
function validate(s){
 if(!s||s.format!==FORMAT||s.version!==1||!['room','background'].includes(s.room)||!validPoint(s.start)||!validPoint(s.end)||!Array.isArray(s.path)||s.path.length>200||!s.path.every(validPoint)||!Object.hasOwn(directions,s.facing)||!Number.isFinite(s.height)||s.height<.15||s.height>.65||typeof s.showActor!=='boolean'||typeof s.intent!=='string'||s.intent.length>20000||!Array.isArray(s.notes)||s.notes.length>200)throw Error('This is not a supported Maziss directions file.');
 for(const n of s.notes){if(!n||typeof n.text!=='string'||n.text.length>10000||!['scene','clip'].includes(n.type)||(n.type==='scene'&&!validPoint(n))||(n.type==='clip'&&(!Number.isFinite(n.time)||n.time<0||typeof n.clip!=='string')))throw Error('A correction in this file is invalid.');}
 return s;
}
try{const saved=localStorage.getItem(KEY);if(saved)state=validate(JSON.parse(saved));}catch(e){storageOK=false;}
function checkpoint(){history.push(clone(state));if(history.length>60)history.shift();}
function saveLocal(){try{localStorage.setItem(KEY,JSON.stringify(state));storageOK=true;$('saveStatus').textContent='Saved in this browser. Download the directions file to share or keep a portable copy.';}catch(e){storageOK=false;$('saveStatus').textContent='Browser storage unavailable. Use “Save directions file” before closing.';}}
function changed(){saveLocal();sync();draw();}
function sync(){
 $('roomChoice').value=state.room;$('size').value=Math.round(state.height*100);$('sizeValue').textContent=Math.round(state.height*100)+'% of view';$('showActor').checked=state.showActor;$('intent').value=state.intent;$('undo').disabled=!history.length;
 document.querySelectorAll('[data-face]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.face===state.facing)));
 $('notes').replaceChildren();state.notes.forEach((n,i)=>{const li=document.createElement('li'),b=document.createElement('button');li.textContent=(n.type==='clip'?`${n.clip} · ${n.time.toFixed(2)}s: `:'')+n.text;b.textContent='×';b.setAttribute('aria-label','Delete correction '+(i+1));b.onclick=()=>{checkpoint();state.notes.splice(i,1);changed();};li.append(b);$('notes').append(li);});
}
function setMode(m){mode=m;document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===m)));$('instruction').textContent={start:'Click at the feet to place Maziss’s start. Drag the turquoise point to adjust.',end:'Click at the feet to place the destination. Drag the gold point to adjust.',path:'Click to add route points between start and destination, in travel order.',note:'Write a comment on the right, then click where the correction belongs.'}[m];}
function arrow(a,b,color,width=5){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();const t=Math.atan2(b.y-a.y,b.x-a.x);ctx.beginPath();ctx.moveTo(b.x,b.y);ctx.lineTo(b.x-18*Math.cos(t-.5),b.y-18*Math.sin(t-.5));ctx.moveTo(b.x,b.y);ctx.lineTo(b.x-18*Math.cos(t+.5),b.y-18*Math.sin(t+.5));ctx.stroke();}
function pixel(p){return{x:p.x*canvas.width,y:p.y*canvas.height};}
function circle(p,color,label){const q=pixel(p);ctx.fillStyle='#10212b';ctx.strokeStyle=color;ctx.lineWidth=4;ctx.beginPath();ctx.arc(q.x,q.y,13,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.font='bold 19px system-ui';ctx.fillStyle=color;ctx.strokeStyle='#10212b';ctx.lineWidth=5;ctx.strokeText(label,q.x+19,q.y+7);ctx.fillText(label,q.x+19,q.y+7);}
function draw(){
 const bg=images[state.room];if(!bg)return;canvas.height=Math.round(canvas.width*bg.naturalHeight/bg.naturalWidth);ctx.drawImage(bg,0,0,canvas.width,canvas.height);
 const route=[state.start,...state.path,state.end];ctx.lineJoin='round';ctx.setLineDash([12,8]);ctx.strokeStyle='#ffda80';ctx.lineWidth=4;ctx.beginPath();route.forEach((p,i)=>{const q=pixel(p);if(i)ctx.lineTo(q.x,q.y);else ctx.moveTo(q.x,q.y);});ctx.stroke();ctx.setLineDash([]);
 if(state.showActor&&images.actor){const h=state.height*canvas.height,w=h*images.actor.naturalWidth/images.actor.naturalHeight,p=pixel(state.start);ctx.drawImage(images.actor,p.x-w/2,p.y-h,w,h);}
 state.path.forEach((p,i)=>circle(p,'#ffda80',String(i+1)));circle(state.start,'#80f2df','START');circle(state.end,'#ffda80','STOP');const p=pixel(state.end),d=directions[state.facing];arrow({x:p.x,y:p.y-22},{x:p.x+d[0]*70,y:p.y-22+d[1]*70},'#ffda80');
 state.notes.forEach((n,i)=>{if(n.type!=='scene')return;const p=pixel(n);ctx.strokeStyle='#ff8fc6';ctx.lineWidth=4;ctx.beginPath();ctx.arc(p.x,p.y,26,0,Math.PI*2);ctx.stroke();ctx.fillStyle='#17232b';ctx.fillRect(p.x+20,p.y-27,30,28);ctx.fillStyle='#ffb9dd';ctx.font='bold 20px system-ui';ctx.fillText(String(i+1),p.x+25,p.y-6);});
}
function position(e){const r=canvas.getBoundingClientRect();return{x:Math.max(0,Math.min(1,(e.clientX-r.left)/r.width)),y:Math.max(0,Math.min(1,(e.clientY-r.top)/r.height))};}
canvas.onpointerdown=e=>{if(e.button!==0)return;const p=position(e),r=canvas.getBoundingClientRect(),dist=k=>Math.hypot((p.x-state[k].x)*r.width,(p.y-state[k].y)*r.height);if(mode!=='note'&&mode!=='path'&&(dist('start')<22||dist('end')<22)){checkpoint();dragging=dist('start')<dist('end')?'start':'end';canvas.setPointerCapture(e.pointerId);return;}
 if(mode==='note'){const text=$('comment').value.trim();if(!text){$('instruction').textContent='First write your correction in the comment box.';$('comment').focus();return;}checkpoint();state.notes.push({type:'scene',...p,text});$('comment').value='';}
 else{checkpoint();if(mode==='path')state.path.push(p);else state[mode]=p;}changed();};
canvas.onpointermove=e=>{if(dragging){state[dragging]=position(e);draw();}};
function endDrag(){if(dragging){dragging=null;changed();}}canvas.onpointerup=endDrag;canvas.onpointercancel=endDrag;
document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>setMode(b.dataset.mode));
document.querySelectorAll('[data-face]').forEach(b=>b.onclick=()=>{checkpoint();state.facing=b.dataset.face;changed();});
$('size').onpointerdown=()=>checkpoint();$('size').oninput=()=>{state.height=Number($('size').value)/100;changed();};
$('roomChoice').onchange=()=>{checkpoint();state.room=$('roomChoice').value;changed();};$('showActor').onchange=()=>{checkpoint();state.showActor=$('showActor').checked;changed();};
$('intent').onfocus=()=>checkpoint();$('intent').oninput=()=>{state.intent=$('intent').value;saveLocal();};
$('undo').onclick=()=>{if(history.length){state=history.pop();changed();}};$('clearPath').onclick=()=>{checkpoint();state.path=[];changed();};
function download(blob,name){const a=document.createElement('a'),url=URL.createObjectURL(blob);a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);}
$('save').onclick=()=>{download(new Blob([JSON.stringify({...state,exportedAt:new Date().toISOString()},null,2)],{type:'application/json'}),'maziss-directions.json');$('saveStatus').textContent='Directions download requested. Attach maziss-directions.json in chat to share it with me.';};
$('load').onclick=()=>$('loadFile').click();$('loadFile').onchange=async()=>{const f=$('loadFile').files[0];if(!f)return;try{if(f.size>1000000)throw Error('Directions file is too large.');const next=validate(JSON.parse(await f.text()));checkpoint();state=next;changed();}catch(e){$('saveStatus').textContent='Could not open: '+e.message;}$('loadFile').value='';};
$('picture').onclick=()=>{
 const out=document.createElement('canvas'),c=out.getContext('2d');out.width=canvas.width;c.font='19px system-ui';
 const lines=[];function wrap(text){let line='';for(const word of text.split(/\s+/)){if(c.measureText(line+' '+word).width>out.width-50&&line){lines.push(line);line='';}line+=(line?' ':'')+word;}if(line)lines.push(line);}
 wrap('Maziss visual directions · '+(state.room==='room'?'Current 16:9 room':'Earlier painted room')+' · Final facing: '+state.facing);
 if(state.intent)wrap('Action: '+state.intent);
 state.notes.forEach((n,i)=>wrap((i+1)+'. '+(n.type==='clip'?n.clip+' at '+n.time.toFixed(2)+'s: ':'')+n.text));
 out.height=canvas.height+35+lines.length*28;c.drawImage(canvas,0,0);c.fillStyle='#17232b';c.fillRect(0,canvas.height,out.width,out.height-canvas.height);c.fillStyle='#fff0d7';c.font='19px system-ui';lines.forEach((l,i)=>c.fillText(l,20,canvas.height+30+i*28));out.toBlob(b=>{if(b)download(b,'maziss-marked-room.png');},'image/png');
};
$('reset').onclick=()=>{if(confirm('Reset all positions and comments? Undo can restore them.')){checkpoint();state=defaults();changed();}};
$('reference').src=ASSETS.original;
$('clipFile').onchange=()=>{const f=$('clipFile').files[0];if(!f)return;if(clipURL)URL.revokeObjectURL(clipURL);clipURL=URL.createObjectURL(f);$('clip').src=clipURL;$('clipPane').hidden=false;};
$('clipNote').onclick=()=>{const text=$('comment').value.trim(),f=$('clipFile').files[0];if(!text){$('comment').focus();$('instruction').textContent='Write a comment, then record it at the paused video time.';return;}$('clip').pause();checkpoint();state.notes.push({type:'clip',clip:f.name,time:$('clip').currentTime,text});$('comment').value='';changed();};
Promise.all(Object.entries(ASSETS).filter(([k])=>k!=='original').map(([k,src])=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{images[k]=im;resolve();};im.onerror=reject;im.src=src;}))).then(()=>{sync();draw();setMode('start');if(storageOK)saveLocal();else $('saveStatus').textContent='Browser storage unavailable or saved file unreadable. Use “Save directions file”.';}).catch(()=>$('instruction').textContent='An embedded image failed to load. Please report this message.');
