// MongoDB Initialisierung für Electro ERP
// Wird beim ersten Start automatisch ausgeführt

print('🔌 Initialisiere Electro ERP MongoDB Datenbank...');

// Datenbank auswählen/erstellen
db = db.getSiblingDB('electro_erp');

// ========== COLLECTIONS ERSTELLEN ==========

// Projects Collection
db.createCollection('projects', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["odoo_id", "name", "created_at"],
            properties: {
                odoo_id: {
                    bsonType: "int",
                    description: "Odoo Project ID - required"
                },
                name: {
                    bsonType: "string",
                    description: "Project name - required"
                },
                project_type: {
                    enum: ["new_building", "renovation", "maintenance", "emergency", "inspection"],
                    description: "Type of electrical project"
                },
                building_type: {
                    enum: ["residential", "commercial", "industrial", "public", "infrastructure"],
                    description: "Type of building"
                },
                building_address: {
                    bsonType: "string"
                },
                iot_devices: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["device_id", "device_type"],
                        properties: {
                            device_id: { bsonType: "string" },
                            device_type: { bsonType: "string" },
                            name: { bsonType: "string" },
                            location: { bsonType: "string" },
                            status: { enum: ["active", "inactive", "maintenance"] }
                        }
                    }
                },
                documents: {
                    bsonType: "array"
                },
                created_at: {
                    bsonType: "date"
                },
                updated_at: {
                    bsonType: "date"
                }
            }
        }
    }
});
print('✓ Collection "projects" erstellt');

// IoT Sensor Readings Collection (Time-Series)
db.createCollection('sensor_readings', {
    timeseries: {
        timeField: "timestamp",
        metaField: "device_id",
        granularity: "minutes"
    }
});
print('✓ Collection "sensor_readings" (Time-Series) erstellt');

// Documents Collection (Pläne, Fotos, PDFs)
db.createCollection('documents', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["project_id", "filename", "document_type", "uploaded_at"],
            properties: {
                project_id: {
                    bsonType: "objectId",
                    description: "Reference to projects collection"
                },
                filename: {
                    bsonType: "string"
                },
                document_type: {
                    enum: ["plan", "photo", "pdf", "certificate", "report"],
                    description: "Type of document"
                },
                mime_type: {
                    bsonType: "string"
                },
                size: {
                    bsonType: "int"
                },
                tags: {
                    bsonType: "array",
                    items: { bsonType: "string" }
                },
                uploaded_by: {
                    bsonType: "string"
                },
                uploaded_at: {
                    bsonType: "date"
                }
            }
        }
    }
});
print('✓ Collection "documents" erstellt');

// Material Transactions Log
db.createCollection('material_transactions', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["project_id", "material_id", "transaction_type", "timestamp"],
            properties: {
                project_id: { bsonType: "objectId" },
                material_id: { bsonType: "int" },
                material_name: { bsonType: "string" },
                transaction_type: {
                    enum: ["usage", "return", "order", "delivery"],
                    description: "Type of transaction"
                },
                quantity: { bsonType: "number" },
                unit: { bsonType: "string" },
                timestamp: { bsonType: "date" },
                user: { bsonType: "string" },
                notes: { bsonType: "string" }
            }
        }
    }
});
print('✓ Collection "material_transactions" erstellt');

// ========== INDEXES ERSTELLEN ==========

// Projects Indexes
db.projects.createIndex({ "odoo_id": 1 }, { unique: true });
db.projects.createIndex({ "project_type": 1 });
db.projects.createIndex({ "created_at": -1 });
db.projects.createIndex({ "building_address": "text", "name": "text" });
print('✓ Indexes für "projects" erstellt');

// Sensor Readings Indexes
db.sensor_readings.createIndex({ "device_id": 1, "timestamp": -1 });
db.sensor_readings.createIndex({ "project_id": 1, "timestamp": -1 });
print('✓ Indexes für "sensor_readings" erstellt');

// Documents Indexes
db.documents.createIndex({ "project_id": 1, "document_type": 1 });
db.documents.createIndex({ "uploaded_at": -1 });
db.documents.createIndex({ "tags": 1 });
db.documents.createIndex({ "filename": "text" });
print('✓ Indexes für "documents" erstellt');

// Material Transactions Indexes
db.material_transactions.createIndex({ "project_id": 1, "timestamp": -1 });
db.material_transactions.createIndex({ "material_id": 1 });
print('✓ Indexes für "material_transactions" erstellt');

// ========== DEMO DATEN EINFÜGEN ==========

print('📦 Füge Demo-Daten ein...');

// Demo Projekt 1: Neubau Einfamilienhaus
const demoProject1 = db.projects.insertOne({
    odoo_id: 1,
    name: "Neubau EFH Musterstrasse 123",
    project_type: "new_building",
    building_type: "residential",
    building_address: "Musterstrasse 123, 8000 Zürich",
    iot_devices: [
        {
            device_id: "sensor_001",
            device_type: "temperature_humidity",
            name: "Wohnzimmer Sensor",
            location: "EG Wohnzimmer",
            status: "active",
            registered_at: new Date(),
            last_seen: new Date()
        },
        {
            device_id: "sensor_002",
            device_type: "energy_meter",
            name: "Hauptverteiler",
            location: "Technikraum UG",
            status: "active",
            registered_at: new Date(),
            last_seen: new Date()
        }
    ],
    metadata: {
        created_by: "Admin",
        company: "Elektro Muster AG"
    },
    document_counts: {
        plan: 0,
        photo: 0,
        pdf: 0
    },
    created_at: new Date(),
    updated_at: new Date(),
    audit_log: [
        {
            action: "created",
            user: "Admin",
            timestamp: new Date(),
            details: "Projekt initial erstellt"
        }
    ]
});
print(`✓ Demo Projekt 1 erstellt: ${demoProject1.insertedId}`);

// Demo Projekt 2: Bürosanierung
const demoProject2 = db.projects.insertOne({
    odoo_id: 2,
    name: "Sanierung Bürogebäude Techpark",
    project_type: "renovation",
    building_type: "commercial",
    building_address: "Technoparkstrasse 1, 8005 Zürich",
    iot_devices: [
        {
            device_id: "sensor_003",
            device_type: "occupancy",
            name: "Büro 4.OG Belegung",
            location: "4. OG Großraumbüro",
            status: "active",
            registered_at: new Date(),
            last_seen: new Date()
        }
    ],
    metadata: {
        created_by: "Admin",
        company: "Elektro Muster AG"
    },
    document_counts: {
        plan: 0,
        photo: 0,
        pdf: 0
    },
    created_at: new Date(),
    updated_at: new Date(),
    audit_log: [
        {
            action: "created",
            user: "Admin",
            timestamp: new Date(),
            details: "Projekt initial erstellt"
        }
    ]
});
print(`✓ Demo Projekt 2 erstellt: ${demoProject2.insertedId}`);

// Demo Sensordaten einfügen
const now = new Date();
for (let i = 0; i < 24; i++) {
    const timestamp = new Date(now.getTime() - (i * 3600000)); // Letzte 24h
    
    // Temperatur/Luftfeuchtigkeit Daten
    db.sensor_readings.insertOne({
        project_id: demoProject1.insertedId,
        device_id: "sensor_001",
        timestamp: timestamp,
        readings: {
            temperature: 20 + Math.random() * 3,
            humidity: 40 + Math.random() * 10
        },
        metadata: {
            unit_temp: "°C",
            unit_humidity: "%"
        }
    });
    
    // Energiemesser Daten
    db.sensor_readings.insertOne({
        project_id: demoProject1.insertedId,
        device_id: "sensor_002",
        timestamp: timestamp,
        readings: {
            power: 2000 + Math.random() * 1000,
            energy_total: 1500 + (i * 50)
        },
        metadata: {
            unit_power: "W",
            unit_energy: "kWh"
        }
    });
}
print('✓ 48 Demo Sensor-Readings eingefügt');

// Demo Dokumente
db.documents.insertOne({
    project_id: demoProject1.insertedId,
    filename: "Elektroplan_EG.pdf",
    document_type: "plan",
    mime_type: "application/pdf",
    size: 2458000,
    tags: ["erdgeschoss", "installationsplan", "esti"],
    uploaded_by: "Admin",
    uploaded_at: new Date(),
    content: null // In Produktion: GridFS verwenden
});

db.documents.insertOne({
    project_id: demoProject1.insertedId,
    filename: "Baustelle_Foto_001.jpg",
    document_type: "photo",
    mime_type: "image/jpeg",
    size: 1245000,
    tags: ["fortschritt", "erdgeschoss"],
    uploaded_by: "Monteur",
    uploaded_at: new Date(),
    content: null
});
print('✓ Demo Dokumente eingefügt');

// ========== BENUTZER ERSTELLEN ==========

// Admin User (nur für Demo - in Produktion via Authentication!)
db.createUser({
    user: "electro_admin",
    pwd: "changeme123",
    roles: [
        { role: "readWrite", db: "electro_erp" },
        { role: "dbAdmin", db: "electro_erp" }
    ]
});
print('✓ Admin User erstellt (Passwort ändern!)');

// ========== FERTIG ==========
print('');
print('✅ MongoDB Initialisierung abgeschlossen!');
print('');
print('📊 Statistiken:');
print('   - Collections: ' + db.getCollectionNames().length);
print('   - Demo Projekte: ' + db.projects.countDocuments());
print('   - Sensor Readings: ' + db.sensor_readings.countDocuments());
print('   - Dokumente: ' + db.documents.countDocuments());
print('');
print('🔐 WICHTIG: Ändere das Admin-Passwort in Produktion!');
print('');
print('🚀 Bereit für Odoo-Integration!');
