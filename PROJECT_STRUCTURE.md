# 📁 Projekt-Struktur

Komplette Dateistruktur des Odoo Electro MongoDB ERP Projekts.

## 🌳 Verzeichnisbaum

```
odoo-electro-mongodb-erp/
│
├── 📄 README.md                          # Haupt-Dokumentation
├── 📄 LICENSE                            # AGPL-3.0 Lizenz
├── 📄 CHANGELOG.md                       # Versionshistorie
├── 📄 CONTRIBUTING.md                    # Beitragsrichtlinien
├── 📄 .gitignore                         # Git Ignore Regeln
├── 📄 .dockerignore                      # Docker Ignore Regeln
├── 📄 docker-compose.yml                 # Docker Orchestrierung
├── 📄 requirements.txt                   # Python Dependencies
├── 📄 pyproject.toml                     # Python Projekt Config
├── 📄 .env.example                       # Umgebungsvariablen Template
│
├── 📁 .github/                           # GitHub Konfiguration
│   ├── 📁 workflows/
│   │   ├── test.yml                     # CI/CD Tests
│   │   └── docker-build.yml             # Docker Build Pipeline
│   ├── 📁 ISSUE_TEMPLATE/
│   │   ├── bug_report.md                # Bug Report Template
│   │   └── feature_request.md           # Feature Request Template
│   └── PULL_REQUEST_TEMPLATE.md         # PR Template
│
├── 📁 electro_erp/                       # 🔥 Haupt-Odoo-Modul
│   ├── __init__.py                      # Modul Init
│   ├── __manifest__.py                  # Odoo Modul Manifest
│   │
│   ├── 📁 models/                        # Datenmodelle (Business Logic)
│   │   ├── __init__.py
│   │   ├── electro_project.py           # Projekt-Modell (inherit project.project)
│   │   ├── electro_offer.py             # Angebotskalkulation
│   │   ├── electro_material.py          # Material & Lagerverwaltung
│   │   ├── electro_material_usage.py    # Material-Verwendung
│   │   ├── employee_skills.py           # Mitarbeiter Skills & Zertifikate
│   │   ├── electro_timesheet.py         # Erweiterte Zeiterfassung
│   │   └── mongodb_integration.py       # MongoDB Integration Service
│   │
│   ├── 📁 controllers/                   # Web-Controller & APIs
│   │   ├── __init__.py
│   │   ├── main.py                      # Haupt Web-Controller
│   │   ├── mongodb_api.py               # REST API für MongoDB
│   │   └── iot_webhook.py               # IoT Webhooks
│   │
│   ├── 📁 views/                         # XML Views (UI)
│   │   ├── electro_menu.xml             # Hauptmenü
│   │   ├── electro_project_views.xml    # Projekt Views (Form, Tree, Kanban)
│   │   ├── electro_offer_views.xml      # Angebots Views
│   │   ├── electro_material_views.xml   # Material Views
│   │   ├── employee_skills_views.xml    # Skills & Zertifikate Views
│   │   ├── mongodb_dashboard_views.xml  # MongoDB Dashboard
│   │   └── electro_templates.xml        # QWeb Templates
│   │
│   ├── 📁 security/                      # Zugriffsrechte & Sicherheit
│   │   ├── electro_security_groups.xml  # Benutzergruppen
│   │   ├── ir.model.access.csv          # Modell-Zugriffsrechte
│   │   └── record_rules.xml             # Datensatz-Regeln
│   │
│   ├── 📁 data/                          # Stammdaten
│   │   ├── demo_data.xml                # Demo-Daten für Tests
│   │   ├── material_categories.xml      # Material-Kategorien
│   │   ├── project_types.xml            # Projekt-Typen
│   │   └── swiss_standards.xml          # CH-Standards (ESTI, SUVA)
│   │
│   ├── 📁 reports/                       # Berichte & Druckvorlagen
│   │   ├── __init__.py
│   │   ├── offer_report.xml             # Angebotsbericht (QWeb)
│   │   ├── project_report.xml           # Projektbericht
│   │   ├── material_report.xml          # Materialbericht
│   │   └── timesheet_report.py          # Zeiterfassung Report
│   │
│   ├── 📁 wizard/                        # Assistenten (Wizards)
│   │   ├── __init__.py
│   │   ├── import_offer_wizard.py       # Import von Angeboten
│   │   ├── import_offer_wizard_views.xml
│   │   ├── export_mongo_wizard.py       # Export nach MongoDB
│   │   ├── export_mongo_wizard_views.xml
│   │   ├── esti_wizard.py               # ESTI-Abnahme Wizard
│   │   └── esti_wizard_views.xml
│   │
│   ├── 📁 static/                        # Frontend Assets
│   │   ├── 📁 description/
│   │   │   ├── icon.png                 # Modul Icon (128x128)
│   │   │   ├── banner.png               # Banner für Store
│   │   │   └── index.html               # Modul-Beschreibung
│   │   ├── 📁 img/                       # UI Bilder
│   │   │   ├── logo.png
│   │   │   └── placeholder.png
│   │   └── 📁 src/
│   │       ├── 📁 js/                    # JavaScript
│   │       │   ├── mongodb_widget.js    # Custom Widget
│   │       │   └── iot_dashboard.js     # IoT Dashboard JS
│   │       └── 📁 css/                   # Stylesheets
│   │           └── electro_erp.css      # Custom Styles
│   │
│   ├── 📁 i18n/                          # Übersetzungen
│   │   ├── de.po                        # Deutsch (Hauptsprache)
│   │   ├── fr.po                        # Französisch
│   │   ├── it.po                        # Italienisch
│   │   └── en.po                        # Englisch
│   │
│   └── 📁 tests/                         # Unit Tests (Odoo-spezifisch)
│       ├── __init__.py
│       ├── test_electro_project.py
│       ├── test_mongodb_integration.py
│       └── common.py                    # Test Utilities
│
├── 📁 mongodb/                           # MongoDB Konfiguration
│   ├── init.js                          # DB Initialisierung
│   ├── indexes.js                       # Index-Definition
│   ├── sample_data.json                 # Beispieldaten
│   └── backup_script.sh                 # Backup-Skript
│
├── 📁 docker/                            # Docker Konfiguration
│   ├── Dockerfile.odoo                  # Custom Odoo Image
│   ├── Dockerfile.mongodb               # Custom MongoDB Image (optional)
│   ├── entrypoint.sh                    # Container Startskript
│   └── odoo.conf                        # Odoo Konfiguration
│
├── 📁 docs/                              # Dokumentation
│   ├── index.md                         # Doku Hauptseite
│   ├── installation.md                  # Installation Guide
│   ├── 📁 user-guide/                    # Benutzerhandbuch
│   │   ├── getting-started.md           # Erste Schritte
│   │   ├── project-management.md        # Projektmanagement
│   │   ├── offer-calculation.md         # Angebotskalkulation
│   │   ├── material-management.md       # Materialwirtschaft
│   │   ├── mongodb-integration.md       # MongoDB Features
│   │   └── swiss-compliance.md          # ESTI & SUVA
│   └── 📁 developer/                     # Entwickler-Doku
│       ├── architecture.md              # Systemarchitektur
│       ├── api-reference.md             # API Dokumentation
│       ├── database-schema.md           # Datenbankschema
│       ├── extending.md                 # Erweiterungen entwickeln
│       └── testing.md                   # Testing Guide
│
├── 📁 tests/                             # Integration & E2E Tests
│   ├── __init__.py
│   ├── conftest.py                      # Pytest Konfiguration
│   ├── test_electro_models.py           # Model Tests
│   ├── test_mongodb_integration.py      # MongoDB Tests
│   ├── test_api_endpoints.py            # API Tests
│   ├── test_workflows.py                # Workflow Tests
│   └── fixtures/                        # Test Fixtures
│       ├── sample_project.json
│       └── sample_materials.csv
│
├── 📁 scripts/                           # Hilfsskripte
│   ├── setup_dev_env.sh                 # Dev Environment Setup
│   ├── import_sample_data.py            # Daten Import
│   ├── backup_mongodb.sh                # MongoDB Backup
│   ├── restore_mongodb.sh               # MongoDB Restore
│   ├── update_translations.sh           # i18n Update
│   └── deploy_production.sh             # Production Deploy
│
└── 📁 config/                            # Konfigurationsdateien
    ├── odoo.conf                        # Odoo Produktiv-Config
    ├── odoo-dev.conf                    # Odoo Dev-Config
    └── logging.conf                     # Logging-Config
```

## 📋 Datei-Beschreibungen

### Core Files

| Datei | Beschreibung |
|-------|--------------|
| `__manifest__.py` | Odoo Modul-Metadaten, Dependencies, Datenfiles |
| `docker-compose.yml` | Definiert alle Services (Odoo, PostgreSQL, MongoDB) |
| `requirements.txt` | Python Abhängigkeiten (pymongo, fastapi, etc.) |

### Models (Business Logic)

| Datei | Zweck |
|-------|-------|
| `electro_project.py` | Hauptmodell für Elektroprojekte, inherit von project.project |
| `electro_offer.py` | Angebotskalkulation mit CH-Standards |
| `electro_material.py` | Materialverwaltung, Lager, Preise |
| `employee_skills.py` | Skills-Management, ESTI/SUVA Zertifikate |
| `mongodb_integration.py` | Abstract Model für MongoDB CRUD Operations |

### Views (User Interface)

| Datei | UI-Komponenten |
|-------|----------------|
| `electro_project_views.xml` | Form, Tree, Kanban Views für Projekte |
| `mongodb_dashboard_views.xml` | Dashboard für IoT-Daten und Dokumente |
| `electro_menu.xml` | Hauptmenü-Struktur |

### Security

| Datei | Funktion |
|-------|----------|
| `electro_security_groups.xml` | Definiert Benutzergruppen (Admin, Manager, Monteur) |
| `ir.model.access.csv` | CRUD-Rechte pro Gruppe und Modell |
| `record_rules.xml` | Row-Level Security Rules |

### MongoDB

| Datei | Zweck |
|-------|-------|
| `init.js` | Erstellt Collections, Indexes, Demo-Daten |
| `indexes.js` | Performance-Indexes für Queries |

## 🎯 Wichtigste Dateien für den Start

1. **README.md** - Projektübersicht und Quick Start
2. **docker-compose.yml** - Starte mit `docker-compose up`
3. **__manifest__.py** - Odoo Modul-Definition
4. **electro_project.py** - Hauptmodell mit MongoDB Integration
5. **mongodb/init.js** - MongoDB Setup

## 🔄 Workflow: Neue Datei hinzufügen

### Neues Model:
```bash
# 1. Model erstellen
touch electro_erp/models/mein_model.py

# 2. In __init__.py registrieren
echo "from . import mein_model" >> electro_erp/models/__init__.py

# 3. View erstellen
touch electro_erp/views/mein_model_views.xml

# 4. In __manifest__.py eintragen
# data: ['views/mein_model_views.xml']

# 5. Security definieren
# Zeile in ir.model.access.csv hinzufügen
```

### Neuer Test:
```bash
# 1. Test-Datei erstellen
touch tests/test_mein_feature.py

# 2. Test schreiben
# 3. Ausführen
docker-compose exec odoo pytest tests/test_mein_feature.py
```

## 📦 Dateigrößen-Richtlinien

- **Models**: 200-500 Zeilen pro Datei
- **Views**: Separate XML für Form/Tree/Kanban
- **Tests**: Eine Test-Datei pro Model
- **Docs**: Markdown, max 500 Zeilen, dann aufteilen

## 🚀 Build-Artefakte

Werden von `.gitignore` ignoriert:
- `__pycache__/`
- `*.pyc`
- `filestore/`
- `sessions/`
- `.odoo_history`
- Docker volumes

---

**Aktualisiert:** 2024-12-06
