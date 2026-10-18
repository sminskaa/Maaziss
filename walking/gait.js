(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.MazissGait = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const copy=p=>({x:p.x,y:p.y});
  const mix=(a,b,t)=>({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t});
  const dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  function unit(v) {const n=Math.hypot(v.x,v.y);return n>1e-8?{x:v.x/n,y:v.y/n}:{x:1,y:0};}
  class Gait {
    constructor(options={}) {this.isWalkable=options.isWalkable||(()=>true);this.contact=0;this.ready=false;}
    safe(candidate,origin) {
      // Test the complete contact projection, rather than only its endpoint.
      let last=copy(origin);
      for(let i=1;i<=24;i++) {const p=mix(origin,candidate,i/24);if(!this.isWalkable(p))break;last=p;}
      return last;
    }
    lateral(id,height=this.height) {
      const side=id==='left'?-1:1;
      return {x:-this.direction.y*height*.028*side,y:this.direction.x*height*.012*side};
    }
    reset(position,height=400) {
      this.position=copy(position);this.height=height;this.direction={x:1,y:0};
      this.travel=0;this.cycle=0;this.progress=0;this.length=height*.18;this.swing='right';this.walking=false;
      this.legs=['left','right'].map(id=>{const o=this.lateral(id);return {id,stance:true,contactId:++this.contact,ground:this.safe({x:position.x+o.x,y:position.y+o.y},position),lift:0,bootAngle:0};});
      this.start=copy(this.legs[1].ground);this.target=copy(this.start);this.ready=true;return this.getPose();
    }
    begin(short=false,position=this.position) {
      // A depth step is foreshortened on the screen. Using a side-view stride
      // in screen Y would require impossibly long legs when walking upscreen.
      this.stride=this.height*.36*(.4+.6*Math.abs(this.direction.x));
      const support=this.legs.find(l=>l.id!==this.swing);
      const ahead=(support.ground.x-position.x)*this.direction.x+(support.ground.y-position.y)*this.direction.y;
      // A contact shortened by a corner cannot support a full normal stride.
      // Turnaround/catch-up steps finish sooner instead of dragging that leg.
      this.length=clamp(ahead+this.stride*.5,this.height*.045,this.stride*(short?.5:1));this.progress=0;
      this.stepDirection=copy(this.direction);
      const leg=this.legs.find(l=>l.id===this.swing);
      this.start=copy(leg.ground);leg.stance=false;this.walking=true;
    }
    targetAt(position) {
      const o=this.lateral(this.swing),ahead=this.length-this.progress+this.stride*.5;
      return this.safe({x:position.x+this.direction.x*ahead+o.x,y:position.y+this.direction.y*ahead+o.y},position);
    }
    swingPose(position,maxMotion) {
      const leg=this.legs.find(l=>l.id===this.swing),t=clamp(this.progress/this.length,0,1);
      this.target=this.targetAt(position);
      // Two legal endpoints can interpolate across a concave clearance corner.
      // Keep the airborne projection legal too; never move a stance contact.
      const projected=mix(this.start,this.target,t*t*(3-2*t));
      const legal=this.isWalkable(projected)?projected:this.safe(projected,position);
      const movement=dist(leg.ground,legal);
      const bounded=movement>maxMotion?mix(leg.ground,legal,maxMotion/movement):legal;
      leg.ground=this.isWalkable(bounded)?bounded:this.safe(bounded,leg.ground);
      leg.lift=Math.sin(Math.PI*t)*this.height*.038;
      leg.bootAngle=Math.sin(2*Math.PI*t)*.12*this.direction.x;
    }
    update(position,height,dt,moving,directionVector) {
      if(!this.ready)return this.reset(position,height);
      const d=dist(position,this.position),old=copy(this.position);
      if(!Number.isFinite(d)||!Number.isFinite(height)||height<=0)throw new TypeError('Finite position and positive height required');
      if(d>height*.75)return this.reset(position,height); // Explicit teleports are not steps.
      this.height=height;
      if(directionVector&&Math.hypot(directionVector.x,directionVector.y)>1e-6)this.direction=unit(directionVector);
      if(moving&&d>1e-7) {
        if(!this.walking)this.begin(true);
        if(this.direction.x*this.stepDirection.x+this.direction.y*this.stepDirection.y<.5) {
          const support=this.legs.find(l=>l.id!==this.swing);
          const ahead=(support.ground.x-old.x)*this.direction.x+(support.ground.y-old.y)*this.direction.y;
          this.length=Math.min(this.length,this.progress+Math.max(height*.025,ahead+this.stride*.5));
          this.stepDirection=copy(this.direction);
        }
        let consumed=0;
        while(consumed<d-1e-8) {
          const delta=Math.min(d-consumed,this.length-this.progress);
          consumed+=delta;this.progress+=delta;this.travel+=delta;this.cycle+=.5*delta/this.length;
          const p=mix(old,position,consumed/d);
          this.swingPose(p,delta*4);
          if(this.progress>=this.length-1e-7) {
            const leg=this.legs.find(l=>l.id===this.swing);
            leg.lift=0;leg.bootAngle=0;leg.stance=true;leg.contactId=++this.contact;
            this.swing=this.swing==='left'?'right':'left';this.begin(false,p);
          }
        }
      } else if(!moving && dt>0) {
        // A stopped character lowers its airborne boot; dt=0 preserves a paused pose.
        const leg=this.legs.find(l=>!l.stance);
        if(leg) {
          leg.lift=Math.max(0,leg.lift-height*.35*dt);leg.bootAngle*=Math.exp(-dt*18);
          if(leg.lift<.001) {leg.lift=0;leg.bootAngle=0;leg.stance=true;leg.contactId=++this.contact;this.walking=false;}
        } else this.walking=false;
      }
      this.position=copy(position);return this.getPose();
    }
    getPose() {
      if(!this.ready)return null;
      const h=this.height,p=this.position;
      const phase=this.cycle%1;
      const bob=this.walking?-Math.cos(phase*Math.PI*4)*h*.003:0;
      const pelvis={x:p.x,y:p.y-h*.45+bob};
      // The pelvis follows the root in X, but accommodates projected depth
      // contacts in Y. Both leg chains retain their physical bone lengths.
      let lower=-Infinity,upper=Infinity;
      for(const leg of this.legs) {
        const lateral=this.lateral(leg.id),dx=leg.ground.x-pelvis.x-lateral.x;
        const reach=Math.sqrt(Math.max(0,(h*.449)**2-dx*dx));
        const ankleY=leg.ground.y-leg.lift-h*.018;
        lower=Math.max(lower,ankleY-reach-lateral.y);
        upper=Math.min(upper,ankleY+reach-lateral.y);
      }
      if(lower<=upper)pelvis.y=clamp(pelvis.y,lower,upper);
      const legs=this.legs.map(leg=>{
        const lateral=this.lateral(leg.id),hip={x:pelvis.x+lateral.x,y:pelvis.y+lateral.y};
        const ankle={x:leg.ground.x,y:leg.ground.y-leg.lift-h*.018};
        const dx=ankle.x-hip.x,dy=ankle.y-hip.y,actual=Math.hypot(dx,dy),n=Math.max(actual,1e-9);
        // Equal-length two-bone IK; a tiny extension margin avoids a straight-knee flip.
        const bone=h*.225,length=Math.min(actual,bone*1.999),along=length/2;
        const bend=Math.sqrt(Math.max(0,bone*bone-along*along));
        const side=Math.abs(this.direction.x)>.15?(this.direction.x>=0?-1:1):(leg.id==='left'?1:-1);
        const knee={x:hip.x+dx/n*along-dy/n*bend*side,y:hip.y+dy/n*along+dx/n*bend*side};
        return {...leg,ground:copy(leg.ground),hip,knee,ankle};
      });
      const angle=this.walking?this.direction.x*.025:0;
      return {pelvis,torso:{x:pelvis.x,y:pelvis.y,angle},bob,phase,travel:this.travel,legs};
    }
  }
  return {Gait};
});
