#!/usr/bin/env python3
"""Actual pixel and garment-registration checks for the private FBX study.

This is scoped rendering evidence, not a judgement of human naturalness. Captured
pixels and motion coordinates stay under ignored build/checks/clothing-walk/.
Uses the existing cloud QA stack: Playwright, Pillow, NumPy and SciPy.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
from PIL import Image
from scipy import ndimage
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def pixel_regions(path: Path):
    alpha = np.asarray(Image.open(path).getchannel('A'))
    labels, _ = ndimage.label(alpha > 64)
    result = []
    for index, bounds in enumerate(ndimage.find_objects(labels), 1):
        if bounds is None:
            continue
        count = int(np.sum(labels[bounds] == index))
        if count > 3:
            result.append({'pixels': count, 'bounds': [bounds[1].start,
                           bounds[0].start, bounds[1].stop-1, bounds[0].stop-1]})
    return sorted(result, key=lambda region: region['pixels'], reverse=True)


def interior_holes(path: Path, leather_body=False):
    """Only apply to one garment, never the gap between two separate legs."""
    alpha = np.asarray(Image.open(path).getchannel('A'))
    nonzero_y, _ = np.nonzero(alpha > 64)
    # A tool eye or loop in the bag's hardware is legitimately transparent.
    # The owner's continuity requirement applies to the leather below it.
    leather_start = (float(nonzero_y.min()+.35*(nonzero_y.max()-nonzero_y.min()))
                     if leather_body and len(nonzero_y) else -1)
    occupied = alpha >= 32
    labels, _ = ndimage.label(ndimage.binary_fill_holes(occupied) & ~occupied)
    result = []
    for index, bounds in enumerate(ndimage.find_objects(labels), 1):
        if bounds is None:
            continue
        count = int(np.sum(labels[bounds] == index))
        if count > 3 and bounds[0].start >= leather_start:
            result.append({'pixels': count, 'bounds': [bounds[1].start,
                           bounds[0].start, bounds[1].stop-1, bounds[0].stop-1]})
    return result


CAPTURE = """()=>{
 const gait=new MazissFbxGait.Gait(FBX_MOTION),out=[];
 for(const [view,yaw] of Object.entries({right:{x:1,y:0},front:{x:0,y:1},back:{x:0,y:-1},left:{x:-1,y:0}})){
  gait.reset({x:320,y:570},440);gait.yaw=yaw;
  for(let frame=-1;frame<24;frame++){
   gait.weight=frame<0?0:1;gait.mode=frame<0?'idle':'walking';gait.cycle=Math.max(0,frame)/24;
   const pose=gait.getPose(),canvas=document.createElement('canvas');canvas.width=640;canvas.height=620;
   const metrics=mazissWalk.renderPose(canvas.getContext('2d'),pose,440);
   out.push({name:view+'-'+(frame<0?'idle':frame),view,frame,pose,metrics,png:canvas.toDataURL()});
  }
 }
 return out;
}"""


ITEM_CAPTURE = """()=>{
 const painter=mazissWalk.getPainter(),gait=new MazissFbxGait.Gait(FBX_MOTION),out=[],layers=[];
 function find(node,path){
  if(node&&node.canvas){layers.push({layer:node,path,original:node.canvas});return;}
  if(node&&typeof node==='object')for(const[k,v]of Object.entries(node))find(v,path+'.'+k);
 }
 find(painter.cache,'cache');
 const blanks=new Map(layers.map(l=>{const c=document.createElement('canvas');c.width=l.original.width;c.height=l.original.height;return[l,c];}));
 function draw(view,pose,item,leg,phase){
  for(const l of layers){const tail=l.path.split('.').at(-1).toLowerCase();
   const keep=item==='pants'?tail.includes('pants'):item==='boot'?tail.includes('boot'):tail===item;
   l.layer.canvas=keep?l.original:blanks.get(l);
  }
  const canvas=document.createElement('canvas');canvas.width=640;canvas.height=620;
  const isolated={...pose,legs:leg?[leg]:pose.legs};
  const metrics=painter.drawParts(canvas.getContext('2d'),isolated,440);
  const sourceName=view==='right'||view==='left'?'Side':view==='front'?'Front':'Back';
  const p=MazissPaintedCharacter.profiles[sourceName],scale=440/p.height,face=view==='left'?-1:1;
  const shoulderProbes=item==='body'?p.arms.map(a=>{
   const x=(a.pivot[0]-p.hip[0])*scale*(sourceName==='Side'?face:1),y=(a.pivot[1]-p.hip[1])*scale;
   const c=Math.cos(pose.torso.angle),s=Math.sin(pose.torso.angle);
   const X=pose.pelvis.x+x*c-y*s,Y=pose.pelvis.y+x*s+y*c;
   return{x:X+Math.sign(pose.pelvis.x-X)*6,y:Y};
  }):[];
  out.push({name:view+'-'+item+'-'+(leg?leg.id+'-':'')+phase,view,item,leg:leg?leg.id:null,
            phase,cuff:leg?leg.cuff:null,shoulderProbes,metrics,png:canvas.toDataURL()});
 }
 try{
  for(const[view,yaw]of Object.entries({right:{x:1,y:0},front:{x:0,y:1},back:{x:0,y:-1},left:{x:-1,y:0}})){
   gait.reset({x:320,y:570},440);gait.yaw=yaw;gait.weight=0;gait.mode='idle';
   const idle=gait.getPose();
   for(const item of ['body','bag'])draw(view,idle,item,null,0);
   for(const leg of idle.legs)draw(view,idle,'boot',leg,0);
   gait.weight=1;gait.mode='walking';
   for(let i=0;i<8;i++){gait.cycle=i/8;const pose=gait.getPose();for(const leg of pose.legs)draw(view,pose,'pants',leg,i);}
  }
 }finally{for(const l of layers)l.layer.canvas=l.original;}
 return out;
}"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html', type=Path, default=ROOT/'visual-preview/maziss-walking-v8.html')
    parser.add_argument('--manifest', type=Path, default=ROOT/'build/checks/clothing-walk/build-manifest.json')
    parser.add_argument('--output', type=Path, default=ROOT/'build/checks/clothing-walk/qa')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    source = args.html.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    manifest = json.loads(args.manifest.read_text())
    passed, failed, errors, requests = [], [], [], []

    def check(condition, label, evidence=None):
        (passed if condition else failed).append({'check': label, 'evidence': evidence})

    def sources_match():
        return all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected
                   for name, expected in manifest['source_sha256'].items())

    check(digest == manifest['output_sha256'], 'Actual HTML matches the frozen build manifest')
    check(sources_match(), 'Actual source files match the frozen manifest')
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        context = browser.new_context(offline=True, viewport={'width': 1450, 'height': 1050})
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: requests.append(request.url))
        page.set_content(source.decode(), wait_until='load')
        page.wait_for_function('()=>window.mazissWalk&&mazissWalk.getState().ready')
        captures = page.evaluate(CAPTURE)
        regions = {}
        for sample in captures:
            path = args.output/(sample['name']+'.png')
            path.write_bytes(base64.b64decode(sample.pop('png').split(',')[1]))
            regions[sample['name']] = pixel_regions(path)
        (args.output/'poses.json').write_text(json.dumps(captures, indent=2)+'\n')

        for view in ('right', 'front', 'back', 'left'):
            group = [sample for sample in captures if sample['view'] == view]
            orphans = [{'pose': sample['name'], 'regions': regions[sample['name']][1:]}
                       for sample in group
                       if any(region['pixels'] > 16 for region in regions[sample['name']][1:])]
            check(not orphans, view+': actual transparent poses contain no detached painted fragments above 16 pixels', orphans)
            # Sample a narrow interior band about each actual bone. Silhouette
            # holes between legs are deliberately excluded from this check.
            uncovered = []
            for sample in group:
                alpha = Image.open(args.output/(sample['name']+'.png')).getchannel('A')
                for leg in sample['pose']['legs']:
                    for start, end in (('hip', 'knee'), ('knee', 'cuff')):
                        a, b = leg[start], leg[end]
                        dx, dy = b['x']-a['x'], b['y']-a['y']
                        length = math.hypot(dx, dy)
                        missing = 0
                        for i in range(2, 19):
                            t = i/20
                            for offset in range(-3, 4):
                                x = round(a['x']+dx*t-dy/length*offset)
                                y = round(a['y']+dy*t+dx/length*offset)
                                missing += alpha.getpixel((x, y)) < 64
                        if missing:
                            uncovered.append({'pose': sample['name'], 'leg': leg['id'],
                                              'bone': start+'-'+end, 'pixels': missing})
            check(not uncovered, view+': actual thigh/shin interior bands stay filled through the cycle', uncovered)
            mismatches = []
            for sample in group:
                for joint in sample['metrics']['joins']:
                    leg = next(leg for leg in sample['pose']['legs'] if leg['id'] == joint['id'])
                    error = math.hypot(joint['shinEnd']['x']-leg['cuff']['x'],
                                       joint['shinEnd']['y']-leg['cuff']['y'])
                    if error > 1e-7:
                        mismatches.append({'pose': sample['name'], 'leg': leg['id'], 'pixels': error})
            check(not mismatches, view+': cloth endpoint uses the actual skeletal cuff without a separate boot-height relocation', mismatches)

        items = page.evaluate(ITEM_CAPTURE)
        item_regions, item_holes = {}, {}
        for sample in items:
            path = args.output/(sample['name']+'.png')
            path.write_bytes(base64.b64decode(sample.pop('png').split(',')[1]))
            item_regions[sample['name']] = pixel_regions(path)
            item_holes[sample['name']] = interior_holes(path, leather_body=sample['item']=='bag')
        (args.output/'items.json').write_text(json.dumps(items, indent=2)+'\n')
        for item in ('pants', 'body', 'bag'):
            group = [sample for sample in items if sample['item'] == item]
            absent = [sample['name'] for sample in group if not item_regions[sample['name']]]
            holes = [{'pose': sample['name'], 'holes': item_holes[sample['name']]}
                     for sample in group if item_holes[sample['name']]]
            fragments = [{'pose': sample['name'], 'regions': item_regions[sample['name']][1:]}
                         for sample in group
                         if any(region['pixels'] > 16 for region in item_regions[sample['name']][1:])]
            check(not absent, item+': actual isolated production garment is present', absent)
            check(not holes, item+': actual isolated cloth/leather body has no enclosed transparency holes above 3 pixels', holes)
            check(not fragments, item+': actual isolated garment remains one connected painted item above 16 pixels', fragments)

        shoulder_gaps = []
        for sample in (sample for sample in items if sample['item'] == 'body'):
            alpha = Image.open(args.output/(sample['name']+'.png')).getchannel('A')
            for index, point in enumerate(sample['shoulderProbes']):
                transparent = sum(alpha.getpixel((round(point['x'])+dx, round(point['y'])+dy)) < 64
                                  for dy in range(-3, 4) for dx in range(-3, 4))
                if transparent:
                    shoulder_gaps.append({'pose': sample['name'], 'shoulder': index, 'pixels': transparent})
        check(not shoulder_gaps,
              'Real jacket backing covers both arm attachment interiors when the arms are hidden', shoulder_gaps)

        # Compare the real painted lower shoe against its actual ankle rather
        # than trusting the zero-angle transform. Both toes biasing observer-
        # left was the previous candidate's untested visual defect.
        foot_bias = {}
        for view in ('front', 'back'):
            pair = [sample for sample in items if sample['view'] == view and sample['item'] == 'boot']
            offsets = []
            for sample in pair:
                alpha = np.asarray(Image.open(args.output/(sample['name']+'.png')).getchannel('A'))
                ys, xs = np.nonzero(alpha > 128)
                cutoff = float(ys.min()+.60*(ys.max()-ys.min()))
                selected = ys >= cutoff
                offsets.append(float(np.mean(xs[selected])-sample['cuff']['x']))
            foot_bias[view] = offsets
            check(len(offsets) == 2 and min(offsets) <= 1 and max(offsets) >= -1,
                  view+': real paired lower-boot silhouettes do not both lean to the same side', offsets)

        dense = page.evaluate("""()=>{
         const g=new MazissFbxGait.Gait(FBX_MOTION);g.reset({x:0,y:0},440);g.weight=1;g.mode='walking';
         const out=[];for(let i=0;i<=240;i++){g.cycle=i/240;out.push(g.getPose());}return out;
        }""")
        lengths = [[math.dist(leg['local']['hip'], leg['local']['knee']),
                    math.dist(leg['local']['knee'], leg['local']['cuff'])]
                   for pose in dense for leg in pose['legs']]
        ranges = [max(pair[index] for pair in lengths)-min(pair[index] for pair in lengths)
                  for index in range(2)]
        check(max(ranges) < 1e-7,
              'Actual FBX retargeting retains fixed bone lengths while allowing real projected foreshortening', ranges)
        seam = max(math.hypot(a[key]['x']-b[key]['x'], a[key]['y']-b[key]['y'])
                   for a, b in zip(dense[0]['legs'], dense[-1]['legs'])
                   for key in ('hip', 'knee', 'cuff'))
        check(seam < 1e-7, 'Actual FBX leg geometry closes the loop without teleporting', seam)
        for view in ('right', 'front', 'back', 'left'):
            page.click('[data-view="'+view+'"]')
            page.wait_for_timeout(180)
            if not page.evaluate('mazissWalk.getState().paused'):
                page.click('#pause')
            frozen = page.evaluate('mazissWalk.getState().pose')
            page.wait_for_timeout(90)
            check(page.evaluate('mazissWalk.getState().pose') == frozen,
                  view+': actual owner pause control freezes the complete pose')
            page.click('#step')
            stepped = page.evaluate('mazissWalk.getState().pose')
            expected = page.evaluate('1/30/FBX_MOTION.cycleSeconds')
            check(abs((stepped['phase']-frozen['phase']) % 1-expected) < 1e-7,
                  view+': actual frame-step control retains FBX timing')
            page.click('#pause')
            page.click('#stand')
            page.wait_for_function('()=>mazissWalk.getState().pose.mode==="idle"', timeout=3000)
            check(not page.evaluate('mazissWalk.getState().study'),
                  view+': actual Stand still control settles to neutral')
            page.locator('#detail').screenshot(path=str(args.output/(view+'-actual-idle.png')))
        renderer_ms = page.evaluate("""()=>{
         const g=new MazissFbxGait.Gait(FBX_MOTION);g.reset({x:320,y:570},440);g.weight=1;g.mode='walking';
         const canvas=document.createElement('canvas');canvas.width=640;canvas.height=620;
         const ctx=canvas.getContext('2d'),samples=[];
         for(let i=0;i<40;i++){g.cycle=i/40;const p=g.getPose(),start=performance.now();mazissWalk.renderPose(ctx,p,440);if(i>=10)samples.push(performance.now()-start);}
         samples.sort((a,b)=>a-b);return{median:samples[15],p95:samples[28],max:samples[29]};
        }""")
        check(not errors, 'No JavaScript runtime errors', errors)
        check(not requests, 'Self-contained candidate executes with browser networking disabled', requests)
        version = browser.version
        browser.close()

    check(hashlib.sha256(args.html.read_bytes()).hexdigest() == digest,
          'HTML did not change during the focused run')
    check(sources_match(), 'Runtime sources did not change during the focused run')
    result = {'build': manifest['build'], 'html_sha256': digest, 'passed': passed,
              'failed': failed, 'browser': version, 'seconds': round(time.monotonic()-started, 2),
              'captures': len(captures), 'isolated_item_captures': len(items),
              'painted_foot_offsets_pixels': foot_bias, 'renderer_only_milliseconds': renderer_ms,
              'limits': [
                  'Owner visual judgement is required for naturalness and clothing appeal.',
                  'No native Windows or Godot execution is covered.',
                  'Whole-body alpha holes may be legitimate gaps between limbs; only constrained garment checks are claimed.']}
    (args.output/'browser-results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'build': manifest['build'][:12], 'passed': len(passed),
                      'failed': failed, 'seconds': result['seconds']}))
    raise SystemExit(bool(failed))


if __name__ == '__main__':
    main()
