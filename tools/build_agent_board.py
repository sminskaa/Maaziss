#!/usr/bin/env python3
"""Build a static, offline activity board from recorded native-agent observations."""
from datetime import datetime
from html import escape
import json
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def e(value: object) -> str:
    return escape(str(value))


def local_time(value: str) -> str:
    return datetime.fromisoformat(value).astimezone(ZoneInfo('Europe/Paris')).strftime('%d %B %Y, %H:%M:%S %Z')


def main() -> None:
    registry = ROOT / 'production/agent-board.json'
    data = json.loads(registry.read_text())
    cards = []
    for task in data['tasks']:
        criteria = ''.join('<li>' + e(c) + '</li>' for c in task['acceptance'])
        files = ', '.join(task['allowed_files'])
        report = ''
        deliverable = task['deliverable']
        # Read only project-relative deliverables, never arbitrary registry paths.
        candidate = (ROOT / deliverable).resolve()
        if candidate.is_relative_to(ROOT / 'production') and candidate.is_file():
            report = '<details><summary>Read the worker’s report</summary><pre>' + e(candidate.read_text()) + '</pre></details>'
        cards.append(f'''<article><div class="tag">{e(task['id'])} · {e(task['role'])}</div>
<h3>{e(task['title'])}</h3><p><strong>Task status:</strong> {e(task['status'])}</p>
<p><strong>Actual worker:</strong> <code>{e(task['agent'] or 'Not started')}</code></p>
<p>{e(task['objective'])}</p><p><strong>Deliverable:</strong> {e(deliverable)}</p>
<details><summary>Assignment and acceptance criteria</summary><p>Allowed files: {e(files)}</p><ul>{criteria}</ul></details>
<p><strong>Result:</strong> {e(task['result'] or 'No completed result recorded yet.')}</p>{report}</article>''')
    roles = ''.join('<tr><td>' + e(r['role']) + '</td><td>' + e(r['activation']) + '</td></tr>' for r in data['roles'])
    events = ''.join('<li><time>' + e(local_time(v['time'])) + '</time> · <strong>' + e(v['task']) + '</strong>: ' + e(v['event']) + '</li>' for v in reversed(data['events']))
    guide = (ROOT / 'docs/AGENT_WORKFLOW.md').read_text() if (ROOT / 'docs/AGENT_WORKFLOW.md').is_file() else 'Guide is being prepared.'
    document = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Maziss — agent activity board</title><style>
body{background:#152128;color:#f5e8ce;font:17px/1.55 system-ui;margin:0;padding:24px}main{max-width:1150px;margin:auto}h1,h2,h3{line-height:1.2}h2{margin-top:38px}article,.notice{background:#22353d;border:1px solid #63766d;border-radius:10px;padding:20px;margin:18px 0}.notice{border-color:#e6b65f}.tag{color:#efbf69;font-weight:bold}p{margin:12px 0}code,pre{font-size:14px;overflow-wrap:anywhere}pre{white-space:pre-wrap;background:#122027;padding:16px;border-radius:8px}summary{cursor:pointer;color:#efbf69}details{margin:14px 0}table{border-collapse:collapse;width:100%}td,th{padding:12px;border-bottom:1px solid #506166;text-align:left}li{margin:8px 0}time,.muted{color:#bec9c7}a{color:#efbf69}
</style><main><h1>Maziss — agent activity board</h1>'''
    document += '<div class="notice"><strong>Recorded snapshot, not live monitoring.</strong><p>Last observed update: ' + e(local_time(data['updated_at'])) + '</p><p>' + e(data['snapshot_note']) + '</p><p>This page cannot start, stop or watch native agents itself. Ask the coordinating assistant to check the real agent status and update the board. Browser refresh only reloads the saved snapshot.</p></div>'
    document += '<h2>Actual assignments</h2>' + ''.join(cards)
    document += '<h2>Defined roles</h2><p>A defined role is a set of instructions. It does not mean another agent is running. The coordinator and liaison are currently the same assistant.</p><table><thead><tr><th>Role</th><th>Activation</th></tr></thead><tbody>' + roles + '</tbody></table>'
    document += '<h2>Observed activity</h2><ol>' + events + '</ol>'
    document += '<h2>How to use the team</h2><details open><summary>Beginner workflow guide</summary><pre>' + e(guide) + '</pre></details></main></html>'
    target = ROOT / 'production/index.html'
    target.write_text(document)
    target.chmod(0o644)
    target.parent.chmod(0o755)
    registry.chmod(0o644)
    print(f'Created {target.relative_to(ROOT)} ({target.stat().st_size:,} bytes), {len(data["tasks"])} assignments')


if __name__ == '__main__':
    main()
