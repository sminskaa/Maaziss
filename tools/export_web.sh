#!/usr/bin/env bash
set -euo pipefail
project_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
mkdir -p "$project_dir/build/web"
touch "$project_dir/build/.gdignore"
bash "$project_dir/tools/godot.sh" --headless --path "$project_dir" --editor --import
bash "$project_dir/tools/godot.sh" --headless --path "$project_dir" --export-release Web "$project_dir/build/web/index.html"
python3 - "$project_dir" <<'PY'
from pathlib import Path
import sys
import zipfile
root = Path(sys.argv[1])
notices = root / 'docs/engine-notices'
if not all((notices / name).is_file() for name in ('LICENSE.txt', 'COPYRIGHT.txt')):
    raise SystemExit('Required Godot engine notices are missing; keep them with distribution artifacts.')
for name in ('LICENSE.txt', 'COPYRIGHT.txt'):
    (root / 'build/web' / ('GODOT-' + name)).write_bytes((notices / name).read_bytes())
with zipfile.ZipFile(root / 'build/maziss-opening-web.zip', 'w', compression=zipfile.ZIP_DEFLATED) as out:
    for path in sorted((root / 'build/web').rglob('*')):
        if path.is_file():
            out.write(path, path.relative_to(root / 'build/web'))
print('Created build/maziss-opening-web.zip')
PY
