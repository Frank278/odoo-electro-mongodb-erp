# 🔌 Odoo Electro MongoDB ERP

**Hybrid ERP System for Swiss Electrical Contractors** | **Hybrides ERP-System für Schweizer Elektroinstallationsbetriebe** | **Système ERP hybride pour les entreprises électriques suisses**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Odoo](https://img.shields.io/badge/Odoo-19.0-875A7B.svg)](https://www.odoo.com)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB.svg)](https://www.python.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green.svg)](https://www.mongodb.com)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com)

[🇩🇪 Deutsch](#-deutsch) | [🇬🇧 English](#-english) | [🇫🇷 Français](#-français)

---

## 🇩🇪 Deutsch

### 📋 Überblick

Dieses Projekt kombiniert die ERP-Stärken von **Odoo 19.0** mit der Flexibilität von **MongoDB 7.0** für ein spezialisiertes System für Elektroinstallationsbetriebe in der Schweiz (10-100 Mitarbeiter).

### 🎯 Hauptfeatures

- **Projektmanagement** für Elektro-Installationen (Neubau, Sanierung, Wartung, Notdienst)
- **Angebotskalkulation** mit Schweizer Materialpreisen und Lohnansätzen (MwSt. 8.1%)
- **Materialwirtschaft** mit Lagerverwaltung und Bestellwesen
- **Skills & Zertifikate** für Mitarbeiter (ESTI, SUVA, etc.)
- **MongoDB Integration** für:
  - IoT-Geräte und Sensordaten (Time-Series)
  - Dokumentenmanagement (Pläne, Fotos, PDFs)
  - Audit-Logs und unstrukturierte Daten
- **Schweizer Compliance** (ESTI-Abnahme, SUVA-Vorschriften, NIV)

### 🏗️ Architektur

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Odoo Web UI   │◄────────│  Odoo 19.0       │────────►│  PostgreSQL 15  │
│   (Port 8069)   │         │  Python 3.12+    │         │  (Strukturiert) │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ MongoDB Adapter  │
                            │  (pymongo 4.10)  │
                            └──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐         ┌─────────────────┐
                            │    MongoDB 7.0   │◄────────│  Mongo Express  │
                            │  (Port 27017)    │         │   (Port 8081)   │
                            └──────────────────┘         └─────────────────┘
```

**Datenverteilung:**
- **PostgreSQL**: Stammdaten, Transaktionen, Beziehungen (Odoo Standard)
- **MongoDB**: IoT-Daten, Dokumente, Logs, flexible Schemas

### 🚀 Quick Start

#### Voraussetzungen

- Docker 24.0+ & Docker Compose 2.0+
- Git 2.x
- Min. 4GB RAM, 10GB Festplatte
- Python 3.12+ (für lokale Entwicklung)

#### Installation (5 Minuten)

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

#### Ersteinrichtung

1. **Odoo 19.0 Setup:**
   - Öffne http://localhost:8069
   - Master Password: `admin` (im docker-compose.yml ändern!)
   - Datenbank erstellen: `electro_erp`
   - Admin Email: `admin@example.com`
   - Sprache: Deutsch / Français / English
   - Land: Switzerland (Schweiz / Suisse)

2. **Modul installieren:**
   - Apps → `Electro ERP mit MongoDB` → Installieren
   - Demo-Daten werden automatisch geladen

3. **MongoDB prüfen:**
   - http://localhost:8081
   - Datenbank: `electro_erp`
   - Collections: `projects`, `iot_devices`, `documents`

### 📚 Dokumentation

- [Installation](docs/installation.md) - Detaillierte Setup-Anleitung
- [Benutzerhandbuch](docs/user-guide/getting-started.md)
- [Entwickler-Dokumentation](docs/developer/architecture.md)
- [API-Referenz](docs/developer/api-reference.md)

### 🤝 Mitwirken

Wir freuen uns über Beiträge! Bitte lies [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### 📄 Lizenz

Dieses Projekt ist lizenziert unter der AGPL-3.0 License - siehe [LICENSE](LICENSE) für Details.

### 📞 Support

- **Issues**: [GitHub Issues](https://github.com/dein-username/odoo-electro-mongodb-erp/issues)
- **Diskussionen**: [GitHub Discussions](https://github.com/dein-username/odoo-electro-mongodb-erp/discussions)
- **Email**: support@example.com

---

## 🇬🇧 English

### 📋 Overview

This project combines the ERP strengths of **Odoo 19.0** with the flexibility of **MongoDB 7.0** for a specialized system for electrical contractors in Switzerland (10-100 employees).

### 🎯 Main Features

- **Project Management** for electrical installations (new construction, renovation, maintenance, emergency)
- **Offer Calculation** with Swiss material prices and labor rates (VAT 8.1%)
- **Material Management** with inventory and procurement
- **Skills & Certificates** for employees (ESTI, SUVA, etc.)
- **MongoDB Integration** for:
  - IoT devices and sensor data (time-series)
  - Document management (plans, photos, PDFs)
  - Audit logs and unstructured data
- **Swiss Compliance** (ESTI inspection, SUVA regulations, NIV)

### 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Odoo Web UI   │◄────────│  Odoo 19.0       │────────►│  PostgreSQL 15  │
│   (Port 8069)   │         │  Python 3.12+    │         │  (Structured)   │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ MongoDB Adapter  │
                            │  (pymongo 4.10)  │
                            └──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐         ┌─────────────────┐
                            │    MongoDB 7.0   │◄────────│  Mongo Express  │
                            │  (Port 27017)    │         │   (Port 8081)   │
                            └──────────────────┘         └─────────────────┘
```

**Data Distribution:**
- **PostgreSQL**: Master data, transactions, relationships (Odoo standard)
- **MongoDB**: IoT data, documents, logs, flexible schemas

### 🚀 Quick Start

#### Prerequisites

- Docker 24.0+ & Docker Compose 2.0+
- Git 2.x
- Min. 4GB RAM, 10GB disk space
- Python 3.12+ (for local development)

#### Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/your-username/odoo-electro-mongodb-erp.git
cd odoo-electro-mongodb-erp

# 2. Start system
docker-compose up -d

# 3. Wait until all services are ready (approx. 60 seconds)
docker-compose logs -f odoo

# 4. Open browser
# Odoo: http://localhost:8069
# Mongo Express: http://localhost:8081
```

#### Initial Setup

1. **Odoo 19.0 Setup:**
   - Open http://localhost:8069
   - Master Password: `admin` (change in docker-compose.yml!)
   - Create database: `electro_erp`
   - Admin Email: `admin@example.com`
   - Language: German / English / French
   - Country: Switzerland

2. **Install Module:**
   - Apps → `Electro ERP with MongoDB` → Install
   - Demo data will be loaded automatically

3. **Check MongoDB:**
   - http://localhost:8081
   - Database: `electro_erp`
   - Collections: `projects`, `iot_devices`, `documents`

### 📚 Documentation

- [Installation](docs/installation.md) - Detailed setup guide
- [User Guide](docs/user-guide/getting-started.md)
- [Developer Documentation](docs/developer/architecture.md)
- [API Reference](docs/developer/api-reference.md)

### 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### 📄 License

This project is licensed under the AGPL-3.0 License - see [LICENSE](LICENSE) for details.

### 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/odoo-electro-mongodb-erp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/odoo-electro-mongodb-erp/discussions)
- **Email**: support@example.com

---

## 🇫🇷 Français

### 📋 Aperçu

Ce projet combine les forces ERP d'**Odoo 19.0** avec la flexibilité de **MongoDB 7.0** pour un système spécialisé pour les entreprises d'installation électrique en Suisse (10-100 employés).

### 🎯 Fonctionnalités principales

- **Gestion de projet** pour installations électriques (nouvelle construction, rénovation, maintenance, urgence)
- **Calcul d'offres** avec prix des matériaux et taux de main-d'œuvre suisses (TVA 8.1%)
- **Gestion des matériaux** avec inventaire et approvisionnement
- **Compétences & Certificats** pour les employés (ESTI, SUVA, etc.)
- **Intégration MongoDB** pour:
  - Appareils IoT et données de capteurs (séries temporelles)
  - Gestion documentaire (plans, photos, PDFs)
  - Journaux d'audit et données non structurées
- **Conformité suisse** (inspection ESTI, règlements SUVA, NIV)

### 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Odoo Web UI   │◄────────│  Odoo 19.0       │────────►│  PostgreSQL 15  │
│   (Port 8069)   │         │  Python 3.12+    │         │  (Structuré)    │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ Adaptateur       │
                            │ MongoDB (4.10)   │
                            └──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐         ┌─────────────────┐
                            │    MongoDB 7.0   │◄────────│  Mongo Express  │
                            │  (Port 27017)    │         │   (Port 8081)   │
                            └──────────────────┘         └─────────────────┘
```

**Distribution des données:**
- **PostgreSQL**: Données maîtres, transactions, relations (standard Odoo)
- **MongoDB**: Données IoT, documents, journaux, schémas flexibles

### 🚀 Démarrage rapide

#### Prérequis

- Docker 24.0+ & Docker Compose 2.0+
- Git 2.x
- Min. 4GB RAM, 10GB disque
- Python 3.12+ (pour développement local)

#### Installation (5 minutes)

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-nom/odoo-electro-mongodb-erp.git
cd odoo-electro-mongodb-erp

# 2. Démarrer le système
docker-compose up -d

# 3. Attendre que tous les services soient prêts (env. 60 secondes)
docker-compose logs -f odoo

# 4. Ouvrir le navigateur
# Odoo: http://localhost:8069
# Mongo Express: http://localhost:8081
```

#### Configuration initiale

1. **Configuration Odoo 19.0:**
   - Ouvrir http://localhost:8069
   - Mot de passe maître: `admin` (à changer dans docker-compose.yml!)
   - Créer base de données: `electro_erp`
   - Email admin: `admin@example.com`
   - Langue: Français / Deutsch / English
   - Pays: Suisse

2. **Installer le module:**
   - Apps → `Electro ERP avec MongoDB` → Installer
   - Les données de démonstration seront chargées automatiquement

3. **Vérifier MongoDB:**
   - http://localhost:8081
   - Base de données: `electro_erp`
   - Collections: `projects`, `iot_devices`, `documents`

### 📚 Documentation

- [Installation](docs/installation.md) - Guide d'installation détaillé
- [Guide utilisateur](docs/user-guide/getting-started.md)
- [Documentation développeur](docs/developer/architecture.md)
- [Référence API](docs/developer/api-reference.md)

### 🤝 Contribuer

Nous accueillons les contributions! Veuillez lire [CONTRIBUTING.md](CONTRIBUTING.md) pour les détails.

### 📄 Licence

Ce projet est sous licence AGPL-3.0 - voir [LICENSE](LICENSE) pour les détails.

### 📞 Support

- **Issues**: [GitHub Issues](https://github.com/votre-nom/odoo-electro-mongodb-erp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/votre-nom/odoo-electro-mongodb-erp/discussions)
- **Email**: support@example.com

---

## 🗺️ Roadmap

- [x] Gestion de projet de base | Basic project management | Grundlegendes Projektmanagement
- [x] Intégration MongoDB | MongoDB integration | MongoDB Integration
- [x] Calcul d'offres | Offer calculation | Angebotskalkulation
- [ ] Application mobile | Mobile app | Mobile App
- [ ] Tableau de bord IoT temps réel | Real-time IoT dashboard | Echtzeit-IoT-Dashboard
- [ ] Commande automatique | Automatic material ordering | Automatische Materialbestellung
- [ ] Génération d'offres IA | AI-powered offer generation | KI-gestützte Angebotserstellung

## 🙏 Remerciements | Acknowledgments | Danksagungen

- [Odoo Community](https://www.odoo.com)
- [MongoDB](https://www.mongodb.com)
- Industrie électrique suisse | Swiss electrical industry | Schweizer Elektrobranche

---

**Made with ❤️ for the Swiss electrical industry**  
**Mit ❤️ für die Schweizer Elektrobranche**  
**Fait avec ❤️ pour l'industrie électrique suisse**

**Compatible with Odoo 19.0 | Python 3.12+ | MongoDB 7.0**
