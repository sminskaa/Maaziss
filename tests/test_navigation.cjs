'use strict';
const assert=require('node:assert/strict');
const {Navigation,distance}=require('../walking/navigation.js');
const room=require('../walking/room.json');
const nav=new Navigation(room);
let assertions=0;
function check(value,message){assert.ok(value,message);assertions++;}
check(nav.isWalkable(room.start),'Initial feet are in clear floor');
check(!nav.isWalkable({x:900,y:300}),'Door/wall is not floor');
check(!nav.isWalkable({x:1300,y:545}),'Chest footprint is solid');
check(!nav.isWalkable({x:150,y:730}),'Foreground bottles are solid');
check(!nav.isWalkable({x:1260-10,y:545}),'Foot clearance keeps feet away from chest edge');
check(nav.findPath(room.start,{x:900,y:100}).status==='unreachable','High wall click rejected');
check(nav.findPath(room.start,{x:1300,y:545}).status==='adjusted','Furniture click adjusts to clear floor');
check(nav.findPath(room.start,{x:NaN,y:3}).status==='unreachable','Non-finite input rejected');
check(nav.findPath({x:0,y:0},room.start).status==='unreachable','Invalid start cannot teleport');
const rearLeft={x:1030,y:563},rearRight={x:1460,y:598};
check(nav.isWalkable(rearLeft)&&nav.isWalkable(rearRight),'Detour test endpoints valid');
check(!nav.segmentSafe(rearLeft,rearRight),'Chest blocks direct segment');
const detour=nav.findPath(rearLeft,rearRight);
check(detour.path.length>2,'Route actually bends around chest');
for(const [i,p] of detour.path.entries())if(i)check(nav.segmentSafe(detour.path[i-1],p),'Detour has clearance on each segment');
// Broad deterministic room coverage: every pair of sampled reachable endpoints.
const points=nav.nodes.filter((_,i)=>i%37===0).map(({x,y})=>({x,y}));
for(const start of points)for(const end of points){
  const result=nav.findPath(start,end);
  check(result.status==='exact','All authored floor remains connected');
  check(distance(result.path[0],start)<1e-6&&distance(result.path.at(-1),end)<1e-6,'No snapping at route endpoints');
  for(let i=1;i<result.path.length;i++){
    const a=result.path[i-1],b=result.path[i];check(nav.segmentSafe(a,b),'Smoothed segment has continuous clearance');
    for(let s=0;s<=8;s++)check(nav.isWalkable({x:a.x+(b.x-a.x)*s/8,y:a.y+(b.y-a.y)*s/8}),'Sampled route remains inside floor');
  }
}
// Redirecting starts at the actual mid-route feet, never the previous destination.
const route=nav.findPath(room.start,rearLeft).path;
const midpoint={x:(route[0].x+route[1].x)/2,y:(route[0].y+route[1].y)/2};
const redirected=nav.findPath(midpoint,{x:600,y:660});
check(redirected.path.length>=2&&distance(redirected.path[0],midpoint)<1e-6,'Redirection preserves current position');
console.log(`${assertions} navigation assertions passed; ${nav.nodes.length} clear grid nodes.`);
