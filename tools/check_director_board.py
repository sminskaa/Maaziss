#!/usr/bin/env python3
"""Check the visual direction file round-trip and actual browser controls.
Start python3 -m http.server 8765 in the repository first.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/checks/director-board';OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1400,'height':1050},accept_downloads=True)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8765/visual-preview/maziss-director.html')
 page.wait_for_function('Object.keys(images).length===3')
 def click(x,y):
  box=page.locator('#scene').bounding_box();page.mouse.click(box['x']+box['width']*x,box['y']+box['height']*y)
 click(.50,.84)
 page.locator('[data-mode=end]').click();click(.77,.74)
 page.locator('[data-mode=path]').click();click(.63,.82)
 page.locator('[data-face=NE]').click()
 page.locator('#comment').fill('Keep the right hand clear of the bag. <test>')
 page.locator('[data-mode=note]').click();click(.52,.65)
 page.locator('#intent').fill('Walk to the desk and stop.')
 expected=page.evaluate('JSON.parse(JSON.stringify(state))')
 assert len(expected['notes'])==1 and expected['facing']=='NE' and len(expected['path'])==1
 # Drag start using the rendered feet marker.
 page.locator('[data-mode=start]').click();box=page.locator('#scene').bounding_box()
 page.mouse.move(box['x']+box['width']*.50,box['y']+box['height']*.84);page.mouse.down();page.mouse.move(box['x']+box['width']*.47,box['y']+box['height']*.85);page.mouse.up()
 assert abs(page.evaluate('state.start.x')-.47)<.002
 page.locator('#undo').click();assert page.evaluate('JSON.stringify(state)')==json.dumps(expected,separators=(',',':'))
 page.reload();page.wait_for_function('Object.keys(images).length===3');assert page.evaluate('JSON.stringify(state)')==json.dumps(expected,separators=(',',':'))
 with page.expect_download() as event:page.locator('#save').click()
 event.value.save_as(OUT/'directions.json');export=json.loads((OUT/'directions.json').read_text());assert export['notes']==expected['notes']
 page.locator('[data-face=W]').click();page.locator('#loadFile').set_input_files(OUT/'directions.json')
 page.wait_for_function('state.facing==="NE"');assert page.locator('#notes').inner_text().find('<test>')>=0
 (OUT/'invalid.json').write_text('{"format":"wrong"}')
 page.locator('#loadFile').set_input_files(OUT/'invalid.json');page.wait_for_function('document.getElementById("saveStatus").textContent.startsWith("Could not open")');assert page.evaluate('state.facing')=='NE'
 with page.expect_download() as event:page.locator('#picture').click()
 event.value.save_as(OUT/'marked-room.png')
 page.screenshot(path=str(OUT/'desktop.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(OUT/'mobile.png'),full_page=True)
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.locator('#roomChoice').select_option('background');assert page.evaluate('state.room')=='background'
 page.locator('#showActor').uncheck();assert page.evaluate('state.showActor') is False
 assert not errors,errors
 report={'checks':['placement and path','facing','literal annotation text','drag and undo','browser reload persistence','JSON export/import','invalid import preserves work','marked PNG export','mobile layout without horizontal overflow','room selection and marker toggle'],'javascriptErrors':errors,'htmlBytes':(ROOT/'visual-preview/maziss-director.html').stat().st_size}
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));b.close()
