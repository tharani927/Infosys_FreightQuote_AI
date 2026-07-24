
import streamlit as st

def apply_ui():
    st.markdown("""
    <style>

    .stApp{
        background:#F5F7FB;
    }

    .stButton>button{
        background:#2563EB;
        color:white;
        border-radius:12px;
        height:45px;
        font-weight:bold;
    }

    div[data-testid="stMetric"]{
        border-radius:15px;
        padding:15px;
        box-shadow:0px 4px 12px rgba(0,0,0,.1);
    }

    </style>
    """, unsafe_allow_html=True)
