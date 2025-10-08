
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os, psycopg2
from opensearchpy import OpenSearch

DB_URL = os.getenv("DATABASE_URL", "postgresql://rag:ragpass@localhost:5432/ragdb")
OS_URL = os.getenv("OPENSEARCH_URL", "http://localhost:9200")

app = FastAPI(title="retriever")

class SearchRequest(BaseModel):
    query: str
    repo: Optional[str] = None
    k: int = 12

def os_client():
    return OpenSearch(OS_URL, http_compress=True, use_ssl=False, verify_certs=False)

@app.post("/search")
def search(req: SearchRequest):
    cl = os_client()
    must = [{"match": {"content": req.query}}]
    if req.repo:
        must.append({"term": {"repo.keyword": req.repo}})
    q = {"query": {"bool": {"must": must}}}
    res = cl.search(index="code_chunks", body=q, size=req.k)["hits"]["hits"]
    items = [dict(repo=r["_source"]["repo"], path=r["_source"]["path"], content=r["_source"]["content"], score=r["_score"]) for r in res]
    return {"results": items}
