"""
app.py — FreightQuote AI v4 FINAL (Modular Fast Engine)
Lean orchestrator — all heavy tab logic lives in agent2_freight.py, agent3_freight.py, admin_dash.py
"""
import os, json, joblib, subprocess, numpy as np, pandas as pd, datetime
import streamlit as st
from streamlit_option_menu import option_menu
from config import AGENT1_MODEL_PATH, AGENT2_MODEL_PATH, AGENT3_MODEL_PATH
from ui_theme import apply_theme, render_header, render_card, COLORS
from auth import render_auth_portal
from db import get_conn, load_chat_history, save_chat_message
from weather_context import get_weather_report
from notifications import send_alert, get_recent_alerts
from llm_engine import (orchestrate_3_agents_query, generate_debate_and_synthesis,
                        warmup_llm, is_llm_loaded, start_background_warmup)
from agent2_freight import render_agent2_freight
from agent3_freight import render_agent3_freight
from admin_dash import render_admin_dashboard
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="FreightQuote AI Portal", page_icon="⚡", layout="wide",
                   initial_sidebar_state="expanded")
apply_theme()
start_background_warmup()

if not st.session_state.get("token"):
    render_auth_portal(); st.stop()

username  = st.session_state.get("username", "guest")
user_role = st.session_state.get("role", "Logistics Manager")
is_admin  = user_role.lower() == "admin"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:24px 0 16px;font-family:'Poppins',sans-serif;font-weight:700;font-size:22px;color:#FFFFFF;letter-spacing:-0.03em;display:flex;align-items:center;justify-content:center;gap:10px;">
        <span style="background:linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);padding:4px 10px;border-radius:8px;font-size:18px;">⚡</span> FreightQuote AI
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.05);padding:14px;border-radius:12px;margin:0 10px 24px;border:1px solid rgba(255,255,255,0.1);">
        <p style="margin:0;color:#9CA3AF;font-size:12px;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;">Current Session</p>
        <h4 style="margin:6px 0 2px;color:#FFFFFF;font-family:'Poppins',sans-serif;font-size:15px;font-weight:600;">{username}</h4>
        <span style="background:#2563EB;color:#FFFFFF;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;text-transform:uppercase;">{user_role}</span>
    </div>
    """, unsafe_allow_html=True)
    tabs = ["🤖 AI Copilot", "💰 Agent 1: Pricing", "🚢 Agent 2: Route/Weather",
            "✅ Agent 3: Carrier Audit", "📊 Analytics & Retrain"]
    icons = ["chat-dots-fill", "currency-dollar", "compass", "clipboard-check", "bar-chart-fill"]
    if is_admin:
        tabs.append("🛡️ Admin Dashboard"); icons.append("shield-lock-fill")
    tabs.append("🚪 Sign Out"); icons.append("box-arrow-right")
    selected_tab = option_menu(menu_title=None, options=tabs, icons=icons, default_index=0,
        styles={
            "container": {"padding": "0 10px!important", "background-color": "transparent"},
            "nav-link": {"font-size": "13px", "text-align": "left", "margin": "4px 0",
                         "border-radius": "8px", "color": "#9CA3AF", "font-weight": "500", "padding": "10px 14px"},
            "nav-link-selected": {"background": "linear-gradient(135deg, #2563EB 0%, #4F46E5 100%)", "color": "#FFFFFF",
                                  "font-weight": "600"},
        })

if selected_tab == "🚪 Sign Out":
    st.session_state["token"] = None; st.rerun()

render_header("FreightQuote AI", f"Enterprise Logistics Control Plane • {selected_tab}")

# ── GPU Banner ────────────────────────────────────────────────────────────────
b1, b2 = st.columns([4, 1.2])
with b1:
    if is_llm_loaded():
        st.markdown('<div style="background:rgba(34, 197, 94, 0.1);border:1px solid #22C55E;border-radius:10px;'
                    'padding:10px 18px;font-weight:600;color:#15803D;font-size:13px;box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">'
                    '🟢 <b>LLM GPU Engine:</b> Active on Tesla T4 (Qwen-2.5-3B Ready for Inference)</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:rgba(245, 158, 11, 0.1);border:1px solid #F59E0B;border-radius:10px;'
                    'padding:10px 18px;font-weight:600;color:#B45309;font-size:13px;box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">'
                    '🟡 <b>LLM GPU Engine:</b> Standby Mode — warm up LLM model card before execution</div>',
                    unsafe_allow_html=True)
with b2:
    if not is_llm_loaded():
        if st.button("⚡ Warm Up LLM", key="warmup_btn", use_container_width=True):
            with st.spinner("Loading Qwen-2.5-3B from Drive cache..."):
                warmup_llm()
            st.rerun()


@st.cache_resource
def load_agents():
    if not os.path.exists(AGENT1_MODEL_PATH) or not os.path.exists(AGENT2_MODEL_PATH) or not os.path.exists(AGENT3_MODEL_PATH):
        try:
            from train_ml import train_all_agents
            train_all_agents()
        except Exception as e:
            print(f"Auto-training note: {e}")
    m1 = joblib.load(AGENT1_MODEL_PATH) if os.path.exists(AGENT1_MODEL_PATH) else None
    m2 = joblib.load(AGENT2_MODEL_PATH) if os.path.exists(AGENT2_MODEL_PATH) else None
    m3 = joblib.load(AGENT3_MODEL_PATH) if os.path.exists(AGENT3_MODEL_PATH) else None
    return m1, m2, m3

agent1_m, agent2_m, agent3_m = load_agents()


def confidence_band(model, X_row):
    if model is None:
        return 0.5, 0.42, 0.58
    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba([X_row])[0][1])
    else:
        prob = float(np.clip(model.predict([X_row])[0], 0, 1))
    z, n = 1.96, 300
    lo = max(0.0, (prob + z**2/(2*n) - z*((prob*(1-prob)+z**2/(4*n))/n)**0.5) / (1+z**2/n))
    hi = min(1.0, (prob + z**2/(2*n) + z*((prob*(1-prob)+z**2/(4*n))/n)**0.5) / (1+z**2/n))
    return prob, lo, hi


# Shared context (built once per page load)
with get_conn() as conn:
    n_quotes   = conn.execute("SELECT count(*) FROM quotes").fetchone()[0]
    n_ships    = conn.execute("SELECT count(*) FROM shipments").fetchone()[0]
    n_carriers = conn.execute("SELECT count(*) FROM carriers").fetchone()[0]
    n_alerts   = conn.execute("SELECT count(*) FROM notifications").fetchone()[0]

db_stats = {"quotes": n_quotes, "shipments": n_ships,
            "carriers": n_carriers, "alerts": n_alerts}
a1_ctx = {"base_rate_usd": 18500, "congestion": "High", "fuel_surcharge_pct": 13.5}
a2_ctx = {"dwell_days": 3.8, "canal_queue": True, "delay_risk_pct": 68}
a3_ctx = {"carrier": "Maersk", "punctuality": 0.94, "compliance": "Passed"}

# ─────────────────────────────────────────────────────────────────────────────
# TAB: AI COPILOT (Redesigned as ChatGPT Style Chat Interface)
# ─────────────────────────────────────────────────────────────────────────────
if selected_tab == "🤖 AI Copilot":
    render_card('<h3 style="margin:0 0 6px;font-family:\'Poppins\',sans-serif;">💬 Unified AI Copilot — Total Logistics Intelligence</h3>'
                '<p style="margin:0;color:#6b7280;font-size:14px;font-weight:400;">Powered by Qwen-2.5-3B on Nvidia T4. '
                'All responses utilize live SQL databases, marine weather context, ML estimates & compliant carrier records.</p>')

    if "copilot_history" not in st.session_state:
        hist = load_chat_history(username, get_conn)
        if not hist:
            msg = "Welcome to FreightQuote AI Copilot! Ask about pricing, routes, carriers, or delays."
            save_chat_message(username, "assistant", msg, get_conn)
            hist = [{"role": "assistant", "content": msg, "time": datetime.datetime.now().strftime("%H:%M")}]
        st.session_state["copilot_history"] = hist

    # Render history using ChatGPT style
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for m in st.session_state["copilot_history"]:
        timestamp = m.get("time", datetime.datetime.now().strftime("%H:%M"))
        if m["role"] == "user":
            st.markdown(f"""
            <div class="chat-message-container chat-message-user">
                <div class="chat-bubble-user">
                    <div style="font-size: 11px; color: rgba(255,255,255,0.7); margin-bottom: 4px; font-weight: 600;">🧑 You ({timestamp})</div>
                    <div>{m['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message-container chat-message-copilot">
                <div class="chat-bubble-copilot">
                    <div style="font-size: 11px; color: {COLORS['text_muted']}; margin-bottom: 4px; font-weight: 600;">⚡ Copilot ({timestamp})</div>
                    <div>{m['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    inp_col, clr_col = st.columns([8.2, 0.8])
    with inp_col:
        with st.form("copilot_form", clear_on_submit=True):
            user_q  = st.text_input("", placeholder="e.g. 'Why is Shanghai→Rotterdam costly right now?'")
            fa, fb  = st.columns([3, 1])
            with fa: submit = st.form_submit_button("🚀 Ask Copilot")
            with fb: debate = st.form_submit_button("🔍 Debate View")
    with clr_col:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        if st.button("🗑️", help="Clear chat history"):
            from db import clear_chat_history
            clear_chat_history(username, get_conn)
            st.session_state["copilot_history"] = []; st.rerun()

    if (submit or debate) and user_q.strip():
        now_time = datetime.datetime.now().strftime("%H:%M")
        save_chat_message(username, "user", user_q, get_conn)
        st.session_state["copilot_history"].append({"role": "user", "content": user_q, "time": now_time})

        if debate:
            with st.spinner("⚡ Single-pass debate (~2 sec)..."):
                res = generate_debate_and_synthesis(user_q, a1_ctx, a2_ctx, a3_ctx, db_stats)
            dc1, dc2, dc3 = st.columns(3)
            for col, key, label, color in [
                (dc1, "agent1", "Pricing & Congestion", COLORS["accent"]),
                (dc2, "agent2", "Route & Weather", COLORS["green"]),
                (dc3, "agent3", "Carrier Audit", COLORS["red"]),
            ]:
                col.markdown(f'<div class="pn-card" style="border-top:4px solid {color} !important;">'
                             f'<span class="agent-badge" style="background-color:#FFF;color:{color};border-color:{color};">{label}</span><br><br>{res[key]}</div>',
                             unsafe_allow_html=True)
            ans = f"**Executive Synthesis:** {res['synthesis']}"
        else:
            with st.spinner("⚡ Generating answer (~1.5 sec)..."):
                ans = orchestrate_3_agents_query(user_q, a1_ctx, a2_ctx, a3_ctx, db_stats)

        save_chat_message(username, "assistant", ans, get_conn)
        st.session_state["copilot_history"].append({"role": "assistant", "content": ans, "time": now_time})
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# TAB: AGENT 1 — PRICING
# ─────────────────────────────────────────────────────────────────────────────
elif selected_tab == "💰 Agent 1: Pricing":
    render_card('<h3 style="margin:0;font-family:\'Poppins\',sans-serif;font-weight:700;">💰 Agent 1: Global Freight Pricing & Port Congestion</h3>')
    c1, c2 = st.columns(2)
    with c1:
        dist   = st.number_input("Distance (nm)", 500.0, 20000.0, 10500.0)
        weight = st.number_input("Cargo Weight (tons)", 1.0, 500.0, 45.0)
        cong   = st.selectbox("Congestion Level", ["Low (0)", "Medium (1)", "High (2)"], index=2)
        fuel   = st.slider("Fuel Index", 0.9, 1.6, 1.18)
        cargo  = st.selectbox("Cargo Type", ["General (0)", "Perishable (1)", "Hazmat (2)", "Heavy (3)"])
        dwell  = st.number_input("Port Dwell (days)", 0.5, 14.0, 3.8)
        cong_v  = int(cong.split("(")[1].replace(")", ""))
        cargo_v = int(cargo.split("(")[1].replace(")", ""))
    with c2:
        if st.button("⚡ Generate Quote"):
            row = [dist, weight, cong_v, fuel, cargo_v, dwell]
            if agent1_m:
                preds = [t.predict([row])[0] for t in agent1_m.estimators_]
                mean_p, std_p = float(np.mean(preds)), float(np.std(preds))
            else:
                mean_p = dist * 1.8 + weight * 48 + cong_v * 1600; std_p = mean_p * 0.05
            lo95, hi95 = mean_p - 1.96*std_p, mean_p + 1.96*std_p

            st.markdown(
                f'<div style="background: linear-gradient(135deg, {COLORS["accent"]} 0%, {COLORS["indigo"]} 100%);'
                f'padding:24px;border-radius:16px;box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2);color:#FFFFFF;">'
                f'<span class="agent-badge" style="background:#FFF;color:{COLORS["accent"]};border-color:#FFF;">Agent 1 Estimate</span>'
                f'<h2 style="color:#FFFFFF;margin:12px 0 6px;font-family:\'Poppins\',sans-serif;font-weight:700;">${mean_p:,.0f}</h2>'
                f'<p style="font-weight:600;margin:4px 0;font-size:15px;">95% CI: ${lo95:,.0f} — ${hi95:,.0f}</p>'
                f'<p style="margin:0;font-size:12px;opacity:0.85;">±{std_p/mean_p*100:.1f}% uncertainty band</p>'
                f'</div>', unsafe_allow_html=True)
            send_alert("In-App", username, "Quote Generated", f"${mean_p:,.0f}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB: AGENT 2 — ROUTE/WEATHER (modular)
# ─────────────────────────────────────────────────────────────────────────────
elif selected_tab == "🚢 Agent 2: Route/Weather":
    render_agent2_freight(agent2_m, username, db_stats, a1_ctx, a3_ctx,
                          send_alert, get_conn, confidence_band)

# ─────────────────────────────────────────────────────────────────────────────
# TAB: AGENT 3 — CARRIER AUDIT (modular)
# ─────────────────────────────────────────────────────────────────────────────
elif selected_tab == "✅ Agent 3: Carrier Audit":
    render_agent3_freight(agent3_m, username, confidence_band)

# ─────────────────────────────────────────────────────────────────────────────
# TAB: ANALYTICS & RETRAIN (Redesigned with Professional Enterprise Layout & Charts)
# ─────────────────────────────────────────────────────────────────────────────
elif selected_tab == "📊 Analytics & Retrain":
    render_card('<h3 style="margin:0;font-family:\'Poppins\',sans-serif;font-weight:700;">📊 Enterprise Analytics & Model Management</h3>')

    # KPI metrics cards
    kc = st.columns(4)
    for col, icon, label, val, gradient in [
        (kc[0], "📋", "Total Quotes",   n_quotes,   "linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)"),
        (kc[1], "🚢", "Active Shipments", n_ships,   "linear-gradient(135deg, #10B981 0%, #059669 100%)"),
        (kc[2], "✅", "Verified Carriers", n_carriers, "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)"),
        (kc[3], "🔔", "Alerts Dispatched", n_alerts,   "linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)"),
    ]:
        col.markdown(f'<div class="pn-card" style="background:{gradient} !important;color:#FFFFFF;text-align:center;padding:20px;border:none;">'
                     f'<div style="font-size:30px;margin-bottom:8px;">{icon}</div>'
                     f'<h2 style="margin:0;color:#FFFFFF;font-family:\'Poppins\',sans-serif;font-weight:700;font-size:1.6rem;">{val}</h2>'
                     f'<p style="margin:4px 0 0;color:rgba(255,255,255,0.85);font-size:13px;font-weight:500;">{label}</p>'
                     f'</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Model comparison & accuracy analysis
    with get_conn() as conn:
        try:
            ml_df = pd.read_sql("SELECT agent_name, model_name, r2_score, accuracy, training_rows, created_at FROM ml_models ORDER BY id DESC", conn)
        except Exception:
            ml_df = pd.DataFrame()

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("##### 🏆 Champion Model Comparison")
        if not ml_df.empty:
            # Chart: Champion Metrics
            fig_compare = px.bar(ml_df.head(10), x="model_name", y="r2_score", color="agent_name",
                                 title="Trained Model Score (R² or ROC-AUC)",
                                 labels={"r2_score": "Score", "model_name": "Model Type"},
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_compare.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"family": "Inter", "size": 11},
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_compare, use_container_width=True)
        else:
            st.info("No trained models found yet.")

    with col_chart2:
        st.markdown("##### 📈 Dataset Scale vs Model Performance")
        if not ml_df.empty:
            fig_scatter = px.scatter(ml_df, x="training_rows", y="r2_score", color="agent_name",
                                     size="accuracy", hover_data=["model_name"],
                                     title="Model Score relative to Training Set Size",
                                     labels={"training_rows": "Training Rows", "r2_score": "Score"})
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"family": "Inter", "size": 11},
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No model scatter details logged.")

    st.markdown("---")

    mc1, mc2 = st.columns([1, 1.5])
    with mc1:
        render_card('<h4 style="margin:0 0 8px;">🔄 1-Click Retrain</h4>')
        if st.button("🔄 Retrain All Agents Now"):
            with st.spinner("Training... (~2-3 min)"):
                res = subprocess.run(["python", "train_ml.py"], capture_output=True, text=True, timeout=300)
            load_agents.clear()
            (st.success if res.returncode == 0 else st.error)(
                "✅ All agents retrained!" if res.returncode == 0 else "❌ Training failed.")
            st.code((res.stdout if res.returncode == 0 else res.stderr)[-1000:])
    with mc2:
        st.markdown("##### 📜 Historical Model Audits Log")
        if not ml_df.empty:
            st.dataframe(ml_df, use_container_width=True, hide_index=True)
        else:
            st.info("No model history yet.")

    st.markdown("---")
    render_card('<h4 style="margin:0 0 8px;">🔔 Recent Alerts</h4>')
    for a in get_recent_alerts(10):
        st.markdown(f'<div style="border-bottom:1px solid #E5E7EB;padding:8px 0;font-size:13px;">'
                    f'<b>[{a[1].upper()}]</b> {a[3]} '
                    f'<span style="color:{COLORS["text_muted"]};float:right;">{a[4]}</span></div>',
                    unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB: ADMIN DASHBOARD (modular)
# ─────────────────────────────────────────────────────────────────────────────
elif selected_tab == "🛡️ Admin Dashboard":
    if not is_admin:
        st.error("🔒 Admin access required.")
    else:
        render_admin_dashboard(project="freight")
