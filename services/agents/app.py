
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI(title="agents")

class BugReport(BaseModel):
    stacktrace: str
    query_hint: Optional[str] = None
    k: int = 8

@app.post("/bugfinder")
def bugfinder(rep: BugReport):
    q = rep.query_hint or rep.stacktrace.splitlines()[-1][:200]
    res = requests.post("http://retriever:7020/search", json={"query": q, "k": rep.k}).json()
    suspects = [{"path": it["path"], "preview": it["content"][:160]} for it in res["results"]]
    return {"query": q, "suspects": suspects}

class RefactorPlan(BaseModel):
    goal: str
    scope_glob: Optional[str] = "**/*.py"

@app.post("/refactor/plan")
def plan(p: RefactorPlan):
    steps = [
        {"id": 1, "desc": f"Survey files in {p.scope_glob}"},
        {"id": 2, "desc": "Draft minimal diff for one file; run tests"},
        {"id": 3, "desc": "Expand to remaining files; batch changes"},
    ]
    return {"goal": p.goal, "steps": steps}
