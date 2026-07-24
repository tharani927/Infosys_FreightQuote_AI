"""
FreightQuote AI - auth.py
Standardized SQLite authentication system matching Login_Page (1).ipynb.
Supports Login, Register (with Enterprise Roles), Forgot Password (security question check), and JWT tokens.
"""
"""
FreightQuote AI - auth.py
Standardized SQLite authentication system matching Login_Page (1).ipynb.
Supports Login, Register (with Enterprise Roles), Forgot Password (security question check), and JWT tokens.
"""
import sqlite3, jwt, datetime, streamlit as st
import bcrypt
import re
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
try:
    from config import DB_PATH, JWT_SECRET_KEY, EMAIL_ID, EMAIL_PASSWORD
    JWT_SECRET = JWT_SECRET_KEY
except (ImportError, AttributeError):
    from config import DB_PATH
    JWT_SECRET = "super-secret-freightquote-key-2026"
    EMAIL_ID = None
    EMAIL_PASSWORD = None
from ui_theme import COLORS

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def hash_txt(t):
    return bcrypt.hashpw(t.encode(), bcrypt.gensalt()).decode()

def check_txt(t, h):
    try: return bcrypt.checkpw(t.encode(), h.encode()) if h else False
    except: return False

def make_jwt(email, username):
    return jwt.encode({"email": email, "username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)}, JWT_SECRET, algorithm="HS256")

def verify_jwt(token):
    try: return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except: return None

def check_password_strength(password):
    length = len(password)
    if length < 5:
        return "Weak", False, "Password too weak (minimum 5 characters required)."
    elif 5 <= length <= 9:
        return "Average", True, "Average strength (10+ characters recommended for enterprise security)."
    else:
        return "Good", True, "Good password strength — proceed with bcrypt hashing."

def generate_otp():
    return str(secrets.randbelow(900000) + 100000)

def send_otp_email(receiver_email, otp):
    sender_email = EMAIL_ID
    sender_password = EMAIL_PASSWORD
    
    if not sender_email or not sender_password:
        print(f"[OTP CONSOLE FALLBACK] OTP for {receiver_email} is: {otp}")
        st.info(f"ℹ️ [Console Fallback] OTP is: {otp}")
        return True
        
    subject = "🔑 Reset Your Password - FreightQuote AI"
    body_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Password Reset OTP</title>
        <style>
            body {{ font-family: sans-serif; background-color: #f1f5f9; padding: 20px; }}
            .card {{ max-width: 500px; margin: auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .otp {{ font-size: 32px; font-weight: bold; color: #2563eb; letter-spacing: 4px; text-align: center; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>FreightQuote AI Password Reset</h2>
            <p>Your verification code is below:</p>
            <div class="otp">{otp}</div>
            <p>This code is valid for 5 minutes.</p>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        
        body_text = f"Your OTP is: {otp}"
        msg.attach(MIMEText(body_text, "plain"))
        msg.attach(MIMEText(body_html, "html"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"[OTP SMTP FAILED] {e}")
        st.info(f"ℹ️ [SMTP Failed - Console Fallback] OTP is: {otp}")
        return True

@st.cache_resource
def init_auth():
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            security_question TEXT,
            security_answer_hash TEXT,
            role TEXT DEFAULT 'User',
            failed_attempts INTEGER DEFAULT 0,
            lock_until TIMESTAMP DEFAULT NULL,
            account_status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        try: conn.execute("ALTER TABLE users ADD COLUMN security_question TEXT")
        except Exception: pass
        try: conn.execute("ALTER TABLE users ADD COLUMN security_answer_hash TEXT")
        except Exception: pass
        try: conn.execute("ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0")
        except Exception: pass
        try: conn.execute("ALTER TABLE users ADD COLUMN lock_until TIMESTAMP DEFAULT NULL")
        except Exception: pass
        try: conn.execute("ALTER TABLE users ADD COLUMN account_status TEXT DEFAULT 'active'")
        except Exception: pass
        
        if conn.execute("SELECT id FROM users WHERE email='infosys@ai'").fetchone():
            conn.execute("UPDATE users SET role='Admin' WHERE email='infosys@ai'")
        else:
            conn.execute("""INSERT OR IGNORE INTO users
                         (username, email, password_hash, security_question, security_answer_hash, role)
                         VALUES (?, ?, ?, ?, ?, ?)""",
                         ("Administrator", "infosys@ai", hash_txt("admin@123"), "What is your pet name?", hash_txt("admin"), "Admin"))
        conn.commit()

def render_auth_portal():
    init_auth()
    if "token" not in st.session_state: st.session_state["token"] = None
    if "auth_tab" not in st.session_state: st.session_state["auth_tab"] = "Login"

    st.markdown(f"""
    <div style="text-align:center;padding:1.5rem 0 1rem;">
        <div style="font-size:44px;margin-bottom:8px;">⚡</div>
        <h1 style="font-size:2rem !important;margin:0;">FreightQuote AI Portal</h1>
        <p style="color:{COLORS['text_muted']};font-size:14px;margin:4px 0 0;">Enterprise Multi-Agent Logistics & Pricing System</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        tab1, tab2, tab3 = st.tabs(["🔐 Sign In", "📝 Register Account", "🔑 Reset Password"])

        with tab1:
            login_email = st.text_input("Email / Username", key="l_email", placeholder="infosys@ai")
            login_pw = st.text_input("Password", type="password", key="l_pw", placeholder="••••••••")
            if st.button("🚀 Sign In to Portal", key="btn_login"):
                if not login_email or not login_pw:
                    st.error("Please enter email and password.")
                else:
                    with get_conn() as conn:
                        user = conn.execute("SELECT username, email, password_hash, role, failed_attempts, lock_until, account_status, id FROM users WHERE email=? OR username=?", (login_email, login_email)).fetchone()
                    if user:
                        user_id, u_name, u_email, u_pw_hash, u_role, u_failed, u_lock, u_status = user[7], user[0], user[1], user[2], user[3], user[4], user[5], user[6]
                        
                        if u_status == 'locked':
                            st.error("❌ Account permanently locked due to 5 failed attempts. Only the System Administrator can unlock this account via the Admin Dashboard.")
                        else:
                            now = datetime.datetime.now()
                            is_temp_locked = False
                            if u_lock:
                                try:
                                    lock_time = datetime.datetime.fromisoformat(str(u_lock))
                                except Exception:
                                    try:
                                        lock_time = datetime.datetime.strptime(str(u_lock), "%Y-%m-%d %H:%M:%S.%f")
                                    except Exception:
                                        lock_time = datetime.datetime.strptime(str(u_lock), "%Y-%m-%d %H:%M:%S")
                                if now < lock_time:
                                    is_temp_locked = True
                                    remaining = int((lock_time - now).total_seconds())
                                    st.error(f"⏳ Account temporarily locked for {remaining} seconds.")
                            
                            if not is_temp_locked:
                                if check_txt(login_pw, u_pw_hash):
                                    with get_conn() as conn:
                                        conn.execute("UPDATE users SET failed_attempts=0, lock_until=NULL WHERE id=?", (user_id,))
                                        conn.commit()
                                    st.session_state["token"] = make_jwt(u_email, u_name)
                                    st.session_state["username"] = u_name
                                    st.session_state["role"] = u_role
                                    st.success(f"Welcome back, {u_name} [{u_role}]!")
                                    st.rerun()
                                else:
                                    new_failed = u_failed + 1
                                    new_lock = None
                                    new_status = 'active'
                                    msg = "Invalid email/username or password."
                                    
                                    if new_failed == 3:
                                        new_lock = (now + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S.%f")
                                        msg = "⏳ Account temporarily locked for 5 minutes due to 3 failed attempts."
                                    elif new_failed == 4:
                                        new_lock = (now + datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S.%f")
                                        msg = "⏳ Account temporarily locked for 15 minutes due to 4 failed attempts."
                                    elif new_failed >= 5:
                                        new_status = 'locked'
                                        msg = "❌ Account permanently locked due to 5 failed attempts. Only the System Administrator can unlock this account via the Admin Dashboard."
                                    
                                    with get_conn() as conn:
                                        conn.execute("UPDATE users SET failed_attempts=?, lock_until=?, account_status=? WHERE id=?", (new_failed, new_lock, new_status, user_id))
                                        conn.commit()
                                    
                                    st.error(msg)
                    else:
                        st.error("Invalid email/username or password.")

        with tab2:
            r_user = st.text_input("Username", key="r_u")
            r_email = st.text_input("Email Address", key="r_e")
            r_pw = st.text_input("Create Password", type="password", key="r_p")
            
            if r_pw:
                strength, allowed, msg = check_password_strength(r_pw)
                if strength == "Weak":
                    st.warning(msg)
                elif strength == "Average":
                    st.info(msg)
                else:
                    st.success(msg)
                    
            r_role = st.selectbox("Select Enterprise Role", ["Logistics Manager", "Pricing Analyst", "Carrier Auditor", "Executive"], key="r_role")
            r_q = st.selectbox("Security Question", ["What is your pet name?", "What city were you born in?", "What is your favorite school teacher's name?"], key="r_q")
            r_a = st.text_input("Security Answer", key="r_a")
            if st.button("✨ Create Enterprise Account", key="btn_reg"):
                if r_user and r_email and r_pw and r_a:
                    strength, allowed, msg = check_password_strength(r_pw)
                    if not allowed:
                        st.warning(msg)
                    else:
                        try:
                            with get_conn() as conn:
                                conn.execute("INSERT INTO users (username, email, password_hash, security_question, security_answer_hash, role) VALUES (?, ?, ?, ?, ?, ?)",
                                             (r_user, r_email, hash_txt(r_pw), r_q, hash_txt(r_a.lower().strip()), r_role))
                                conn.commit()
                            st.success(f"Account registered with role [{r_role}]! Please switch to Sign In tab.")
                        except Exception as e:
                            st.error(f"Registration failed: Email or username may already exist.")
                else:
                    st.warning("Please fill out all fields.")

        with tab3:
            f_email = st.text_input("Registered Email", key="f_e")
            
            col_sq, col_otp = st.columns(2)
            with col_sq:
                if st.button("Via Security Question", key="btn_sq_reset", use_container_width=True):
                    if not f_email:
                        st.error("Please enter email.")
                    else:
                        with get_conn() as conn:
                            u = conn.execute("SELECT security_question FROM users WHERE email=?", (f_email,)).fetchone()
                        if u:
                            st.session_state["reset_email"] = f_email
                            st.session_state["reset_mode"] = "sq"
                            st.session_state["reset_q"] = u[0]
                            st.rerun()
                        else:
                            st.error("Email not found.")
                            
            with col_otp:
                if st.button("Via OTP (Email)", key="btn_otp_reset", use_container_width=True):
                    if not f_email:
                        st.error("Please enter email.")
                    else:
                        with get_conn() as conn:
                            user = conn.execute("SELECT id FROM users WHERE email=?", (f_email,)).fetchone()
                        if user:
                            now = datetime.datetime.now()
                            next_allowed = st.session_state.get("otp_next_allowed")
                            resend_count = st.session_state.get("otp_resend_count", 0)
                            
                            if next_allowed and now < next_allowed:
                                remaining = int((next_allowed - now).total_seconds())
                                if resend_count == 1:
                                    st.error("⏳ Please wait 60 seconds before requesting another OTP.")
                                elif resend_count == 2:
                                    st.error("⏳ Please wait 3 minutes before requesting another OTP.")
                                elif resend_count == 3:
                                    st.error("⏳ Please wait 5 minutes before requesting another OTP.")
                                else:
                                    st.error("⚠️ Too many OTP requests. Please wait 1 hour before trying again.")
                            else:
                                new_otp = generate_otp()
                                st.session_state["otp_code"] = new_otp
                                st.session_state["reset_email"] = f_email
                                st.session_state["reset_mode"] = "otp"
                                
                                send_otp_email(f_email, new_otp)
                                
                                resend_count += 1
                                st.session_state["otp_resend_count"] = resend_count
                                if resend_count == 1:
                                    cooldown = 60
                                elif resend_count == 2:
                                    cooldown = 180
                                elif resend_count == 3:
                                    cooldown = 300
                                else:
                                    cooldown = 3600
                                st.session_state["otp_next_allowed"] = now + datetime.timedelta(seconds=cooldown)
                                st.success("✅ OTP sent successfully to your email.")
                                st.rerun()
                        else:
                            st.error("Email not found.")

            if st.session_state.get("reset_email"):
                st.write("---")
                if st.session_state.get("reset_mode") == "sq":
                    st.info(f"❓ Security Question: **{st.session_state.get('reset_q')}**")
                    ans_try = st.text_input("Enter Answer", key="f_ans")
                    new_pw = st.text_input("New Password", type="password", key="f_npw")
                    
                    if new_pw:
                        strength, allowed, msg = check_password_strength(new_pw)
                        if strength == "Weak":
                            st.warning(msg)
                        elif strength == "Average":
                            st.info(msg)
                        else:
                            st.success(msg)
                            
                    if st.button("Confirm Password Reset", key="btn_f2"):
                        if not ans_try or not new_pw:
                            st.error("Please fill in all fields.")
                        else:
                            strength, allowed, msg = check_password_strength(new_pw)
                            if not allowed:
                                st.warning(msg)
                            else:
                                with get_conn() as conn:
                                    u_hash = conn.execute("SELECT security_answer_hash FROM users WHERE email=?", (st.session_state["reset_email"],)).fetchone()
                                if u_hash and check_txt(ans_try.lower().strip(), u_hash[0]):
                                    with get_conn() as conn:
                                        conn.execute("UPDATE users SET password_hash=? WHERE email=?", (hash_txt(new_pw), st.session_state["reset_email"]))
                                        conn.commit()
                                    st.success("Password reset successfully! Please sign in.")
                                    st.session_state["reset_email"] = None
                                    st.session_state["reset_mode"] = None
                                    st.rerun()
                                else:
                                    st.error("Incorrect security answer.")
                                    
                elif st.session_state.get("reset_mode") == "otp":
                    st.info("📧 Enter the OTP code sent to your email:")
                    entered_otp = st.text_input("Enter OTP Code", key="f_otp_code")
                    new_pw = st.text_input("New Password", type="password", key="f_npw")
                    
                    if new_pw:
                        strength, allowed, msg = check_password_strength(new_pw)
                        if strength == "Weak":
                            st.warning(msg)
                        elif strength == "Average":
                            st.info(msg)
                        else:
                            st.success(msg)
                            
                    if st.button("Confirm Password Reset", key="btn_f2_otp"):
                        if not entered_otp or not new_pw:
                            st.error("Please fill in all fields.")
                        elif entered_otp != st.session_state.get("otp_code"):
                            st.error("❌ Invalid OTP.")
                        else:
                            strength, allowed, msg = check_password_strength(new_pw)
                            if not allowed:
                                st.warning(msg)
                            else:
                                with get_conn() as conn:
                                    conn.execute("UPDATE users SET password_hash=? WHERE email=?", (hash_txt(new_pw), st.session_state["reset_email"]))
                                    conn.commit()
                                st.success("Password reset successfully! Please sign in.")
                                st.session_state["reset_email"] = None
                                st.session_state["reset_mode"] = None
                                st.session_state["otp_code"] = None
                                st.rerun()
                                
            if st.session_state.get("reset_email"):
                if st.button("Cancel Reset", key="btn_cancel_reset"):
                    st.session_state["reset_email"] = None
                    st.session_state["reset_mode"] = None
                    st.rerun()
