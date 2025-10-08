
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from libs.utils.scrub import scrub

app = FastAPI(title="llm-proxy")

class ContextSpan(BaseModel):
    repo: str
    path: str
    line_start: int
    line_end: int
    content: str

class AnswerRequest(BaseModel):
    question: str
    contexts: List[ContextSpan]
    mode: Optional[str] = "explain"

@app.post("/answer")
def answer(req: AnswerRequest):
    citations = [f"{c.path}#{c.line_start}-{c.line_end}" for c in req.contexts[:5]]
    previews = []
    for c in req.contexts[:5]:
        lines = c.content.splitlines()[:5]
        previews.append(f"- {c.path}:{c.line_start}-{c.line_end} ⇒ " + " ".join(lines)[:160])
    text = "Question: " + req.question + "\n\nGrounded summary based on retrieved contexts:\n" + "\n".join(previews)
    return {"answer": scrub(text), "citations": citations}
