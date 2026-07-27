"""
agent3_freight.py — Enriched Agent 3: Carrier Audit & Tariff Compliance
New features: Carrier comparison bar chart, Flag Carrier button, Audit Report generator, Tier Matrix.
"""
"""
agent3_freight.py — Enriched Agent 3: Carrier Audit & Tariff Compliance
New features: Carrier comparison bar chart, Flag Carrier button, Audit Report generator, Tier Matrix.
"""
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ui_theme import render_card, COLORS
from db import get_conn
from llm_engine import generate_json
from notifications import send_alert


def render_agent3_freight(agent3_m, username, confidence_band):
    render_card('<h3 style="margin:0;">✅ Agent 3: Carrier Audit & Tariff Compliance</h3>')

    with get_conn() as conn:
        carriers_df = pd.read_sql("SELECT * FROM carriers", conn)

    if carriers_df.empty:
        st.warning("No carrier data found. Run seed_data first.")
        return

    # ── Top section: table + audit panel ─────────────────────────────────────
    c1, c2 = st.columns([1.4, 1])
    with c1:
        st.dataframe(carriers_df, use_container_width=True, hide_index=True)

    with c2:
        sel = st.selectbox("Select Carrier to Audit", carriers_df["carrier_name"].tolist())
        row_c = carriers_df[carriers_df["carrier_name"] == sel].iloc[0]
        complaint = 0.02 if str(row_c.get("tier_rating", "")).lower() == "apex" else 0.06
        X_row = [
            float(row_c["punctuality_rate"]),
            float(row_c["avg_delay_days"]),
            complaint,
            float(row_c["fuel_surcharge_pct"]),
            float(row_c["tariff_compliance_score"]),
            1.0,
        ]
        prob, lo, hi = confidence_band(agent3_m, X_row) if agent3_m else (
            float(row_c["tariff_compliance_score"]), 0.0, 1.0)

        # Map to premium soft alert color styling
        if prob > 0.7:
            badge_bg, badge_fg, border_color = "#D1FAE5", "#065F46", "#6EE7B7"
        elif prob > 0.5:
            badge_bg, badge_fg, border_color = "#FEF3C7", "#92400E", "#FDE047"
        else:
            badge_bg, badge_fg, border_color = "#FEE2E2", "#991B1B", "#FCA5A5"

        is_flagged = bool(row_c.get("flagged", 0))
        st.markdown(
            f'<div style="background:{badge_bg};color:{badge_fg};padding:18px;border-radius:12px;'
            f'border:1px solid {border_color};box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);">'
            f'<span class="agent-badge" style="background:#FFF;border-color:{border_color};color:{badge_fg};">Agent 3 Estimate</span>'
            f'{"<span style=\"background:#EF4444;color:#fff;padding:2px 8px;border-radius:6px;font-size:12px;margin-left:8px;font-weight:600;\">🚨 FLAGGED</span>" if is_flagged else ""}'
            f'<h2 style="color:{badge_fg};margin:10px 0 4px;font-family:\'Poppins\',sans-serif;font-weight:700;">{prob * 100:.1f}% Compliance</h2>'
            f'<p style="margin:4px 0;font-weight:600;font-size:14px;">95% CI: {lo * 100:.1f}% — {hi * 100:.1f}%</p>'
            f'<p style="margin:0;font-size:12px;opacity:0.85;">'
            f'Punctuality: {row_c["punctuality_rate"] * 100:.1f}% | '
            f'Fuel Surcharge: {row_c["fuel_surcharge_pct"]}%</p>'
            f'</div>', unsafe_allow_html=True)

        # Flag / Unflag button
        fa, fb = st.columns(2)
        with fa:
            if st.button("🚨 Flag Carrier" if not is_flagged else "✅ Clear Flag",
                         key="btn_flag", use_container_width=True):
                new_flag = 0 if is_flagged else 1
                with get_conn() as conn:
                    conn.execute("UPDATE carriers SET flagged=? WHERE carrier_name=?",
                                 (new_flag, sel))
                send_alert("In-App", username, "Carrier Flagged" if new_flag else "Flag Cleared", sel)
                st.rerun()
        with fb:
            if st.button("📋 Audit Report", key="btn_report", use_container_width=True):
                with st.spinner("Generating audit report (~2 sec)..."):
                    report = generate_json(
                        f"Carrier: {sel}. Punctuality: {row_c['punctuality_rate']:.2f}. "
                        f"Avg delay: {row_c['avg_delay_days']} days. "
                        f"Tariff compliance: {row_c['tariff_compliance_score']:.2f}. "
                        f"Fuel surcharge: {row_c['fuel_surcharge_pct']}%. "
                        "Generate carrier audit assessment.",
                        schema_keys=["risk_level", "recommended_action",
                                     "penalty_estimate_usd", "next_audit_date"])
                st.json(report)

    st.markdown("---")
    tab_compare, tab_matrix = st.tabs(["📊 Carrier Comparison", "🏆 Tier Matrix"])

    # ── Carrier Comparison Bar Chart ──────────────────────────────────────────
    with tab_compare:
        metrics = st.multiselect(
            "Compare metrics",
            ["punctuality_rate", "tariff_compliance_score", "fuel_surcharge_pct", "avg_delay_days"],
            default=["punctuality_rate", "tariff_compliance_score"])
        if metrics:
            melt = carriers_df[["carrier_name"] + metrics].melt(
                id_vars="carrier_name", var_name="metric", value_name="value")
            fig = px.bar(melt, x="carrier_name", y="value", color="metric", barmode="group",
                         title="Carrier Performance Comparison",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              height=320, margin=dict(l=10, r=10, t=40, b=10),
                              font=dict(family="Inter", size=11))
            st.plotly_chart(fig, use_container_width=True)

    # ── Tier Matrix ───────────────────────────────────────────────────────────
    with tab_matrix:
        st.markdown(f'<h4 style="color:{COLORS["text_heading"]};margin:0 0 10px;">🏆 Carrier Tier Matrix</h4>',
                    unsafe_allow_html=True)
        tier_data = {
            "Tier Rating": ["Apex (Elite)", "Standard Tier", "Restricted"],
            "Min Punctuality": ["92%+", "80% - 91%", "Under 80%"],
            "Compliance Threshold": ["95%+", "85% - 94%", "Under 85%"],
            "Audit Frequency": ["Annual Auto-Renewal", "Bi-Annual Review", "Immediate Audit Required"],
            "Operational Priority": ["High-Priority Allocations", "Standard Allocations", "Suspended Allocations"],
        }
        st.dataframe(tier_data, use_container_width=True, hide_index=True)
