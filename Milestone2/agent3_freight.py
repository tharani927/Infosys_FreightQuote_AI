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
        # Flag badge overlay
        def style_row(row):
            return ["background:#fff0f0" if row.get("flagged", 0) else ""] * len(row)
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

        badge_c = "#34d399" if prob > 0.7 else ("#ffd803" if prob > 0.5 else "#f87171")
        is_flagged = bool(row_c.get("flagged", 0))
        st.markdown(
            f'<div style="background:{badge_c};padding:14px;border-radius:12px;'
            f'border:2px solid {COLORS["border"]};">'
            f'<span class="agent-badge">Agent 3</span>'
            f'{"<span style=\"background:#f87171;color:#fff;padding:2px 8px;border-radius:6px;font-size:12px;margin-left:8px;\">🚨 FLAGGED</span>" if is_flagged else ""}'
            f'<h2 style="color:#272343;margin:8px 0 0;">{prob * 100:.1f}% Compliance</h2>'
            f'<p style="margin:4px 0;font-weight:600;">95% CI: {lo * 100:.1f}% — {hi * 100:.1f}%</p>'
            f'<p style="margin:0;font-size:12px;">'
            f'Punctuality: {row_c["punctuality_rate"] * 100:.1f}% | '
            f'Fuel: {row_c["fuel_surcharge_pct"]}%</p>'
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
                         color_discrete_sequence=["#00c5cd", "#272343", "#ffd803", "#f87171"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              height=340, margin=dict(l=10, r=10, t=40, b=80),
                              xaxis_tickangle=-30)
            st.plotly_chart(fig, use_container_width=True)

    # ── Tier Rating Matrix ────────────────────────────────────────────────────
    with tab_matrix:
        carriers_df["composite_score"] = (
            carriers_df["punctuality_rate"] * 0.4 +
            carriers_df["tariff_compliance_score"] * 0.4 +
            (1 - carriers_df["fuel_surcharge_pct"] / 25) * 0.2
        ).round(3)
        ranked = carriers_df[["carrier_name", "tier_rating", "composite_score",
                               "punctuality_rate", "tariff_compliance_score",
                               "fuel_surcharge_pct"]].sort_values(
            "composite_score", ascending=False).reset_index(drop=True)
        ranked.index += 1

        def color_tier(val):
            c = {"Apex": "#d1fae5", "Preferred": "#fef9c3", "Standard": "#fee2e2"}.get(str(val), "")
            return f"background-color:{c}" if c else ""

        st.dataframe(ranked.style.applymap(color_tier, subset=["tier_rating"]),
                     use_container_width=True)
