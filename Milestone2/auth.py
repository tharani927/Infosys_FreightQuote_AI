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
            otp TEXT DEFAULT NULL,
            otp_created_time TIMESTAMP DEFAULT NULL,
            otp_resend_count INTEGER DEFAULT 0,
            otp_next_allowed TIMESTAMP DEFAULT NULL,
            otp_attempts INTEGER DEFAULT 0,
            last_login TIMESTAMP DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        # Ensure default account always has Admin role
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

    # Inject styling for auth layout
    st.markdown(f"""
    <style>
    .auth-card {{
        background: rgba(255, 255, 255, 0.85) !important;
        border: 1px solid rgba(229, 231, 235, 0.5) !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
        backdrop-filter: blur(12px) !important;
        margin-top: 10px;
    }}
    .auth-logo {{
        background: linear-gradient(135deg, #0B1220 0%, #1E293B 100%);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 24px;
        color: #FFFFFF;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #1E293B;
    }}
    </style>
    <div class="auth-logo">
        <div style="font-size:52px;margin-bottom:12px;">⚡</div>
        <h1 style="font-size:2.2rem !important;margin:0;color:#FFFFFF;font-family:'Poppins',sans-serif;font-weight:700;">FreightQuote AI</h1>
        <p style="color:#94A3B8;font-size:15px;margin:8px 0 0;font-weight:400;">Enterprise Multi-Agent Logistics & Pricing System</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["🔐 Sign In", "📝 Register Account", "🔑 Reset Password"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            login_email = st.text_input("Email / Username", key="l_email", placeholder="infosys@ai")
            login_pw = st.text_input("Password", type="password", key="l_pw", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
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
                                        conn.execute("UPDATE users SET failed_attempts=0, lock_until=NULL, account_status='active', last_login=? WHERE id=?", (now.strftime("%Y-%m-%d %H:%M:%S"), user_id))
                                        conn.commit()
                                    st.session_state["token"] = make_jwt(u_email, u_name)
                                    st.session_state["username"] = u_name
                                    st.session_state["role"] = u_role
                                    st.success(f"Welcome back, {u_name} [{u_role}]!")
                                    st.rerun()
                                else:
                                    new_failed = (u_failed or 0) + 1
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
            st.markdown("<br>", unsafe_allow_html=True)
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
            st.markdown("<br>", unsafe_allow_html=True)
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
            st.markdown("<br>", unsafe_allow_html=True)
            f_email = st.text_input("Registered Email", key="f_e")
            st.markdown("<br>", unsafe_allow_html=True)

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
                            user = conn.execute("SELECT otp_resend_count, otp_next_allowed FROM users WHERE email=?", (f_email,)).fetchone()
                        if user:
                            now = datetime.datetime.now()
                            u_resends, u_next = user[0], user[1]

                            # Check resend cooldown
                            is_cooldown_active = False
                            if u_next:
                                try:
                                    next_time = datetime.datetime.fromisoformat(str(u_next))
                                except Exception:
                                    try:
                                        next_time = datetime.datetime.strptime(str(u_next), "%Y-%m-%d %H:%M:%S.%f")
                                    except Exception:
                                        next_time = datetime.datetime.strptime(str(u_next), "%Y-%m-%d %H:%M:%S")
                                if now < next_time:
                                    is_cooldown_active = True
                                    remaining = int((next_time - now).total_seconds())

                            if is_cooldown_active:
                                if u_resends == 1:
                                    st.error("⏳ Please wait 60 seconds before requesting another OTP.")
                                elif u_resends == 2:
                                    st.error("⏳ Please wait 3 minutes before requesting another OTP.")
                                elif u_resends == 3:
                                    st.error("⏳ Please wait 5 minutes before requesting another OTP.")
                                else:
                                    st.error("⚠️ Too many OTP requests. Please wait 1 hour before trying again.")
                            else:
                                new_otp = generate_otp()
                                new_resends = (u_resends or 0) + 1

                                # Set cooldown durations
                                if new_resends == 1:
                                    cooldown = 60
                                elif new_resends == 2:
                                    cooldown = 180
                                elif new_resends == 3:
                                    cooldown = 300
                                else:
                                    cooldown = 3600

                                next_allowed_time = (now + datetime.timedelta(seconds=cooldown)).strftime("%Y-%m-%d %H:%M:%S.%f")

                                with get_conn() as conn:
                                    conn.execute("UPDATE users SET otp=?, otp_created_time=?, otp_resend_count=?, otp_next_allowed=?, otp_attempts=0 WHERE email=?",
                                                 (new_otp, now.strftime("%Y-%m-%d %H:%M:%S.%f"), new_resends, next_allowed_time, f_email))
                                    conn.commit()

                                send_otp_email(f_email, new_otp)
                                st.session_state["reset_email"] = f_email
                                st.session_state["reset_mode"] = "otp"
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
                        else:
                            # Retrieve OTP details
                            with get_conn() as conn:
                                u_data = conn.execute("SELECT otp, otp_created_time, otp_attempts FROM users WHERE email=?", (st.session_state["reset_email"],)).fetchone()

                            if u_data:
                                db_otp, db_time, db_attempts = u_data[0], u_data[1], u_data[2]
                                new_attempts = (db_attempts or 0) + 1

                                # Update attempts immediately
                                with get_conn() as conn:
                                    conn.execute("UPDATE users SET otp_attempts=? WHERE email=?", (new_attempts, st.session_state["reset_email"]))
                                    conn.commit()

                                now = datetime.datetime.now()
                                try:
                                    created_time = datetime.datetime.fromisoformat(str(db_time))
                                except Exception:
                                    try:
                                        created_time = datetime.datetime.strptime(str(db_time), "%Y-%m-%d %H:%M:%S.%f")
                                    except Exception:
                                        created_time = datetime.datetime.strptime(str(db_time), "%Y-%m-%d %H:%M:%S")

                                # Verify max attempts (max 3 verification attempts)
                                if new_attempts > 3:
                                    with get_conn() as conn:
                                        conn.execute("UPDATE users SET otp=NULL, otp_created_time=NULL, otp_attempts=0 WHERE email=?", (st.session_state["reset_email"],))
                                        conn.commit()
                                    st.error("❌ Maximum verification attempts exceeded. Please request a new OTP.")
                                # Check expiry (5 minutes)
                                elif (now - created_time).total_seconds() > 300:
                                    with get_conn() as conn:
                                        conn.execute("UPDATE users SET otp=NULL, otp_created_time=NULL, otp_attempts=0 WHERE email=?", (st.session_state["reset_email"],))
                                        conn.commit()
                                    st.error("❌ OTP has expired. Please request a new OTP.")
                                # Verify OTP match
                                elif entered_otp != db_otp:
                                    st.error(f"❌ Invalid OTP. Attempt {new_attempts} of 3.")
                                else:
                                    # Success
                                    strength, allowed, msg = check_password_strength(new_pw)
                                    if not allowed:
                                        st.warning(msg)
                                    else:
                                        with get_conn() as conn:
                                            conn.execute("UPDATE users SET password_hash=?, otp=NULL, otp_created_time=NULL, otp_attempts=0, otp_resend_count=0, otp_next_allowed=NULL WHERE email=?",
                                                         (hash_txt(new_pw), st.session_state["reset_email"]))
                                            conn.commit()
                                        st.success("Password reset successfully! Please sign in.")
                                        st.session_state["reset_email"] = None
                                        st.session_state["reset_mode"] = None
                                        st.rerun()
                            else:
                                st.error("Reset session not found. Please verify email again.")

            if st.session_state.get("reset_email"):
                if st.button("Cancel Reset", key="btn_cancel_reset"):
                    st.session_state["reset_email"] = None
                    st.session_state["reset_mode"] = None
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
