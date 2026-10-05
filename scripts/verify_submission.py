"""Check submission completeness, source/output consistency and evidence images."""
from pathlib import Path
import struct

import jupytext
import nbformat

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / 'submission'
files = sorted((SUB / 'notebooks').glob('[0-9]*.ipynb'))
assert len(files) == 8, f'Expected 8 notebooks, found {len(files)}'
for path in files:
    nb = nbformat.read(path, as_version=4)
    original = jupytext.read(ROOT / 'notebooks' / f'{path.stem}.py')
    # First two cells are submission identity and portable import bootstrap.
    assert len(nb.cells) == len(original.cells) + 2
    assert [c.source for c in nb.cells[2:]] == [c.source for c in original.cells], path.name
    code = [c for c in nb.cells if c.cell_type == 'code']
    assert [c.execution_count for c in code] == list(range(1, len(code) + 1)), path.name
    assert all(o.output_type != 'error' for c in code for o in c.outputs)
    chunks = []
    for c in code:
        texts = []
        for o in c.outputs:
            if o.output_type == 'stream':
                texts.append(o.text)
            elif 'text/plain' in o.get('data', {}):
                texts.append(o.data['text/plain'])
        if texts:
            chunks.append(f'Cell [{c.execution_count}]\n' + ''.join(texts))
    output = '\n\n'.join(chunks)
    assert output == (SUB / 'evidence' / f'{path.stem}.txt').read_text()
    assert '[FAIL]' not in output
    screenshot = SUB / 'screenshots' / f'{path.stem}.png'
    png = screenshot.read_bytes()
    assert png[:8] == b'\x89PNG\r\n\x1a\n'
    width, height = struct.unpack('>II', png[16:24])
    assert width >= 1000 and height >= 500
    print(f'PASS {path.name}: {len(code)} executed cells, matching source/output, PNG {width}×{height}')
reflection = (SUB / 'REFLECTION.md').read_text()
assert len(reflection.split()) <= 200
assert 'AI_USAGE.md' in reflection
for required in ['INFO.md', 'PLAN.md', 'AI_USAGE.md', 'requirements-lock.txt']:
    assert (SUB / required).is_file()
print(f'PASS reflection ≤200 whitespace words: {len(reflection.split())}')
print('PASS 8/8 submission artifacts complete; GitHub submission remains pending.')
