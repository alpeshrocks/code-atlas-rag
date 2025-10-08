
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="reranker")

class Item(BaseModel):
    content: str
    score: float

class RerankRequest(BaseModel):
    query: str
    items: List[Item]

@app.post("/rerank")
def rerank(req: RerankRequest):
    tokens = set(req.query.lower().split())
    rescored = []
    for it in req.items:
        add = sum(1 for t in tokens if t in it.content.lower()) * 0.1
        rescored.append({"content": it.content, "score": it.score + add})
    rescored.sort(key=lambda x: x["score"], reverse=True)
    return {"items": rescored}
