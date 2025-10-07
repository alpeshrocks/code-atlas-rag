
# 🚀 CodeAtlas RAG
**AI-Powered Code Intelligence & Developer Assistant**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Backend: FastAPI](https://img.shields.io/badge/backend-FastAPI-blue)]()
[![Frontend: Next.js](https://img.shields.io/badge/frontend-Next.js-black)]()
[![DB: Postgres+pgvector](https://img.shields.io/badge/db-Postgres%2Bpgvector-316192)]()
[![Search: OpenSearch](https://img.shields.io/badge/search-OpenSearch-005EB8)]()

> **CodeAtlas RAG** turns your codebase into a **living knowledge graph**. It blends **hybrid retrieval**, **graph signals**, and **LLM agents** to help engineers **search, explain, refactor, and debug** complex repositories — with **grounded, citable answers**.

---

## ✨ Features
- 🔎 **Hybrid Search** — natural language + BM25 + (pluggable) vector search; multi-repo.
- 📖 **Grounded Explanations** — answers cite file and line ranges.
- 🧠 **Agents**
  - *BugFinder*: localizes likely culprit code from stack traces.
  - *RefactorBot*: proposes safe, minimal diffs with tests.
  - *TestGen* (stub): test skeletons from code + examples.
- 🧩 **Code Intelligence** — call/import graph (stub), ownership insights (planned), change heatmaps (planned).
- 🖥️ **DX** — Next.js web app, VS Code extension, REST API.
- 🔐 **Safety** — secret scrubber and audit-friendly logging (extendable), RBAC hooks.

---

## 🏛️ Architecture
```
Sources → Ingestion → Embeddings + Graph Index → Hybrid Retrieval + Reranker
→ LLM Proxy (tool-using) → Agents → API Gateway → Web / VS Code
```
- **Stores**: Postgres (pgvector), OpenSearch, Redis, Neo4j
- **Services**: Ingestion, Retriever, Reranker, LLM Proxy, Agents, API Gateway
- **Apps**: Web UI, VS Code Extension

---

## ⚡ Quick Start
### 1) Clone & configure
```bash
git clone https://github.com/your-username/code-atlas-rag.git
cd code-atlas-rag
cp infra/docker/.env.example .env
```
### 2) Run infra & services
```bash
docker compose up -d
```
### 3) Ingest a repo
```bash
curl -X POST http://localhost:7010/ingest   -H "Content-Type: application/json"   -d '{"repo_url":"https://github.com/pallets/flask"}'
```
### 4) Ask your repo
```bash
curl -X POST http://localhost:8080/v1/answer   -H "Content-Type: application/json"   -d '{"question":"Where is request routing implemented?"}'
```
Open the web app: **http://localhost:3000**

---

## 📸 Screenshots
> _Tip: add a couple GIFs — web search, answer with citations, and the VS Code command._

---

## 🧩 Project Structure
```
apps/
  web/                # Next.js web UI
  vscode-extension/   # VS Code plugin
services/
  ingestion/          # Repo crawl → chunks → embeddings → indexes
  retriever/          # Hybrid search (BM25 + vector, pluggable)
  reranker/           # Cross-encoder reranker (stub)
  llm-proxy/          # Grounded answer synthesis with citations
  agents/             # BugFinder, RefactorBot, TestGen
  api-gateway/        # Single API entrypoint
libs/                 # Chunkers, embeddings, simple graph builder, secret scrubber
schemas/              # Postgres schemas (pgvector + graph edges)
infra/                # Docker & deployment configs
data/eval/            # Sample eval cases
```
---

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python 3.11)
- **Frontend**: Next.js + React
- **Infra**: Docker Compose (K8s ready)
- **Datastores**: Postgres (pgvector), OpenSearch, Redis, Neo4j
- **IDE**: VS Code extension (TypeScript)

---

## 🔧 Configuration & Extensibility
- **Embeddings**: replace `libs/embeddings/simple_embed.py` with OpenAI, Azure, or local vector backends.
- **Dense Search**: add query embeddings + `ORDER BY embedding <-> query_vec` in retriever.
- **Reranker**: swap stub with cross-encoder (e.g., bge-reranker, Cohere re-rank).
- **Agents**: wire `git diff` generation and CI test runs; add patch application with approvals.
- **Security**: plug in OIDC/SSO, RBAC per repo/path, secret scanning/SAST.
- **Graphs**: replace stub with tree-sitter/LSP-based call/import graphs.

---

## 🧪 Evaluation (recommended)
- Curate Q→gold file/line pairs in `data/eval/`.
- Track retrieval quality (nDCG@k, Recall@k) across commits.
- Add A/B flags for hybrid weights, rerankers, and graph expansion.

---

## 🤝 Contributing
1. Fork this repo
2. Create a feature branch: `git checkout -b feature/my-idea`
3. Commit changes: `git commit -m "feat: add my idea"`
4. Push: `git push origin feature/my-idea`
5. Open a Pull Request 🎉

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 💼 Why this is resume-worthy
- Demonstrates **end-to-end systems design** (ingestion → indexing → retrieval → rerank → LLM → agents → UI).
- Shows **data/AI engineering + SWE** in one cohesive platform.
- Emphasizes **practical developer impact** (bug localization, refactoring, testing).
- Uses **industry-standard tooling** (Docker, FastAPI, Next.js, pgvector, OpenSearch).
- Clear roadmap and contributor docs imply **maintainability and leadership**.
---

## 👤 Author

**Alpesh Shinde**  
🎓 MS CS @ USC | Data Engineering • Data Science • AI/ML • SWE  
🌍 Passion for food, travel, and building impactful tech.  

[LinkedIn](https://www.linkedin.com/in/alpeshshinde/) • [GitHub](https://github.com/alpeshrocks) • [Portfolio](https://alpeshrocks.github.io/alpesh-portfolio/)

---

## 📜 License
This project is licensed under the MIT License — free to use and adapt.
