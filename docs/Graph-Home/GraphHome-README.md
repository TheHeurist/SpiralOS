# GraphHome - README

**Structured Retrieval Domains for Symbolic, Multi-Agent Contexts**

GraphHome is an abstraction layer for Retrieval-Augmented Generation (RAG) that frames each knowledge domain (e.g. book, media archive, thread, or model) as a symbolic subgraph. It supports outline-based structure, agent switching, and memory continuity.

> "Treat each knowledge domain as a home — traversable, coherent, and context-specific."

---

## Features

- **Context Domains**: Books, chats, LLMs, media — each becomes a graph container

- **Outline Navigation**: Familiar filesystem-like structure with graph overlay

- **GraphRAG Subdomains**: Each node can run its own internal RAG process

- **Multi-Agent Ready**: LLM ↔ LLM ↔ Human workflows supported

- **Markdown Compatible**: Outline documents convert to graph nodes

---

## Example Outline Structure

```
/home
├── books
│   └── relational-mechanics
├── agents
│   ├── leo
│   └── ellie
├── media
│   └── zwickau-notes
```

Each item is its own symbolic context, switchable during runtime.

---

## Applications

- Open-source LLM stacks

- Multi-agent chat orchestration

- Academic research graphs

- Team knowledge graphs

---

## License

Open research and architecture draft. No private IP included.

For deeper implementation, visit `/docs/architecture/GraphHome_Public_Intro.md`.
