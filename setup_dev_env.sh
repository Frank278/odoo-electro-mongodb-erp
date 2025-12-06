#!/bin/bash

# Electro ERP Development Environment Setup Script
# ================================================
# Automatisiert das Setup der Entwicklungsumgebung

set -e  # Exit bei Fehler

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║   🔌 Electro ERP Development Environment Setup       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Funktion für Status-Meldungen
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Prüfe Voraussetzungen
print_status "Prüfe Voraussetzungen..."

# Docker prüfen
if ! command -v docker &> /dev/null; then
    print_error "Docker ist nicht installiert!"
    echo "Bitte installiere Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
print_success "Docker gefunden: $(docker --version)"

# Docker Compose prüfen
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose ist nicht installiert!"
    echo "Bitte installiere Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
print_success "Docker Compose gefunden: $(docker-compose --version)"

# Git prüfen
if ! command -v git &> /dev/null; then
    print_warning "Git ist nicht installiert (empfohlen für Entwicklung)"
else
    print_success "Git gefunden: $(git --version)"
fi

# Python prüfen (optional für lokale Tests)
if command -v python3 &> /dev/null; then
    print_success "Python3 gefunden: $(python3 --version)"
else
    print_warning "Python3 nicht gefunden (für lokale Tests empfohlen)"
fi

echo ""
print_status "Alle Voraussetzungen erfüllt!"
echo ""

# Verzeichnisstruktur erstellen
print_status "Erstelle Verzeichnisstruktur..."

# Hauptverzeichnisse
mkdir -p electro_erp/{models,views,controllers,security,data,reports,static/{description,img,src/{js,css}},wizard,i18n,tests}
mkdir -p mongodb
mkdir -p docker
mkdir -p docs/{user-guide,developer}
mkdir -p tests
mkdir -p scripts
mkdir -p config
mkdir -p logs
mkdir -p .github/{workflows,ISSUE_TEMPLATE}

print_success "Verzeichnisstruktur erstellt"

# __init__.py Dateien erstellen
print_status "Erstelle __init__.py Dateien..."

touch electro_erp/__init__.py
touch electro_erp/models/__init__.py
touch electro_erp/controllers/__init__.py
touch electro_erp/reports/__init__.py
touch electro_erp/wizard/__init__.py
touch tests/__init__.py

print_success "__init__.py Dateien erstellt"

# Beispiel .env Datei erstellen
print_status "Erstelle .env.example..."

cat > .env.example << 'EOF'
# Electro ERP Environment Variables
# ==================================
# Kopiere diese Datei nach .env und passe die Werte an

# PostgreSQL
POSTGRES_DB=postgres
POSTGRES_USER=odoo
POSTGRES_PASSWORD=changeme_secure_password

# MongoDB
MONGODB_URI=mongodb://mongodb:27017/electro_erp
MONGODB_DB=electro_erp

# Odoo
ODOO_ADMIN_PASSWORD=changeme_admin_password
ODOO_WORKERS=2

# Mongo Express
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=changeme_admin_password
EOF

print_success ".env.example erstellt"

# Prüfe ob .env existiert
if [ ! -f .env ]; then
    print_warning ".env nicht gefunden - kopiere von .env.example"
    cp .env.example .env
    print_success ".env erstellt (ACHTUNG: Passwörter ändern!)"
else
    print_warning ".env existiert bereits - nicht überschrieben"
fi

# Docker Images pullen
print_status "Lade Docker Images (kann einige Minuten dauern)..."

docker pull postgres:15-alpine
docker pull mongo:7.0
docker pull mongo-express:latest
docker pull odoo:17.0

print_success "Docker Images geladen"

# Docker Network erstellen
print_status "Erstelle Docker Network..."
docker network create electro_network 2>/dev/null || print_warning "Network existiert bereits"

# Erste Docker Container starten
print_status "Starte Docker Container..."
print_warning "Dies kann beim ersten Mal 2-3 Minuten dauern..."

docker-compose up -d

# Warte bis Services bereit sind
print_status "Warte auf Service-Bereitschaft..."

# Warte auf PostgreSQL
print_status "Warte auf PostgreSQL..."
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U odoo &> /dev/null; then
        print_success "PostgreSQL ist bereit"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "PostgreSQL Timeout"
        exit 1
    fi
    sleep 2
done

# Warte auf MongoDB
print_status "Warte auf MongoDB..."
for i in {1..30}; do
    if docker-compose exec -T mongodb mongosh --eval "db.runCommand({ ping: 1 })" &> /dev/null; then
        print_success "MongoDB ist bereit"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "MongoDB Timeout"
        exit 1
    fi
    sleep 2
done

# Warte auf Odoo
print_status "Warte auf Odoo (kann 60-90 Sekunden dauern)..."
for i in {1..60}; do
    if curl -s http://localhost:8069/web/database/selector &> /dev/null; then
        print_success "Odoo ist bereit"
        break
    fi
    if [ $i -eq 60 ]; then
        print_warning "Odoo Timeout - möglicherweise noch am Starten"
    fi
    sleep 2
done

# Python Abhängigkeiten installieren (falls Python lokal verfügbar)
if command -v python3 &> /dev/null && command -v pip3 &> /dev/null; then
    print_status "Installiere Python Abhängigkeiten..."
    pip3 install -r requirements.txt --quiet || print_warning "Lokale Python Installation fehlgeschlagen (nicht kritisch)"
fi

# Git Konfiguration
if command -v git &> /dev/null && [ -d .git ]; then
    print_status "Konfiguriere Git Hooks..."
    
    # Pre-commit Hook für Code-Qualität
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit Hook für Code-Qualität

# Flake8 prüfen (wenn installiert)
if command -v flake8 &> /dev/null; then
    echo "Running flake8..."
    flake8 electro_erp/ --count --select=E9,F63,F7,F82 --show-source
    if [ $? -ne 0 ]; then
        echo "❌ Flake8 Fehler gefunden - Commit abgebrochen"
        exit 1
    fi
fi

echo "✓ Pre-commit Checks erfolgreich"
EOF
    
    chmod +x .git/hooks/pre-commit
    print_success "Git Hooks konfiguriert"
fi

# Zusammenfassung
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗"
echo "║          ✓ Setup erfolgreich abgeschlossen!          ║"
echo "╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Nächste Schritte:${NC}"
echo ""
echo "1. Öffne im Browser:"
echo "   - Odoo:          http://localhost:8069"
echo "   - Mongo Express: http://localhost:8081"
echo ""
echo "2. Erstelle Odoo Datenbank:"
echo "   - Datenbankname: electro_erp"
echo "   - Master Passwort: (aus .env)"
echo "   - Sprache: Deutsch"
echo "   - Land: Schweiz"
echo ""
echo "3. Installiere das Modul:"
echo "   - Apps → 'Electro ERP mit MongoDB' suchen"
echo "   - Installieren klicken"
echo ""
echo -e "${BLUE}🔧 Nützliche Befehle:${NC}"
echo ""
echo "# Logs anzeigen"
echo "docker-compose logs -f odoo"
echo ""
echo "# Container neu starten"
echo "docker-compose restart"
echo ""
echo "# Tests ausführen"
echo "docker-compose exec odoo pytest"
echo ""
echo "# Shell im Odoo Container"
echo "docker-compose exec odoo bash"
echo ""
echo "# Alles stoppen"
echo "docker-compose down"
echo ""
echo -e "${YELLOW}⚠️  WICHTIG:${NC}"
echo "Ändere die Passwörter in der .env Datei!"
echo ""
echo -e "${GREEN}Happy Coding! 🚀${NC}"
