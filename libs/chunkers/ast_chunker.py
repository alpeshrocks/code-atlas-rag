
from typing import List, Dict
import re

def chunk_code(path: str, text: str, lang: str) -> List[Dict]:
    lines = text.splitlines()
    chunks = []
    def push(symbol, start, end, typ="func"):
        content = "\n".join(lines[start-1:end])
        chunks.append(dict(type=typ, symbol=symbol, line_start=start, line_end=end, content=content))

    if lang.lower() in ("python","py"):
        pattern = re.compile(r"^(def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)
        starts = [(m.group(1), m.group(2), text[:m.start()].count('\n')+1) for m in pattern.finditer(text)]
    elif lang.lower() in ("ts","tsx","js","jsx","javascript","typescript"):
        pattern = re.compile(r"^(export\s+)?(function|class)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)
        starts = [(m.group(2), m.group(3), text[:m.start()].count('\n')+1) for m in pattern.finditer(text)]
    else:
        starts = []

    if starts:
        for i, (kw, name, line) in enumerate(starts):
            end_line = len(lines)
            if i+1 < len(starts):
                end_line = starts[i+1][2]-1
            push(name, line, end_line, "class" if kw=="class" else "func")
    else:
        CHUNK = 120
        for i in range(0, len(lines), CHUNK):
            push(f"chunk_{i//CHUNK}", i+1, min(i+CHUNK, len(lines)), "file")
    return chunks
