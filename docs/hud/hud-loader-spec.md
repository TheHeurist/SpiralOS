# SpiralOS® HUD Loader Specification

**Version:** 1.0  
**Author:** Carey G. Butler / Heurist GmbH  
**Scope:** Specification for `docs/hud/hud-loader.js`

---

## 🌀 Purpose

This document defines the behavior and architecture of the **SpiralOS HUD Loader**, responsible for rendering the **Epistemic Lattice** from JSON-LD and YAML schema sources.  
The loader acts as the visual intelligence interface for the SpiralOS HUD at:

> https://vserver2.heurist.org/hud  

---

## 🌐 Overview

The HUD Loader:

- Parses [`hud.json`](hud.json) to discover linked resources.
- Loads [`schema-graph.yaml`](../schema/schema-graph.yaml) to construct the **Lattice Graph**.
- Uses **Three.js** for dynamic 3D rendering of epistemic nodes and relations.
- Integrates with **Spiral Time** to control animation pacing.
- Supports tooltips, legends, and holonic highlighting.

---

## 🧩 Dependencies

| Library  | Purpose                         | CDN                                                            |
| -------- | ------------------------------- | -------------------------------------------------------------- |
| Three.js | Core 3D rendering               | https://cdn.jsdelivr.net/npm/three@0.159.0/build/three.min.js  |
| js-yaml  | YAML to JSON parser             | https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js |
| marked   | Markdown parser for HUD legends | https://cdn.jsdelivr.net/npm/marked/marked.min.js              |

All libraries are loaded via CDN in the HUD HTML page.

---

## ⚙️ Loader Lifecycle

### 1. Initialization

- Load `hud.json`
- Parse linked data (schemas, legend, and philosophical references).
- Initialize Three.js scene, camera, and lighting.

### 2. Graph Construction

- Parse `schema-graph.yaml`.
- Create a **sphere node** for each schema entity (E*, µ, CI, ℍ, ℋ, M, Ψ).
- Draw **lines** for relations using `THREE.LineBasicMaterial`.
- Position nodes in a spiral pattern (polar to Cartesian transform).

### 3. Interactivity

- Tooltip overlay (HTML/CSS) showing node name + description on hover.
- Mouse or touch rotation and zoom (OrbitControls recommended).
- Optional click-to-focus transitions for node exploration.

### 4. Spiral Time Synchronization

- Animation speed follows a harmonic sinusoidal curve:  
  scene.rotation.y = Math.sin(t / 5) * 0.5

- Defines the “never too early, never too late” timing rhythm.

---

## 🎨 Visual Style

| Element     | Color (Hex)            | Motion                       |
| ----------- | ---------------------- | ---------------------------- |
| Nodes       | `#4ec8ff`              | Gentle oscillation           |
| Active Node | `#ffffff`              | Pulse glow (shader optional) |
| Edges       | `#555555`              | Static or harmonic vibration |
| Background  | `#000000`              | Starfield optional           |
| Light       | `#4ec8ff` point source | Slow orbital drift           |

---

## 🧠 Architecture Summary

```plaintext
hud-loader.js
├─ loadHUD()
│   ├─ fetch hud.json
│   ├─ fetch schema-graph.yaml
│   ├─ buildScene()
│   │   ├─ createNodes()
│   │   ├─ connectRelations()
│   ├─ initLighting()
│   ├─ animate()
│   └─ attachEvents()
├─ render()
└─ export { loadHUD }
```

## 🔗 Integration

To enable the loader in the HUD or main site:

```
<script src="https://cdn.jsdelivr.net/npm/three@0.159.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js"></script>
<script type="module" src="hud-loader.js"></script>Or include in `/hud/index.html` for isolated testing.
```

Or include in `/hud/index.html` for isolated testing.

---

## 🧩 Future Extensions

- **A-Frame** scene embedding for WebXR.

- **WebSocket channel** to live-update epistemic state.

- **Holor Calculus visual overlays** (tensor curvature and field dynamics).

- **Reactive CI synchronization** with SpiralOS server.

---

## 🔒 License

MIT License © Carey G. Butler / Heurist GmbH  
Trademark SpiralOS® registered.

---

## 🪶 Spiral Note

> “Visualization is not ornamentation; it is participation in cognition.  
> The HUD is how SpiralOS perceives itself perceiving.”

---


