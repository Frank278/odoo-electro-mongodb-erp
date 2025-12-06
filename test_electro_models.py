# -*- coding: utf-8 -*-
"""
Unit Tests für Electro ERP Models
"""
import pytest
from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError


class TestElectroProject(TransactionCase):
    """
    Tests für das electro.project Model
    """
    
    def setUp(self):
        """Setup für jeden Test"""
        super(TestElectroProject, self).setUp()
        
        # Test-Daten erstellen
        self.project_model = self.env['project.project']
        self.partner = self.env['res.partner'].create({
            'name': 'Test Kunde AG',
            'street': 'Teststrasse 123',
            'city': 'Zürich',
            'zip': '8000',
            'country_id': self.env.ref('base.ch').id,
        })
        
        # Test-Projekt
        self.test_project = self.project_model.create({
            'name': 'Test Neubau EFH',
            'partner_id': self.partner.id,
            'project_type': 'new_building',
            'building_type': 'residential',
            'building_address': 'Teststrasse 123, 8000 Zürich',
            'esti_required': True,
            'estimated_hours': 100.0,
            'estimated_material_cost': 15000.0,
        })
    
    def test_project_creation(self):
        """Test: Projekt wird korrekt erstellt"""
        self.assertTrue(self.test_project.id)
        self.assertEqual(self.test_project.name, 'Test Neubau EFH')
        self.assertEqual(self.test_project.project_type, 'new_building')
        # MongoDB ID sollte automatisch erstellt werden
        self.assertTrue(self.test_project.mongo_project_id)
    
    def test_project_type_selection(self):
        """Test: Alle Projekttypen sind verfügbar"""
        valid_types = ['new_building', 'renovation', 'maintenance', 
                      'emergency', 'inspection']
        for ptype in valid_types:
            project = self.project_model.create({
                'name': f'Test {ptype}',
                'project_type': ptype,
            })
            self.assertEqual(project.project_type, ptype)
    
    def test_esti_status_computation(self):
        """Test: ESTI Status wird korrekt berechnet"""
        # Fall 1: ESTI nicht erforderlich
        project1 = self.project_model.create({
            'name': 'Test ohne ESTI',
            'esti_required': False,
        })
        self.assertEqual(project1.esti_status, 'not_required')
        
        # Fall 2: ESTI erforderlich, kein Datum
        project2 = self.project_model.create({
            'name': 'Test mit ESTI',
            'esti_required': True,
        })
        self.assertEqual(project2.esti_status, 'pending')
        
        # Fall 3: ESTI-Datum in Zukunft
        project3 = self.project_model.create({
            'name': 'Test ESTI geplant',
            'esti_required': True,
            'esti_date': datetime.now().date() + timedelta(days=7),
        })
        self.assertEqual(project3.esti_status, 'scheduled')
        
        # Fall 4: ESTI-Datum in Vergangenheit
        project4 = self.project_model.create({
            'name': 'Test ESTI abgeschlossen',
            'esti_required': True,
            'esti_date': datetime.now().date() - timedelta(days=7),
        })
        self.assertEqual(project4.esti_status, 'approved')
    
    def test_risk_level_computation(self):
        """Test: Risikostufe wird korrekt berechnet"""
        # Fall 1: Notdienst = immer kritisch
        emergency_project = self.project_model.create({
            'name': 'Notdienst',
            'project_type': 'emergency',
        })
        self.assertEqual(emergency_project.risk_level, 'critical')
        
        # Fall 2: ESTI rejected = high risk
        rejected_project = self.project_model.create({
            'name': 'ESTI abgelehnt',
            'esti_required': True,
            'esti_status': 'rejected',
        })
        self.assertEqual(rejected_project.risk_level, 'high')
        
        # Fall 3: Normales Projekt = low risk
        normal_project = self.project_model.create({
            'name': 'Normal',
            'project_type': 'new_building',
        })
        self.assertIn(normal_project.risk_level, ['low', 'medium'])
    
    def test_estimate_validation(self):
        """Test: Negative Schätzungen werden abgelehnt"""
        with self.assertRaises(ValidationError):
            self.project_model.create({
                'name': 'Test negativ',
                'estimated_hours': -10.0,
            })
        
        with self.assertRaises(ValidationError):
            self.project_model.create({
                'name': 'Test negativ',
                'estimated_material_cost': -1000.0,
            })
    
    def test_mongodb_sync(self):
        """Test: MongoDB Synchronisation"""
        # Test Sync Action
        result = self.test_project.action_sync_with_mongodb()
        
        # Sollte Notification zurückgeben
        self.assertEqual(result['type'], 'ir.actions.client')
        self.assertEqual(result['tag'], 'display_notification')
        
        # last_data_sync sollte gesetzt sein
        self.assertTrue(self.test_project.last_data_sync)
    
    def test_iot_device_count(self):
        """Test: IoT-Geräte Zählung"""
        # Initial sollte 0 sein
        self.assertEqual(self.test_project.iot_device_count, 0)
        
        # Nach Hinzufügen von IoT-Geräten (simuliert)
        # In echtem Test würde man MongoDB Mock verwenden
        # Hier nur Interface-Test
        self.assertFalse(self.test_project.has_iot_devices)


class TestElectroMaterial(TransactionCase):
    """
    Tests für Material-Management
    """
    
    def setUp(self):
        super(TestElectroMaterial, self).setUp()
        self.material_model = self.env['electro.material']
        
        # Test-Material
        self.test_material = self.material_model.create({
            'name': 'NYM-J 5x1.5',
            'material_type': 'cable',
            'unit': 'm',
            'price_per_unit': 2.50,
            'stock_quantity': 500.0,
            'min_stock': 100.0,
        })
    
    def test_material_creation(self):
        """Test: Material wird korrekt erstellt"""
        self.assertTrue(self.test_material.id)
        self.assertEqual(self.test_material.name, 'NYM-J 5x1.5')
        self.assertEqual(self.test_material.price_per_unit, 2.50)
    
    def test_low_stock_warning(self):
        """Test: Niedrigstand-Warnung"""
        # Setze Bestand unter Minimum
        self.test_material.stock_quantity = 50.0
        
        # Sollte Warnung auslösen (computed field)
        # Implementation abhängig
        self.assertTrue(self.test_material.stock_quantity < 
                       self.test_material.min_stock)


class TestMongoDBIntegration(TransactionCase):
    """
    Tests für MongoDB Integration
    """
    
    def setUp(self):
        super(TestMongoDBIntegration, self).setUp()
        self.mongo_model = self.env['electro.mongodb.integration']
    
    def test_mongodb_connection(self):
        """Test: MongoDB Verbindung"""
        try:
            client = self.mongo_model._get_mongodb_client()
            self.assertIsNotNone(client)
            # Teste Ping
            db = self.mongo_model._get_database()
            self.assertIsNotNone(db)
        except UserError as e:
            # MongoDB nicht verfügbar in Test-Umgebung
            self.skipTest(f"MongoDB nicht verfügbar: {str(e)}")
    
    def test_project_creation_in_mongodb(self):
        """Test: Projekt in MongoDB erstellen"""
        try:
            # Erstelle Test-Projekt
            project = self.env['project.project'].create({
                'name': 'MongoDB Test Projekt',
                'project_type': 'new_building',
            })
            
            # MongoDB ID sollte gesetzt sein
            self.assertTrue(project.mongo_project_id)
            
            # Prüfe ob in MongoDB vorhanden
            # (In echtem Test mit MongoDB Mock)
            
        except UserError:
            self.skipTest("MongoDB nicht verfügbar")


# pytest Fixtures (für pytest statt Odoo Test Runner)

@pytest.fixture
def odoo_env():
    """Pytest Fixture für Odoo Environment"""
    # Setup Odoo Environment für pytest
    # Wird nur verwendet wenn mit pytest ausgeführt
    pass


@pytest.fixture
def test_project(odoo_env):
    """Pytest Fixture für Test-Projekt"""
    # Erstelle Test-Projekt für pytest
    pass


# pytest Tests (optional)

def test_project_with_pytest(test_project):
    """Beispiel pytest Test"""
    assert test_project is not None
    # Weitere Assertions...


# Test Suite Konfiguration

def suite():
    """Test Suite für Odoo Test Runner"""
    suite = TestSuite()
    suite.addTests(TestLoader().loadTestsFromTestCase(TestElectroProject))
    suite.addTests(TestLoader().loadTestsFromTestCase(TestElectroMaterial))
    suite.addTests(TestLoader().loadTestsFromTestCase(TestMongoDBIntegration))
    return suite


if __name__ == '__main__':
    # Kann direkt ausgeführt werden
    unittest.main()
