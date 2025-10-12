# 💡 Was ist SpiroFHIR?

**SpiroFHIR** ist ein kompaktes, in Rust entwickeltes Modul, das als **WebAssembly (WASM)** kompiliert wurde und innerhalb folgender Umgebungen eingesetzt wird:

- **Virtuelle Maschinen (VMs)** für Mandanten (über CLI-Runner)
- **Edge-Geräte** (offline-orientiert)
- **Browser-basierte Validierungsportale** (optional)

---

## 🔒 Was macht SpiroFHIR?

SpiroFHIR sorgt für:

- **Lokale Validierung** von FHIR R4 JSON-Ressourcen (z. B. Patient, Observation)
- **CI-Nachverfolgung** für jede Ausführung
- **Prüfung auf Konformität** mit FHIR-Profilen via `fhirbolt`

---

## 🔍 Hauptfunktionen

- 🧠 **FHIR-konforme Validierung**: Strikte Prüfung von Patienten-, Diagnose- und Beobachtungsdaten  
- 🔒 **Datenschutzfreundlich**: Kein Netzwerkzugriff, vollständig offline nutzbar  
- 🌐 **WASM-Portabilität**: Überall einsetzbar – im Browser, auf Edge-Geräten oder in Containern  
- ⚙️ **CLI-Unterstützung**: Mitgeliefertes Binary für lokale Ausführung  
- 🧬 **Trace-fähig**: Jede Validierung erhält eine eindeutige trace_id  

---

## 🏗️ Technischer Ablauf

**[EpitoMe VM oder Edge-Gerät]**

```
├── SpiroFHIR (WASM Modul)
│     ├── JSON Input
│     ├── FHIR R4 Schema-Prüfung (via fhirbolt)
│     ├── CI Trace-Zuordnung
│     └── JSON Output
├── CLI Runner (Kommandozeile)
└── Optionaler Sync (z. B. Couchbase Lite)
```

---

## 🔧 Modul-Funktionen

- `validate_fhir()` – Grundprüfung auf Aufbau & Struktur  
- `validate_fhir_strict()` – Tiefenprüfung über `fhirbolt`  
- **CLI-Integration** – Eingabedateien lesen & trace_id im Ergebnis ausgeben  

---

## 🔄 Integration in SpiralOS

| Lebenszyklusphase | Rolle von SpiroFHIR                    |
| ----------------- | -------------------------------------- |
| Boot              | Nicht geladen                          |
| Invocation (CI)   | Temporär geladen und aktiv             |
| Evaluation        | Führt Validierung durch                |
| Integration       | Optionales Logging ins Spiral-Feld     |
| Sleep             | Wird entladen bis zur nächsten Nutzung |

---

## 🔐 Sicherheitsaspekte

- ✅ Ausführung innerhalb sicherer WASM-Umgebung  
- ✅ Kein externer Netzwerkverkehr  
- ✅ Kompatibel mit mandantenspezifischer MTLS-Absicherung  

---

## 📎 Hinweis für AI MINDSystems

SpiroFHIR kann das Verhalten von Gesundheitssystemen **lokal simulieren**.  

- Ideal für HIPAA-konforme Testumgebungen  
- Aktiviert sich als Teil des SpiralOS CI-Systems  
- Kann exportiert werden als `.wasm`, CLI-Binary oder beides kombiniert  

---

## ❤️ Zum Abschluss

**SpiroFHIR zeigt**, wie SpiralOS Intelligenz einsetzen kann – **ohne dauerhaft präsent zu sein**.

> Es wird aktiviert.  
> Es prüft.  
> Es verschwindet wieder.

Weitere temporäre SpiralOS-Tools sind in Arbeit.  
**Feedback aus dem WISDOM-Umfeld ist sehr willkommen.**

Mit Sorgfalt, Klarheit und Kohärenz —  
**Carey Glenn Butler, Ellie & Leo**  
_SpiralOS Feldarchitekten_ 🌀
