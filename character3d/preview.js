/* Offline review of complete closed meshes and shared FBX-driven skeleton. */
(async function(){
'use strict';
const canvas=document.getElementById('model'),status=document.getElementById('status'),fallback=document.getElementById('fallback');
let data;
try{
 const packed=Uint8Array.from(atob(MODEL_DATA),c=>c.charCodeAt(0));
 data=JSON.parse(await new Response(new Blob([packed]).stream().pipeThrough(new DecompressionStream('gzip'))).text());
 const textures={};
 for(const [name,url] of Object.entries(PAINT_SOURCES)){
  textures[name]=await new THREE.TextureLoader().loadAsync(url);textures[name].colorSpace=THREE.SRGBColorSpace;
  textures[name].minFilter=THREE.LinearMipmapLinearFilter;textures[name].magFilter=THREE.LinearFilter;
 }
 const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,preserveDrawingBuffer:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setSize(900,720,false);renderer.outputColorSpace=THREE.SRGBColorSpace;
 renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(35,900/720,.02,30),target=new THREE.Vector3(0,0,1.04);
 scene.add(new THREE.HemisphereLight(0xc7dce1,0x493422,2));
 const key=new THREE.DirectionalLight(0xffe1b1,2.4);key.position.set(-2,-3,5);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.camera.left=-2;key.shadow.camera.right=2;key.shadow.camera.top=3;key.shadow.camera.bottom=-2;key.shadow.normalBias=.02;scene.add(key);
 const fill=new THREE.DirectionalLight(0x97c7db,1.1);fill.position.set(2,1,3);scene.add(fill);
 const floor=new THREE.Mesh(new THREE.CircleGeometry(2.2,64),new THREE.MeshStandardMaterial({color:0x9c8f74,roughness:1}));floor.rotation.x=-Math.PI/2;floor.position.z=-.01; // overwritten below: model uses Z-up
 floor.rotation.set(0,0,0);floor.position.set(0,0,.002);floor.receiveShadow=true;scene.add(floor);
 const contact=new THREE.Mesh(new THREE.CircleGeometry(.26,48),new THREE.MeshBasicMaterial({color:0x211524,transparent:true,opacity:.2,depthWrite:false}));contact.scale.y=.5;contact.position.z=.003;scene.add(contact);
 camera.up.set(0,0,1);
 const rigRoot=new THREE.Group();scene.add(rigRoot);
 const bones=data.bones.map(b=>{const bone=new THREE.Bone(),m=new THREE.Matrix4().fromArray(b.matrix);m.decompose(bone.position,bone.quaternion,bone.scale);rigRoot.add(bone);return bone;});
 rigRoot.updateMatrixWorld(true);const skeleton=new THREE.Skeleton(bones);
 const rest=data.bones.map((b,i)=>({head:new THREE.Vector3(...b.head),dir:new THREE.Vector3(...b.tail).sub(new THREE.Vector3(...b.head)).normalize(),q:bones[i].quaternion.clone()}));
 const meshes=[],groups={};let vertices=0;
 for(const item of data.objects){
  const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(item.positions,3));geometry.setAttribute('normal',new THREE.Float32BufferAttribute(item.normals,3));geometry.setAttribute('skinIndex',new THREE.Uint16BufferAttribute(item.skinIndices,4));geometry.setAttribute('skinWeight',new THREE.Float32BufferAttribute(item.skinWeights,4));geometry.setIndex(item.indices);
  geometry.computeBoundingSphere();vertices+=item.positions.length/3;
  for(const [name,size] of [['paintFront',2],['paintBack',2],['paintSide',2],['paintBlend',3]])geometry.setAttribute(name,new THREE.Float32BufferAttribute(item[name],size));
  const palette={'Head and neck':0xc08b5d,'Eyes':0xc08b5d,'Mouth':0x9f6347,'Hair':0x50321f,'Jacket':0x47584d,'Shirt':0xbb8c42,'Pants':0x62533f,'Boots':0x704825,'Bag':0x855023,'Upper arms':0xc08b5d,'Lower arms':0xc08b5d,'Hands':0xc08b5d};
  const color=item.name.toLowerCase().includes('sole')?new THREE.Color(0x34281e):palette[item.group]?new THREE.Color(palette[item.group]):new THREE.Color(...item.color);
  const material=new THREE.MeshBasicMaterial({color,side:THREE.DoubleSide});
  if(item.paintKind!=='solid'){
   const garment=item.paintKind==='garment';
   material.onBeforeCompile=shader=>{
    shader.uniforms.paintDepth={value:textures[garment?'garment':'depth']};shader.uniforms.paintSideMap={value:textures[garment?'garment':'side']};
    shader.vertexShader='attribute vec2 paintFront;attribute vec2 paintBack;attribute vec2 paintSide;attribute vec3 paintBlend;varying vec2 pf;varying vec2 pb;varying vec2 ps;varying vec3 pw;\n'+shader.vertexShader;
    shader.vertexShader=shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\npf=paintFront;pb=paintBack;ps=paintSide;pw=paintBlend;');
    shader.fragmentShader='uniform sampler2D paintDepth;uniform sampler2D paintSideMap;varying vec2 pf;varying vec2 pb;varying vec2 ps;varying vec3 pw;float softRect(vec2 p,vec2 c,vec2 h){vec2 d=abs(p-c)-h;return 1.0-smoothstep(-1.0,2.0,max(d.x,d.y));}\n'+shader.fragmentShader;
    shader.fragmentShader=shader.fragmentShader.replace('#include <map_fragment>',`vec4 f=texture2D(paintDepth,pf),b=texture2D(paintDepth,pb),s=texture2D(paintSideMap,ps);
     ${item.name==='Head'?`vec2 fp=vec2(pf.x*1774.0,(1.0-pf.y)*887.0),sp=vec2(ps.x*1774.0,(1.0-ps.y)*887.0);
     float fm=max(max(softRect(fp,vec2(244.0,65.0),vec2(12.0,14.0)),softRect(fp,vec2(278.0,65.0),vec2(12.0,14.0))),max(softRect(fp,vec2(223.0,78.0),vec2(9.0,19.0)),softRect(fp,vec2(294.0,78.0),vec2(9.0,19.0))));
     float sm=max(softRect(sp,vec2(310.0,60.0),vec2(12.0,14.0)),softRect(sp,vec2(276.0,72.0),vec2(11.0,17.0)));
     vec3 skin=texture2D(paintDepth,vec2(272.0/1774.0,1.0-86.0/887.0)).rgb;
     f.rgb=mix(f.rgb,skin,fm);s.rgb=mix(s.rgb,skin,sm);`:''}
     vec3 confidence=${item.paintKind==='portrait'?'smoothstep(vec3(.18),vec3(.85),vec3(f.a,b.a,s.a))':'vec3(1.0)'};
     vec3 w=max(pw,vec3(0.0))*confidence;
     if(w.x+w.y+w.z<.01)w=confidence;
     if(w.x+w.y+w.z<.01)w=max(pw,vec3(0.0));
     w/=max(.00001,w.x+w.y+w.z);
     vec3 painted=mix(diffuse,f.rgb,smoothstep(.18,.85,f.a))*w.x+mix(diffuse,b.rgb,smoothstep(.18,.85,b.a))*w.y+mix(diffuse,s.rgb,smoothstep(.18,.85,s.a))*w.z;
     diffuseColor.rgb=painted;`);
   };
   material.customProgramCacheKey=()=> 'reference-paint-'+item.paintKind+(item.name==='Head'?'-skin-features':'');
  }
  const mesh=new THREE.SkinnedMesh(geometry,material);mesh.name=item.name;mesh.frustumCulled=false;mesh.castShadow=mesh.receiveShadow=true;scene.add(mesh);mesh.bind(skeleton,new THREE.Matrix4());meshes.push({mesh,item});(groups[item.group]??=[]).push(mesh);
  if(item.name!=='Neck'&&['Jacket','Pants','Boots','Bag','Head and neck','Hands'].includes(item.group)&&item.positions.length>300){
   const ink=new THREE.MeshBasicMaterial({color:0x302219,side:THREE.BackSide});
   ink.onBeforeCompile=shader=>{shader.vertexShader=shader.vertexShader.replace('#include <begin_vertex>','vec3 transformed=vec3(position+normal*.0025);');};ink.customProgramCacheKey=()=> 'rounded-ink';
   const outline=new THREE.SkinnedMesh(geometry,ink);outline.name='Ink '+item.name;outline.frustumCulled=false;outline.bind(skeleton,new THREE.Matrix4());mesh.add(outline);
  }
 }
 let angle=0,elevation=.16,distance=4.3,phase=0,playing=true,walk=true,turntable=false,rate=1,wire=false,last=null,frames=0;
 function backdrop(value){floor.visible=value!=='room';document.querySelector('.stage').classList.toggle('room',value==='room');}
 document.getElementById('setting').onchange=e=>{backdrop(e.target.value);draw();};backdrop('room');
 document.getElementById('surface').onchange=e=>{for(const {mesh,item} of meshes){mesh.material=e.target.value==='paint'?mesh.userData.paint:new THREE.MeshStandardMaterial({color:0x969492,roughness:1,side:THREE.DoubleSide});}draw();};
 meshes.forEach(({mesh})=>mesh.userData.paint=mesh.material);
 function view(){camera.position.set(Math.sin(angle)*distance,-Math.cos(angle)*distance,1.05+elevation*distance);camera.lookAt(target);}
 function pose(){
  const n=data.motion.frames.length-1,t=((phase%1)+1)%1*n,i=Math.floor(t),a=walk?data.motion.frames[i]:data.motion.idle,b=walk?data.motion.frames[(i+1)%n]:data.motion.idle,u=walk?t-i:0;
  for(let k=0;k<bones.length;k++){
   const head=new THREE.Vector3(...a[k].head).lerp(new THREE.Vector3(...b[k].head),u),tail=new THREE.Vector3(...a[k].tail).lerp(new THREE.Vector3(...b[k].tail),u),direction=tail.sub(head).normalize();
   bones[k].position.copy(head);bones[k].quaternion.copy(new THREE.Quaternion().setFromUnitVectors(rest[k].dir,direction).multiply(rest[k].q));
  }
  rigRoot.updateMatrixWorld(true);skeleton.update();
 }
 function draw(){view();pose();renderer.render(scene,camera);frames++;}
 const defaults=['Head and neck','Hair','Eyes','Mouth','Body','Upper arms','Lower arms','Hands','Upper legs','Lower legs','Feet','Shirt','Jacket','Belt','Pants','Boots','Bag'];
 const list=document.getElementById('items');for(const name of [...defaults,...Object.keys(groups).filter(x=>!defaults.includes(x))]){if(!groups[name])continue;const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=true;input.dataset.group=name;input.addEventListener('change',()=>{groups[name].forEach(m=>m.visible=input.checked);draw();});label.append(input,document.createTextNode(name));list.append(label);}
 document.getElementById('anatomy').onclick=()=>{for(const input of list.querySelectorAll('input')){const garment=['Shirt','Jacket','Belt','Pants','Boots','Bag'].includes(input.dataset.group);input.checked=!garment;groups[input.dataset.group].forEach(m=>m.visible=!garment);}draw();};
 document.getElementById('dressed').onclick=()=>{for(const input of list.querySelectorAll('input')){input.checked=true;groups[input.dataset.group].forEach(m=>m.visible=true);}draw();};
 document.getElementById('pause').onclick=()=>{playing=!playing;document.getElementById('pause').textContent=playing?'Pause':'Play';};
 document.getElementById('idle').onclick=()=>{walk=!walk;document.getElementById('idle').textContent=walk?'Stand still':'Walk';draw();};
 document.getElementById('step').onclick=()=>{playing=false;walk=true;phase=(phase+1/30/data.motion.cycleSeconds)%1;document.getElementById('pause').textContent='Play';document.getElementById('idle').textContent='Stand still';draw();};
 document.getElementById('rate').onchange=e=>{rate=+e.target.value;};
 document.getElementById('spin').onchange=e=>{turntable=e.target.checked;};
 document.getElementById('wire').onchange=e=>{wire=e.target.checked;meshes.forEach(({mesh})=>mesh.material.wireframe=wire);draw();};
 for(const button of document.querySelectorAll('[data-angle]'))button.onclick=()=>{angle=+button.dataset.angle*Math.PI/180;draw();};
 let drag=null;canvas.onpointerdown=e=>{drag={x:e.clientX,y:e.clientY,a:angle,h:elevation};canvas.setPointerCapture(e.pointerId);};canvas.onpointermove=e=>{if(drag){angle=drag.a+(e.clientX-drag.x)*.008;elevation=Math.max(-.03,Math.min(.65,drag.h+(e.clientY-drag.y)*.003));draw();}};canvas.onpointerup=()=>drag=null;canvas.onpointercancel=()=>drag=null;
 canvas.addEventListener('wheel',e=>{e.preventDefault();distance=Math.max(2.7,Math.min(6,distance+e.deltaY*.002));draw();},{passive:false});
 function tick(now){const dt=last===null?0:Math.min(.05,(now-last)/1000);last=now;let changed=false;if(playing&&walk){phase=(phase+dt*rate/data.motion.cycleSeconds)%1;changed=true;}if(turntable){angle+=dt*.35;changed=true;}if(changed)draw();requestAnimationFrame(tick);}
 window.maziss3d={ready:true,data,renderer,scene,camera,meshes,bones,groups,
  getState:()=>({phase,playing,walk,angle,frames,vertices,objects:meshes.length,visible:Object.fromEntries(Object.entries(groups).map(([n,m])=>[n,m.every(x=>x.visible)]))}),
  setView:a=>{angle=a*Math.PI/180;draw();},setPhase:p=>{phase=p;playing=false;walk=true;draw();},setWalking:value=>{walk=value;draw();},setBackdrop:backdrop,draw,
  snapshot:()=>{draw();return canvas.toDataURL('image/png');}};
 status.textContent=`Ready — original-art surface study. Drag to orbit; scroll to zoom.`;
 fallback.hidden=true;draw();requestAnimationFrame(tick);
}catch(error){status.textContent='The live 3D viewer could not start here. Open the rendered review link above.';fallback.hidden=false;window.maziss3d={ready:false,error:String(error)};console.error(error);}
})();
