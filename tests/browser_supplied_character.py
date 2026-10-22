#!/usr/bin/env python3
"""Audit the owner's private GLB and optionally exercise its compact offline review.

This records engineering evidence, not an art-approval verdict. Position-only intake
models may be useful reconstruction references while being unready for game runtime.
All output, input geometry, captures and reports with raw coordinates remain private.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import struct
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def read_glb(path):
    raw = path.read_bytes()
    if len(raw) < 12 or struct.unpack_from('<III', raw) != (0x46546C67, 2, len(raw)):
        raise ValueError('Not a complete glTF 2 GLB file')
    chunks = {}; offset = 12
    while offset < len(raw):
        length, kind = struct.unpack_from('<II', raw, offset); offset += 8
        chunks[kind] = raw[offset:offset+length]; offset += length
    doc = json.loads(chunks[0x4E4F534A]); binary = chunks[0x004E4942]
    def accessor(index):
        item = doc['accessors'][index]; view = doc['bufferViews'][item['bufferView']]
        dtype = np.dtype({5120:'i1', 5121:'u1', 5122:'<i2', 5123:'<u2', 5125:'<u4', 5126:'<f4'}[item['componentType']])
        width = {'SCALAR':1, 'VEC2':2, 'VEC3':3, 'VEC4':4, 'MAT4':16}[item['type']]
        offset = view.get('byteOffset', 0)+item.get('byteOffset', 0)
        stride = view.get('byteStride', width*dtype.itemsize)
        if 'sparse' in item: raise ValueError('Sparse accessors are not supported by this scoped intake audit')
        return np.ndarray((item['count'], width), dtype=dtype, buffer=binary,
                          offset=offset, strides=(stride, dtype.itemsize)).copy()
    return raw, doc, accessor


def topology(vertices, triangles):
    edges = defaultdict(list); adjacency = [set() for _ in vertices]
    links = [[] for _ in vertices]
    for number, face in enumerate(triangles):
        for i in range(3):
            a, b = int(face[i]), int(face[(i+1)%3]); c = int(face[(i+2)%3])
            edges[tuple(sorted((a,b)))].append((number,a,b))
            adjacency[a].add(b); adjacency[b].add(a); links[a].append((b,c))
    def components(graph):
        seen=set(); sizes=[]
        for start in graph:
            if start in seen: continue
            stack=[start]; seen.add(start); size=0
            while stack:
                node=stack.pop();size+=1
                for other in graph[node]:
                    if other not in seen: seen.add(other); stack.append(other)
            sizes.append(size)
        return sorted(sizes,reverse=True)
    component_sizes=components(dict(enumerate(adjacency)))
    bad_links=[]
    for index, opposite_edges in enumerate(links):
        graph=defaultdict(set)
        for a,b in opposite_edges:graph[a].add(b);graph[b].add(a)
        sizes=components(graph); degrees=Counter(len(n) for n in graph.values())
        if len(sizes)!=1 or any(degree!=2 for degree in degrees):
            bad_links.append({'vertex':index,'linkComponents':len(sizes),'linkDegrees':dict(degrees)})
    a,b,c=(vertices[triangles[:,i]] for i in range(3))
    areas=np.linalg.norm(np.cross(b-a,c-a),axis=1)/2
    return {'vertices':len(vertices),'triangles':len(triangles),'edges':len(edges),
            'finite':bool(np.isfinite(vertices).all()),
            'degenerateTriangles':int((areas<1e-12).sum()),
            'boundaryEdges':sum(len(x)==1 for x in edges.values()),
            'nonmanifoldEdges':sum(len(x)>2 for x in edges.values()),
            'inconsistentSharedEdgeWinding':sum(len(x)==2 and x[0][1:]==x[1][1:] for x in edges.values()),
            'connectedComponentVertexCounts':component_sizes,
            'nonmanifoldVertexLinks':bad_links,
            'eulerCharacteristic':len(vertices)-len(edges)+len(triangles),
            'signedVolume':float(np.einsum('ij,ij->i',a,np.cross(b,c)).sum()/6),
            'bounds':[vertices.min(0).tolist(),vertices.max(0).tolist()]}


def authoring_audit(blend, output):
    """Evaluate the actual keyed authoring surface; keep coordinates private."""
    script = output/'inspect-rig.py'
    script.write_text(r'''import bpy,math,json
from pathlib import Path
scene=bpy.context.scene
body=bpy.data.objects['Maziss supplied sculpt']
meshes=[o for o in scene.objects if o.type=='MESH']
frames=[]
for index in range(50):
 frame=scene.frame_start+(scene.frame_end-scene.frame_start)*index/49
 scene.frame_set(int(frame),subframe=frame-int(frame));deps=bpy.context.evaluated_depsgraph_get();points=[];body_points=None
 for obj in meshes:
  evaluated=obj.evaluated_get(deps);mesh=evaluated.to_mesh()
  vertices=[evaluated.matrix_world@v.co for v in mesh.vertices];points.extend(vertices)
  if obj==body:body_points=vertices
  evaluated.to_mesh_clear()
 ratios=[]
 for edge in body.data.edges:
  a,b=edge.vertices;rest=(body.data.vertices[a].co-body.data.vertices[b].co).length
  if rest>1e-5:ratios.append((body_points[a]-body_points[b]).length/rest)
 frames.append({'frame':frame,'finite':all(math.isfinite(x) for point in points for x in point),
                'minZ':min(p.z for p in points),'maxEdgeStretchRatio':max(ratios)})
features={}
for obj in meshes:
 if obj==body:continue
 features[obj.name]={'allHeadWeight':all(len(v.groups)==1 and obj.vertex_groups[v.groups[0].group].name=='Head' and abs(v.groups[0].weight-1)<1e-6 for v in obj.data.vertices),
                     'armatureModifierCount':sum(m.type=='ARMATURE' for m in obj.modifiers),
                     'materialSlots':len(obj.data.materials)}
report={'frames':frames,'features':features,
        'scope':'Evaluated baked authoring animation; a fourfold edge-stretch bound is a study defect detector, not an industry quality standard.'}
Path(OUTPUT).write_text(json.dumps(report,indent=2))
'''.replace('OUTPUT',repr(str(output/'authoring-results.json'))))
    run=subprocess.run(['blender','--background',str(blend),'--python',str(script)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (output/'authoring.log').write_text(run.stdout)
    if run.returncode:raise RuntimeError('Actual Blender authoring audit failed; inspect private authoring.log')
    return json.loads((output/'authoring-results.json').read_text())


def browser_review(html, output):
    from playwright.sync_api import sync_playwright
    errors=[]; requests=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        context=browser.new_context(offline=True,viewport={'width':1280,'height':1000})
        page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
        page.set_content(html.read_text(),wait_until='load')
        page.locator('video').first.wait_for(state='visible')
        page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
        page.wait_for_function('document.querySelector("video").readyState>=2')
        metadata=page.locator('video').evaluate('(v)=>({width:v.videoWidth,height:v.videoHeight,duration:v.duration,controls:v.controls})')
        page.locator('video').evaluate('(v)=>{v.pause();v.currentTime=Math.min(.3,v.duration/2)}')
        page.wait_for_function('!document.querySelector("video").seeking')
        start=page.locator('video').evaluate('(v)=>v.currentTime')
        page.locator('video').evaluate('(v)=>{v.muted=true;return v.play()}')
        page.wait_for_function('(start)=>document.querySelector("video").currentTime>start+.2',arg=start)
        page.locator('video').evaluate('(v)=>v.pause()')
        metadata['playbackAdvanced']=True
        page.screenshot(path=str(output/'compact-review.png'),full_page=True)
        assert metadata['width']>0 and metadata['height']>0 and metadata['controls']
        assert not errors,errors
        assert not requests,requests
        result={'bytes':html.stat().st_size,'metadata':metadata,'errors':errors,'externalRequests':requests,
                'browser':browser.version,'capture':'compact-review.png',
                'deliveryLimit':'Internal browser success does not prove that the host panel displays the file.'}
        browser.close();return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=ROOT/'private/models/white_mesh.glb')
    parser.add_argument('--output',type=Path,default=ROOT/'build/checks/supplied-character/qa')
    parser.add_argument('--html',type=Path)
    parser.add_argument('--blend',type=Path)
    parser.add_argument('--require-rig',action='store_true',help='Fail if scoped game-exchange engineering criteria are missing')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    raw,doc,accessor=read_glb(args.input)
    reports=[]
    for mesh in doc.get('meshes',[]):
        for primitive in mesh['primitives']:
            if primitive.get('mode',4)!=4:raise ValueError('Only triangle intake meshes are audited')
            vertices=accessor(primitive['attributes']['POSITION'])
            triangles=accessor(primitive['indices']).reshape(-1,3)
            report=topology(vertices,triangles);report['attributes']=list(primitive['attributes'])
            attributes={name:accessor(index) for name,index in primitive['attributes'].items()}
            report['finiteAttributes']=all(bool(np.isfinite(array).all()) for array in attributes.values())
            if 'NORMAL' in attributes:
                lengths=np.linalg.norm(attributes['NORMAL'],axis=1)
                report['normalLengthRange']=[float(lengths.min()),float(lengths.max())]
                report['normalLengthsValid']=bool(np.allclose(lengths,1,atol=2e-3))
            if 'WEIGHTS_0' in attributes:
                weights=attributes['WEIGHTS_0']
                report['maximumWeightsPerVertex']=int((weights>1e-6).sum(axis=1).max())
                report['weightsNormalized']=bool(np.allclose(weights.sum(axis=1),1,atol=2e-4) and (weights>=0).all())
            if 'JOINTS_0' in attributes:
                report['maximumJointIndex']=int(attributes['JOINTS_0'].max())
            reports.append(report)
    result={'inputSHA256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'meshes':reports,
            'skins':len(doc.get('skins',[])),'animations':len(doc.get('animations',[])),
            'materials':len(doc.get('materials',[])),
            'hasRequiredRigInputs':bool(doc.get('skins')) and all('JOINTS_0'in p['attributes'] and 'WEIGHTS_0'in p['attributes'] for m in doc['meshes'] for p in m['primitives'])}
    animation_checks=[]
    for animation in doc.get('animations',[]):
        for sampler in animation.get('samplers',[]):
            times=accessor(sampler['input']).ravel(); values=accessor(sampler['output'])
            animation_checks.append({'finite':bool(np.isfinite(times).all() and np.isfinite(values).all()),
                                     'strictlyIncreasingTime':bool((np.diff(times)>0).all()),
                                     'samples':len(times),'duration':float(times[-1]-times[0])})
    result['animationSamplers']=animation_checks
    result['skinJointCounts']=[len(skin['joints']) for skin in doc.get('skins',[])]
    checks={'finitePositionAndAttributes':all(m['finite'] and m['finiteAttributes'] for m in reports),
            'noDegenerateTriangles':not any(m['degenerateTriangles'] for m in reports)}
    if args.require_rig:
        checks.update({'hasSkinnedAttributes':result['hasRequiredRigInputs'],
                       'normalizedWeights':all(m.get('weightsNormalized',False) for m in reports),
                       'atMostFourWeights':all(m.get('maximumWeightsPerVertex',99)<=4 for m in reports),
                       'unitNormals':all(m.get('normalLengthsValid',False) for m in reports),
                       'jointIndicesInRange':bool(result['skinJointCounts']) and all(m.get('maximumJointIndex',999)<max(result['skinJointCounts']) for m in reports),
                       'finiteIncreasingAnimation':bool(animation_checks) and all(x['finite'] and x['strictlyIncreasingTime'] and x['duration']>0 for x in animation_checks),
                       'hasMaterials':bool(doc.get('materials'))})
    if args.blend:
        authored=authoring_audit(args.blend,args.output);result['authoring']=authored
        checks.update({'evaluatedAnimationFinite':all(f['finite'] for f in authored['frames']),
                       'evaluatedFloorClearance':all(f['minZ']>=-.001 for f in authored['frames']),
                       'noSevereLocalStretch':all(f['maxEdgeStretchRatio']<4 for f in authored['frames']),
                       'facialFeaturesBoundToSharedHead':all(f['allHeadWeight'] and f['armatureModifierCount']==1 for f in authored['features'].values())})
    result['engineeringChecks']=checks
    if args.html:result['compactReview']=browser_review(args.html,args.output)
    (args.output/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(not all(checks.values()))

if __name__=='__main__':main()
