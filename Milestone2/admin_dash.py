"""admin_dash.py — Shared Admin Dashboard renderer for FreightQuote & FranchiseOps AI"""
"""admin_dash.py — Shared Admin Dashboard renderer for FreightQuote & FranchiseOps AI"""
"""admin_dash.py — Shared Admin Dashboard renderer for FreightQuote & FranchiseOps AI"""
import subprocess, datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_conn
from notifications import get_recent_alerts
from ui_theme import render_card, COLORS

_APP_START = datetime.datetime.now()

def _smi(query):
    try:
        r = subprocess.run(
            ["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=3)
        return r.stdout.strip()
    except Exception:
        return "N/A"

def render_admin_dashboard(project="freight"):
    render_card('<h3 style="margin:0;font-family:\'Poppins\',sans-serif;font-weight:700;">🛡️ System Administration Console</h3>')

    tab_stats, tab_users, tab_model_card, tab_activity, tab_alerts = st.tabs([
        "📊 System Stats & KPIs",
        "👥 User Management",
        "📈 ML Model Card",
        "🤖 LLM Activity Monitor",
        "🔔 Live Alert Log"
    ])

    with get_conn() as conn:
        try:
            total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            active_users = conn.execute("SELECT COUNT(*) FROM users WHERE account_status = 'active'").fetchone()[0]
            locked_users = conn.execute("SELECT COUNT(*) FROM users WHERE account_status = 'locked' OR failed_attempts >= 5").fetchone()[0]
        except Exception:
            total_users = active_users = locked_users = 0

    # ── 1. System Stats & KPIs ───────────────────────────────────────────────
    with tab_stats:
        st.markdown(f'<h4 style="color:{COLORS["text_heading"]};margin:16px 0 12px;font-family:\'Poppins\',sans-serif;">⚙️ Engine Health & Live Overview</h4>',
                    unsafe_allow_html=True)
        gpu_mem  = _smi("memory.used")
        gpu_tot  = _smi("memory.total")
        gpu_util = _smi("utilization.gpu")
        uptime   = str(datetime.datetime.now() - _APP_START).split(".")[0]

        h1, h2, h3, h4 = st.columns(4)
        for col, icon, label, val, gradient in [
            (h1, "👥", "Total Users",     total_users,  "linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)"),
            (h2, "🟢", "Active Users",    active_users, "linear-gradient(135deg, #10B981 0%, #059669 100%)"),
            (h3, "🔴", "Locked Users",    locked_users, "linear-gradient(135deg, #EF4444 0%, #B91C1C 100%)"),
            (h4, "🕒", "App Uptime",      uptime,       "linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)"),
        ]:
            col.markdown(
                f'<div class="pn-card" style="background:{gradient} !important;color:#FFFFFF;text-align:center;padding:20px;border:none;">'
                f'<div style="font-size:30px;margin-bottom:8px;">{icon}</div>'
                f'<h3 style="margin:0 0 4px;font-size:1.6rem;color:#FFFFFF;font-family:\'Poppins\',sans-serif;font-weight:700;">{val}</h3>'
                f'<p style="margin:0;color:rgba(255,255,255,0.8);font-size:13px;font-weight:500;">{label}</p>'
                f'</div>', unsafe_allow_html=True)

        col_sys1, col_sys2 = st.columns(2)
        with col_sys1:
            st.markdown("##### 🖥️ GPU Resource Matrix")
            st.markdown(f"""
            - **VRAM Used:** {gpu_mem} / {gpu_tot} MB
            - **GPU Utilization:** {gpu_util}%
            - **LLM Status:** {"Active" if gpu_mem != "N/A" else "Standby"}
            """)
        with col_sys2:
            st.markdown("##### 🔌 Database Status")
            st.markdown(f"""
            - **Connection:** 🟢 SQLite Connected
            - **Engine Protocol:** HS256 JWT
            - **SMTP Dispatcher:** Gmail SSL Active
            """)

        # Recent Logins list
        st.markdown("##### 🕒 Recent User Logins")
        with get_conn() as conn:
            try:
                logins_df = pd.read_sql("SELECT username, role, last_login FROM users WHERE last_login IS NOT NULL ORDER BY last_login DESC LIMIT 5", conn)
                if not logins_df.empty:
                    st.dataframe(logins_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No recent logins tracked yet.")
            except Exception:
                st.info("No login metadata table found.")

        # Recent OTP Requests
        st.markdown("##### 🔑 Recent OTP Requests")
        with get_conn() as conn:
            try:
                otps_df = pd.read_sql("SELECT recipient, message, created_at FROM notifications WHERE subject LIKE '%OTP%' OR message LIKE '%OTP%' ORDER BY id DESC LIMIT 5", conn)
                if not otps_df.empty:
                    st.dataframe(otps_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No recent OTP requests logged.")
            except Exception:
                st.info("No OTP notification records found.")

    # ── 2. User Management ───────────────────────────────────────────────────
    with tab_users:
        st.markdown(f'<h4 style="color:{COLORS["text_heading"]};margin:16px 0 12px;font-family:\'Poppins\',sans-serif;">👥 User Directory</h4>',
                    unsafe_allow_html=True)
        with get_conn() as conn:
            try:
                users_df = pd.read_sql(
                    "SELECT id, username, role, email, failed_attempts, lock_until, account_status, last_login, created_at FROM users ORDER BY id DESC", conn)
            except Exception:
                users_df = pd.DataFrame(columns=["id","username","role","email","failed_attempts","lock_until","account_status","last_login","created_at"])

        if users_df.empty:
            st.info("No users registered yet.")
        else:
            for _, row in users_df.iterrows():
                uc1, uc2, uc3, uc4 = st.columns([2.5, 2, 2.5, 2])

                is_locked = False
                now = datetime.datetime.now()
                if row.get("account_status") == 'locked':
                    is_locked = True
                elif row.get("failed_attempts") is not None and row.get("failed_attempts") >= 5:
                    is_locked = True
                elif row.get("lock_until") is not None and row.get("lock_until") != "":
                    try:
                        lock_time = datetime.datetime.fromisoformat(str(row.get("lock_until")))
                        if now < lock_time:
                            is_locked = True
                    except Exception:
                        pass

                if is_locked:
                    status_badge = '<span style="border:1px solid #FCA5A5;background:#FEE2E2;color:#991B1B;padding:4px 10px;border-radius:9999px;font-size:12px;font-weight:600;">🔴 Locked</span>'
                else:
                    status_badge = '<span style="border:1px solid #6EE7B7;background:#D1FAE5;color:#065F46;padding:4px 10px;border-radius:9999px;font-size:12px;font-weight:600;">🟢 Active</span>'

                uc1.markdown(f"**{row['username']}**  \n`{row['email']}`")
                uc2.markdown(f'<span style="color:#0066cc;font-weight:600;">[{row["role"]}]</span>  \nStatus: {status_badge}',
                             unsafe_allow_html=True)
                uc3.markdown(f'<span style="color:{COLORS["text_muted"]};font-size:12px;">Last Login: {row.get("last_login") or "—"}  \nFailed Attempts: {row.get("failed_attempts", 0)}</span>', unsafe_allow_html=True)

                with uc4:
                    col_unlock, col_del = st.columns(2)
                    with col_unlock:
                        if is_locked:
                            if st.button("🔓 Unlock", key=f"unlock_{row['id']}", help=f"Unlock {row['username']}"):
                                with get_conn() as c:
                                    c.execute("UPDATE users SET failed_attempts=0, lock_until=NULL, account_status='active' WHERE id=?", (row["id"],))
                                    c.commit()
                                st.success("User unlocked successfully. ✅")
                                st.rerun()
                        else:
                            st.write("")
                    with col_del:
                        with st.popover("🗑️", help=f"Delete {row['username']}"):
                            st.write(f"Delete {row['username']}?")
                            if st.button("Confirm Delete", key=f"del_user_{row['id']}"):
                                with get_conn() as c:
                                    c.execute("DELETE FROM users WHERE id=?", (row["id"],))
                                    c.commit()
                                st.success(f"Deleted {row['username']}")
                                st.rerun()
                st.markdown("---")

        st.markdown("### ➕ Add User Portal")
        with st.form("add_user_form", clear_on_submit=True):
            st.write("Create a new user account with custom credentials:")
            new_username = st.text_input("Username", key="add_u_username")
            new_email = st.text_input("Email Address", key="add_u_email")
            new_password = st.text_input("Initial Password", type="password", key="add_u_pw")
            new_role = st.selectbox("Role", ["Admin", "Logistics Manager", "Pricing Analyst", "Carrier Auditor", "Executive"], key="add_u_role")
            new_q = st.selectbox("Security Question", [
                "What is your pet name?",
                "What city were you born in?",
                "What is your favorite school teacher's name?"
            ], key="add_u_q")
            new_a = st.text_input("Security Answer", key="add_u_a")
            submit_add = st.form_submit_button("Add User Account")
            if submit_add:
                if new_username and new_email and new_password and new_a:
                    from auth import hash_txt, check_password_strength
                    strength, allowed, msg = check_password_strength(new_password)
                    if not allowed:
                        st.error(msg)
                    else:
                        try:
                            with get_conn() as c:
                                c.execute(
                                    "INSERT INTO users (username, email, password_hash, security_question, security_answer_hash, role) VALUES (?, ?, ?, ?, ?, ?)",
                                    (new_username, new_email, hash_txt(new_password), new_q, hash_txt(new_a.lower().strip()), new_role)
                                )
                                c.commit()
                            st.success(f"User {new_username} added successfully! ✅")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error adding user: {e}")
                else:
                    st.error("Please fill in all fields.")

    # ── 3. ML Model Card ─────────────────────────────────────────────────────
    with tab_model_card:
        st.markdown(f'<h4 style="color:{COLORS["text_heading"]};margin:16px 0 12px;font-family:\'Poppins\',sans-serif;">📈 ML Model Card</h4>',
                    unsafe_allow_html=True)
        st.write("Compare trained algorithms and view the metrics of the saved champion models:")
        with get_conn() as conn:
            try:
                ml_all = pd.read_sql("SELECT id, agent_name, model_name, r2_score, rmse, accuracy, training_rows, created_at FROM ml_models ORDER BY id DESC", conn)
            except Exception:
                ml_all = pd.DataFrame()

        pricing_champ = None
        delay_champ = None
        carrier_champ = None

        if not ml_all.empty:
            p_df = ml_all[ml_all['agent_name'].str.contains('pricing|Agent1', case=False, na=False)]
            if not p_df.empty:
                pricing_champ = p_df.sort_values(by='r2_score', ascending=False).iloc[0]
            d_df = ml_all[ml_all['agent_name'].str.contains('delay|Agent2', case=False, na=False)]
            if not d_df.empty:
                delay_champ = d_df.sort_values(by='r2_score', ascending=False).iloc[0]
            c_df = ml_all[ml_all['agent_name'].str.contains('carrier|Agent3', case=False, na=False)]
            if not c_df.empty:
                carrier_champ = c_df.sort_values(by='r2_score', ascending=False).iloc[0]

        c_p, c_d, c_c = st.columns(3)
        with c_p:
            st.markdown("### 💰 Agent 1: Pricing")
            if pricing_champ is not None:
                st.markdown(f"""
                <div class="pn-card" style="border-left: 5px solid {COLORS['accent']};">
                    <h4 style="font-family:'Poppins',sans-serif;font-weight:600;margin:0 0 6px;">{pricing_champ['model_name']}</h4>
                    <p style="font-size:12px;color:{COLORS['text_muted']};margin:0 0 10px;">Champion Model (Regression)</p>
                    <hr style="margin: 8px 0; border:0; border-top:1px solid #EEE;">
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>R² Score:</span><strong>{pricing_champ['r2_score']:.4f}</strong></div>
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>RMSE:</span><strong>{pricing_champ['rmse']:.2f}</strong></div>
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>Training Rows:</span><strong>{pricing_champ['training_rows']}</strong></div>
                    <div style="display:flex;justify-content:space-between;font-size:10px;color:grey;margin-top:8px;padding-top:4px;border-top:1px solid #F3F4F6;"><span>Trained At:</span><span>{str(pricing_champ['created_at'])[:16]}</span></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No Pricing model metrics found.")
        with c_d:
            st.markdown("### 🚢 Agent 2: Route Delay")
            if delay_champ is not None:
                st.markdown(f"""
                <div class="pn-card" style="border-left: 5px solid {COLORS['green']};">
                    <h4 style="font-family:'Poppins',sans-serif;font-weight:600;margin:0 0 6px;">{delay_champ['model_name']}</h4>
                    <p style="font-size:12px;color:{COLORS['text_muted']};margin:0 0 10px;">Champion Model (Classification)</p>
                    <hr style="margin: 8px 0; border:0; border-top:1px solid #EEE;">
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>ROC-AUC:</span><strong>{delay_champ['r2_score']:.4f}</strong></div>
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>Accuracy:</span><strong>{delay_champ['accuracy']*100:.1f}%</strong></div>
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>Training Rows:</span><strong>{delay_champ['training_rows']}</strong></div>
                    <div style="display:flex;justify-content:space-between;font-size:10px;color:grey;margin-top:8px;padding-top:4px;border-top:1px solid #F3F4F6;"><span>Trained At:</span><span>{str(delay_champ['created_at'])[:16]}</span></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No Route Delay model metrics found.")
        with c_c:
            st.markdown("### ✅ Agent 3: Carrier Audit")
            if carrier_champ is not None:
                st.markdown(f"""
                <div class="pn-card" style="border-left: 5px solid {COLORS['red']};">
                    <h4 style="font-family:'Poppins',sans-serif;font-weight:600;margin:0 0 6px;">{carrier_champ['model_name']}</h4>
                    <p style="font-size:12px;color:{COLORS['text_muted']};margin:0 0 10px;">Champion Model (Classification)</p>
                    <hr style="margin: 8px 0; border:0; border-top:1px solid #EEE;">
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>ROC-AUC:</span><strong>{carrier_champ['r2_score']:.4f}</strong></div>
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>Accuracy:</span><strong>{carrier_champ['accuracy']*100:.1f}%</strong></div>
                    <div style="display:flex;justify-content:space-between;padding:3px 0;"><span>Training Rows:</span><strong>{carrier_champ['training_rows']}</strong></div>
                    <div style="display:flex;justify-content:space-between;font-size:10px;color:grey;margin-top:8px;padding-top:4px;border-top:1px solid #F3F4F6;"><span>Trained At:</span><span>{str(carrier_champ['created_at'])[:16]}</span></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No Carrier Audit model metrics found.")
        st.markdown("---")
        st.markdown("#### 📜 Model Audits History Log")
        if not ml_all.empty:
            st.dataframe(ml_all, use_container_width=True, hide_index=True)
        else:
            st.info("No history log available.")

    # ── 4. LLM Activity Monitor ──────────────────────────────────────────────
    with tab_activity:
        st.markdown(f'<h4 style="color:{COLORS["text_heading"]};margin:16px 0 12px;font-family:\'Poppins\',sans-serif;">🤖 LLM Activity Monitor</h4>',
                    unsafe_allow_html=True)
        with get_conn() as conn:
            try:
                chat_df = pd.read_sql(
                    "SELECT username, count(*) as queries FROM chat_history "
                    "WHERE role='user' GROUP BY username ORDER BY queries DESC", conn)
                total_q = int(chat_df["queries"].sum()) if not chat_df.empty else 0
            except Exception:
                chat_df = pd.DataFrame(columns=["username","queries"])
                total_q = 0

        mc1, mc2 = st.columns([1, 1.6])
        with mc1:
            st.metric("Total Copilot Queries", total_q)
            st.dataframe(chat_df, use_container_width=True, hide_index=True)
        with mc2:
            if not chat_df.empty:
                fig = px.pie(chat_df, names="username", values="queries",
                             title="Queries per User", hole=0.4,
                             color_discrete_sequence=px.colors.sequential.Teal)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  height=250, margin=dict(l=10,r=10,t=40,b=10),
                                  font=dict(family="Inter", size=11))
                st.plotly_chart(fig, use_container_width=True)

    # ── 5. Live Alert Log ────────────────────────────────────────────────────
    with tab_alerts:
        st.markdown(f'<h4 style="color:{COLORS["text_heading"]};margin:16px 0 12px;font-family:\'Poppins\',sans-serif;">🔔 Live Alert Log</h4>',
                    unsafe_allow_html=True)
        filt = st.selectbox("Filter by type", ["All","In-App","Email","SMS"], key="admin_alert_filt")
        alerts = get_recent_alerts(50)
        for a in alerts:
            if filt != "All" and a[1].lower() != filt.lower():
                continue
            badge = {"email":"#3B82F6","sms":"#EF4444","in-app":"#10B981"}.get(a[1].lower(),"#6B7280")
            st.markdown(
                f'<div style="border-left:4px solid {badge};padding:6px 12px;margin:6px 0;background:#FFFFFF;border-radius:0 8px 8px 0;'
                f'font-size:13px;box-shadow:0 1px 2px rgba(0,0,0,0.02);border-top:1px solid #F3F4F6;border-bottom:1px solid #F3F4F6;border-right:1px solid #F3F4F6;">'
                f'<b>[{a[1].upper()}]</b> {a[3]} '
                f'<span style="color:{COLORS["text_muted"]};float:right;font-size:11px;">{a[4]}</span></div>',
                unsafe_allow_html=True)
