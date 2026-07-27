"""
Shared ui_theme.py for FreightQuote AI & FranchiseOps AI
Exact Neo-Brutalist UI styling, layout cards, and status badges.
"""
import streamlit as st

COLORS = {
    "bg_main":       "#090D16",
    "bg_sidebar":    "#06090F",
    "bg_card":       "#121824",
    "bg_alt":        "#1E293B",
    "text_heading":  "#F9FAFB",
    "text_body":     "#E5E7EB",
    "text_main":     "#F9FAFB",
    "text_muted":    "#9CA3AF",
    "border":        "#1E293B",
    "accent":        "#2563EB",
    "accent_hover":  "#3B82F6",
    "accent_text":   "#FFFFFF",
    "cyan":          "#06B6D4",
    "pink":          "#EC4899",
    "green":         "#10B981",
    "yellow":        "#F59E0B",
    "red":           "#EF4444",
    "indigo":        "#4F46E5",
    "purple":        "#7C3AED",
}

DARK_OBSIDIAN_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

/* Main Page Container & Background */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: {COLORS["text_body"]} !important;
    background-color: {COLORS["bg_main"]} !important;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: 'Poppins', sans-serif;
    color: {COLORS["text_heading"]} !important;
    font-weight: 600;
    letter-spacing: -0.02em;
}}

/* Sidebar Customization */
section[data-testid="stSidebar"] {{
    background-color: {COLORS["bg_sidebar"]} !important;
    border-right: 1px solid {COLORS["border"]} !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
    color: #F3F4F6 !important;
    font-weight: 500;
}}

section[data-testid="stSidebar"] * {{
    color: #F3F4F6 !important;
}}

/* Option Menu Link Styling Inside Sidebar */
.nav-link {{
    font-family: 'Inter', sans-serif !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    color: #9CA3AF !important;
    font-weight: 500 !important;
    transition: all 0.2s ease-in-out !important;
}}
.nav-link:hover {{
    color: #FFFFFF !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}}
.nav-link-selected {{
    background: linear-gradient(135deg, {COLORS["accent"]} 0%, {COLORS["purple"]} 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}}

/* Card Elements (Rounded, Soft Shadows, Lift on Hover) */
.pn-card, .premium-card {{
    background: {COLORS["bg_card"]} !important;
    border: 1px solid {COLORS["border"]} !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    animation: fadeIn 0.4s ease-out;
}}
.pn-card:hover, .premium-card:hover {{
    transform: translateY(-4px) !important;
    box-shadow: 0 20px 30px rgba(0, 0, 0, 0.5) !important;
    border-color: {COLORS["accent"]} !important;
}}

/* Alternative Card styling */
.pn-card-alt {{
    background: linear-gradient(135deg, {COLORS["bg_card"]} 0%, {COLORS["bg_alt"]} 100%) !important;
    border: 1px solid {COLORS["border"]} !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
}}

/* Modern Badges */
.pn-badge {{
    display: inline-block;
    padding: 4px 10px;
    border: 1px solid {COLORS["border"]};
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background-color: {COLORS["bg_alt"]};
    color: {COLORS["text_heading"]};
}}

.agent-badge {{
    display: inline-block;
    padding: 4px 12px;
    background-color: {COLORS["bg_alt"]};
    color: {COLORS["cyan"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 9999px;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 12px;
}}

/* Button Styling Override */
div.stButton > button, div.stFormSubmitButton > button {{
    background: linear-gradient(135deg, {COLORS["accent"]} 0%, {COLORS["purple"]} 100%) !important;
    color: {COLORS["accent_text"]} !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    height: 44px !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100%;
}}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.5) !important;
    background: linear-gradient(135deg, {COLORS["accent_hover"]} 0%, {COLORS["purple"]} 100%) !important;
}}
div.stButton > button:active, div.stFormSubmitButton > button:active {{
    transform: translateY(0px) !important;
}}

/* Input and Select Element Styling Override */
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
    background-color: {COLORS["bg_card"]} !important;
    border: 1px solid {COLORS["border"]} !important;
    border-radius: 8px !important;
    color: {COLORS["text_heading"]} !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.2s ease-in-out !important;
}}
div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {{
    border-color: {COLORS["accent"]} !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.3) !important;
}}
div[data-baseweb="input"] input, div[data-baseweb="select"] * {{
    color: {COLORS["text_heading"]} !important;
}}

/* Tabs Customization */
button[data-baseweb="tab"] {{
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    color: {COLORS["text_muted"]} !important;
    background-color: transparent !important;
    border: none !important;
    padding: 12px 20px !important;
    transition: all 0.2s !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {COLORS["accent"]} !important;
    border-bottom: 2px solid {COLORS["accent"]} !important;
    font-weight: 600 !important;
}}

/* Styled tables */
div[data-testid="stTable"] table, div[data-testid="stDataFrame"] table {{
    border-collapse: collapse !important;
    width: 100% !important;
    border: 1px solid {COLORS["border"]} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}
div[data-testid="stTable"] th, div[data-testid="stDataFrame"] th {{
    background-color: {COLORS["bg_sidebar"]} !important;
    color: {COLORS["text_heading"]} !important;
    font-weight: 600 !important;
    padding: 14px !important;
    border-bottom: 1px solid {COLORS["border"]} !important;
}}
div[data-testid="stTable"] td, div[data-testid="stDataFrame"] td {{
    background-color: {COLORS["bg_card"]} !important;
    color: {COLORS["text_body"]} !important;
    padding: 14px !important;
    border-bottom: 1px solid {COLORS["border"]} !important;
}}

/* Chat overrides for ChatGPT bubble styling */
.chat-container {{
    display: flex;
    flex-direction: column;
    gap: 12px;
}}
.chat-message-container {{
    display: flex;
    margin-bottom: 16px;
    gap: 12px;
}}
.chat-message-user {{
    justify-content: flex-end;
}}
.chat-message-copilot {{
    justify-content: flex-start;
}}
.chat-bubble-user {{
    background: linear-gradient(135deg, {COLORS["accent"]} 0%, {COLORS["purple"]} 100%) !important;
    color: #FFFFFF !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 14px 20px !important;
    max-width: 75% !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
}}
.chat-bubble-copilot {{
    background-color: {COLORS["bg_card"]} !important;
    color: {COLORS["text_main"]} !important;
    border: 1px solid {COLORS["border"]} !important;
    border-left: 4px solid {COLORS["purple"]} !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 14px 20px !important;
    max-width: 75% !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}}

/* Custom styling for metrics blocks */
div[data-testid="stMetricValue"] {{
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    color: {COLORS["text_heading"]} !important;
}}

/* Fade-in Animation */
@keyframes fadeIn {{
    from {{
        opacity: 0;
        transform: translateY(8px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}
</style>
"""

def inject_css():
    st.markdown(DARK_OBSIDIAN_CSS, unsafe_allow_html=True)

def apply_theme():
    inject_css()

def render_header(title, subtitle="", icon="⚡"):
    inject_css()
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #06090F 0%, #121824 100%); border-radius: 16px; padding: 28px 32px; margin-bottom: 28px; color: #FFFFFF; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4); border: 1px solid #1E293B;">
        <div style="display:flex; align-items:center; gap:20px;">
            <div style="font-size:44px; line-height:1;">{icon}</div>
            <div>
                <h1 style="margin:0; color:#FFFFFF; font-size:28px; font-family:'Poppins', sans-serif; font-weight:700;">{title}</h1>
                <p style="margin:8px 0 0; color:#9CA3AF; font-size:15px; font-weight:400;">{subtitle}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_card(content, alt=False):
    c_class = "pn-card-alt" if alt else "pn-card"
    st.markdown(f'<div class="{c_class}">{content}</div>', unsafe_allow_html=True)

def risk_badge(text, level="Low"):
    color_map = {
        "Low":      "rgba(16, 185, 129, 0.15)",
        "Medium":   "rgba(245, 158, 11, 0.15)",
        "High":     "rgba(239, 68, 68, 0.15)",
        "Critical": "rgba(239, 68, 68, 0.15)",
    }
    text_color_map = {
        "Low":      "#34D399",
        "Medium":   "#FBBF24",
        "High":     "#FCA5A5",
        "Critical": "#FCA5A5",
    }
    bg_color = color_map.get(level, "rgba(107, 114, 128, 0.15)")
    text_color = text_color_map.get(level, "#9CA3AF")
    return f'<span class="pn-badge" style="background-color:{bg_color}; color:{text_color}; border-color:{text_color}88; font-weight:600;">{text}</span>'
