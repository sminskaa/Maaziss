#!/usr/bin/env python3
"""Scoped QA for the painted 3D study; this does not approve finished character art.

Inputs, captured renders and full measurement arrays stay in ignored build/checks.
The check examines actual exported geometry, embedded art and offline controls.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import time

import numpy as np
from playwright.sync_api import sync_playwright

from browser_character3d import closed_mesh

ROOT = Path(__file__).resolve().parents[1]
ART = ('art/walking/maziss-side-atlas.png', 'art/walking/maziss-depth-atlas.png')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_authoring(directory, output):
    """Read the actual .blend and evaluate its deformed triangles, not AABBs."""
    script = output/'inspect-authoring.py'
    script.write_text('''import bpy, json, hashlib
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
directory=Path(DIRECTORY)
data=json.loads((directory/'model-private.json').read_text())
arm=next(o for o in bpy.data.objects if o.type=='ARMATURE')
arm.animation_data_clear()
objects={o.name:o for o in bpy.data.objects if o.type=='MESH'}
packed=[{'name':im.name,'packed':bool(im.packed_file),
         'sha256':hashlib.sha256(im.packed_file.data).hexdigest() if im.packed_file else None}
        for im in bpy.data.images if im.name not in ('Render Result','Viewer Node')]
uv_missing=[item['name'] for item in data['objects'] if item['paintKind']!='solid'
            and not all(key in objects[item['name']].data.uv_layers
                        for key in ('paintFront','paintBack','paintSide'))]
rest={b.name:b for b in arm.data.bones}
triangles={}
def surface(obj,deps):
    evaluated=obj.evaluated_get(deps);mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
    vertices=[evaluated.matrix_world@v.co for v in mesh.vertices]
    triangles[obj.name]=[tuple(t.vertices) for t in mesh.loop_triangles]
    tree=BVHTree.FromPolygons(vertices,triangles[obj.name],all_triangles=True)
    evaluated.to_mesh_clear();return tree
samples=[]
for i,frame in enumerate([data['motion']['idle']]+data['motion']['frames']):
    for item,target in zip(data['bones'],frame):
        bone=rest[item['name']];head=Vector(target['head']);tail=Vector(target['tail'])
        delta=(bone.tail_local-bone.head_local).normalized().rotation_difference((tail-head).normalized())
        arm.pose.bones[bone.name].matrix=Matrix.LocRotScale(head,delta@bone.matrix_local.to_quaternion(),Vector((1,1,1)))
        bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    bags=[(o.name,surface(o,deps)) for o in objects.values()
          if o.get('part_group')=='Bag' and o.name!='Shoulder strap']
    collisions=[]
    for name in ('RightHand','RightForeArm'):
        tree=surface(objects[name],deps)
        for bag,btree in bags:
            hits=tree.overlap(btree)
            if hits:collisions.append({'limb':name,'bagPart':bag,'trianglePairs':len(hits)})
    pants=surface(objects['Pants'],deps);max_z=0;skin_pairs=0
    for name in ('LeftThigh','RightThigh','LeftShin','RightShin'):
        tree=surface(objects[name],deps);hits=tree.overlap(pants);skin_pairs+=len(hits)
        for _,triangle in hits:
            max_z=max(max_z,*(objects['Pants'].data.vertices[v].co.z for v in triangles['Pants'][triangle]))
    samples.append({'sample':i,'collisions':collisions,'skinTrouserPairs':skin_pairs,'skinHitMaxSourceZ':max_z})
result={'packedImages':packed,'missingUVLayers':uv_missing,'samples':samples,
        'collisionSamples':sum(bool(sample['collisions']) for sample in samples),
        'maxSkinHitSourceZ':max(sample['skinHitMaxSourceZ'] for sample in samples)}
Path(OUTPUT).write_text(json.dumps(result,indent=2)+'\\n')
print('AUTHORING_QA',json.dumps({key:value for key,value in result.items() if key!='samples'}))
'''.replace('DIRECTORY', repr(str(directory))).replace('OUTPUT', repr(str(output/'authoring-results.json'))))
    run = subprocess.run(['blender', '--background', str(directory/'maziss-construction.blend'),
                          '--python', str(script)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (output/'authoring.log').write_text(run.stdout)
    if run.returncode:
        raise RuntimeError('Blender authoring inspection failed; see authoring.log')
    return json.loads((output/'authoring-results.json').read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=ROOT/'build/checks/painted-character')
    parser.add_argument('--html', type=Path, default=ROOT/'visual-preview/maziss-painted-3d.html')
    parser.add_argument('--skip-authoring', action='store_true', help='Only for quick browser debugging; not the final evidence run')
    args = parser.parse_args()
    output = args.directory/'qa'; output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((args.directory/'build-manifest.json').read_text())
    data = json.loads((args.directory/'model-private.json').read_text())
    started = time.monotonic(); passed = []; failed = []

    def check(value, label, evidence=None):
        (passed if value else failed).append({'check': label, 'evidence': evidence})

    def source_match():
        return all(digest(ROOT/path) == sha for path, sha in manifest['source_sha256'].items())

    check(digest(args.html) == manifest['output_sha256'], 'Actual HTML matches frozen manifest')
    check(source_match(), 'Model, art and viewer sources match manifest')
    unchanged = {}
    for path in ART:
        original = subprocess.check_output(['git', 'show', 'HEAD:'+path], cwd=ROOT)
        unchanged[path] = hashlib.sha256(original).hexdigest() == digest(ROOT/path)
    check(all(unchanged.values()), 'Original front/back and side drawings remain byte-for-byte unchanged', unchanged)

    topology = [closed_mesh(item) for item in data['objects']]
    bad = [item for item in topology if item['boundary'] or item['nonmanifold']]
    check(not bad, 'Every complete mesh is closed after coincident vertices are welded for counting', bad)
    principal = [item for item in topology if item['name'] in ('Pants', 'Jacket', 'Shirt', 'Head')]
    check(len(principal) == 4 and all(item['components'] == 1 for item in principal),
          'Pants, jacket, shirt and rounded head each form one connected surface', principal)
    malformed = []
    for item in data['objects']:
        n = len(item['positions'])//3
        for name, size in (('paintFront', 2), ('paintBack', 2), ('paintSide', 2), ('paintBlend', 3)):
            if len(item[name]) != n*size or not np.isfinite(item[name]).all():
                malformed.append((item['name'], name))
        w = np.asarray(item['skinWeights']).reshape(-1, 4)
        if not np.allclose(w.sum(axis=1), 1, atol=3e-6) or np.min(w) < 0:
            malformed.append((item['name'], 'skinning'))
    check(not malformed, 'Every vertex has finite fixed paint coordinates and normalized skin weights', malformed)

    errors = []; network = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path='/usr/bin/chromium',
                                    args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        context = browser.new_context(offline=True, viewport={'width': 1400, 'height': 1080})
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
        page.on('request', lambda request: network.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
        page.set_content(args.html.read_text(), wait_until='load')
        page.wait_for_function('window.maziss3d && maziss3d.ready', timeout=90000)
        page.evaluate("()=>{maziss3d.setPhase(0);maziss3d.setBackdrop('neutral');maziss3d.renderer.setPixelRatio(1);maziss3d.renderer.setSize(480,600);maziss3d.camera.aspect=.8;maziss3d.camera.updateProjectionMatrix()}")
        check(page.evaluate('maziss3d.meshes.length') == len(data['objects']), 'All complete objects are loaded in the actual renderer')
        material = page.evaluate('''()=>maziss3d.meshes.every(({mesh})=>
          !mesh.material.transparent && mesh.material.opacity===1 && mesh.material.alphaTest===0
          && mesh.material.depthWrite && mesh.material.depthTest)''')
        check(material, 'Actual painted surfaces remain opaque and depth occluded; source alpha cannot cut geometry')
        art_bytes = page.evaluate('()=>Object.fromEntries(Object.entries(PAINT_SOURCES).map(([k,v])=>[k,v]))')
        actual_art = {key: hashlib.sha256(base64.b64decode(url.split(',', 1)[1])).hexdigest()
                      for key, url in art_bytes.items()}
        check(actual_art['side'] == digest(ROOT/ART[0]) and actual_art['depth'] == digest(ROOT/ART[1]),
              'Browser actually embeds the unchanged original drawings', actual_art)
        check(actual_art['garment'] == digest(ROOT/'art/walking/maziss-clean-garment-reference.png'),
              'Clean jacket reference is embedded separately from original art')
        page.evaluate('''()=>{window.qaUV=maziss3d.meshes.map(({mesh})=>
          ['paintFront','paintBack','paintSide','paintBlend'].map(n=>Array.from(mesh.geometry.attributes[n].array)));}''')
        page.evaluate('maziss3d.setPhase(.65)')
        stable = page.evaluate('''()=>maziss3d.meshes.every(({mesh},i)=>
          ['paintFront','paintBack','paintSide','paintBlend'].every((n,j)=>
          mesh.geometry.attributes[n].array.every((v,k)=>v===qaUV[i][j][k])))''')
        check(stable, 'Paint registrations stay attached to rest surfaces when the walk changes')
        frames = page.evaluate('''()=>{
          let out=[];for(let f=0;f<24;f++){
            maziss3d.setPhase(f/24);let bad=0,minBootZ=Infinity,maxZ=-Infinity,maxRadius=0;
            for(const {mesh,item}of maziss3d.meshes){let p=new THREE.Vector3();
              for(let i=0;i<mesh.geometry.attributes.position.count;i++){
                mesh.getVertexPosition(i,p);if(!Number.isFinite(p.x+p.y+p.z))bad++;
                maxZ=Math.max(maxZ,p.z);maxRadius=Math.max(maxRadius,Math.hypot(p.x,p.y));
                if(item.group==='Boots')minBootZ=Math.min(minBootZ,p.z);
              }}out.push({f,bad,minBootZ,maxZ,maxRadius});}return out;
        }''')
        check(not any(frame['bad'] for frame in frames), 'Actual skinned vertices remain finite in 24 cycle samples')
        check(all(frame['maxRadius'] < 1 and 1.5 < frame['maxZ'] < 2.5 for frame in frames),
              'Actual deformed geometry stays inside the intended character envelope')
        check(min(frame['minBootZ'] for frame in frames) > -.005, 'Actual boot vertices stay above the floor tolerance', min(frame['minBootZ'] for frame in frames))
        (output/'deformed-vertices.json').write_text(json.dumps(frames, indent=2)+'\n')
        captures = []
        for angle in range(0, 360, 45):
            for frame in range(4):
                page.evaluate('([a,p])=>{maziss3d.setView(a);maziss3d.setPhase(p)}', [angle, frame/4])
                target = output/f'painted-{angle}-{frame}.png'
                target.write_bytes(base64.b64decode(page.evaluate('maziss3d.snapshot()').split(',', 1)[1]))
                captures.append(target.name)
        # A contact sheet consists solely of actual renderer frames.
        image_tags = ''.join(f'<figure><figcaption>{name}</figcaption><img src="{name}" width="240"></figure>' for name in captures)
        (output/'review.html').write_text('<!doctype html><style>body{background:#65717b;color:white;display:grid;grid-template-columns:repeat(4,250px)}figure{margin:5px}img{display:block}</style>'+image_tags)
        page.click('#idle'); check(not page.evaluate('maziss3d.getState().walk'), 'Standing control uses an actual neutral pose')
        page.click('#step'); step = page.evaluate('maziss3d.getState()')
        check(step['walk'] and not step['playing'], 'Frame step returns to walking and pauses playback')
        page.select_option('#surface', 'clay')
        check(page.evaluate('maziss3d.meshes.every(({mesh})=>mesh.material.type==="MeshStandardMaterial")'), 'Plain geometry option exposes the underlying construction')
        page.select_option('#surface', 'paint')
        check(page.evaluate('maziss3d.meshes.every(({mesh})=>mesh.material===mesh.userData.paint)'), 'Painted artwork option restores actual mapped materials')
        page.select_option('#setting', 'room')
        check(page.locator('.stage').evaluate('s=>s.classList.contains("room")'), 'Approved-room setting shows the embedded painted environment')
        check(not errors, 'No JavaScript runtime errors', errors)
        check(not network, 'Self-contained viewer works with browser networking disabled', network)
        version = browser.version; browser.close()

    if not args.skip_authoring:
        authoring = check_authoring(args.directory, output)
        packed_hashes = {item['sha256'] for item in authoring['packedImages'] if item['packed']}
        expected = {digest(ROOT/path) for path in (*ART, 'art/walking/maziss-clean-garment-reference.png')}
        check(expected <= packed_hashes, 'Authoring .blend packs all three actual reference images')
        check(not authoring['missingUVLayers'], 'Authoring .blend retains all three registered UV layers on painted meshes', authoring['missingUVLayers'])
        check(authoring['collisionSamples'] == 0, 'Evaluated hand and forearm triangles do not intersect bag/tool triangles in idle plus all walking samples', authoring['collisionSamples'])
        check(authoring['maxSkinHitSourceZ'] <= .211, 'Anatomical skin intersects trousers only at closed lower caps enclosed by boots', authoring['maxSkinHitSourceZ'])

    check(digest(args.html) == manifest['output_sha256'] and source_match(), 'Reviewed HTML and all manifested inputs stayed fixed through the run')
    result = {'build': manifest['build'], 'html_sha256': manifest['output_sha256'],
              'passed': passed, 'failed': failed, 'objects': len(topology), 'captures': len(captures),
              'browser': version, 'seconds': round(time.monotonic()-started, 2),
              'limits': ['Finite, closed opaque surfaces can still overlap or stretch.',
                         'A sampled walk is not a proof for arbitrary future poses.',
                         'Texture mapping, face likeness and style require visual review.',
                         'This is not native Windows, Godot or performance testing.']}
    (output/'browser-results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'build': manifest['build'][:12], 'passed': len(passed), 'failed': failed,
                      'seconds': result['seconds']}))
    raise SystemExit(bool(failed))


if __name__ == '__main__':
    main()
