/* Offline review of complete closed meshes and shared FBX-driven skeleton. */
(async function(){
'use strict';
const canvas=document.getElementById('model'),status=document.getElementById('status'),fallback=document.getElementById('fallback');
let data;
try{
 const packed=Uint8Array.from(atob(MODEL_DATA),c=>c.charCodeAt(0));
 data=JSON.parse(await new Response(new Blob([packed]).stream().pipeThrough(new DecompressionStream('gzip'))).text());
 const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,preserveDrawingBuffer:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setSize(900,720,false);renderer.outputColorSpace=THREE.SRGBColorSpace;
 renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(35,900/720,.02,30),target=new THREE.Vector3(0,0,1.04);
 scene.add(new THREE.HemisphereLight(0xc7dce1,0x493422,2));
 const key=new THREE.DirectionalLight(0xffe1b1,2.4);key.position.set(-2,-3,5);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.camera.left=-2;key.shadow.camera.right=2;key.shadow.camera.top=3;key.shadow.camera.bottom=-2;key.shadow.normalBias=.02;scene.add(key);
 const fill=new THREE.DirectionalLight(0x97c7db,1.1);fill.position.set(2,1,3);scene.add(fill);
 const floor=new THREE.Mesh(new THREE.CircleGeometry(2.2,64),new THREE.MeshStandardMaterial({color:0x9c8f74,roughness:1}));floor.rotation.x=-Math.PI/2;floor.position.z=-.01; // overwritten below: model uses Z-up
 floor.rotation.set(0,0,0);floor.position.set(0,0,.002);floor.receiveShadow=true;scene.add(floor);
 camera.up.set(0,0,1);
 const rigRoot=new THREE.Group();scene.add(rigRoot);
 const bones=data.bones.map(b=>{const bone=new THREE.Bone(),m=new THREE.Matrix4().fromArray(b.matrix);m.decompose(bone.position,bone.quaternion,bone.scale);rigRoot.add(bone);return bone;});
 rigRoot.updateMatrixWorld(true);const skeleton=new THREE.Skeleton(bones);
 const rest=data.bones.map((b,i)=>({head:new THREE.Vector3(...b.head),dir:new THREE.Vector3(...b.tail).sub(new THREE.Vector3(...b.head)).normalize(),q:bones[i].quaternion.clone()}));
 const meshes=[],groups={};let vertices=0;
 for(const item of data.objects){
  const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(item.positions,3));geometry.setAttribute('normal',new THREE.Float32BufferAttribute(item.normals,3));geometry.setAttribute('skinIndex',new THREE.Uint16BufferAttribute(item.skinIndices,4));geometry.setAttribute('skinWeight',new THREE.Float32BufferAttribute(item.skinWeights,4));geometry.setIndex(item.indices);
  geometry.computeBoundingSphere();vertices+=item.positions.length/3;
  const color=new THREE.Color(...item.color),material=new THREE.MeshToonMaterial({color,side:THREE.DoubleSide});
  const mesh=new THREE.SkinnedMesh(geometry,material);mesh.name=item.name;mesh.frustumCulled=false;mesh.castShadow=mesh.receiveShadow=true;scene.add(mesh);mesh.bind(skeleton,new THREE.Matrix4());meshes.push({mesh,item});(groups[item.group]??=[]).push(mesh);
 }
 let angle=0,elevation=.16,distance=4.3,phase=0,playing=true,walk=true,turntable=false,rate=1,wire=false,last=null,frames=0;
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
 function tick(now){const dt=last===null?0:Math.min(.05,(now-last)/1000);last=now;if(playing&&walk)phase=(phase+dt*rate/data.motion.cycleSeconds)%1;if(turntable)angle+=dt*.35;draw();requestAnimationFrame(tick);}
 window.maziss3d={ready:true,data,renderer,scene,camera,meshes,bones,groups,
  getState:()=>({phase,playing,walk,angle,frames,vertices,objects:meshes.length,visible:Object.fromEntries(Object.entries(groups).map(([n,m])=>[n,m.every(x=>x.visible)]))}),
  setView:a=>{angle=a*Math.PI/180;draw();},setPhase:p=>{phase=p;playing=false;walk=true;draw();},setWalking:value=>{walk=value;draw();},draw,
  snapshot:()=>{draw();return canvas.toDataURL('image/png');}};
 status.textContent=`Ready — ${data.bones.length} bones, ${meshes.length} mesh objects. Drag to orbit; scroll to zoom.`;
 fallback.hidden=true;draw();requestAnimationFrame(tick);
}catch(error){status.textContent='The live 3D viewer could not start here. Open the rendered review link above.';fallback.hidden=false;window.maziss3d={ready:false,error:String(error)};console.error(error);}
})();
