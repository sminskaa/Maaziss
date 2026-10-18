(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.MazissNavigation = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const point = p => Array.isArray(p) ? {x:p[0], y:p[1]} : {x:p.x, y:p.y};
  const distance = (a,b) => Math.hypot(a.x-b.x,a.y-b.y);
  function edgeDistance(p,a,b) {
    const dx=b.x-a.x,dy=b.y-a.y,l=dx*dx+dy*dy;
    const t=l ? Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.y-a.y)*dy)/l)) : 0;
    return Math.hypot(p.x-a.x-t*dx,p.y-a.y-t*dy);
  }
  function inside(p,poly) {
    let yes=false;
    for(let i=0,j=poly.length-1;i<poly.length;j=i++) {
      const a=poly[i],b=poly[j];
      if(((a.y>p.y)!==(b.y>p.y)) && p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x) yes=!yes;
    }
    return yes;
  }
  function intersects(a,b,c,d) {
    const cross=(p,q,r)=>(q.x-p.x)*(r.y-p.y)-(q.y-p.y)*(r.x-p.x);
    const x=cross(a,b,c),y=cross(a,b,d),u=cross(c,d,a),v=cross(c,d,b);
    return x*y<0 && u*v<0;
  }
  function segmentDistance(a,b,c,d) {
    if(intersects(a,b,c,d)) return 0;
    return Math.min(edgeDistance(a,c,d),edgeDistance(b,c,d),edgeDistance(c,a,b),edgeDistance(d,a,b));
  }
  class Navigation {
    constructor(room) {
      this.room=room; this.clearance=room.clearance; this.gridSize=room.gridSize;
      this.boundary=room.walkable.map(point);
      this.obstacles=room.obstacles.map(o=>o.polygon.map(point));
      this.edges=[];
      [this.boundary,...this.obstacles].forEach(poly=>poly.forEach((a,i)=>this.edges.push([a,poly[(i+1)%poly.length]])));
      this.nodes=[]; this.cells=new Map();
      for(let y=0;y<=room.height;y+=this.gridSize) for(let x=0;x<=room.width;x+=this.gridSize) {
        const p={x,y}; if(this.isWalkable(p)) {const n={...p,id:this.nodes.length,links:[]};this.nodes.push(n);this.cells.set(x+','+y,n);}
      }
      for(const n of this.nodes) for(const dx of [-1,0,1]) for(const dy of [-1,0,1]) {
        if(!dx&&!dy)continue;
        const other=this.cells.get((n.x+dx*this.gridSize)+','+(n.y+dy*this.gridSize));
        if(other && this.segmentSafe(n,other)) n.links.push(other.id);
      }
    }
    isWalkable(p) {
      if(!p || !Number.isFinite(p.x)||!Number.isFinite(p.y)) return false;
      if(!inside(p,this.boundary)||this.obstacles.some(poly=>inside(p,poly))) return false;
      return this.edges.every(([a,b])=>edgeDistance(p,a,b)>=this.clearance-1e-6);
    }
    segmentSafe(a,b) {
      return this.isWalkable(a)&&this.isWalkable(b)&&this.edges.every(([c,d])=>segmentDistance(a,b,c,d)>=this.clearance-1e-6);
    }
    resolveTarget(target) {
      if(!target || !Number.isFinite(target.x)||!Number.isFinite(target.y)) return null;
      if(this.isWalkable(target))return {...target,adjusted:false};
      let best=null,dist=this.room.maxAdjustment;
      for(const n of this.nodes) {const d=distance(n,target);if(d<dist){dist=d;best=n;}}
      return best ? {x:best.x,y:best.y,adjusted:true}:null;
    }
    findPath(start,requested) {
      const end=this.resolveTarget(requested);
      if(!this.isWalkable(start)||!end) return {status:'unreachable',path:[],target:null};
      const status=end.adjusted?'adjusted':'exact';
      if(this.segmentSafe(start,end))return {status,path:[point(start),point(end)],target:end};
      const nodes=[...this.nodes,{...point(start),id:this.nodes.length,links:[]},{...point(end),id:this.nodes.length+1,links:[]}];
      const first=nodes.length-2,last=nodes.length-1;
      // Attach endpoints to several visible grid nodes, rather than snapping feet.
      for(const endpoint of [nodes[first],nodes[last]]) {
        const candidates=this.nodes.map(n=>({n,d:distance(n,endpoint)})).sort((a,b)=>a.d-b.d);
        for(const {n} of candidates) if(this.segmentSafe(endpoint,n)) {endpoint.links.push(n.id);if(endpoint.links.length>=12)break;}
      }
      const endLinks=new Set(nodes[last].links);
      const open=new Set([first]),g=new Map([[first,0]]),parent=new Map();
      while(open.size) {
        let current=-1,score=Infinity;
        for(const id of open){const f=g.get(id)+distance(nodes[id],end);if(f<score){score=f;current=id;}}
        if(current===last) {
          const raw=[];let id=last;while(id!==undefined){raw.unshift(point(nodes[id]));id=parent.get(id);}
          const path=[raw[0]];let i=0;
          while(i<raw.length-1){let j=raw.length-1;while(j>i+1&&!this.segmentSafe(raw[i],raw[j]))j--;path.push(raw[j]);i=j;}
          return {status,path,target:end};
        }
        open.delete(current);
        const links=nodes[current].links;
        for(const next of endLinks.has(current)?[...links,last]:links) {
          const cost=g.get(current)+distance(nodes[current],nodes[next]);
          if(cost<(g.get(next)??Infinity)){g.set(next,cost);parent.set(next,current);open.add(next);}
        }
      }
      return {status:'unreachable',path:[],target:null};
    }
  }
  return {Navigation,distance,inside,edgeDistance};
});
