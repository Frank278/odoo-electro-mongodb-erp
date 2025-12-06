# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import os
from datetime import datetime
from bson import ObjectId

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, PyMongoError
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False
    logging.getLogger(__name__).warning("pymongo not installed")

_logger = logging.getLogger(__name__)


class ElectroMongoDBIntegration(models.AbstractModel):
    """
    Abstraktes Modell für MongoDB-Integration.
    Stellt Verbindung und grundlegende CRUD-Operationen bereit.
    """
    _name = 'electro.mongodb.integration'
    _description = 'MongoDB Integration Service'

    @api.model
    def _get_mongodb_client(self):
        """
        Erstellt MongoDB-Client mit Verbindungsparametern aus Umgebung
        """
        if not PYMONGO_AVAILABLE:
            raise UserError(_('pymongo ist nicht installiert. Bitte installieren Sie es mit: pip install pymongo'))
        
        # MongoDB URI aus Umgebungsvariable oder Config
        mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://mongodb:27017/electro_erp')
        
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            # Test Verbindung
            client.admin.command('ping')
            _logger.info("MongoDB Verbindung erfolgreich hergestellt")
            return client
        except ConnectionFailure as e:
            _logger.error(f"MongoDB Verbindung fehlgeschlagen: {str(e)}")
            raise UserError(_('Kann keine Verbindung zu MongoDB herstellen: %s') % str(e))
    
    @api.model
    def _get_database(self):
        """Gibt MongoDB-Datenbank zurück"""
        client = self._get_mongodb_client()
        db_name = os.environ.get('MONGODB_DB', 'electro_erp')
        return client[db_name]
    
    # ========== PROJECT OPERATIONS ==========
    
    @api.model
    def create_project(self, project):
        """
        Erstellt ein neues Projekt in MongoDB
        
        Args:
            project: Odoo project.project recordset
        
        Returns:
            str: MongoDB ObjectId als String
        """
        db = self._get_database()
        collection = db['projects']
        
        project_doc = {
            'odoo_id': project.id,
            'name': project.name,
            'project_type': project.project_type,
            'building_type': project.building_type,
            'building_address': project.building_address or '',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'metadata': {
                'created_by': self.env.user.name,
                'company': self.env.company.name,
            },
            'iot_devices': [],
            'documents': [],
            'sensor_data': [],
            'audit_log': [{
                'action': 'created',
                'user': self.env.user.name,
                'timestamp': datetime.utcnow(),
            }]
        }
        
        try:
            result = collection.insert_one(project_doc)
            mongo_id = str(result.inserted_id)
            _logger.info(f"MongoDB Projekt erstellt: {mongo_id}")
            return mongo_id
        except PyMongoError as e:
            _logger.error(f"Fehler beim Erstellen des Projekts: {str(e)}")
            raise UserError(_('MongoDB Fehler: %s') % str(e))
    
    @api.model
    def update_project(self, project):
        """
        Aktualisiert Projekt in MongoDB
        
        Args:
            project: Odoo project.project recordset
        """
        if not project.mongo_project_id:
            _logger.warning(f"Projekt {project.name} hat keine MongoDB-ID")
            return False
        
        db = self._get_database()
        collection = db['projects']
        
        update_doc = {
            '$set': {
                'name': project.name,
                'project_type': project.project_type,
                'building_type': project.building_type,
                'building_address': project.building_address or '',
                'updated_at': datetime.utcnow(),
            },
            '$push': {
                'audit_log': {
                    'action': 'updated',
                    'user': self.env.user.name,
                    'timestamp': datetime.utcnow(),
                    'fields_changed': ['name', 'project_type'],
                }
            }
        }
        
        try:
            result = collection.update_one(
                {'_id': ObjectId(project.mongo_project_id)},
                update_doc
            )
            return result.modified_count > 0
        except PyMongoError as e:
            _logger.error(f"Fehler beim Aktualisieren: {str(e)}")
            return False
    
    @api.model
    def sync_project(self, project):
        """
        Vollständige Synchronisation zwischen Odoo und MongoDB
        """
        if not project.mongo_project_id:
            return self.create_project(project)
        else:
            return self.update_project(project)
    
    # ========== IOT DEVICE OPERATIONS ==========
    
    @api.model
    def add_iot_device(self, project_mongo_id, device_data):
        """
        Fügt IoT-Gerät zu einem Projekt hinzu
        
        Args:
            project_mongo_id: MongoDB ObjectId als String
            device_data: Dict mit Gerätedaten
        """
        db = self._get_database()
        collection = db['projects']
        
        device_doc = {
            'device_id': device_data.get('device_id'),
            'device_type': device_data.get('device_type'),
            'name': device_data.get('name'),
            'location': device_data.get('location'),
            'status': 'active',
            'registered_at': datetime.utcnow(),
            'last_seen': datetime.utcnow(),
        }
        
        try:
            result = collection.update_one(
                {'_id': ObjectId(project_mongo_id)},
                {'$push': {'iot_devices': device_doc}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            _logger.error(f"Fehler beim Hinzufügen des IoT-Geräts: {str(e)}")
            return False
    
    @api.model
    def get_iot_device_count(self, project_mongo_id):
        """
        Gibt Anzahl der IoT-Geräte für ein Projekt zurück
        """
        db = self._get_database()
        collection = db['projects']
        
        try:
            project = collection.find_one({'_id': ObjectId(project_mongo_id)})
            if project and 'iot_devices' in project:
                return len(project['iot_devices'])
            return 0
        except PyMongoError:
            return 0
    
    @api.model
    def store_sensor_data(self, project_mongo_id, sensor_data):
        """
        Speichert Sensordaten von IoT-Geräten
        
        Args:
            project_mongo_id: MongoDB ObjectId
            sensor_data: Dict mit Sensordaten
        """
        db = self._get_database()
        collection = db['sensor_readings']
        
        reading_doc = {
            'project_id': ObjectId(project_mongo_id),
            'device_id': sensor_data.get('device_id'),
            'timestamp': datetime.utcnow(),
            'readings': sensor_data.get('readings', {}),
            'metadata': sensor_data.get('metadata', {})
        }
        
        try:
            result = collection.insert_one(reading_doc)
            return str(result.inserted_id)
        except PyMongoError as e:
            _logger.error(f"Fehler beim Speichern der Sensordaten: {str(e)}")
            return None
    
    # ========== DOCUMENT OPERATIONS ==========
    
    @api.model
    def upload_document(self, project_mongo_id, document_data, file_content):
        """
        Lädt Dokument (Plan, Foto, PDF) nach MongoDB hoch
        
        Args:
            project_mongo_id: MongoDB ObjectId
            document_data: Dict mit Metadaten
            file_content: Binary file content
        """
        db = self._get_database()
        collection = db['documents']
        
        doc = {
            'project_id': ObjectId(project_mongo_id),
            'filename': document_data.get('filename'),
            'document_type': document_data.get('type'),  # 'plan', 'photo', 'pdf'
            'mime_type': document_data.get('mime_type'),
            'size': len(file_content),
            'uploaded_by': self.env.user.name,
            'uploaded_at': datetime.utcnow(),
            'tags': document_data.get('tags', []),
            'content': file_content,  # GridFS für große Dateien verwenden!
        }
        
        try:
            result = collection.insert_one(doc)
            
            # Update Projekt-Dokumentenzähler
            projects = db['projects']
            projects.update_one(
                {'_id': ObjectId(project_mongo_id)},
                {'$inc': {f'document_counts.{document_data.get("type")}': 1}}
            )
            
            return str(result.inserted_id)
        except PyMongoError as e:
            _logger.error(f"Fehler beim Hochladen des Dokuments: {str(e)}")
            return None
    
    @api.model
    def get_document_stats(self, project_mongo_id):
        """
        Gibt Dokumenten-Statistiken zurück
        
        Returns:
            dict: {'total': 0, 'plans': 0, 'photos': 0, 'pdfs': 0}
        """
        db = self._get_database()
        collection = db['documents']
        
        try:
            pipeline = [
                {'$match': {'project_id': ObjectId(project_mongo_id)}},
                {'$group': {
                    '_id': '$document_type',
                    'count': {'$sum': 1}
                }}
            ]
            
            results = list(collection.aggregate(pipeline))
            
            stats = {'total': 0, 'plans': 0, 'photos': 0, 'pdfs': 0}
            for result in results:
                doc_type = result['_id']
                count = result['count']
                stats[doc_type] = count
                stats['total'] += count
            
            return stats
        except PyMongoError as e:
            _logger.error(f"Fehler beim Abrufen der Statistiken: {str(e)}")
            return {'total': 0, 'plans': 0, 'photos': 0, 'pdfs': 0}
    
    # ========== ANALYTICS ==========
    
    @api.model
    def get_project_analytics(self, project_mongo_id):
        """
        Komplexe Analytics aus MongoDB für Dashboard
        """
        db = self._get_database()
        
        analytics = {
            'iot_summary': self._get_iot_summary(db, project_mongo_id),
            'document_summary': self.get_document_stats(project_mongo_id),
            'sensor_trends': self._get_sensor_trends(db, project_mongo_id),
            'activity_timeline': self._get_activity_timeline(db, project_mongo_id),
        }
        
        return analytics
    
    def _get_iot_summary(self, db, project_mongo_id):
        """IoT-Geräte Zusammenfassung"""
        collection = db['projects']
        project = collection.find_one({'_id': ObjectId(project_mongo_id)})
        
        if not project or 'iot_devices' not in project:
            return {'total': 0, 'active': 0, 'inactive': 0}
        
        devices = project['iot_devices']
        active = sum(1 for d in devices if d.get('status') == 'active')
        
        return {
            'total': len(devices),
            'active': active,
            'inactive': len(devices) - active,
        }
    
    def _get_sensor_trends(self, db, project_mongo_id):
        """Letzte 24h Sensor-Trends"""
        # Implementierung für Zeit-Series Daten
        return {}
    
    def _get_activity_timeline(self, db, project_mongo_id):
        """Aktivitäts-Timeline aus Audit Log"""
        collection = db['projects']
        project = collection.find_one({'_id': ObjectId(project_mongo_id)})
        
        if project and 'audit_log' in project:
            return project['audit_log'][-10:]  # Letzte 10 Einträge
        
        return []
