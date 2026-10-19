/* Offline review controller. Assets are actual fixed-camera Blender renders. */
(async function () {
  'use strict';
  const DATA = window.SOFA_DATA;
  const canvas = document.querySelector('#room');
  const ctx = canvas.getContext('2d');
  const status = document.querySelector('#status');
  const verbButtons = [...document.querySelectorAll('[data-verb]')];
  const W = 1672, H = 941;
  const polygon = DATA.floor;
  const sofaPolygon = [[0, 410], [145, 370], [510, 375], [605, 555], [575, 670], [390, 755], [0, 800]];
  const load = src => new Promise((resolve, reject) => {
    const image = new Image(); image.onload = () => resolve(image); image.onerror = reject; image.src = src;
  });
  const room = await load(DATA.room);
  const sheets = {};
  for (const [name, entry] of Object.entries(DATA.sheets)) {
    if (entry.kind === 'video') {
      const video = document.createElement('video'); video.muted = true; video.playsInline = true;
      video.preload = 'auto'; video.loop = name.startsWith('walk-');
      await new Promise((resolve, reject) => { video.onloadeddata = resolve; video.onerror = reject; video.src = entry.src; });
      sheets[name] = { ...entry, video };
    } else sheets[name] = { ...entry, image: await load(entry.src) };
  }
  const cachedActor = document.createElement('canvas'); cachedActor.width = DATA.renderSize[0]; cachedActor.height = DATA.renderSize[1];
  const cachedContext = cachedActor.getContext('2d'); let activeSheet = null;
  const seat = DATA.seat;
  let selectedVerb = 'Walk', mode = 'idle', position = { x: 1080, y: 815 };
  let heading = 90, phase = 0, path = [], pendingSit = false, afterStand = null;
  let sitProgress = 0, turnDestination = 335, turnAfter = null, poseIndex = 0;
  let last = performance.now(), loaded = true, walkDistance = 0;
  let message = 'Click the floor to walk. Select Use, then click the sofa to sit.';
  const say = text => { message = text; status.textContent = text; };
  const norm = value => (value % 360 + 360) % 360;
  const difference = (a, b) => ((b - a + 540) % 360) - 180;
  function inside(point, points = polygon) {
    let hit = false;
    for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
      const a = points[i], b = points[j];
      if ((a[1] > point.y) !== (b[1] > point.y) && point.x < (b[0] - a[0]) * (point.y - a[1]) / (b[1] - a[1]) + a[0]) hit = !hit;
    }
    return hit;
  }
  function distance(a, b) { return Math.hypot(a.x - b.x, a.y - b.y); }
  function visible(a, b) {
    const count = Math.max(2, Math.ceil(distance(a, b) / 9));
    for (let i = 0; i <= count; i++) {
      const t = i / count;
      if (!inside({ x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t })) return false;
    }
    return true;
  }
  // A small visibility graph respects the concave floor outline around sofa
  // and desk. Its nodes lie just inside the manually calibrated floor edge.
  const corners = DATA.routeNodes.map(([x, y]) => ({ x, y }));
  function route(start, target) {
    if (!inside(target)) return null;
    if (visible(start, target)) return [target];
    const nodes = [start, target, ...corners], costs = nodes.map(() => Infinity), previous = nodes.map(() => -1), used = new Set();
    costs[0] = 0;
    for (let k = 0; k < nodes.length; k++) {
      let current = -1;
      for (let i = 0; i < nodes.length; i++) if (!used.has(i) && (current < 0 || costs[i] < costs[current])) current = i;
      if (current < 0 || !Number.isFinite(costs[current])) break;
      if (current === 1) break;
      used.add(current);
      for (let i = 0; i < nodes.length; i++) {
        if (used.has(i) || i === current || !visible(nodes[current], nodes[i])) continue;
        const cost = costs[current] + distance(nodes[current], nodes[i]);
        if (cost < costs[i]) { costs[i] = cost; previous[i] = current; }
      }
    }
    if (!Number.isFinite(costs[1])) return null;
    const result = []; let at = 1;
    while (at !== 0) { result.unshift(nodes[at]); at = previous[at]; if (at < 0) return null; }
    return result;
  }
  const pixelsPerMetre = y => seat.pixelsPerMetre * (y + 100) / (seat.origin[1] + 100);
  function beginTurn(target, next) { mode = 'turning'; turnDestination = norm(target); turnAfter = next; }
  function arrive() {
    path = [];
    if (pendingSit) { pendingSit = false; beginTurn(335, 'sitting'); say('Turning toward the clear cushion…'); }
    else { mode = 'idle'; say('Ready.'); }
  }
  function startWalk(target, sit = false) {
    const planned = route(position, target);
    if (!planned) { say('There is no clear floor route there.'); return; }
    pendingSit = sit; path = planned;
    if (distance(position, target) < 2) arrive();
    else { mode = 'walking'; say(sit ? 'Walking to the clear cushion…' : 'Walking…'); }
  }
  function requestWalk(target, sit = false) {
    if (mode === 'seated' || mode === 'sitting') {
      afterStand = { target, sit }; mode = 'standing'; say('Standing up…'); return;
    }
    if (mode === 'standing') { afterStand = { target, sit }; return; }
    startWalk(target, sit);
  }
  function chooseVerb(verb) {
    selectedVerb = verb;
    verbButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.verb === verb)));
    say(verb === 'Use' ? 'Use: click the sofa to sit on the clear cushion.' : verb === 'Look at' ? 'Look at: click something to examine it.' : 'Click clear floor to walk.');
  }
  verbButtons.forEach(button => button.addEventListener('click', () => chooseVerb(button.dataset.verb)));
  document.querySelector('#reset').addEventListener('click', () => {
    mode = 'idle'; position = { x: 1080, y: 815 }; heading = 90; phase = 0;
    path = []; pendingSit = false; afterStand = null; sitProgress = 0; chooseVerb('Walk');
  });
  function pointOf(event) {
    const box = canvas.getBoundingClientRect();
    return { x: (event.clientX - box.left) * W / box.width, y: (event.clientY - box.top) * H / box.height };
  }
  canvas.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    const point = pointOf(event), onSofa = inside(point, sofaPolygon);
    if (selectedVerb === 'Look at') { say(onSofa ? 'A clear place on the right cushion. The pillows can stay where they are.' : 'A little room, with a lot of repairs waiting.'); return; }
    if (onSofa) {
      if (selectedVerb === 'Use') {
        if (mode === 'seated') say('Already sitting on the clear cushion.');
        else if (mode === 'sitting' || (mode === 'turning' && turnAfter === 'sitting')) say('Settling onto the clear cushion…');
        else requestWalk({ x: seat.origin[0], y: seat.origin[1] }, true);
      } else requestWalk({ x: seat.origin[0], y: seat.origin[1] });
      return;
    }
    if (!inside(point)) { say('Maziss cannot walk through the wall or furniture.'); return; }
    requestWalk(point);
  });
  canvas.addEventListener('contextmenu', event => {
    event.preventDefault(); say(inside(pointOf(event), sofaPolygon) ? 'The clear right cushion is available. Use the sofa to sit.' : 'Nothing to use here.');
  });
  function stamp(sheetName, frame, x, y, scale) {
    const sheet = sheets[sheetName], size = DATA.cell;
    if (activeSheet !== sheetName) {
      if (activeSheet && sheets[activeSheet].video) sheets[activeSheet].video.pause();
      activeSheet = sheetName;
      if (sheet.video) {
        const v = sheet.video;
        v.currentTime = sheetName.startsWith('walk-') ? phase * v.duration : sheetName === 'stand' ? (1 - sitProgress) * v.duration : sitProgress * v.duration;
        v.playbackRate = sheetName.startsWith('walk-') ? 1.05 * v.duration / DATA.strideMetres : v.duration / DATA.sitSeconds;
        if (mode !== 'seated') v.play().catch(error => console.error(error));
      }
    }
    if (sheet.video) {
      const v = sheet.video;
      if (mode === 'seated' && !v.paused) { v.pause(); v.currentTime = Math.max(0, v.duration - .001); }
      if (!v.seeking && v.readyState >= 2) { cachedContext.clearRect(0, 0, cachedActor.width, cachedActor.height); cachedContext.drawImage(v, 0, 0, cachedActor.width, cachedActor.height); }
      ctx.drawImage(cachedActor, x, y, DATA.renderSize[0] * scale, DATA.renderSize[1] * scale); return;
    }
    frame = Math.max(0, Math.min(sheet.frames - 1, frame));
    const sx = (frame % sheet.columns) * size[0], sy = Math.floor(frame / sheet.columns) * size[1];
    ctx.drawImage(sheet.image, sx, sy, size[0], size[1], x, y, DATA.renderSize[0] * scale, DATA.renderSize[1] * scale);
  }
  function draw() {
    ctx.clearRect(0, 0, W, H); ctx.drawImage(room, 0, 0, W, H);
    const sitting = ['sitting', 'seated', 'standing'].includes(mode);
    const angle = Math.round(norm(heading) / 45) % 8 * 45;
    const ppm = sitting ? seat.pixelsPerMetre : pixelsPerMetre(position.y);
    const scale = ppm / DATA.renderPixelsPerMetre;
    const x = position.x - DATA.groundPixel[0] * scale, y = position.y - DATA.groundPixel[1] * scale;
    // Soft contact cues follow projected sole positions. They are review
    // compositing, not physically cast shadows from a modeled room.
    const shadows = DATA.footShadows[sitting ? 'sit' : String(angle)];
    ctx.fillStyle = 'rgba(37,18,33,.23)';
    if (mode === 'walking') {
      ctx.fillStyle = 'rgba(37,18,33,.16)'; ctx.beginPath(); ctx.ellipse(position.x, position.y + 5 * scale, 29 * scale, 6 * scale, 0, 0, Math.PI * 2); ctx.fill();
    } else for (const p of shadows) { ctx.beginPath(); ctx.ellipse(x + p[0] * scale, y + p[1] * scale, 16 * scale, 4 * scale, 0, 0, Math.PI * 2); ctx.fill(); }
    if (sitting && sitProgress > .65) {
      ctx.fillStyle = `rgba(55,10,12,${.13 * sitProgress})`; ctx.beginPath(); ctx.ellipse(seat.contact[0], seat.contact[1] + 4, 42, 8, 0, 0, Math.PI * 2); ctx.fill();
    }
    if (sitting) {
      poseIndex = Math.round(sitProgress * (DATA.sitFrames - 1)); stamp(mode === 'standing' ? 'stand' : 'sit', poseIndex, x, y, scale);
    } else if (mode === 'walking') {
      poseIndex = Math.floor(phase * 24) % 24; stamp(`walk-${angle}`, poseIndex, x, y, scale);
    } else {
      const idleAngle = Math.round(norm(heading) / 22.5) % 16;
      poseIndex = idleAngle; stamp('idle', idleAngle, x, y, scale);
    }
    // Only the painted near sofa arm is a foreground occluder in the sitting
    // zone. This gives the same proxy a stable screen-space depth boundary.
    if (sitting) {
      ctx.save(); ctx.beginPath();
      const points = DATA.nearArm; ctx.moveTo(...points[0]); points.slice(1).forEach(p => ctx.lineTo(...p)); ctx.closePath(); ctx.clip(); ctx.drawImage(room, 0, 0, W, H); ctx.restore();
    }
    if (document.querySelector('#guide').checked) {
      ctx.strokeStyle = '#ffdb77'; ctx.lineWidth = 2; ctx.beginPath();
      DATA.seatGuide.forEach((p, i) => i ? ctx.lineTo(...p) : ctx.moveTo(...p)); ctx.closePath(); ctx.stroke();
      ctx.fillStyle = '#ffdb77'; ctx.beginPath(); ctx.arc(seat.contact[0], seat.contact[1], 5, 0, Math.PI * 2); ctx.fill();
    }
  }
  function update(now) {
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    if (mode === 'walking' && path.length) {
      const goal = path[0], dx = goal.x - position.x, dy = goal.y - position.y;
      const worldMetric = Math.hypot(dx, dy / DATA.floorForeshortening);
      const amount = Math.min(1, 1.05 * pixelsPerMetre(position.y) * dt / Math.max(.001, worldMetric));
      const old = { ...position }; position.x += dx * amount; position.y += dy * amount;
      const travelled = Math.hypot(position.x - old.x, (position.y - old.y) / DATA.floorForeshortening) / pixelsPerMetre(position.y);
      walkDistance += travelled; phase = (phase + travelled / DATA.strideMetres) % 1;
      heading = norm(Math.atan2(-dx, dy / DATA.floorForeshortening) * 180 / Math.PI);
      if (distance(position, goal) < 1) { position = { ...goal }; path.shift(); if (!path.length) arrive(); }
    } else if (mode === 'turning') {
      const delta = difference(heading, turnDestination), step = Math.sign(delta) * Math.min(Math.abs(delta), 360 * dt);
      heading = norm(heading + step);
      if (Math.abs(delta) < .2) { mode = turnAfter; heading = turnDestination; sitProgress = 0; say('Sitting down…'); }
    } else if (mode === 'sitting') {
      sitProgress = Math.min(1, sitProgress + dt / DATA.sitSeconds);
      if (sitProgress === 1) { mode = 'seated'; say('Seated on the clear cushion. Click the floor to stand and walk.'); }
    } else if (mode === 'standing') {
      sitProgress = Math.max(0, sitProgress - dt / DATA.sitSeconds);
      if (sitProgress === 0) { mode = 'idle'; heading = 335; const next = afterStand; afterStand = null; if (next) startWalk(next.target, next.sit); }
    }
    draw(); requestAnimationFrame(update);
  }
  Object.defineProperty(window, 'mazissReview', { value: Object.freeze({
    snapshot: () => ({ loaded, mode, selectedVerb, position: { ...position }, heading, path: path.map(p => ({ ...p })),
      pendingSit, sitProgress, renderFrame: poseIndex, walkDistance, message,
      media: activeSheet && sheets[activeSheet].video ? { activeSheet, currentTime: sheets[activeSheet].video.currentTime, duration: sheets[activeSheet].video.duration, readyState: sheets[activeSheet].video.readyState, paused: sheets[activeSheet].video.paused } : { activeSheet },
      seat: JSON.parse(JSON.stringify(seat)), floor: polygon.map(p => [...p]), sceneSize: [W, H],
      sourceModelSHA256: DATA.sourceModelSHA256, scalePixelsPerMetre: mode === 'seated' ? seat.pixelsPerMetre : pixelsPerMetre(position.y) })
  }), writable: false });
  document.querySelector('#loading').hidden = true; chooseVerb('Walk'); requestAnimationFrame(update);
})().catch(error => { document.querySelector('#status').textContent = 'The interactive view could not load. The still below remains available.'; console.error(error); });
