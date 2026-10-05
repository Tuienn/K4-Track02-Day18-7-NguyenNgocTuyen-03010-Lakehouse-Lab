"""Execute original Jupytext cells with a venv kernel; preserve real outputs.

Run from the repo root with .venv/bin/python scripts/execute_submission.py [1..8].
Execution errors stop the command. HTML/text evidence is derived solely from
executed notebook outputs; screenshots use scripts/screenshot_submission.cjs.
"""
from __future__ import annotations

import argparse
import html
import os
import sys
from pathlib import Path

import jupytext
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submission"
BOOTSTRAP = '''from pathlib import Path
import sys
_candidates = [Path.cwd(), *Path.cwd().parents]
_repo = next(p for p in _candidates if (p / "scripts/lakehouse.py").is_file()
             and (p / "notebooks/_setup.py").is_file())
sys.path.insert(0, str(_repo / "notebooks"))
'''


def execute(number: int) -> None:
    source = next((ROOT / "notebooks").glob(f"{number:02d}_*.py"))
    nb = jupytext.read(source)
    nb.cells.insert(0, nbformat.v4.new_markdown_cell(
        "**Bài cá nhân:** Nguyễn Ngọc Tuyền — MSSV 2A202603010. "
        "Đường lightweight. Output dưới đây do kernel thực thi; "
        "phạm vi hỗ trợ AI được khai trong `submission/AI_USAGE.md`."))
    nb.cells.insert(1, nbformat.v4.new_code_cell(BOOTSTRAP))
    # Pass the actual venv executable instead of relying on PATH or a user's kernel.
    client = NotebookClient(nb, timeout=600, kernel_name="python3",
                            resources={"metadata": {"path": str(ROOT)}})
    os.environ.setdefault("JUPYTER_RUNTIME_DIR", "/tmp/lakehouse-jupyter-runtime")
    os.environ.setdefault("IPYTHONDIR", "/tmp/lakehouse-ipython")
    client.create_kernel_manager()
    client.km.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher",
                                  "-f", "{connection_file}"]
    client.execute()
    for cell in nb.cells:
        if cell.cell_type == "code":
            assert cell.execution_count is not None
            assert not any(o.output_type == "error" for o in cell.outputs)
    (SUB / "notebooks").mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, SUB / "notebooks" / f"{source.stem}.ipynb")
    chunks = []
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        texts = []
        for output in cell.outputs:
            if output.output_type == "stream":
                texts.append(output.text)
            elif "text/plain" in output.get("data", {}):
                texts.append(output.data["text/plain"])
        if texts:
            chunks.append(f"Cell [{cell.execution_count}]\n" + "".join(texts))
    output = "\n\n".join(chunks)
    evidence = SUB / "evidence"
    evidence.mkdir(exist_ok=True)
    (evidence / f"{source.stem}.txt").write_text(output, encoding="utf-8")
    page = f'''<!doctype html><html lang="vi"><meta charset="utf-8">
<title>{source.stem} — output thực thi</title>
<style>body{{font:16px sans-serif;margin:36px;max-width:1400px}}pre{{font:15px monospace;
white-space:pre-wrap;overflow-wrap:anywhere;border:1px solid #ccc;padding:18px;
line-height:1.45;background:#f7f8fa}}h1{{font-size:24px}}</style>
<h1>{source.stem}</h1><p>Nguyễn Ngọc Tuyền · 2A202603010 · Lightweight</p>
<p>Output lấy nguyên văn từ notebook đã thực thi, không sửa số liệu.</p>
<pre>{html.escape(output)}</pre></html>'''
    (evidence / f"{source.stem}.html").write_text(page, encoding="utf-8")
    print(f"PASS {source.name}: {len(chunks)} output cells preserved")
    print(output[-3500:])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("numbers", nargs="*", type=int, choices=range(1, 9))
    args = parser.parse_args()
    for number in args.numbers or range(1, 9):
        execute(number)
