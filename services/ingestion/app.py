
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os, tempfile, os.path, json
from git import Repo
import psycopg2
from opensearchpy import OpenSearch

from libs.chunkers.ast_chunker import chunk_code
from libs.embeddings.simple_embed import embed_texts
from libs.graphs.build_graph import build_edges

DB_URL = os.getenv("DATABASE_URL", "postgresql://rag:ragpass@localhost:5432/ragdb")
OS_URL = os.getenv("OPENSEARCH_URL", "http://localhost:9200")

app = FastAPI(title="ingestion")

class IngestRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = "main"
    repo_name: Optional[str] = None

def detect_lang(path: str) -> str:
    p = path.lower()
    if p.endswith(".py"): return "python"
    if p.endswith((".ts",".tsx")): return "ts"
    if p.endswith((".js",".jsx")): return "js"
    if p.endswith(".java"): return "java"
    if p.endswith(".go"): return "go"
    if p.endswith((".md",".mdx",".rst")): return "md"
    return "txt"

def pg():
    return psycopg2.connect(DB_URL)

def os_client():
    return OpenSearch(OS_URL, http_compress=True, use_ssl=False, verify_certs=False)

@app.post("/ingest")
def ingest(req: IngestRequest):
    repo_name = req.repo_name or os.path.splitext(os.path.basename(req.repo_url.rstrip("/")))[0]
    tmp = tempfile.mkdtemp(prefix="repo_")
    Repo.clone_from(req.repo_url, tmp, branch=req.branch, depth=1)

    records = []
    for root, _, files in os.walk(tmp):
        for f in files:
            if f.startswith("."): continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, tmp)
            try:
                txt = open(path, "r", encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            if not txt.strip(): continue
            lang = detect_lang(rel)
            chunks = chunk_code(rel, txt, lang)
            for ch in chunks:
                ch.update({"repo": repo_name, "path": rel, "lang": lang})
                records.append(ch)

    # embeddings (placeholder random but deterministic-ish)
    import numpy as np
    vecs = embed_texts([r["content"] for r in records], dim=768)

    # PG store
    conn = pg(); conn.autocommit=True; cur = conn.cursor()
    cur.execute(open("schemas/chunks.sql","r").read())
    for r, v in zip(records, vecs):
        cur.execute("""
            INSERT INTO chunks (repo, path, lang, type, symbol, line_start, line_end, sha, meta, embedding)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (r["repo"], r["path"], r["lang"], r["type"], r.get("symbol"),
              r["line_start"], r["line_end"], "HEAD", json.dumps({}), list(v)))

    # OpenSearch lexical
    osc = os_client()
    idx = "code_chunks"
    if not osc.indices.exists(idx):
        osc.indices.create(idx, body={"mappings": {"properties": {
            "repo":{"type":"keyword"}, "path":{"type":"keyword"}, "content":{"type":"text"}
        }}})
    bulk = []
    for i, r in enumerate(records):
        bulk.append({"index": {"_index": idx, "_id": f"{repo_name}:{i}:{r['path']}"}})
        bulk.append({"repo": repo_name, "path": r["path"], "content": r["content"]})
    if bulk:
        from opensearchpy.helpers import bulk as os_bulk
        os_bulk(osc, bulk)

    # graph edges (toy)
    edges = build_edges(records)
    for e in edges:
        cur.execute("INSERT INTO graphs_edges (src_id, dst_id, edge_type, weight) VALUES (%s,%s,%s,%s)",
                    (e["src"]+1, e["dst"]+1, e["edge_type"], e["weight"]))

    return {"ok": True, "repo": repo_name, "chunks": len(records)}
