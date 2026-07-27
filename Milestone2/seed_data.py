"""
FreightQuote AI - seed_data.py
Pre-seeds the database with realistic global carriers, quotes, shipments, and merged Kaggle tables.
"""
from db import get_conn, init_db
from notifications import send_alert

def seed_all():
    init_db()
    with get_conn() as conn:
        # Seed Carriers
        if not conn.execute("SELECT count(*) FROM carriers").fetchone()[0]:
            carriers = [
                ("CAR-001", "Maersk Global Line", "Ocean", 0.94, 1.2, 12.5, 0.98, "Tier 1 (Apex)"),
                ("CAR-002", "MSC Mediterranean Shipping", "Ocean", 0.91, 1.8, 13.0, 0.96, "Tier 1 (Apex)"),
                ("CAR-003", "CMA CGM Logistics", "Ocean", 0.88, 2.4, 14.2, 0.92, "Tier 2 (Standard)"),
                ("CAR-004", "DHL Air Cargo Express", "Air", 0.99, 0.2, 18.0, 0.99, "Tier 1 (Apex)"),
                ("CAR-005", "FedEx International Freight", "Air", 0.98, 0.3, 17.5, 0.99, "Tier 1 (Apex)"),
                ("CAR-006", "DB Schenker Overland Rail", "Rail/Truck", 0.89, 2.1, 11.0, 0.94, "Tier 2 (Standard)"),
            ]
            conn.executemany("INSERT INTO carriers (carrier_id, carrier_name, transport_mode, "
            "punctuality_rate, avg_delay_days, fuel_surcharge_pct, "
            "tariff_compliance_score, tier_rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", carriers)

        # Seed Quotes
        if not conn.execute("SELECT count(*) FROM quotes").fetchone()[0]:
            quotes = [
                ("Q-1001", "infosys@ai", "Mumbai JNPT (IN)", "Rotterdam (NL)", 10500, 45.0, "Ocean", "High", "Electronics", 18500, 3200, 1.15, 24304, 0.96, "Moderate Risk (Monsoon)", "Passed Audit"),
                ("Q-1002", "infosys@ai", "Shanghai (CN)", "Mundra Port (IN)", 7800, 120.0, "Ocean", "Medium", "General Cargo", 42000, 4500, 1.05, 48360, 0.95, "Low Risk", "Passed Audit"),
                ("Q-1003", "infosys@ai", "Chennai Port (IN)", "Singapore (SG)", 4800, 15.0, "Air", "Low", "Pharmaceuticals", 31000, 0, 1.08, 33170, 0.98, "Minimal Risk", "Passed Audit"),
                ("Q-1004", "infosys@ai", "Cochin Port (IN)", "Dubai (AE)", 10800, 60.0, "Ocean", "High", "Chemicals", 26000, 5200, 1.12, 35880, 0.94, "High Risk (Squalls)", "Flagged Surcharge"),
            ]
            conn.executemany("INSERT INTO quotes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", quotes)

        # Seed Shipments
        if not conn.execute("SELECT count(*) FROM shipments").fetchone()[0]:
            shipments = [
                ("SH-8001", "Q-1001", "Maersk Global Line", 24304, 32, 2, "Delivered"),
                ("SH-8002", "Q-1002", "MSC Mediterranean Shipping", 48360, 24, 0, "Delivered"),
                ("SH-8003", "Q-1003", "DHL Air Cargo Express", 33170, 3, 0, "In Transit"),
                ("SH-8004", "Q-1004", "CMA CGM Logistics", 35880, 35, 5, "Delayed (Port Queue)"),
            ]
            conn.executemany("INSERT INTO shipments (shipment_id, quote_id, carrier_name, actual_cost, transit_days, delay_days, status) VALUES (?, ?, ?, ?, ?, ?, ?)", shipments)
            conn.commit()

    send_alert("Email", "admin@freightquote.ai", "System Initialized", "Database seeded with 6 carriers, quotes, and historical shipments.")
    print("✅ Database pre-seeded successfully.")
