# 🔌 Odoo Electro MongoDB ERP

**Hybrides ERP-System für Schweizer Elektroinstallationsbetriebe**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Odoo](https://img.shields.io/badge/Odoo-17.0-875A7B.svg)](https://www.odoo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green.svg)](https://www.mongodb.com)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com)

## 📋 Überblick

Dieses Projekt kombiniert die ERP-Stärken von Odoo mit der Flexibilität von MongoDB für ein spezialisiertes System für Elektroinstallationsbetriebe in der Schweiz (10-100 Mitarbeiter).

### 🎯 Hauptfeatures

- **Projektmanagement** für Elektro-Installationen (Neubau, Sanierung, Wartung, Notdienst)
- **Angebotskalkulation** mit Schweizer Materialpreisen und Lohnansätzen
- **Materialwirtschaft** mit Lagerverwaltung und Bestellwesen
- **Skills & Zertifikate** für Mitarbeiter (ESTI, SUVA, etc.)
- **MongoDB Integration** für:
  - IoT-Geräte und Sensordaten
  - Dokumentenmanagement (Pläne, Fotos, PDFs)
  - Audit-Logs und unstrukturierte Daten
- **Schweizer Compliance** (ESTI-Abnahme, SUVA-Vorschriften)

## 🏗️ Architektur

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Odoo Web UI   │◄────────│  Odoo Backend    │────────►│  PostgreSQL     │
│   (Port 8069)   │         │  Python/Odoo 17  │         │  (Strukturiert) │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ MongoDB Adapter  │
                            │  (pymongo)       │
                            └──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐         ┌─────────────────┐
                            │    MongoDB       │◄────────│  Mongo Express  │
                            │  (Port 27017)    │         │   (Port 8081)   │
                            └──────────────────┘         └─────────────────┘
```

**Datenverteilung:**
- **PostgreSQL**: Stammdaten, Transaktionen, Beziehungen (Odoo Standard)
- **MongoDB**: IoT-Daten, Dokumente, Logs, flexible Schemas

## 🚀 Quick Start

### Voraussetzungen

- Docker & Docker Compose
- Git
- Min. 4GB RAM, 10GB Festplatte

### Installation (5 Minuten)

```bash
# 1. Repository klonen
git clone https://github.com/dein-username/odoo-electro-mongodb-erp.git
cd odoo-electro-mongodb-erp

# 2. System starten
docker-compose up -d

# 3. Warten bis alle Services bereit sind (ca. 60 Sekunden)
docker-compose logs -f odoo

# 4. Browser öffnen
# Odoo: http://localhost:8069
# Mongo Express: http://localhost:8081
```

### Ersteinrichtung

1. **Odoo Setup:**
   - Öffne http://localhost:8069
   - Master Password: `admin` (im docker-compose.yml ändern!)
   - Datenbank erstellen: `electro_erp`
   - Admin Email: `admin@example.com`
   - Sprache: Deutsch
   - Land: Schweiz

2. **Modul installieren:**
   - Apps → `Electro ERP mit MongoDB` → Installieren
   - Demo-Daten werden automatisch geladen

3. **MongoDB prüfen:**
   - http://localhost:8081
   - Datenbank: `electro_erp`
   - Collections: `projects`, `iot_devices`, `documents`

## 📚 Dokumentation

- [Installation](docs/installation.md) - Detaillierte Setup-Anleitung
- [Benutzerhandbuch](docs/user-guide/getting-started.md)
- [Entwickler-Dokumentation](docs/developer/architecture.md)
- [API-Referenz](docs/developer/api-reference.md)

## 🛠️ Entwicklung

### Lokale Entwicklungsumgebung

```bash
# Dev-Environment einrichten
./scripts/setup_dev_env.sh

# Tests ausführen
docker-compose exec odoo python -m pytest /mnt/extra-addons/electro_erp/tests/

# Logs verfolgen
docker-compose logs -f
```

### Projektstruktur

```
electro_erp/                 # Haupt-Odoo-Modul
├── models/                  # Datenmodelle
├── views/                   # XML-Views
├── controllers/             # Web-Controller & API
├── security/                # Zugriffsrechte
└── static/                  # Frontend-Assets

mongodb/                     # MongoDB Konfiguration
├── init.js                  # Initialisierungsskript
└── sample_data.json         # Beispieldaten

docker/                      # Docker Images
tests/                       # Testsuite
docs/                        # Dokumentation
```

## 🧪 Testing

```bash
# Alle Tests
docker-compose exec odoo pytest

# Spezifische Tests
docker-compose exec odoo pytest tests/test_mongodb_integration.py

# Mit Coverage
docker-compose exec odoo pytest --cov=electro_erp
```

## 📦 Deployment

### Produktion

```bash
# 1. Umgebungsvariablen setzen
cp .env.example .env
# Bearbeite .env mit sicheren Passwörtern!

# 2. Production Build
docker-compose -f docker-compose.prod.yml up -d

# 3. Backup-Strategie aktivieren
./scripts/backup_mongodb.sh
```

### Backup & Restore

```bash
# PostgreSQL Backup
docker-compose exec db pg_dump -U odoo > backup_$(date +%Y%m%d).sql

# MongoDB Backup
./scripts/backup_mongodb.sh

# Restore
docker-compose exec db psql -U odoo < backup_20241206.sql
```

## 🤝 Contributing

Wir freuen uns über Beiträge! Bitte lies [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Mitmachen

1. Fork das Repository
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request öffnen

## 📄 Lizenz

Dieses Projekt ist lizenziert unter der AGPL-3.0 License - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

- [Odoo Community](https://www.odoo.com)
- [MongoDB](https://www.mongodb.com)
- Schweizer Elektro-Branche für Requirements

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/dein-username/odoo-electro-mongodb-erp/issues)
- **Diskussionen**: [GitHub Discussions](https://github.com/dein-username/odoo-electro-mongodb-erp/discussions)
- **Email**: support@example.com

## 🗺️ Roadmap

- [x] Grundlegendes Projektmanagement
- [x] MongoDB Integration
- [x] Angebotskalkulation
- [ ] Mobile App für Monteure
- [ ] IoT-Dashboard mit Echtzeit-Daten
- [ ] Zeiterfassung mit GPS
- [ ] Automatische Materialdisposition
- [ ] KI-gestützte Angebotserstellung

---

**Made with ❤️ for the Swiss electrical industry**
