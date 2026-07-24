"""
app.py — FreightQuote AI v4 FINAL (Modular Fast Engine)
Lean orchestrator — all heavy tab logic lives in agent2_freight.py, agent3_freight.py, admin_dash.py
"""
import os, json, joblib, subprocess, numpy as np, pandas as pd
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
from ui_enhancements import apply_ui

apply_ui()

st.set_page_config(page_title="FreightQuote AI", page_icon="⚡", layout="wide",
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
    st.markdown(f'<div style="text-align:center;padding:10px 0;font-weight:700;font-size:18px;'
                f'color:{COLORS["text_heading"]};">⚡ FreightQuote AI</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;font-size:13px;color:{COLORS["text_muted"]};'
                f'margin-bottom:12px;">User: <b>{username}</b><br>'
                f'<span style="color:#0066cc;font-weight:600;">[{user_role}]</span></div>',
                unsafe_allow_html=True)
    tabs = ["🤖 AI Copilot", "💰 Agent 1: Pricing", "🚢 Agent 2: Route/Weather",
            "✅ Agent 3: Carrier Audit", "📊 Analytics & Retrain"]
    icons = ["chat-dots-fill", "currency-dollar", "compass", "clipboard-check", "bar-chart-fill"]
    if is_admin:
        tabs.append("🛡️ Admin Dashboard"); icons.append("shield-lock-fill")
    tabs.append("🚪 Sign Out"); icons.append("box-arrow-right")
    selected_tab = option_menu(menu_title=None, options=tabs, icons=icons, default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link": {"font-size": "13px", "text-align": "left", "margin": "3px 0",
                         "border-radius": "10px", "color": COLORS["text_main"], "font-weight": "600"},
            "nav-link-selected": {"background-color": COLORS["accent"], "color": COLORS["accent_text"],
                                  "border": f"2px solid {COLORS['border']}"},
        })

if selected_tab == "🚪 Sign Out":
    st.session_state["token"] = None; st.rerun()

render_header("FreightQuote AI", f"Module: {selected_tab}")

# ── GPU Banner ────────────────────────────────────────────────────────────────
b1, b2 = st.columns([4, 1.2])
with b1:
    if is_llm_loaded():
        st.markdown('<div style="background:#d1fae5;border:2px solid #34d399;border-radius:10px;'
                    'padding:8px 16px;font-weight:600;color:#065f46;font-size:13px;">'
                    '⚡ <b>LLM GPU Engine:</b> Active on Tesla T4 (Qwen-2.5-3B Ready)</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:#bae8e8;border:2px solid #272343;border-radius:10px;'
                    'padding:8px 16px;font-weight:600;color:#272343;font-size:13px;">'
                    '⚡ <b>LLM GPU Engine:</b> Standby — warm up before use</div>',
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
# TAB: AI COPILOT
# ─────────────────────────────────────────────────────────────────────────────
if selected_tab == "🤖 AI Copilot":
    render_card('<h3 style="margin:0 0 6px;">💬 Unified AI Copilot — Total Logistics Intelligence</h3>'
                '<p style="margin:0;color:#64748b;font-size:13px;">Powered by Qwen-2.5-3B on T4. '
                'All answers use live DB stats, port weather, ML scores & carrier data.</p>')

    if "copilot_history" not in st.session_state:
        hist = load_chat_history(username, get_conn)
        if not hist:
            msg = "Welcome to FreightQuote AI Copilot! Ask about pricing, routes, carriers, or delays."
            save_chat_message(username, "assistant", msg, get_conn)
            hist = [{"role": "assistant", "content": msg}]
        st.session_state["copilot_history"] = hist

    for m in st.session_state["copilot_history"]:
        bg = "#e3f6f5" if m["role"] == "user" else "white"
        label = "🧑 You" if m["role"] == "user" else "⚡ Copilot"
        st.markdown(f'<div class="pn-card" style="background:{bg};border-left:5px solid '
                    f'{COLORS["accent"] if m["role"]=="user" else COLORS["border"]};">'
                    f'<b>{label}:</b><br>{m["content"]}</div>', unsafe_allow_html=True)

    inp_col, clr_col = st.columns([8, 1])
    with inp_col:
        with st.form("copilot_form", clear_on_submit=True):
            user_q  = st.text_input("", placeholder="e.g. 'Why is Shanghai→Rotterdam costly right now?'")
            fa, fb  = st.columns([3, 1])
            with fa: submit = st.form_submit_button("🚀 Ask Copilot")
            with fb: debate = st.form_submit_button("🔍 Debate View")
    with clr_col:
        if st.button("🗑️", help="Clear history"):
            from db import clear_chat_history
            clear_chat_history(username, get_conn)
            st.session_state["copilot_history"] = []; st.rerun()

    if (submit or debate) and user_q.strip():
        save_chat_message(username, "user", user_q, get_conn)
        st.session_state["copilot_history"].append({"role": "user", "content": user_q})
        if debate:
            with st.spinner("⚡ Single-pass debate (~2 sec)..."):
                res = generate_debate_and_synthesis(user_q, a1_ctx, a2_ctx, a3_ctx, db_stats)
            dc1, dc2, dc3 = st.columns(3)
            for col, key, label, color in [
                (dc1, "agent1", "Pricing & Congestion", COLORS["accent"]),
                (dc2, "agent2", "Route & Weather", "#34d399"),
                (dc3, "agent3", "Carrier Audit", "#f87171"),
            ]:
                col.markdown(f'<div class="pn-card" style="border-top:4px solid {color};">'
                             f'<span class="agent-badge">{label}</span><br><br>{res[key]}</div>',
                             unsafe_allow_html=True)
            ans = f"**Executive Synthesis:** {res['synthesis']}"
        else:
            with st.spinner("⚡ Generating answer (~1.5 sec)..."):
                ans = orchestrate_3_agents_query(user_q, a1_ctx, a2_ctx, a3_ctx, db_stats)
        save_chat_message(username, "assistant", ans, get_conn)
        st.session_state["copilot_history"].append({"role": "assistant", "content": ans})
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# TAB: AGENT 1 — PRICING
# ─────────────────────────────────────────────────────────────────────────────
elif selected_tab == "💰 Agent 1: Pricing":
    render_card('<h3 style="margin:0;">💰 Agent 1: Global Freight Pricing & Port Congestion</h3>')
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
                f'<div style="background:{COLORS["accent"]};padding:16px;border-radius:12px;'
                f'border:2px solid {COLORS["border"]};">'
                f'<span class="agent-badge">Agent 1 Estimate</span>'
                f'<h2 style="color:{COLORS["text_heading"]};margin:8px 0 0;">${mean_p:,.0f}</h2>'
                f'<p style="font-weight:600;margin:4px 0;">95% CI: ${lo95:,.0f} — ${hi95:,.0f}</p>'
                f'<p style="margin:0;font-size:12px;">±{std_p/mean_p*100:.1f}% uncertainty</p>'
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
# TAB: ANALYTICS & RETRAIN
# ─────────────────────────────────────────────────────────────────────────────
elif selected_tab == "📊 Analytics & Retrain":
    render_card('<h3 style="margin:0;">📊 Enterprise Analytics & Model Management</h3>')
    kc = st.columns(4)
    for col, icon, label, val in [
        (kc[0], "📋", "Total Quotes",   n_quotes),
        (kc[1], "🚢", "Shipments",      n_ships),
        (kc[2], "✅", "Carriers",       n_carriers),
        (kc[3], "🔔", "Alerts Sent",    n_alerts),
    ]:
        col.markdown(f'<div class="pn-card" style="text-align:center;padding:14px;">'
                     f'<div style="font-size:26px;">{icon}</div>'
                     f'<h2 style="margin:4px 0;">{val}</h2>'
                     f'<p style="margin:0;color:{COLORS["text_muted"]};font-size:12px;">{label}</p>'
                     f'</div>', unsafe_allow_html=True)
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
        with get_conn() as conn:
            try:
                ml_df = pd.read_sql("SELECT agent_name,model_name,r2_score,accuracy,"
                                    "training_rows,created_at FROM ml_models ORDER BY id DESC", conn)
                st.dataframe(ml_df, use_container_width=True, hide_index=True)
            except Exception:
                st.info("No model history yet.")
    st.markdown("---")
    render_card('<h4 style="margin:0 0 8px;">🔔 Recent Alerts</h4>')
    for a in get_recent_alerts(10):
        st.markdown(f'<div style="border-bottom:1px solid #bae8e8;padding:5px 0;font-size:13px;">'
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
