from pathlib import Path
import re
import shutil

root = Path(r'd:\my-blog\src\content\posts')
for d in [root / '_releases', root / '_color-schemes']:
    if d.exists():
        shutil.rmtree(d)

for path in list(root.rglob('*.md')) + list(root.rglob('*.mdx')):
    if any(part in {'_releases', '_color-schemes'} for part in path.relative_to(root).parts):
        continue
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    new_lines = []
    for line in lines:
        if line.lstrip().startswith('description:'):
            m = re.match(r'^(\s*description:\s*")(.*)("\s*)$', line)
            if m:
                val = m.group(2)
                idx = val.find('[![image]')
                if idx != -1:
                    val = val[:idx].rstrip()
                    line = f'{m.group(1)}{val}{m.group(3)}'
        if re.search(r'\[!\[image\]\(https?://', line):
            line = '<!-- Hotlink image placeholder: replace with a local asset later. -->'
        new_lines.append(line)
    new_text = '\n'.join(new_lines) + '\n'
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
print('Done')
