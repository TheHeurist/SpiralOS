# Library of the Endless Now — Technical Development Roadmap

This roadmap outlines the **phased plan** for developing the Library of the Endless Now within SpiralOS. It combines immersive design, graph-based navigation, and trusted backend integration. It explicitly includes **spatial graphs (e.g., 3d-force-graph)** and Unity/VR pathways.

---

## Phase 1 — Foundations (EKR + Graph & Storage)

**Goal:** Stand up the trusted data backbone and minimal schema for Epistemic Knowledge Representation (EKR).

- **Graph Store (JanusGraph):**
  - Schema: `Pearl`, `Artifact`, `Trail`, `Topic`, `Person`, `Portal`, `Obelisk` nodes; edges like `CONTAINS`, `REFERS_TO`, `NEXT`, `DERIVED_FROM`, `OWNS`, `OPEN_PORTAL_TO`.
  - Indices on `uid`, `type`, `timestamp`, `tags`, `title`, `hash`.
  - Persistence across container restarts; snapshotting enabled.
- **Files & Blobs (Nextcloud):**
  - Canonical storage for documents, media, transcripts. 
  - WebDAV paths referenced from graph nodes; checksum + size for integrity.
- **Search (Elasticsearch/OpenSearch):**
  - Full‑text over extracted text; embeddings computed asynchronously.
  - Access restricted to internal network only (container‑internal).
- **APIs:**
  - REST + GraphQL gateway (SpiralGraph). 
  - Token‑based mutation protection; service accounts for ETL jobs.
- **Security & Backups:**
  - Nightly graph + file metadata backups; 5‑day rolling retention.
  - Secrets in vault; audit log for write paths.

**Deliverable:** Minimal EKR populated from 1–2 seeded collections (e.g., Lumo docs, SpiralOS notes) and visible via GraphQL.

---

## Phase 2 — Spatial Graph (Web) ⚡ 3d‑force‑graph

**Goal:** Fast, shareable browser canvas for exploring the knowledge field.

- **Frontend Stack:** Next.js + React + **3d‑force‑graph** (Three.js under the hood).
- **Graph Mapping:**
  - Nodes styled by type (Pearl/Artifact/Trail/Portal/Obelisk).
  - Size = centrality/importance; glow = freshness; orbit = scope/depth level.
- **Interactions:**
  - Click = open right‑panel detail (metadata, preview, links to artifacts/portals).
  - Shift‑click = pin node; Ctrl‑drag = lasso select; `F` to focus + fit.
  - Minimap + breadcrumb of **Trail** edges; time slider for temporal replay.
- **Retrieval:** Hybrid search (keyword + vector) → highlight candidate subgraph (community extraction).
- **Auth:** JWT/session cookies; role‑based visibility on nodes/edges.

**Deliverable:** Deployed web explorer with live data; shareable read‑only links for Heather.

---

## Phase 3 — Immersive Prototype (Unity/WebXR)

**Goal:** Bring the Library’s symbolic hall to life with **orbs, obelisks, shelves, portals, and spiral stair**.

- **Unity Scene:** Central Atrium (orbs = Pearls/Trails), perimeter **Portal Obelisks** (domain chambers), **Archives** (bookshelves), **World Portals**, **Endless Spiral Stair**.
- **Data Binding:** WebSocket/HTTP to GraphQL; lazy‑load node details; sprite/text meshes for metadata.
- **Locomotion:** Smooth + teleport; comfort vignetting; controller + keyboard fallback.
- **Interactions:**
  - Gaze/point → reveal metadata; select → open 3D trail ribbon (conversation/flow playback).
  - Stairs up/down → scope/depth conjugation (macro overview ↔ micro detail).
  - Portals → encapsulated external chambers (Internet, GitHub, Nextcloud) that maintain symbolic coherence.
- **Performance:** GPU instancing for orbs; imposters for distant nodes; async streaming.

**Deliverable:** Click‑through demo path (5–7 minutes) showcasing the full “journey loop.”

---

## Phase 4 — ETL & Ingestion Mesh

**Goal:** Continuous ingestion from trusted sources with provenance and de‑duplication.

- **Connectors:** Nextcloud folders, Markdown/Docs, transcripts, PDFs, Git repos.
- **Pipelines:**
  - Extract → normalize → chunk → embed; compute checksums; attach provenance.
  - Build **Trails** automatically from chat logs and meeting transcripts.
- **Entity/Topic Linking:** NER + ontology hints; map to `Person`, `Topic`, `Project` nodes.
- **Provenance Graph:** Edge annotations (who/when/how); replayable ingestion history.

**Deliverable:** Dashboard showing ingestion status; new content appears in web explorer within minutes.

---

## Phase 5 — Reasoning & Retrieval (RAG → GraphRAG)

**Goal:** Layer **GraphRAG** over standard RAG for relational sense‑making.

- **Standard RAG:** Vector search over text chunks; cite sources.
- **GraphRAG:**
  - Query → subgraph extraction via BFS/DFS + community detection.
  - Hybrid scoring (text similarity × relational proximity × freshness × role).
  - Cypher/Gremlin queries for precision lookups; cached subgraphs.
- **Agentic Orchestration:** LangGraph workflows for multi‑step research; result pearls written back as `Trail` segments.

**Deliverable:** Ask‑and‑walk experience: a query lights up a corridor of orbs; answers are contextual and cited.

---

## Phase 6 — Collaboration & Presence

**Goal:** Multi‑user co‑navigation and shared trails.

- **Presence:** Avatars/cursors; voice chat zones; handoff tokens for guiding others.
- **Trail Sharing:** Save + publish replayable routes (per‑share RBAC permissions).
- **Annotations:** Sticky notes, highlights; comment threads attach to nodes/edges.

**Deliverable:** Two‑person guided tour through a domain (e.g., Lumo in context) recorded as a shareable pearl.

---

## Phase 7 — Trust, Compliance, and Ops

**Goal:** Production‑grade security, governance, and observability.

- **Security:**
  - Mutual TLS for services; signed URLs for blob fetch; 2FA; IP allow‑lists.
  - Field‑level ACLs; audit events streamed to SIEM.
- **Privacy:** E2E expectations; private‑by‑default nodes; redaction tools.
- **Compliance:** GDPR data map; retention policies; export/delete per subject.
- **Observability:** Tracing (OpenTelemetry), metrics (Prometheus), logs (Loki), alerts (Grafana). 

**Deliverable:** Green security review; runbooks for incidents and backups.

---

## Phase 8 — CI/CD & Performance

**Goal:** Smooth deployments and silky UX.

- **CI/CD:** GitHub Actions; lint, test, container builds; Blue‑Green/Rolling deploys.
- **Perf Budgets:** Initial scene < 2s TTFB (web); < 120k tris visible; batching; lazy hydration.
- **Load Tests:** Graph query p95 < 300ms for 10K nodes; websocket fan‑out under 1s.

**Deliverable:** Automated release pipeline with canary environments.

---

## Data Contracts & Types (excerpt)

```ts
// Node
interface Node { uid: string; type: 'Pearl'|'Artifact'|'Trail'|'Topic'|'Person'|'Portal'|'Obelisk';
  title?: string; summary?: string; tags?: string[]; createdAt: string; updatedAt: string; checksum?: string; blobRef?: string }
// Edge
interface Edge { src: string; dst: string; rel: 'CONTAINS'|'REFERS_TO'|'NEXT'|'DERIVED_FROM'|'OWNS'|'OPEN_PORTAL_TO'; weight?: number; since?: string }
```

---

## Milestones (indicative)

- **M1 (2–3 wks):** Phase 1 complete; GraphQL online; first ingestion.
- **M2 (2 wks):** Phase 2 web explorer live with 3d‑force‑graph.
- **M3 (3–4 wks):** Phase 3 Unity/WebXR prototype demo.
- **M4 (3 wks):** Phase 5 GraphRAG answers with visible subgraphs.
- **M5 (ongoing):** Phases 6–8; security hardening; team onboarding.

---

## Risks & Mitigations

- **Graph scale & layout clutter:** Use community detection, level‑of‑detail, server‑side pruning.
- **VR motion sickness:** Comfort locomotion, snap turns, adjustable vignette.
- **Data privacy leaks:** Strict RBAC, redaction pipeline, private‑by‑default ingestion.
- **Drift between Unity & Web graphs:** Shared schema + rendering adapters; snapshot tests.

---

### Summary

This plan turns the vision into an executable path: **Phase 2 delivers immediate value via 3d‑force‑graph on the web**, Phase 3 delivers the immersive feel, and Phases 4–5 make it intelligent with **GraphRAG**. All of it rides on a secure, trusted backbone aligned with Heather’s ethos.
