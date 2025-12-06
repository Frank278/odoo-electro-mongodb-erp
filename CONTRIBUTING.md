# Contributing to Odoo Electro MongoDB ERP

Vielen Dank für dein Interesse, zu diesem Projekt beizutragen! 🎉

## 📋 Inhaltsverzeichnis

- [Code of Conduct](#code-of-conduct)
- [Wie kann ich beitragen?](#wie-kann-ich-beitragen)
- [Entwicklungsumgebung einrichten](#entwicklungsumgebung-einrichten)
- [Coding Standards](#coding-standards)
- [Pull Request Prozess](#pull-request-prozess)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)

## 📜 Code of Conduct

Wir verpflichten uns, eine offene und einladende Umgebung zu schaffen. Bitte lies unseren [Code of Conduct](CODE_OF_CONDUCT.md).

## 🤝 Wie kann ich beitragen?

### Typen von Beiträgen

- 🐛 **Bug Fixes**: Behebe Fehler im Code
- ✨ **Features**: Implementiere neue Funktionen
- 📚 **Dokumentation**: Verbessere Docs und Kommentare
- 🧪 **Tests**: Füge Tests hinzu oder verbessere sie
- 🌍 **Übersetzungen**: Hilf bei Übersetzungen (DE, FR, IT, EN)
- 🎨 **UI/UX**: Verbessere Benutzeroberfläche

### Erste Schritte

1. **Fork das Repository**
   ```bash
   git clone https://github.com/dein-username/odoo-electro-mongodb-erp.git
   cd odoo-electro-mongodb-erp
   ```

2. **Erstelle einen Feature Branch**
   ```bash
   git checkout -b feature/mein-neues-feature
   # oder
   git checkout -b bugfix/fix-issue-123
   ```

3. **Mache deine Änderungen**

4. **Teste deine Änderungen**
   ```bash
   docker-compose up -d
   docker-compose exec odoo pytest
   ```

5. **Committe mit aussagekräftigen Nachrichten**
   ```bash
   git commit -m "feat: Füge IoT Dashboard Widget hinzu"
   ```

6. **Push und erstelle Pull Request**
   ```bash
   git push origin feature/mein-neues-feature
   ```

## 🛠️ Entwicklungsumgebung einrichten

### Voraussetzungen

- Docker & Docker Compose
- Python 3.11+
- Git
- Code Editor (VS Code empfohlen)

### Setup

```bash
# 1. Repository klonen
git clone https://github.com/dein-username/odoo-electro-mongodb-erp.git
cd odoo-electro-mongodb-erp

# 2. Dev-Environment Script ausführen
./scripts/setup_dev_env.sh

# 3. Docker Container starten
docker-compose up -d

# 4. Warten bis Odoo bereit ist
docker-compose logs -f odoo

# 5. Im Browser öffnen
# http://localhost:8069
```

### VS Code Extensions (empfohlen)

- Python
- Pylance
- Docker
- GitLens
- Odoo Snippets

## 📏 Coding Standards

### Python Code Style

Wir folgen **PEP 8** mit einigen Odoo-spezifischen Anpassungen:

```python
# Gut ✅
class ElectroProject(models.Model):
    _inherit = 'project.project'
    _description = 'Elektro-Installationsprojekt'
    
    project_type = fields.Selection([
        ('new_building', 'Neubau'),
        ('renovation', 'Sanierung'),
    ], string='Projekttyp', required=True)
    
    def action_sync_mongodb(self):
        """Synchronisiert Projekt mit MongoDB"""
        self.ensure_one()
        # Implementation...
        return True

# Schlecht ❌
class electroProject(models.Model):
    project_type=fields.Selection([('new_building','Neubau')])
    def sync(self):
        return True
```

### Odoo Konventionen

- **Model Namen**: CamelCase mit Punktnotation (`electro.project`)
- **Feld Namen**: snake_case (`project_type`)
- **Methoden**: snake_case mit Präfix (`action_`, `_compute_`, `_onchange_`)
- **Private Methoden**: Unterstrich-Präfix (`_get_data()`)

### XML Views

```xml
<!-- Gut ✅ -->
<odoo>
    <record id="view_electro_project_form" model="ir.ui.view">
        <field name="name">electro.project.form</field>
        <field name="model">project.project</field>
        <field name="arch" type="xml">
            <form string="Elektro-Projekt">
                <sheet>
                    <group>
                        <field name="project_type"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```

### Commit Messages

Wir nutzen [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Füge ESTI-Abnahme Wizard hinzu
fix: Behebt MongoDB Verbindungsfehler
docs: Aktualisiere Installation Guide
test: Füge Tests für electro_project hinzu
refactor: Vereinfache MongoDB Integration
style: Formatiere Code nach PEP8
chore: Update Dependencies
```

**Typen:**
- `feat`: Neue Funktionalität
- `fix`: Bugfix
- `docs`: Dokumentation
- `test`: Tests
- `refactor`: Code-Refactoring
- `style`: Formatierung
- `chore`: Maintenance

## 🔄 Pull Request Prozess

### Vor dem PR

- [ ] Code folgt Coding Standards
- [ ] Alle Tests laufen durch (`pytest`)
- [ ] Keine Lint-Fehler (`flake8`)
- [ ] Dokumentation aktualisiert
- [ ] CHANGELOG.md ergänzt
- [ ] Commit Messages sind aussagekräftig

### PR Template

```markdown
## Beschreibung
Kurze Beschreibung der Änderungen

## Art der Änderung
- [ ] Bug Fix
- [ ] Neues Feature
- [ ] Breaking Change
- [ ] Dokumentation

## Testing
Wie wurde getestet?

## Screenshots (wenn relevant)

## Checklist
- [ ] Code folgt Standards
- [ ] Tests hinzugefügt
- [ ] Dokumentation aktualisiert
```

### Review Prozess

1. **Automatische Checks**: GitHub Actions muss grün sein
2. **Code Review**: Mindestens 1 Reviewer Approval
3. **Testing**: Manuelle Tests wenn nötig
4. **Merge**: Squash & Merge in main Branch

## 🐛 Bug Reports

### Gute Bug Reports enthalten:

1. **Titel**: Klare, kurze Zusammenfassung
2. **Beschreibung**: Was ist passiert?
3. **Erwartetes Verhalten**: Was sollte passieren?
4. **Reproduktion**: Schritte zum Nachstellen
5. **Umgebung**: OS, Docker Version, Browser
6. **Screenshots**: Wenn hilfreich
7. **Logs**: Relevante Fehlermeldungen

**Beispiel:**

```markdown
### Bug: MongoDB Sync schlägt bei großen Projekten fehl

**Beschreibung:**
Beim Synchronisieren eines Projekts mit >100 IoT-Geräten 
tritt ein Timeout-Fehler auf.

**Erwartetes Verhalten:**
Sync sollte auch bei vielen Geräten funktionieren.

**Schritte zum Reproduzieren:**
1. Projekt mit 150 IoT-Geräten erstellen
2. "Sync mit MongoDB" Button klicken
3. Fehler tritt auf nach 30 Sekunden

**Umgebung:**
- OS: Ubuntu 22.04
- Docker: 24.0.5
- Browser: Chrome 120

**Logs:**
```
ERROR: pymongo.errors.ServerSelectionTimeoutError: 
localhost:27017: [Errno 110] Connection timed out
```
```

## ✨ Feature Requests

### Gute Feature Requests enthalten:

1. **Titel**: Klare Feature-Beschreibung
2. **Problem**: Welches Problem löst es?
3. **Lösung**: Wie sollte es funktionieren?
4. **Alternativen**: Andere Lösungsansätze?
5. **Zusätzlicher Kontext**: Screenshots, Mockups

**Beispiel:**

```markdown
### Feature: Automatische Materialdisposition

**Problem:**
Monteure müssen Material oft manuell nachbestellen.
Das führt zu Verzögerungen auf der Baustelle.

**Vorgeschlagene Lösung:**
Automatisches System das basierend auf:
- Projekttyp
- Historischen Daten
- Lagerbestand

benötigtes Material vorschlägt und automatisch bestellt.

**Alternativen:**
- Manuelle Checklisten
- Erinnerungen für Disponenten

**Zusätzlicher Kontext:**
Ähnlich zu Bausoftware XY, aber integriert mit MongoDB
für Echtzeit-Updates.
```

## 🌍 Übersetzungen

Wir benötigen Hilfe bei Übersetzungen:

- **Deutsch** (DE) ✅ Hauptsprache
- **Französisch** (FR) ⚠️ Teilweise
- **Italienisch** (IT) ⚠️ Teilweise
- **Englisch** (EN) ⚠️ Teilweise

Übersetzungsdateien: `electro_erp/i18n/*.po`

## 📞 Fragen?

- **GitHub Discussions**: Für allgemeine Fragen
- **Issues**: Für Bugs und Features
- **Email**: dev@example.com

---

**Vielen Dank für deinen Beitrag! 🙏**
