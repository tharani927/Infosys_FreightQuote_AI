import sqlite3
from config import DB_PATH

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS carriers (
            carrier_id TEXT PRIMARY KEY, carrier_name TEXT, transport_mode TEXT,
            punctuality_rate REAL, avg_delay_days REAL, fuel_surcharge_pct REAL,
            tariff_compliance_score REAL, tier_rating TEXT, flagged INTEGER DEFAULT 0)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS quotes (
            quote_id TEXT PRIMARY KEY, created_by TEXT, origin TEXT, destination TEXT,
            distance_nm REAL, weight_tons REAL, shipment_mode TEXT, port_congestion TEXT,
            cargo_type TEXT, base_cost_usd REAL, margin_usd REAL, adjustment_factor REAL,
            final_cost_usd REAL, delay_risk_prob REAL, risk_summary TEXT, audit_flag TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS shipments (
            shipment_id TEXT PRIMARY KEY, quote_id TEXT, carrier_name TEXT,
            actual_cost REAL, transit_days INTEGER, delay_days INTEGER,
            status TEXT DEFAULT 'In Transit',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS merged_datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT, agent_target TEXT, dataset_source TEXT,
            origin TEXT, destination TEXT, distance_nm REAL, weight_tons REAL,
            freight_cost_usd REAL, shipment_mode TEXT, port_congestion TEXT,
            dwell_time_days REAL, berth_capacity INTEGER, weather_disruption_level REAL,
            carrier_punctuality REAL, fuel_surcharge_pct REAL, compliance_status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE,
            email TEXT UNIQUE, password_hash TEXT,
            security_question TEXT, security_answer_hash TEXT,
            role TEXT DEFAULT 'User',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

        # Add columns automatically if they do not exist
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]

        cols_to_add = {
            "failed_attempts": "INTEGER DEFAULT 0",
            "lock_until": "TIMESTAMP DEFAULT NULL",
            "account_status": "TEXT DEFAULT 'active'",
            "otp": "TEXT DEFAULT NULL",
            "otp_created_time": "TIMESTAMP DEFAULT NULL",
            "otp_resend_count": "INTEGER DEFAULT 0",
            "otp_next_allowed": "TIMESTAMP DEFAULT NULL",
            "otp_attempts": "INTEGER DEFAULT 0",
            "last_login": "TIMESTAMP DEFAULT NULL"
        }
        for col_name, col_type in cols_to_add.items():
            if col_name not in columns:
                try:
                    conn.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                except Exception as e:
                    print(f"Error adding column {col_name}: {e}")

        conn.execute("""CREATE TABLE IF NOT EXISTS ml_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT, model_name TEXT, r2_score REAL,
            rmse REAL, accuracy REAL, training_rows INTEGER,
            file_path TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT, recipient TEXT, subject TEXT, message TEXT,
            status TEXT DEFAULT 'Sent',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        conn.commit()

def save_ml_metrics(agent_name, model_name, r2, rmse, acc, rows, path):
    with get_conn() as conn:
        conn.execute("INSERT INTO ml_models "
                     "(agent_name,model_name,r2_score,rmse,accuracy,training_rows,file_path) "
                     "VALUES (?,?,?,?,?,?,?)",
                     (agent_name, model_name, r2, rmse, acc, rows, path))
        conn.commit()

def load_chat_history(username, conn_fn=None, limit=60):
    fn = conn_fn or get_conn
    with fn() as conn:
        rows = conn.execute(
            "SELECT role,content FROM chat_history WHERE username=? "
            "ORDER BY id DESC LIMIT ?", (username, limit)).fetchall()
    return [{"role":r[0],"content":r[1]} for r in reversed(rows)]

def save_chat_message(username, role, content, conn_fn=None):
    fn = conn_fn or get_conn
    with fn() as conn:
        conn.execute("INSERT INTO chat_history (username,role,content) VALUES (?,?,?)",
                     (username, role, content))
        conn.commit()

def clear_chat_history(username, conn_fn=None):
    fn = conn_fn or get_conn
    with fn() as conn:
        conn.execute("DELETE FROM chat_history WHERE username=?", (username,))
        conn.commit()
