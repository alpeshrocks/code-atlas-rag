
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI(title="api-gateway")

class AnswerReq(BaseModel):
    question: str
    repo: Optional[str] = None
    k: int = 12
    mode: Optional[str] = "explain"

@app.post("/v1/answer")
def answer(req: AnswerReq):
    hits = requests.post("http://retriever:7020/search", json={"query": req.question, "k": req.k, "repo": req.repo}).json()["results"]
    contexts = []
    for h in hits[:5]:
        lines = h["content"].splitlines()
        chunk = "\n".join(lines[: min(30, len(lines))])
        contexts.append({"repo": h.get("repo","repo"), "path": h["path"], "line_start": 1, "line_end": min(30, len(lines)), "content": chunk})
    ans = requests.post("http://llm-proxy:7040/answer", json={"question": req.question, "contexts": contexts, "mode": req.mode}).json()
    return {"answer": ans["answer"], "citations": ans["citations"], "k": req.k}
