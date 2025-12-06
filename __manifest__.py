# -*- coding: utf-8 -*-
{
    'name': 'Electro ERP mit MongoDB',
    'version': '1.0.0',
    'category': 'Industries/Electrical',
    'summary': 'Komplettes ERP-System für Schweizer Elektroinstallationsbetriebe',
    'description': """
Electro ERP mit MongoDB Integration
====================================

Spezialisiertes ERP-System für Elektroinstallationsbetriebe in der Schweiz.

Hauptfeatures:
--------------
* Projektmanagement für Elektro-Installationen
* Angebotskalkulation mit Schweizer Standards
* Materialwirtschaft und Lagerverwaltung
* Skills & Zertifikate Management (ESTI, SUVA)
* MongoDB Integration für IoT und Dokumente
* ESTI-Abnahme und SUVA-Compliance
* Zeiterfassung und Lohnabrechnung
* Mobile Schnittstellen für Monteure

Technologie:
------------
* Odoo 17.0 + PostgreSQL (strukturierte Daten)
* MongoDB 7.0 (IoT-Daten, Dokumente, Logs)
* FastAPI REST-Schnittstellen
* Docker-basierte Deployment

Zielgruppe:
-----------
Schweizer Elektroinstallationsbetriebe mit 10-100 Mitarbeitern
    """,
    
    'author': 'Ihr Name / Ihr Unternehmen',
    'website': 'https://github.com/ihr-username/odoo-electro-mongodb-erp',
    'license': 'AGPL-3',
    
    # Abhängigkeiten von anderen Odoo-Modulen
    'depends': [
        'base',
        'project',
        'sale_management',
        'stock',
        'hr',
        'hr_skills',
        'account',
        'contacts',
    ],
    
    # Daten-Dateien (werden beim Installieren geladen)
    'data': [
        # Sicherheit
        'security/electro_security_groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        
        # Stammdaten
        'data/material_categories.xml',
        'data/project_types.xml',
        
        # Views
        'views/electro_menu.xml',
        'views/electro_project_views.xml',
        'views/electro_offer_views.xml',
        'views/electro_material_views.xml',
        'views/employee_skills_views.xml',
        'views/mongodb_dashboard_views.xml',
        
        # Berichte
        'reports/offer_report.xml',
        'reports/project_report.xml',
        'reports/material_report.xml',
        
        # Wizards
        'wizard/import_offer_wizard_views.xml',
        'wizard/export_mongo_wizard_views.xml',
    ],
    
    # Demo-Daten (nur im Demo-Modus)
    'demo': [
        'data/demo_data.xml',
    ],
    
    # Zusätzliche Assets (JS, CSS)
    'assets': {
        'web.assets_backend': [
            'electro_erp/static/src/js/mongodb_widget.js',
            'electro_erp/static/src/css/electro_erp.css',
        ],
    },
    
    # Modul-Einstellungen
    'installable': True,
    'application': True,  # Erscheint als eigenständige App
    'auto_install': False,
    
    # Externe Abhängigkeiten
    'external_dependencies': {
        'python': ['pymongo', 'fastapi', 'motor'],
    },
    
    # Bilder für App Store
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    
    # Preis (wenn kommerziell)
    'price': 0.00,
    'currency': 'CHF',
}
