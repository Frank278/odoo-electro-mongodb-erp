#!/bin/bash
set -e

# Electro ERP Docker Entrypoint Script
# Erweitert das Standard Odoo Entrypoint um MongoDB und Custom Logic

# Farben für Logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🔌 Electro ERP Starting...               ║${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════╝${NC}"

# Funktion: Warte auf Service
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}⏳ Warte auf ${service} (${host}:${port})...${NC}"
    
    while ! nc -z ${host} ${port} 2>/dev/null; do
        if [ ${attempt} -eq ${max_attempts} ]; then
            echo -e "${RED}✗ Timeout: ${service} nicht erreichbar!${NC}"
            exit 1
        fi
        echo "   Versuch ${attempt}/${max_attempts}..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "${GREEN}✓ ${service} ist bereit${NC}"
}

# Prüfe ob PostgreSQL bereit ist
if [ -n "${HOST}" ]; then
    wait_for_service "${HOST}" "${PORT:-5432}" "PostgreSQL"
fi

# Prüfe ob MongoDB bereit ist
if [ -n "${MONGODB_URI}" ]; then
    # Extrahiere Host und Port aus URI
    MONGO_HOST=$(echo ${MONGODB_URI} | sed -E 's|mongodb://([^:]+):([0-9]+)/.*|\1|')
    MONGO_PORT=$(echo ${MONGODB_URI} | sed -E 's|mongodb://([^:]+):([0-9]+)/.*|\2|')
    
    if [ -n "${MONGO_HOST}" ] && [ -n "${MONGO_PORT}" ]; then
        wait_for_service "${MONGO_HOST}" "${MONGO_PORT}" "MongoDB"
    fi
fi

# Teste MongoDB Verbindung mit Python
echo -e "${YELLOW}🔍 Teste MongoDB Verbindung...${NC}"
python3 << EOF
import sys
import os
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    
    uri = os.environ.get('MONGODB_URI', 'mongodb://mongodb:27017/electro_erp')
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print('\033[0;32m✓ MongoDB Verbindung erfolgreich\033[0m')
    sys.exit(0)
except ImportError:
    print('\033[1;33m⚠ pymongo nicht installiert\033[0m')
    sys.exit(0)
except ConnectionFailure as e:
    print(f'\033[0;31m✗ MongoDB Verbindung fehlgeschlagen: {e}\033[0m')
    sys.exit(1)
except Exception as e:
    print(f'\033[1;33m⚠ MongoDB Test-Fehler: {e}\033[0m')
    sys.exit(0)
EOF

# Setze Odoo Addons Path
if [ -d "/mnt/extra-addons/electro_erp" ]; then
    export ADDONS_PATH="/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"
    echo -e "${GREEN}✓ Electro ERP Modul gefunden${NC}"
else
    echo -e "${YELLOW}⚠ Electro ERP Modul nicht in /mnt/extra-addons gefunden${NC}"
fi

# Setze Umgebungsvariablen für Odoo
export ODOO_RC=${ODOO_RC:-/etc/odoo/odoo.conf}

# Zeige Konfiguration
echo ""
echo -e "${BLUE}📋 Konfiguration:${NC}"
echo "   PostgreSQL: ${HOST:-localhost}:${PORT:-5432}"
echo "   MongoDB:    ${MONGODB_URI:-mongodb://mongodb:27017/electro_erp}"
echo "   Workers:    ${WORKERS:-2}"
echo "   Addons:     ${ADDONS_PATH}"
echo ""

# Development Mode Checks
if [ "${ODOO_DEV}" = "true" ] || [ -n "$(echo $@ | grep '\--dev')" ]; then
    echo -e "${YELLOW}🔧 Development Mode aktiviert${NC}"
    
    # Installiere zusätzliche Dev-Tools
    if command -v pip3 &> /dev/null; then
        echo "   Installiere Dev-Dependencies..."
        pip3 install --quiet watchdog pylint-odoo black || true
    fi
    
    # Setze Dev-spezifische Umgebungsvariablen
    export PYTHONDONTWRITEBYTECODE=1
    export PYTHONUNBUFFERED=1
fi

# Healthcheck Script erstellen
cat > /tmp/healthcheck.sh << 'HEALTHCHECK_EOF'
#!/bin/bash
# Healthcheck für Docker Container

# Prüfe Odoo HTTP
if ! curl -f http://localhost:8069/web/health >/dev/null 2>&1; then
    echo "Odoo HTTP nicht erreichbar"
    exit 1
fi

# Prüfe MongoDB (wenn pymongo verfügbar)
python3 -c "
import os
from pymongo import MongoClient
uri = os.environ.get('MONGODB_URI', 'mongodb://mongodb:27017/electro_erp')
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    client.admin.command('ping')
except:
    pass
" || echo "MongoDB Check übersprungen"

echo "Healthcheck OK"
exit 0
HEALTHCHECK_EOF

chmod +x /tmp/healthcheck.sh

# Log-Verzeichnisse erstellen
mkdir -p /var/log/odoo
chown -R odoo:odoo /var/log/odoo

# Erstelle Odoo Config falls nicht vorhanden
if [ ! -f "${ODOO_RC}" ]; then
    echo -e "${YELLOW}⚠ Erstelle Standard-Konfiguration${NC}"
    
    cat > ${ODOO_RC} << ODOO_CONF_EOF
[options]
addons_path = ${ADDONS_PATH}
data_dir = /var/lib/odoo
admin_passwd = \${ADMIN_PASSWD:-admin}
db_host = \${HOST:-db}
db_port = \${PORT:-5432}
db_user = \${USER:-odoo}
db_password = \${PASSWORD:-odoo}
workers = \${WORKERS:-2}
max_cron_threads = 1
limit_time_cpu = 600
limit_time_real = 1200
log_level = info
logfile = /var/log/odoo/odoo.log
ODOO_CONF_EOF
fi

# Backup alter Logs
if [ -f "/var/log/odoo/odoo.log" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    mv /var/log/odoo/odoo.log "/var/log/odoo/odoo.log.${TIMESTAMP}" 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}✅ Initialisierung abgeschlossen${NC}"
echo -e "${BLUE}🚀 Starte Odoo...${NC}"
echo ""

# Führe Original Odoo Entrypoint aus
# Falls vorhanden, sonst direkt Odoo starten
if [ -f "/entrypoint.sh.orig" ]; then
    exec /entrypoint.sh.orig "$@"
elif [ -x "/usr/bin/odoo" ]; then
    exec /usr/bin/odoo "$@"
else
    exec odoo "$@"
fi
