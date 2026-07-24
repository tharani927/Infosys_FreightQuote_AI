"""
agent2_freight.py — Enriched Agent 2: Route Optimization & Marine Weather Risk
New features: Route radar chart, global delay trend, AI advisory, alternative routes table.
Extended ports list covering India, Middle East, Europe, Americas, Asia-Pacific.
"""
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ui_theme import render_card, COLORS
from weather_context import get_weather_report
from llm_engine import orchestrate_3_agents_query

# ── Full global port list with Indian ports ───────────────────────────────────
ALL_PORTS = [
    # India
    "Mumbai (IN)", "Chennai (IN)", "Nhava Sheva / JNPT (IN)", "Kolkata (IN)",
    "Mundra (IN)", "Cochin (IN)", "Vishakhapatnam (IN)", "Tuticorin (IN)",
    # China / East Asia
    "Shanghai (CN)", "Shenzhen (CN)", "Ningbo (CN)", "Qingdao (CN)",
    "Tianjin (CN)", "Guangzhou (CN)", "Busan (KR)", "Tokyo (JP)", "Osaka (JP)",
    # South-East Asia
    "Singapore (SG)", "Port Klang (MY)", "Laem Chabang (TH)", "Ho Chi Minh (VN)",
    "Jakarta (ID)",
    # Middle East
    "Dubai / Jebel Ali (AE)", "Abu Dhabi (AE)", "Salalah (OM)", "Dammam (SA)",
    # Europe
    "Rotterdam (NL)", "Hamburg (DE)", "Antwerp (BE)", "Felixstowe (GB)",
    "Barcelona (ES)", "Piraeus (GR)", "Genoa (IT)",
    # Americas
    "Los Angeles (US)", "New York / Newark (US)", "Houston (US)",
    "Santos (BR)", "Buenos Aires (AR)", "Manzanillo (MX)",
    # Africa / Other
    "Durban (ZA)", "Mombasa (KE)", "Port Said (EG)",
    # Canal Hubs
    "Suez Canal Hub", "Panama Canal Hub",
]

# Approximate distances (nm) for common route pairs
_DIST = {
    ("Mumbai (IN)",              "Rotterdam (NL)"):            8600,
    ("Nhava Sheva / JNPT (IN)", "Rotterdam (NL)"):            8700,
    ("Chennai (IN)",             "Singapore (SG)"):            1600,
    ("Mundra (IN)",              "Dubai / Jebel Ali (AE)"):    1050,
    ("Kolkata (IN)",             "Shanghai (CN)"):             3200,
    ("Shanghai (CN)",            "Rotterdam (NL)"):            10500,
    ("Shanghai (CN)",            "Los Angeles (US)"):          6500,
    ("Singapore (SG)",           "Dubai / Jebel Ali (AE)"):   3500,
    ("Singapore (SG)",           "Rotterdam (NL)"):            8300,
    ("Los Angeles (US)",         "Hamburg (DE)"):              7800,
    ("Santos (BR)",              "Rotterdam (NL)"):            5700,
    ("Durban (ZA)",              "Rotterdam (NL)"):            7200,
    ("Busan (KR)",               "Rotterdam (NL)"):            11200,
}

def _dist(o, d):
    return _DIST.get((o, d), _DIST.get((d, o), 7500))


def render_agent2_freight(agent2_m, username, db_stats, a1_ctx, a3_ctx, send_alert, get_conn, confidence_band):
    render_card('<h3 style="margin:0;">🚢 Agent 2: Route Optimization & Marine Weather Risk</h3>')

    c1, c2 = st.columns([1.1, 1])
    with c1:
        origin = st.selectbox("Origin Port", ALL_PORTS, index=0)
        dest   = st.selectbox("Destination Port", ALL_PORTS, index=14)
        dwell  = st.slider("Avg Port Dwell (days)", 0.5, 12.0, 3.5)
        canal  = st.checkbox("Canal Queue Active?", value=True)
        season = st.selectbox("Season / Risk Period",
                              ["Normal","Monsoon (Jun–Sep)","Typhoon Season (Jul–Nov)",
                               "Winter North Sea","Suez Disruption Alert"])

    wo = get_weather_report(origin)
    wd = get_weather_report(dest)
    route_nm = _dist(origin, dest)

    with c2:
        render_card(
            f"<b>📍 Origin:</b> {origin}<br>"
            f"Weather: <b>{wo['status']}</b> | Wind: <b>{wo['wind_kt']} kt</b><br><br>"
            f"<b>📍 Destination:</b> {dest}<br>"
            f"Weather: <b>{wd['status']}</b> | Wind: <b>{wd['wind_kt']} kt</b><br><br>"
            f"<b>🗺️ Route Distance:</b> ~{route_nm:,} nm", alt=True)

        if agent2_m is not None:
            w_avg = (wo["delay_penalty_multiplier"] + wd["delay_penalty_multiplier"]) / 2 - 1.0
            season_risk = {"Normal": 0.20, "Monsoon (Jun–Sep)": 0.55, "Typhoon Season (Jul–Nov)": 0.70,
                           "Winter North Sea": 0.45, "Suez Disruption Alert": 0.65}.get(season, 0.25)
            row = [dwell, 20, float(route_nm), float(w_avg), int(canal), season_risk]
            prob, lo, hi = confidence_band(agent2_m, row)
        else:
            prob = min(0.95, dwell / 12 * 0.5 + (0.15 if canal else 0) +
                       (0.2 if "Typhoon" in season or "Monsoon" in season else 0))
            lo, hi = max(0, prob - 0.08), min(1, prob + 0.08)

        badge_c = "#f87171" if prob > 0.6 else ("#ffd803" if prob > 0.35 else "#34d399")
        st.markdown(
            f'<div style="background:{badge_c};padding:14px;border-radius:12px;'
            f'border:2px solid {COLORS["border"]};margin-top:10px;">'
            f'<span class="agent-badge">Agent 2</span>'
            f'<h2 style="color:#272343;margin:6px 0 0;">{prob * 100:.1f}% Delay Risk</h2>'
            f'<p style="margin:4px 0;font-weight:600;">95% CI: {lo * 100:.1f}% — {hi * 100:.1f}%</p>'
            f'<p style="margin:0;font-size:12px;">Season: {season}</p>'
            f'</div>', unsafe_allow_html=True)

    st.markdown("---")
    tab_radar, tab_trend, tab_alt, tab_ai = st.tabs(
        ["📡 Route Radar", "📊 Delay Trend", "🔀 Alt Routes", "🤖 AI Advisory"])

    # ── Radar Chart ──────────────────────────────────────────────────────────
    with tab_radar:
        cats = ["Delay Risk", "Congestion Impact", "Weather Severity",
                "Canal Dependency", "Carrier Availability"]
        vals = [
            prob * 10,
            min(10, dwell * 1.2),
            min(10, (wo["wind_kt"] + wd["wind_kt"]) / 15),
            8.0 if canal else 2.0,
            7.5,
        ]
        fig = go.Figure(go.Scatterpolar(r=vals + [vals[0]], theta=cats + [cats[0]],
                                        fill="toself",
                                        line_color=COLORS["accent"],
                                        fillcolor="rgba(0,197,205,0.2)"))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                          paper_bgcolor="rgba(0,0,0,0)", height=320,
                          margin=dict(l=40, r=40, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    # ── Delay Trend across key routes ────────────────────────────────────────
    with tab_trend:
        routes = [
            "Mumbai→Rotterdam", "Shanghai→Rotterdam", "Singapore→Dubai",
            "LA→Hamburg", "Chennai→Singapore", "Nhava Sheva→Antwerp",
            "Mundra→Jebel Ali", "Kolkata→Shanghai", "Santos→Rotterdam",
        ]
        delays = [62, 68, 38, 55, 28, 58, 22, 45, 48]
        colors = ["#f87171" if d > 55 else ("#ffd803" if d > 35 else "#34d399") for d in delays]
        fig2 = go.Figure(go.Bar(x=routes, y=delays, marker_color=colors,
                                text=[f"{d}%" for d in delays], textposition="outside"))
        fig2.update_layout(title="Delay Probability % — Key Global Routes",
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           yaxis_range=[0, 100], height=320,
                           margin=dict(l=10, r=10, t=40, b=80))
        st.plotly_chart(fig2, use_container_width=True)

    # ── Alternative Routes ────────────────────────────────────────────────────
    with tab_alt:
        st.markdown(f'<h4 style="color:{COLORS["text_heading"]};margin:0 0 10px;">'
                    f'🔀 Alternative Route Suggestions for {origin} → {dest}</h4>',
                    unsafe_allow_html=True)
        alt_data = {
            "Route": [f"{origin} → {dest} (Direct)",
                      f"{origin} → Colombo → {dest}",
                      f"{origin} → Singapore → {dest}"],
            "Extra Distance (nm)": [0, 420, 680],
            "Extra Transit (days)": [0, 1, 2],
            "Risk Level": ["Current", "Lower", "Lowest"],
            "Cost Delta (USD)": [0, "+$380", "+$650"],
        }
        st.dataframe(alt_data, use_container_width=True, hide_index=True)

    # ── AI Advisory ──────────────────────────────────────────────────────────
    with tab_ai:
        if st.button("🤖 Get AI Route Advisory", key="btn_a2_advisory"):
            a2_ctx = {"origin": origin, "dest": dest, "dwell": dwell,
                      "canal_queue": canal, "delay_risk_pct": round(prob * 100, 1),
                      "season": season, "route_nm": route_nm}
            with st.spinner("Generating advisory (~2 sec)..."):
                advice = orchestrate_3_agents_query(
                    f"Best strategy for {origin} to {dest} route given current conditions?",
                    a1_ctx, a2_ctx, a3_ctx, db_stats)
            st.markdown(
                f'<div class="pn-card" style="border-left:6px solid {COLORS["border"]};">'
                f'<b>⚡ AI Route Advisory:</b><br><br>{advice}</div>',
                unsafe_allow_html=True)
            send_alert("In-App", username, "Route Advisory", f"{origin}→{dest}")
