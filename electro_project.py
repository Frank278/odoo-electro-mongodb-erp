# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class ElectroProject(models.Model):
    """
    Erweitertes Projektmodell für Elektroinstallationsprojekte.
    Erweitert das Standard project.project Modell von Odoo.
    """
    _inherit = 'project.project'
    _description = 'Elektro-Installationsprojekt'

    # ========== PROJEKTKLASSIFIZIERUNG ==========
    
    project_type = fields.Selection([
        ('new_building', 'Neubau'),
        ('renovation', 'Sanierung'),
        ('maintenance', 'Wartung'),
        ('emergency', 'Notdienst'),
        ('inspection', 'Kontrolle/Abnahme'),
    ], string='Projekttyp', required=True, default='new_building',
       help='Art des Elektroprojekts')
    
    building_type = fields.Selection([
        ('residential', 'Wohngebäude'),
        ('commercial', 'Gewerbe'),
        ('industrial', 'Industrie'),
        ('public', 'Öffentliche Einrichtung'),
        ('infrastructure', 'Infrastruktur'),
    ], string='Gebäudetyp', help='Art des Gebäudes')
    
    # ========== PROJEKT-DETAILS ==========
    
    building_address = fields.Char('Bauadresse', help='Adresse der Baustelle')
    building_year = fields.Integer('Baujahr', help='Jahr der Erstellung/letzten Sanierung')
    floor_count = fields.Integer('Anzahl Stockwerke')
    total_area = fields.Float('Fläche (m²)', help='Gesamtfläche des Projekts')
    
    # Verantwortlichkeiten
    project_manager_id = fields.Many2one('hr.employee', string='Projektleiter',
                                         domain=[('job_id.name', 'ilike', 'projektleiter')])
    chief_electrician_id = fields.Many2one('hr.employee', string='Elektro-Chef',
                                           domain=[('job_id.name', 'ilike', 'monteur')])
    
    # ========== SWISS COMPLIANCE ==========
    
    esti_required = fields.Boolean('ESTI-Abnahme erforderlich', default=True,
                                    help='Eidg. Starkstrominspektorat Abnahme')
    esti_number = fields.Char('ESTI-Nummer', help='NIV-Installationsmeldung Nummer')
    esti_date = fields.Date('ESTI-Abnahme Datum')
    esti_status = fields.Selection([
        ('not_required', 'Nicht erforderlich'),
        ('pending', 'Ausstehend'),
        ('scheduled', 'Terminiert'),
        ('approved', 'Abgenommen'),
        ('rejected', 'Beanstandet'),
    ], string='ESTI-Status', default='pending', compute='_compute_esti_status', store=True)
    
    suva_compliant = fields.Boolean('SUVA-konform', default=False,
                                     help='Erfüllt SUVA Sicherheitsvorschriften')
    safety_plan_id = fields.Many2one('ir.attachment', string='Sicherheitskonzept')
    
    # ========== MONGODB INTEGRATION ==========
    
    mongo_project_id = fields.Char('MongoDB Project ID', readonly=True,
                                    help='Referenz zur MongoDB Collection')
    has_iot_devices = fields.Boolean('IoT-Geräte verbunden', default=False,
                                     help='Projekt hat verknüpfte IoT-Sensoren')
    iot_device_count = fields.Integer('Anzahl IoT-Geräte', compute='_compute_iot_stats')
    last_data_sync = fields.Datetime('Letzte Daten-Sync', readonly=True)
    
    # Dokumente in MongoDB
    mongodb_document_count = fields.Integer('MongoDB Dokumente', 
                                            compute='_compute_mongodb_stats')
    has_plans = fields.Boolean('Baupläne vorhanden', compute='_compute_mongodb_stats')
    has_photos = fields.Boolean('Fotos vorhanden', compute='_compute_mongodb_stats')
    
    # ========== KALKULATION ==========
    
    estimated_hours = fields.Float('Geschätzte Stunden', help='Geplanter Arbeitsaufwand')
    actual_hours = fields.Float('Tatsächliche Stunden', compute='_compute_actual_hours')
    estimated_material_cost = fields.Monetary('Geschätzte Materialkosten')
    actual_material_cost = fields.Monetary('Tatsächliche Materialkosten',
                                           compute='_compute_actual_costs')
    
    currency_id = fields.Many2one('res.currency', string='Währung',
                                   default=lambda self: self.env.company.currency_id)
    
    # ========== STATUS & TRACKING ==========
    
    installation_phase = fields.Selection([
        ('planning', 'Planung'),
        ('preparation', 'Vorbereitung'),
        ('rough_installation', 'Rohinstallation'),
        ('fine_installation', 'Feininstallation'),
        ('testing', 'Prüfung'),
        ('acceptance', 'Abnahme'),
        ('completed', 'Abgeschlossen'),
    ], string='Installationsphase', default='planning')
    
    risk_level = fields.Selection([
        ('low', 'Niedrig'),
        ('medium', 'Mittel'),
        ('high', 'Hoch'),
        ('critical', 'Kritisch'),
    ], string='Risikostufe', default='low', compute='_compute_risk_level', store=True)
    
    # ========== COMPUTED FIELDS ==========
    
    @api.depends('esti_required', 'esti_date')
    def _compute_esti_status(self):
        """Berechnet den ESTI-Abnahme Status"""
        for project in self:
            if not project.esti_required:
                project.esti_status = 'not_required'
            elif project.esti_date:
                if project.esti_date > fields.Date.today():
                    project.esti_status = 'scheduled'
                else:
                    project.esti_status = 'approved'
            else:
                project.esti_status = 'pending'
    
    @api.depends('mongo_project_id')
    def _compute_iot_stats(self):
        """Holt IoT-Statistiken aus MongoDB"""
        mongo_integration = self.env['electro.mongodb.integration']
        for project in self:
            if project.mongo_project_id:
                stats = mongo_integration.get_iot_device_count(project.mongo_project_id)
                project.iot_device_count = stats
            else:
                project.iot_device_count = 0
    
    @api.depends('mongo_project_id')
    def _compute_mongodb_stats(self):
        """Berechnet Dokumenten-Statistiken aus MongoDB"""
        mongo_integration = self.env['electro.mongodb.integration']
        for project in self:
            if project.mongo_project_id:
                docs = mongo_integration.get_document_stats(project.mongo_project_id)
                project.mongodb_document_count = docs.get('total', 0)
                project.has_plans = docs.get('plans', 0) > 0
                project.has_photos = docs.get('photos', 0) > 0
            else:
                project.mongodb_document_count = 0
                project.has_plans = False
                project.has_photos = False
    
    def _compute_actual_hours(self):
        """Berechnet tatsächlich aufgewendete Stunden aus Zeiterfassung"""
        for project in self:
            timesheets = self.env['account.analytic.line'].search([
                ('project_id', '=', project.id)
            ])
            project.actual_hours = sum(timesheets.mapped('unit_amount'))
    
    def _compute_actual_costs(self):
        """Berechnet tatsächliche Materialkosten"""
        for project in self:
            # Hole Material-Buchungen für dieses Projekt
            materials = self.env['electro.material.usage'].search([
                ('project_id', '=', project.id)
            ])
            project.actual_material_cost = sum(materials.mapped('total_cost'))
    
    @api.depends('project_type', 'esti_status', 'installation_phase')
    def _compute_risk_level(self):
        """Berechnet Risikostufe basierend auf verschiedenen Faktoren"""
        for project in self:
            risk = 'low'
            
            # ESTI-Probleme erhöhen Risiko
            if project.esti_required and project.esti_status == 'rejected':
                risk = 'high'
            elif project.esti_required and project.esti_status == 'pending':
                risk = 'medium'
            
            # Notdienste sind immer kritisch
            if project.project_type == 'emergency':
                risk = 'critical'
            
            # Verzug erhöht Risiko
            if project.date_deadline and project.date_deadline < fields.Date.today():
                if risk == 'low':
                    risk = 'medium'
                elif risk == 'medium':
                    risk = 'high'
            
            project.risk_level = risk
    
    # ========== CONSTRAINTS ==========
    
    @api.constrains('estimated_hours', 'estimated_material_cost')
    def _check_estimates(self):
        """Validiert dass Schätzungen positiv sind"""
        for project in self:
            if project.estimated_hours < 0:
                raise ValidationError(_('Geschätzte Stunden können nicht negativ sein.'))
            if project.estimated_material_cost < 0:
                raise ValidationError(_('Geschätzte Materialkosten können nicht negativ sein.'))
    
    # ========== ACTIONS & METHODS ==========
    
    def action_sync_with_mongodb(self):
        """Manueller Sync-Button: Synchronisiert Projekt mit MongoDB"""
        self.ensure_one()
        mongo_integration = self.env['electro.mongodb.integration']
        
        try:
            result = mongo_integration.sync_project(self)
            self.last_data_sync = fields.Datetime.now()
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Sync erfolgreich'),
                    'message': _('Projekt wurde mit MongoDB synchronisiert.'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            _logger.error(f"MongoDB Sync fehlgeschlagen: {str(e)}")
            raise UserError(_('Synchronisation fehlgeschlagen: %s') % str(e))
    
    def action_view_mongodb_dashboard(self):
        """Öffnet MongoDB Dashboard für dieses Projekt"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('MongoDB Dashboard'),
            'res_model': 'electro.mongodb.dashboard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_project_id': self.id}
        }
    
    def action_schedule_esti_inspection(self):
        """Wizard zum Planen der ESTI-Abnahme"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('ESTI-Abnahme planen'),
            'res_model': 'electro.esti.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_project_id': self.id}
        }
    
    @api.model
    def create(self, vals):
        """Override: Erstellt MongoDB-Eintrag beim Projektanlegen"""
        project = super(ElectroProject, self).create(vals)
        
        # Erstelle MongoDB-Projekt
        if not project.mongo_project_id:
            mongo_integration = self.env['electro.mongodb.integration']
            mongo_id = mongo_integration.create_project(project)
            project.mongo_project_id = mongo_id
        
        return project
    
    def write(self, vals):
        """Override: Synchronisiert Änderungen nach MongoDB"""
        result = super(ElectroProject, self).write(vals)
        
        # Auto-Sync bei wichtigen Feldänderungen
        sync_fields = ['name', 'project_type', 'building_type', 'installation_phase']
        if any(field in vals for field in sync_fields):
            for project in self:
                if project.mongo_project_id:
                    try:
                        mongo_integration = self.env['electro.mongodb.integration']
                        mongo_integration.update_project(project)
                    except Exception as e:
                        _logger.warning(f"Auto-Sync fehlgeschlagen: {str(e)}")
        
        return result
