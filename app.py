import html as html_module
import streamlit as st
import pandas as pd
import json
import re
from datetime import datetime, timezone
from urllib.parse import quote_plus
from supabase import create_client
import logging


logger = logging.getLogger(__name__)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="STEM Pathways NYC",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# BRAND STYLING (consolidated)
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');

    :root {
        --sp-bg: #DBECFF;
        --sp-surface: #ffffff;
        --sp-surface-soft: #DDEFF7;
        --sp-border: #083C5D;
        --sp-text: #083C5D;
        --sp-muted: #083C5D;
        --sp-primary: #018FC7;
        --sp-primary-dark: #00658F;
        --sp-navy: #003F5C;
        --sp-navy-mid: #00577D;
        --sp-accent: #38BDF8;
        --sp-warning: #d97706;
        --sp-danger: #c2410c;
        --sp-success: #15803d;
        --sp-radius: 18px;
        --sp-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
        --sp-font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .main, section.main,
    section[data-testid="stMain"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    html, body, .stApp,
    [data-testid="stAppViewContainer"] *:not([data-testid="stIconMaterial"]):not(svg):not(path):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stSidebar"] *:not([data-testid="stIconMaterial"]):not(svg):not(path):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stMain"] *:not([data-testid="stIconMaterial"]):not(svg):not(path):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stHeader"] *:not([data-testid="stIconMaterial"]):not(svg):not(path):not([class*="material-symbols"]):not([class*="material-icons"]),
    p, h1, h2, h3, h4, h5, h6, li, label, a, button, input, textarea, select,
    span:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    div:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-baseweb] *:not([data-testid="stIconMaterial"]):not(svg):not(path):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] *,
    [data-testid="stMetric"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stAlert"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stExpander"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stTabs"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stSelectbox"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stMultiSelect"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stTextInput"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stNumberInput"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stTextArea"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stRadio"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stCheckbox"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stSlider"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    .stButton button,
    .stButton button *,
    .stLinkButton a,
    .stLinkButton a *,
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stFormSubmitButton"] button *,
    [data-testid="stDownloadButton"] button,
    [data-testid="stDownloadButton"] button * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    [data-testid="stAppViewContainer"] {
        background: #DBECFF !important;
        color: var(--sp-text);
    }

    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    section[data-testid="stMain"] {
        background: #DBECFF !important;
    }

    [data-testid="stAppViewBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"] {
        background: transparent !important;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1480px !important;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 1.35rem !important;
        padding-right: 1.35rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
        width: 100%;
    }

    [data-testid="stHeader"] {
        background: #DBECFF !important;
        backdrop-filter: none;
        pointer-events: none !important;
    }

    [data-testid="stHeader"] button,
    [data-testid="stHeader"] a,
    [data-testid="stHeader"] [role="button"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"] {
        pointer-events: auto !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            var(--sp-navy) 0%,
            var(--sp-navy-mid) 55%,
            #003B57 100%
        ) !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
        min-height: 0 !important;
        height: auto !important;
        padding: 0.08rem 0.2rem 0 0 !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarContent"],
    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0 !important;
        padding-bottom: 0.55rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
        row-gap: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stElementContainer"],
    [data-testid="stSidebar"] [data-testid="element-container"] {
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
        width: 100% !important;
    }

    [data-testid="stSidebar"] [data-testid="stHeading"],
    [data-testid="stSidebar"] [data-testid="stHeadingWithActionElements"] {
        margin: 0 !important;
        padding: 0 !important;
        width: 100%;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        margin: 0 !important;
        padding: 0 !important;
        width: 100%;
    }

    [data-testid="stSidebar"] * {
        color: #f7fbfa;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #A7BAC6 !important;
        letter-spacing: 0.06em;
        font-weight: 600;
        font-size: 0.72rem;
        text-transform: none;
        margin: 0.55rem 0 0.25rem 0 !important;
        padding: 0 !important;
        line-height: 1.3;
        width: 100%;
    }

    [data-testid="stSidebar"] .sp-nav-section {
        display: block;
        position: relative;
        z-index: 1;
        color: #A7BAC6 !important;
        letter-spacing: 0.1em;
        font-weight: 600;
        font-size: 0.74rem;
        text-transform: uppercase;
        margin: 0.8rem 0 0.35rem 0;
        padding: 0;
        line-height: 1.25;
        width: 100%;
        text-align: left;
    }

    [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.sp-nav-section) {
        margin: 0 !important;
        min-height: 1.7rem !important;
        height: auto !important;
        overflow: visible !important;
        padding: 0 !important;
    }

    [data-testid="stSidebar"] hr,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] hr,
    [data-testid="stSidebar"] [data-testid="stDivider"] hr {
        border: none !important;
        border-top: 1.5px solid rgba(255,255,255,0.28) !important;
        margin: 0.75rem 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }

    [data-testid="stSidebar"] .stButton {
        margin: 0 0 0.28rem 0 !important;
        padding: 0 !important;
        width: 100%;
    }

    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stButton > button:active,
    [data-testid="stSidebar"] .stButton > button:focus,
    [data-testid="stSidebar"] .stButton > button:focus-visible,
    [data-testid="stSidebar"] button[kind="secondary"],
    [data-testid="stSidebar"] button[kind="primary"],
    [data-testid="stSidebar"] button[data-testid^="stBaseButton"] {
        background: #364957 !important;
        color: #F3F6F8 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        min-height: 36px !important;
        height: 36px !important;
        max-height: 36px !important;
        padding: 0 0.65rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        line-height: 1 !important;
        justify-content: flex-start !important;
        text-align: left !important;
        transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
        outline: none !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stButton button,
    [data-testid="stSidebar"] .stButton button *,
    [data-testid="stSidebar"] .stButton [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] .stButton [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] .stButton [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] .stButton p,
    [data-testid="stSidebar"] .stButton span,
    [data-testid="stSidebar"] .stButton div {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        line-height: 1.15 !important;
        font-family: var(--sp-font) !important;
    }

    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] .stButton > button span,
    [data-testid="stSidebar"] .stButton > button div,
    [data-testid="stSidebar"] .stButton > button:active p,
    [data-testid="stSidebar"] .stButton > button:active span,
    [data-testid="stSidebar"] .stButton > button:focus p,
    [data-testid="stSidebar"] .stButton > button:focus span {
        color: #F3F6F8 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        width: 100%;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stSidebar"] button[kind="secondary"]:hover,
    [data-testid="stSidebar"] button[data-testid^="stBaseButton-secondary"]:hover {
        background: #435563 !important;
        border-color: rgba(255,255,255,0.16) !important;
        color: #FFFFFF !important;
        transform: none;
    }

    [data-testid="stSidebar"] .stButton > button:hover *,
    [data-testid="stSidebar"] .stButton > button:hover p,
    [data-testid="stSidebar"] .stButton > button:hover span {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] .stButton > button[data-testid^="stBaseButton-primary"],
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:active,
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:focus,
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:focus-visible,
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: #FFFFFF !important;
        border-color: #FFFFFF !important;
        color: var(--sp-navy) !important;
        box-shadow: none !important;
        transform: none;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] .stButton > button[kind="primary"] *,
    [data-testid="stSidebar"] .stButton > button[kind="primary"] p,
    [data-testid="stSidebar"] .stButton > button[kind="primary"] span,
    [data-testid="stSidebar"] .stButton > button[kind="primary"] div,
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover *,
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover p,
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover span {
        color: var(--sp-navy) !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(.sp-sidebar-brand) {
        width: max-content;
        max-width: 100%;
    }

    .sp-sidebar-brand {
        width: max-content;
        max-width: 100%;
        padding: 0;
        margin: 0 0 0.5rem 0;
        text-align: left;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .sp-sidebar-title {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        justify-content: flex-start;
        width: max-content;
        max-width: 100%;
        margin: 0;
        padding: 0;
        line-height: 1.02;
        font-weight: 800;
        letter-spacing: -0.035em;
        text-align: center;
        box-sizing: border-box;
    }

    .sp-sidebar-title .sp-title-line {
        display: flex;
        flex-wrap: nowrap;
        align-items: baseline;
        justify-content: center;
        gap: 0.32em;
        font-size: 2.12rem;
        line-height: 1.05;
        font-weight: 800;
        margin: 0;
        padding: 0;
        white-space: nowrap;
    }

    .sp-sidebar-title .sp-title-nyc {
        display: block;
        width: 100%;
        font-size: 2.18rem;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: 0 !important;
        word-spacing: 0 !important;
        text-align: center;
        color: #72D2F2 !important;
        margin: 0.1rem 0 0 0;
        padding: 0;
        box-sizing: border-box;
    }

    [data-testid="stSidebar"] .sp-sidebar-title .sp-title-blue {
        color: #72D2F2 !important;
        font-weight: 800;
    }

    [data-testid="stSidebar"] .sp-sidebar-title .sp-title-nyc {
        color: #72D2F2 !important;
        font-weight: 800;
    }

    [data-testid="stSidebar"] .sp-sidebar-title .sp-title-yellow {
        color: #F4C542 !important;
        font-weight: 800;
        letter-spacing: inherit;
    }

    .sp-sidebar-accent {
        width: 100%;
        max-width: 100%;
        height: 4px;
        border-radius: 999px;
        background: #72D2F2;
        margin: 0.4rem 0 0 0;
        box-shadow: none;
        display: block;
        align-self: stretch;
        box-sizing: border-box;
    }

    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-size: 1.34rem !important;
        font-weight: 700 !important;
        margin: 0.15rem 0 0.28rem 0 !important;
        padding: 0 !important;
        line-height: 1.2 !important;
        letter-spacing: -0.02em;
        text-align: left;
        width: 100%;
    }

    [data-testid="stSidebar"] .sp-sidebar-meta {
        color: #A7BAC6 !important;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin: 0.08rem 0 0.38rem 0;
        padding: 0;
        line-height: 1.3;
        text-align: left;
        width: 100%;
    }

    [data-testid="stSidebar"] a {
        color: #65D1F5 !important;
        font-weight: 600 !important;
        font-size: 0.72rem !important;
        display: inline-block;
        margin: 0 0 0.35rem 0;
        padding: 0;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        margin: 0 0 0.1rem 0 !important;
        padding: 0 !important;
        line-height: 1.3 !important;
        text-align: left;
    }

    .sp-contact-card {
        margin: 0;
        width: 100%;
        box-sizing: border-box;
        border-radius: 10px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.14);
        padding: 0.45rem 0.7rem;
    }

    .sp-contact-title {
        color: #FFFFFF !important;
        font-size: 0.78rem;
        font-weight: 800;
        margin-bottom: 0.15rem;
    }

    .sp-contact-text {
        color: #CDEAF5 !important;
        font-size: 0.7rem;
        line-height: 1.3;
        margin-bottom: 0.28rem;
    }

    .sp-contact-email {
        color: #63D2F6 !important;
        font-size: 0.68rem;
        font-weight: 700;
        text-decoration: none !important;
        overflow-wrap: anywhere;
        margin: 0 !important;
    }

    .sp-contact-email:hover {
        color: #FFFFFF !important;
        text-decoration: underline !important;
    }

    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapseButton"] [role="button"],
    button[aria-label*="collapse sidebar" i],
    button[title*="collapse sidebar" i] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        background: #0B1F33 !important;
        background-color: #0B1F33 !important;
        color: #FFFFFF !important;
        border: 1px solid #0B1F33 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.24) !important;
        z-index: 2147483647 !important;
    }

    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"] [role="button"],
    button[aria-label*="open sidebar" i],
    button[aria-label*="expand sidebar" i],
    button[title*="open sidebar" i],
    button[title*="expand sidebar" i] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        position: fixed !important;
        top: 0.75rem !important;
        left: 0.75rem !important;
        width: 46px !important;
        height: 46px !important;
        min-width: 46px !important;
        min-height: 46px !important;
        align-items: center !important;
        justify-content: center !important;
        background: #0B1F33 !important;
        background-color: #0B1F33 !important;
        color: #FFFFFF !important;
        border: 1px solid #0B1F33 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.24) !important;
        z-index: 2147483647 !important;
    }

    [data-testid="stSidebarCollapsedControl"] > div,
    [data-testid="stSidebarCollapsedControl"] [data-testid*="Button"] {
        background: transparent !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapseButton"] svg *,
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] svg *,
    button[aria-label*="sidebar" i] svg,
    button[aria-label*="sidebar" i] svg * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebarCollapseButton"]:hover,
    [data-testid="stSidebarCollapsedControl"]:hover,
    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover,
    button[aria-label*="sidebar" i]:hover,
    [data-testid="stHeader"] button:first-of-type:hover {
        background: #071521 !important;
        background-color: #071521 !important;
        border-color: #071521 !important;
    }

    [data-testid="stHeader"] button:first-of-type {
        background: #0B1F33 !important;
        background-color: #0B1F33 !important;
        color: #FFFFFF !important;
        border: 1px solid #0B1F33 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.24) !important;
    }

    h1, h2, h3 {
        color: var(--sp-text) !important;
        letter-spacing: -0.02em;
        font-family: var(--sp-font) !important;
    }

    h1 { font-weight: 800 !important; font-size: 1.72rem !important; }
    h2 { font-weight: 750 !important; font-size: 1.45rem !important; }
    h3 { font-weight: 700 !important; font-size: 1.1rem !important; }

    p, li, label {
        color: var(--sp-text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    [data-testid="stMain"] p,
    [data-testid="stMain"] li,
    [data-testid="stMain"] [data-testid="stMarkdownContainer"] p {
        font-size: 0.93rem !important;
        line-height: 1.5;
        color: var(--sp-text) !important;
        font-weight: 500 !important;
    }

    [data-testid="stMain"] h2 {
        color: var(--sp-text) !important;
        font-weight: 750 !important;
    }

    [data-testid="stMain"] h3 {
        color: var(--sp-text) !important;
        font-weight: 650 !important;
    }

    [data-testid="stMain"] label,
    [data-testid="stMain"] [data-testid="stWidgetLabel"],
    [data-testid="stMain"] [data-testid="stWidgetLabel"] p {
        color: var(--sp-text) !important;
        font-weight: 600 !important;
    }

    [data-testid="stMain"] [data-testid="stCaptionContainer"],
    [data-testid="stMain"] [data-testid="stCaptionContainer"] p {
        font-size: 0.8rem !important;
        line-height: 1.4;
        color: var(--sp-muted) !important;
        font-weight: 550 !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] *:not(button):not([kind]),
    [data-testid="stMain"] [data-testid="stMetric"],
    [data-testid="stMain"] [data-testid="stMetric"] *,
    [data-testid="stMain"] [data-testid="stExpander"],
    [data-testid="stMain"] [data-testid="stExpander"] *:not(button):not([kind]),
    [data-testid="stMain"] [data-testid="stAlert"],
    [data-testid="stMain"] [data-testid="stAlert"] *,
    [data-testid="stMain"] [data-testid="stForm"],
    [data-testid="stMain"] [data-testid="stForm"] label,
    [data-testid="stMain"] [data-testid="stForm"] p,
    [data-testid="stMain"] [data-testid="stDataFrame"] {
        color: #083C5D !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h2,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h3,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] li,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] span,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] div,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] label,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"],
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] p {
        color: #083C5D !important;
        font-size: 0.95rem !important;
        line-height: 1.5;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] li,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"],
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] p {
        font-weight: 550 !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h2,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h3 {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #083C5D !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] .stButton > button p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] .stButton > button span,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] button[kind="secondary"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] button[kind="secondary"] span {
        color: #0B4F71 !important;
        font-size: 0.95rem !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] button[kind="primary"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] button[kind="primary"] span {
        color: #0B4F71 !important;
        font-size: 0.95rem !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stMetric"],
    [data-testid="stExpander"] {
        background: #FFFFFF !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stMain"] [data-testid="stMetric"],
    [data-testid="stMain"] [data-testid="stExpander"],
    [data-testid="stMain"] [data-testid="stAlert"],
    [data-testid="stMain"] [data-testid="stForm"],
    [data-testid="stMain"] [data-testid="stDataFrame"] {
        border-color: #083C5D !important;
        border-width: 3px !important;
        border-style: solid !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #083C5D !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08);
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
        padding: 1.4rem 1.4rem !important;
        background: #FFFFFF !important;
        cursor: default !important;
        transform: none !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h3 {
        font-weight: 650 !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"] > div {
        display: flex !important;
        flex-direction: column !important;
        min-width: 0;
        height: 100%;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(4):last-child) {
        display: grid !important;
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        column-gap: 1.35rem !important;
        row-gap: 1.35rem !important;
        margin-bottom: 1.75rem !important;
        align-items: stretch !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child) {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        column-gap: 2.25rem !important;
        row-gap: 2.75rem !important;
        margin-bottom: 2.75rem !important;
        align-items: stretch !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child) > div,
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(4):last-child) > div {
        width: auto !important;
        flex: none !important;
        min-width: 0 !important;
        height: 100%;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
        flex: 1 1 auto;
        height: 100%;
        display: flex !important;
        flex-direction: column !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(.sp-info-card) {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        column-gap: 1.35rem !important;
        row-gap: 1.35rem !important;
        margin-bottom: 1.35rem !important;
        align-items: stretch !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(.sp-info-card) > div {
        width: auto !important;
        flex: none !important;
        min-width: 0 !important;
        height: 100%;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"]:has(.sp-info-card) {
        background: #FFFFFF !important;
        border: 3px solid #083C5D !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08);
        padding: 1.4rem 1.45rem !important;
        min-height: 220px;
        height: 100%;
    }

    .sp-info-card {
        display: none !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stElementContainer"]:has(.sp-info-card) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stMain"] .st-key-profile_cards {
        width: min(920px, 100%) !important;
        max-width: 920px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        margin-top: 2rem !important;
        margin-bottom: 0 !important;
    }

    [data-testid="stMain"] .st-key-profile_cards > [data-testid="stVerticalBlock"],
    [data-testid="stMain"] .st-key-profile_cards > [data-testid="stLayoutWrapper"] > [data-testid="stVerticalBlock"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 2rem !important;
        width: 100% !important;
    }

    [data-testid="stMain"] .st-key-profile_cards [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
        column-gap: 2rem !important;
        row-gap: 2rem !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        align-items: stretch !important;
        justify-content: center !important;
    }

    [data-testid="stMain"] .st-key-profile_cards [data-testid="stHorizontalBlock"] > div {
        width: auto !important;
        flex: none !important;
        min-width: 0 !important;
        height: 340px !important;
        min-height: 340px !important;
        max-height: 340px !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: column !important;
    }

    [data-testid="stMain"] .st-key-profile_cards [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 3px solid #083C5D !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08);
        padding: 1.6rem 1.65rem !important;
        min-height: 340px !important;
        height: 340px !important;
        max-height: 340px !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        contain: paint;
        isolation: isolate;
        transform: none !important;
        cursor: default !important;
        width: 100% !important;
    }

    [data-testid="stMain"] .st-key-profile_cards [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] {
        height: 100% !important;
        max-height: 100% !important;
        min-height: 0 !important;
        overflow: hidden !important;
        gap: 0.45rem !important;
        flex: 1 1 auto !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
    }

    [data-testid="stMain"] .st-key-profile_cards [data-testid="stVerticalBlockBorderWrapper"] h2 {
        margin-top: 0 !important;
        margin-bottom: 0.7rem !important;
        padding-top: 0 !important;
        line-height: 1.25 !important;
        flex-shrink: 0 !important;
    }

    .sp-profile-card {
        display: none !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stElementContainer"]:has(.sp-profile-card) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlock"]:has(.st-key-profile_action_stack) {
        justify-content: flex-start !important;
    }

    [data-testid="stMain"] .st-key-profile_action_stack,
    [data-testid="stMain"] [data-testid="stElementContainer"]:has(.st-key-profile_action_stack) {
        width: min(920px, 100%) !important;
        max-width: 920px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0 !important;
        padding: 0 !important;
        padding-bottom: 0 !important;
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        flex: 0 0 auto !important;
        flex-grow: 0 !important;
        flex-shrink: 0 !important;
        position: static !important;
        overflow: visible !important;
    }

    [data-testid="stMain"] .st-key-profile_action_stack > [data-testid="stVerticalBlock"],
    [data-testid="stMain"] .st-key-profile_action_stack > [data-testid="stLayoutWrapper"] > [data-testid="stVerticalBlock"] {
        display: flex !important;
        flex-direction: column !important;
        flex-wrap: nowrap !important;
        justify-content: flex-start !important;
        align-items: stretch !important;
        gap: 0 !important;
        width: 100% !important;
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        flex: 0 0 auto !important;
        flex-grow: 0 !important;
        position: static !important;
    }

    [data-testid="stMain"] .st-key-profile_action_divider {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        height: auto !important;
        min-height: 0 !important;
        padding: 0 !important;
        position: static !important;
        overflow: visible !important;
    }

    [data-testid="stMain"] .st-key-profile_action_divider > [data-testid="stVerticalBlock"],
    [data-testid="stMain"] .st-key-profile_action_divider [data-testid="stDivider"],
    [data-testid="stMain"] .st-key-profile_action_divider [data-testid="stElementContainer"] {
        display: block !important;
        width: 100% !important;
        height: auto !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        position: static !important;
    }

    [data-testid="stMain"] .st-key-profile_action_divider hr,
    [data-testid="stMain"] .st-key-profile_action_divider [data-testid="stDivider"] hr {
        display: block !important;
        position: static !important;
        border: none !important;
        border-top: 1.75px solid #2b5d84 !important;
        border-color: #2b5d84 !important;
        color: #2b5d84 !important;
        width: 100% !important;
        margin: 0 !important;
    }

    [data-testid="stMain"] .st-key-profile_actions {
        width: min(920px, 100%) !important;
        max-width: 920px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        margin-top: 1.15rem !important;
        margin-bottom: 0 !important;
        padding: 0 !important;
        padding-bottom: 0 !important;
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        flex: 0 0 auto !important;
        flex-grow: 0 !important;
        overflow: visible !important;
        position: static !important;
    }

    [data-testid="stMain"] .st-key-profile_actions > [data-testid="stVerticalBlock"],
    [data-testid="stMain"] .st-key-profile_actions > [data-testid="stLayoutWrapper"] > [data-testid="stVerticalBlock"],
    [data-testid="stMain"] .st-key-profile_actions [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 1.5rem !important;
        width: 100% !important;
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        margin: 0 !important;
        position: static !important;
    }

    [data-testid="stMain"] .st-key-profile_actions [data-testid="stHorizontalBlock"] > div,
    [data-testid="stMain"] .st-key-profile_actions [data-testid="stElementContainer"]:has(.stButton),
    [data-testid="stMain"] .st-key-profile_actions [data-testid="stLayoutWrapper"] {
        height: auto !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        position: static !important;
    }

    [data-testid="stMain"] .st-key-profile_actions [data-testid="stElementContainer"]:has(.stButton),
    [data-testid="stMain"] .st-key-profile_actions .stButton {
        width: 320px !important;
        flex: 0 0 320px !important;
        max-width: 320px !important;
        min-width: 320px !important;
        height: auto !important;
        min-height: 0 !important;
        position: static !important;
    }

    [data-testid="stMain"] .st-key-profile_actions .stButton > button {
        width: 320px !important;
        min-width: 320px !important;
        max-width: 320px !important;
        height: 50px !important;
        min-height: 50px !important;
        position: static !important;
    }

    [data-testid="stMain"] .st-key-profile_action_stack ~ [data-testid="stElementContainer"]:has([data-testid="stDivider"]),
    [data-testid="stMain"] [data-testid="stElementContainer"]:has(.st-key-profile_action_stack) ~ [data-testid="stElementContainer"]:has([data-testid="stDivider"]),
    [data-testid="stMain"] .st-key-profile_action_stack ~ [data-testid="stElementContainer"]:has([data-testid="stCaptionContainer"]),
    [data-testid="stMain"] [data-testid="stElementContainer"]:has(.st-key-profile_action_stack) ~ [data-testid="stElementContainer"]:has([data-testid="stCaptionContainer"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    [data-testid="stMain"]:has(.st-key-profile_action_stack) [data-testid="stMainBlockContainer"] {
        padding-bottom: 1.5rem !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child) [data-testid="stVerticalBlockBorderWrapper"] {
        background: #F7FBFE !important;
        border: 3px solid #0B4F71 !important;
        box-shadow: 0 10px 24px rgba(8, 60, 93, 0.09);
        padding: 1.5rem 1.45rem !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child) [data-testid="stVerticalBlockBorderWrapper"] h3 {
        margin-top: 0 !important;
        margin-bottom: 0.4rem !important;
        min-height: 2.6rem;
        line-height: 1.3 !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child) [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] {
        flex: 1 1 auto;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] .stButton,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stElementContainer"]:has(.stButton) {
        margin-top: auto !important;
        width: 100%;
    }

    html body [data-testid="stMetric"] {
        background: #FFFFFF !important;
        color: #083C5D !important;
        border: 3px solid #083C5D !important;
        border-radius: 14px;
        padding: 1.4rem 1.45rem;
        min-height: 118px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.09);
        cursor: default !important;
        transform: none !important;
    }

    [data-testid="stMetric"] * {
        color: #083C5D !important;
    }

    [data-testid="stMetricLabel"] {
        color: #083C5D !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.45rem;
        min-height: 1.35em;
        align-self: flex-start;
    }

    [data-testid="stMetricValue"] {
        color: #083C5D !important;
        font-weight: 700 !important;
        font-size: 1.45rem !important;
        line-height: 1.25 !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        align-self: flex-start;
        margin-top: 0;
    }

    [data-testid="stMetricValue"] * {
        color: #083C5D !important;
        font-weight: 700 !important;
        font-size: 1.45rem !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }

    [data-testid="stTabs"],
    [data-testid="stRadio"],
    [data-testid="stSelectbox"],
    [data-testid="stMultiSelect"],
    [data-testid="stTextInput"],
    [data-testid="stTextArea"],
    [data-testid="stNumberInput"],
    [data-testid="stSlider"],
    [data-testid="stCheckbox"] {
        background: transparent !important;
    }

    .stButton > button,
    .stLinkButton > a {
        border-radius: 12px !important;
        min-height: 42px !important;
        font-weight: 700 !important;
        transition: 0.18s ease !important;
        font-family: var(--sp-font) !important;
    }

    [data-testid="stMain"] .stButton > button,
    [data-testid="stMain"] button[kind="secondary"],
    [data-testid="stMain"] button[kind="primary"],
    [data-testid="stMain"] button[data-testid^="stBaseButton"],
    [data-testid="stMain"] .stButton > button:active,
    [data-testid="stMain"] .stButton > button:focus,
    [data-testid="stMain"] .stButton > button:focus-visible,
    [data-testid="stMain"] button[kind="secondary"]:active,
    [data-testid="stMain"] button[kind="secondary"]:focus,
    [data-testid="stMain"] button[kind="primary"]:active,
    [data-testid="stMain"] button[kind="primary"]:focus,
    [data-testid="stMain"] button[kind="primary"]:focus-visible,
    [data-testid="stMain"] .stLinkButton > a,
    [data-testid="stMain"] [data-testid="stDownloadButton"] button,
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button,
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button:focus,
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button:active,
    [data-testid="stMain"] [data-testid="stPageLink"] a,
    [data-testid="stMain"] [data-testid="stPageLink-NavLink"] {
        background: #FFFFFF !important;
        color: #0B4F71 !important;
        border: 2px solid #63C7E8 !important;
        border-radius: 12px !important;
        min-height: 42px !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        outline: none !important;
        font-size: 0.95rem !important;
        transform: none !important;
    }

    [data-testid="stMain"] .stButton > button p,
    [data-testid="stMain"] .stButton > button span,
    [data-testid="stMain"] .stButton > button div,
    [data-testid="stMain"] button[kind="secondary"] p,
    [data-testid="stMain"] button[kind="secondary"] span,
    [data-testid="stMain"] button[kind="primary"] p,
    [data-testid="stMain"] button[kind="primary"] span,
    [data-testid="stMain"] .stLinkButton > a p,
    [data-testid="stMain"] .stLinkButton > a span,
    [data-testid="stMain"] [data-testid="stDownloadButton"] button p,
    [data-testid="stMain"] [data-testid="stDownloadButton"] button span,
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button p,
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button span,
    [data-testid="stMain"] [data-testid="stPageLink"] a p,
    [data-testid="stMain"] [data-testid="stPageLink"] a span {
        color: #0B4F71 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        -webkit-text-fill-color: #0B4F71 !important;
    }

    [data-testid="stMain"] .stButton > button:hover,
    [data-testid="stMain"] button[kind="secondary"]:hover,
    [data-testid="stMain"] button[kind="primary"]:hover,
    [data-testid="stMain"] button[data-testid^="stBaseButton"]:hover,
    [data-testid="stMain"] .stLinkButton > a:hover,
    [data-testid="stMain"] [data-testid="stDownloadButton"] button:hover,
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button:hover,
    [data-testid="stMain"] [data-testid="stPageLink"] a:hover,
    [data-testid="stMain"] [data-testid="stPageLink-NavLink"]:hover {
        background: #EAF7FC !important;
        border-color: #083C5D !important;
        color: #083C5D !important;
        box-shadow: none !important;
        transform: none !important;
    }

    [data-testid="stMain"] .stButton > button:hover p,
    [data-testid="stMain"] .stButton > button:hover span,
    [data-testid="stMain"] .stButton > button:hover div,
    [data-testid="stMain"] button[kind="secondary"]:hover p,
    [data-testid="stMain"] button[kind="secondary"]:hover span,
    [data-testid="stMain"] button[kind="primary"]:hover p,
    [data-testid="stMain"] button[kind="primary"]:hover span,
    [data-testid="stMain"] .stLinkButton > a:hover p,
    [data-testid="stMain"] .stLinkButton > a:hover span,
    [data-testid="stMain"] [data-testid="stDownloadButton"] button:hover p,
    [data-testid="stMain"] [data-testid="stDownloadButton"] button:hover span,
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button:hover p,
    [data-testid="stMain"] [data-testid="stFormSubmitButton"] button:hover span {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
    }

    [data-testid="stMain"] [class*="st-key-google_continue"] button,
    [data-testid="stMain"] [class*="st-key-google_continue"] button:active,
    [data-testid="stMain"] [class*="st-key-google_continue"] button:focus,
    [data-testid="stMain"] [class*="st-key-google_continue"] button:hover {
        background: var(--sp-primary) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--sp-primary) !important;
        box-shadow: 0 6px 16px rgba(1, 143, 199, 0.22) !important;
    }

    [data-testid="stMain"] [class*="st-key-google_continue"] button p,
    [data-testid="stMain"] [class*="st-key-google_continue"] button span,
    [data-testid="stMain"] [class*="st-key-google_continue"] button:hover p,
    [data-testid="stMain"] [class*="st-key-google_continue"] button:hover span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-baseweb="input"] > div,
    [data-baseweb="select"] > div,
    [data-baseweb="textarea"] > div {
        border-radius: 12px !important;
        border-color: var(--sp-border) !important;
        background: white !important;
        font-family: var(--sp-font) !important;
    }

    [data-baseweb="tag"] {
        border-radius: 999px !important;
        background: #E6F6FC !important;
        color: var(--sp-primary-dark) !important;
    }

    [data-testid="stMain"] [data-testid="stExpander"] {
        border: 3px solid #083C5D !important;
        border-radius: 14px !important;
        overflow: hidden;
        background: #FFFFFF !important;
    }

    [data-testid="stMain"] [data-testid="stAlert"] {
        border-radius: 14px !important;
        border: 3px solid #083C5D !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
        font-family: var(--sp-font);
    }

    [data-testid="stMain"] [data-testid="stForm"] {
        border: 3px solid #083C5D !important;
        background: #FFFFFF !important;
    }

    [data-testid="stMain"] [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 3px solid #083C5D !important;
        background: #FFFFFF !important;
    }

    [data-testid="stMain"] h2 {
        font-size: 1.45rem !important;
        font-weight: 750 !important;
        margin-top: 3rem !important;
        margin-bottom: 1.15rem !important;
    }

    [data-testid="stMain"] [data-testid="stElementContainer"]:has(hr) + [data-testid="stElementContainer"] h2 {
        margin-top: 1.9rem !important;
    }

    [data-testid="stMain"] h3 {
        margin-bottom: 0.28rem !important;
    }

    [data-testid="stMain"] [data-testid="stAlert"] {
        margin-top: 1.15rem !important;
        margin-bottom: 1.25rem !important;
    }

    hr {
        border: none !important;
        border-top: 1px solid #D7E5EC !important;
        margin: 3rem 0 0 !important;
    }

    [data-testid="stMain"] hr,
    [data-testid="stMain"] [data-testid="stMarkdownContainer"] hr,
    [data-testid="stMain"] [data-testid="stDivider"] hr {
        border: none !important;
        border-top: 1.75px solid #2b5d84 !important;
        border-color: #2b5d84 !important;
        color: #2b5d84 !important;
        margin: 2.6rem 0 0.4rem !important;
    }

    [data-testid="stMain"] [data-testid="stDivider"] {
        border-color: #2b5d84 !important;
        color: #2b5d84 !important;
    }

    [data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, var(--sp-primary), var(--sp-accent)) !important;
    }

    .sp-hero {
        background: linear-gradient(135deg, rgba(0,63,92,0.99), rgba(1,143,199,0.95));
        border-radius: 20px;
        padding: 1.75rem 1.9rem;
        box-shadow: 0 14px 32px rgba(0, 63, 92, 0.18);
        margin: 0.15rem 0 0 0;
        position: relative;
        overflow: hidden;
    }

    .sp-hero::after {
        content: "";
        position: absolute;
        width: 240px;
        height: 240px;
        right: -70px;
        top: -90px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
    }

    .sp-hero h1 {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        margin: 0 0 0.4rem 0;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        line-height: 1.12;
        position: relative;
        z-index: 1;
    }

    .sp-hero p {
        color: #EAF6FC !important;
        -webkit-text-fill-color: #EAF6FC !important;
        margin: 0;
        font-size: 0.93rem !important;
        font-weight: 500 !important;
        max-width: 720px;
        position: relative;
        z-index: 1;
    }

    .sp-page-header {
        background: linear-gradient(135deg, rgba(0,63,92,0.98), rgba(1,143,199,0.92));
        border-radius: 16px;
        padding: 1.15rem 1.3rem;
        box-shadow: 0 10px 28px rgba(0, 63, 92, 0.16);
        margin: 0.15rem 0 1rem 0;
        position: relative;
        overflow: hidden;
    }

    .sp-page-header::after {
        content: "";
        position: absolute;
        width: 140px;
        height: 140px;
        right: -40px;
        top: -50px;
        border-radius: 50%;
        background: rgba(255,255,255,0.07);
    }

    .sp-page-header h1 {
        color: #FFFFFF !important;
        margin: 0 0 0.35rem 0;
        font-size: 1.48rem !important;
        line-height: 1.15;
        position: relative;
        z-index: 1;
    }

    .sp-page-header p {
        color: #E1F5FC !important;
        margin: 0;
        font-size: 0.92rem;
        line-height: 1.45;
        max-width: 820px;
        position: relative;
        z-index: 1;
    }

    .sp-page-header .sp-kicker {
        position: relative;
        z-index: 1;
        margin-bottom: 0.45rem;
    }

    .sp-landing-hero {
        background: linear-gradient(135deg, rgba(0,63,92,0.99), rgba(1,143,199,0.94));
        border-radius: 20px;
        padding: 2.95rem 2.5rem 3.1rem;
        box-shadow: 0 14px 32px rgba(0, 63, 92, 0.16);
        margin: 0;
        position: relative;
        overflow: hidden;
    }

    .sp-landing-hero::before {
        content: "";
        position: absolute;
        width: 170px;
        height: 170px;
        left: -55px;
        bottom: -75px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
    }

    .sp-landing-hero::after {
        content: "";
        position: absolute;
        width: 240px;
        height: 240px;
        right: -70px;
        top: -90px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
    }

    .sp-landing-kicker {
        color: #BDEBFA !important;
        -webkit-text-fill-color: #BDEBFA !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.74rem !important;
        font-weight: 800 !important;
        margin: 0 0 0.7rem 0 !important;
        position: relative;
        z-index: 1;
    }

    .sp-landing-hero h1 {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        margin: 0 0 0.7rem 0 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        line-height: 1.12 !important;
        position: relative;
        z-index: 1;
    }

    .sp-landing-headline {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        margin: 0 0 0.85rem 0 !important;
        font-size: 1.38rem !important;
        font-weight: 650 !important;
        line-height: 1.35 !important;
        position: relative;
        z-index: 1;
        max-width: 780px;
    }

    .sp-landing-desc {
        color: #EAF6FC !important;
        -webkit-text-fill-color: #EAF6FC !important;
        margin: 0 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        line-height: 1.55 !important;
        max-width: 760px;
        position: relative;
        z-index: 1;
    }

    .sp-landing-welcome-title {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
        margin: 0 0 0.65rem 0 !important;
        text-align: center;
    }

    .sp-landing-welcome-copy {
        color: #4A5D6B !important;
        -webkit-text-fill-color: #4A5D6B !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        line-height: 1.55 !important;
        margin: 0 auto 1.35rem auto !important;
        max-width: 560px;
        text-align: center;
    }

    .sp-landing-lower {
        display: flex;
        flex-direction: column;
        gap: 2.6rem;
        margin: 0;
        padding: 0.15rem 0 0.4rem 0;
    }

    .sp-landing-features {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
        margin: 0;
    }

    .sp-landing-feature {
        background: #FFFFFF;
        border: 1px solid #D5DEE6;
        border-radius: 16px;
        box-shadow: 0 6px 16px rgba(8, 60, 93, 0.06);
        padding: 1.5rem 1.35rem 1.55rem;
    }

    .sp-landing-feature h3 {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        font-size: 1.06rem !important;
        font-weight: 750 !important;
        line-height: 1.3 !important;
        margin: 0 0 0.5rem 0 !important;
        min-height: 0 !important;
    }

    .sp-landing-feature p {
        color: #4A5D6B !important;
        -webkit-text-fill-color: #4A5D6B !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        margin: 0 !important;
    }

    .sp-landing-purpose {
        text-align: center;
        max-width: 680px;
        margin: 0 auto;
        padding: 0.85rem 0.75rem 0.35rem;
    }

    .sp-landing-purpose h2 {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        font-size: 1.18rem !important;
        font-weight: 750 !important;
        line-height: 1.35 !important;
        margin: 0 0 0.5rem 0 !important;
        margin-top: 0 !important;
    }

    .sp-landing-purpose p {
        color: #4A5D6B !important;
        -webkit-text-fill-color: #4A5D6B !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        line-height: 1.55 !important;
        margin: 0 !important;
    }

    .sp-landing-footer {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        padding: 0.15rem 0 0.1rem 0;
    }

    .sp-landing-contact {
        background: #FFFFFF;
        border: 1px solid #D5DEE6;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(8, 60, 93, 0.05);
        padding: 0.95rem 1.15rem 1rem;
        max-width: 390px;
        width: 100%;
    }

    .sp-landing-contact-title {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
        margin: 0 0 0.35rem 0 !important;
    }

    .sp-landing-contact p {
        color: #5A6A78 !important;
        -webkit-text-fill-color: #5A6A78 !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        line-height: 1.45 !important;
        margin: 0 0 0.45rem 0 !important;
    }

    .sp-landing-contact a,
    .sp-landing-contact a:visited {
        color: #018FC7 !important;
        -webkit-text-fill-color: #018FC7 !important;
        font-size: 0.88rem !important;
        font-weight: 650 !important;
        text-decoration: none !important;
        word-break: break-word;
    }

    .sp-landing-contact a:hover {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        text-decoration: underline !important;
    }

    [data-testid="stMain"]:has(.sp-landing-hero) [data-testid="stMainBlockContainer"] {
        padding-top: 1.45rem !important;
        padding-bottom: 2.6rem !important;
        min-height: calc(100vh - 1.5rem);
    }

    [data-testid="stMain"]:has(.sp-landing-hero) [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
        gap: 2.35rem !important;
    }

    [data-testid="stMain"]:has(.sp-landing-hero) [class*="st-key-landing_welcome"],
    [data-testid="stMain"]:has(.sp-landing-hero) [class*="st-key-landing_welcome"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid #D5DEE6 !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 24px rgba(8, 60, 93, 0.08) !important;
        padding: 2.4rem 2.55rem 2.2rem !important;
        max-width: 820px;
        margin: 0 auto !important;
        position: relative;
        z-index: 2;
    }

    [data-testid="stMain"]:has(.sp-landing-hero) [class*="st-key-landing_welcome"] [data-testid="stVerticalBlock"] {
        background: transparent !important;
        gap: 0.2rem !important;
    }

    [data-testid="stMain"]:has(.sp-landing-hero) [class*="st-key-google_continue"] {
        margin-top: 0.2rem !important;
        max-width: 100%;
    }

    [data-testid="stMain"]:has(.sp-landing-hero) [class*="st-key-google_continue"] button {
        min-height: 3.2rem !important;
        padding: 0.8rem 1.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        width: 100% !important;
    }

    .sp-kicker {
        color: #BDEBFA !important;
        -webkit-text-fill-color: #BDEBFA !important;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        font-size: 0.74rem;
        font-weight: 800;
        margin-bottom: 0.7rem;
        position: relative;
        z-index: 1;
    }

    .sp-section-subtitle {
        color: #083C5D !important;
        margin-top: 0;
        margin-bottom: 0.85rem;
        font-size: 0.9rem;
        font-weight: 550 !important;
    }

    .sp-pill {
        display: inline-block;
        padding: 0.32rem 0.62rem;
        margin: 0.15rem 0.15rem 0.15rem 0;
        border-radius: 999px;
        background: #E7F6FC;
        color: #00658F;
        border: 1px solid #B9E5F5;
        font-size: 0.82rem;
        font-weight: 700;
    }

    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"] {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .sp-hero {
            padding: 1.5rem;
            border-radius: 18px;
        }

        .sp-hero h1 {
            font-size: 1.55rem !important;
        }

        .sp-page-header {
            padding: 1.1rem 1.15rem;
            border-radius: 14px;
        }

        .sp-page-header h1 {
            font-size: 1.28rem !important;
        }

        .sp-landing-hero {
            padding: 2.1rem 1.4rem 2.2rem;
            border-radius: 16px;
        }

        .sp-landing-hero h1 {
            font-size: 1.75rem !important;
        }

        .sp-landing-headline {
            font-size: 1.12rem !important;
        }

        .sp-landing-desc {
            font-size: 0.94rem !important;
        }

        .sp-landing-features {
            grid-template-columns: 1fr;
        }

        .sp-landing-lower {
            gap: 1.85rem;
        }

        .sp-landing-footer {
            justify-content: stretch;
        }

        .sp-landing-contact {
            max-width: 100%;
        }

        [data-testid="stMain"]:has(.sp-landing-hero) [data-testid="stMainBlockContainer"] {
            padding-top: 1.1rem !important;
            padding-bottom: 2rem !important;
            min-height: 0;
        }

        [data-testid="stMain"]:has(.sp-landing-hero) [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
            gap: 1.65rem !important;
        }

        [data-testid="stMain"]:has(.sp-landing-hero) [class*="st-key-landing_welcome"],
        [data-testid="stMain"]:has(.sp-landing-hero) [class*="st-key-landing_welcome"] [data-testid="stVerticalBlockBorderWrapper"] {
            padding: 1.7rem 1.3rem 1.55rem !important;
            max-width: 100%;
        }

        .sp-landing-welcome-title {
            font-size: 1.4rem !important;
        }
    }

    /* FINAL sidebar nav — consistent light text, dark gray buttons, white active */
    section[data-testid="stSidebar"] .stButton button,
    section[data-testid="stSidebar"] .stButton button p,
    section[data-testid="stSidebar"] .stButton button span,
    section[data-testid="stSidebar"] .stButton button div,
    section[data-testid="stSidebar"] .stButton [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] .stButton [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] .stButton [data-testid="stMarkdownContainer"] span {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        line-height: 1.1 !important;
        font-family: var(--sp-font) !important;
        color: #F3F6F8 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:not([kind="primary"]),
    section[data-testid="stSidebar"] button[kind="secondary"] {
        background: #364957 !important;
        border-color: rgba(255,255,255,0.12) !important;
        color: #F3F6F8 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover,
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: #435563 !important;
        border-color: rgba(255,255,255,0.16) !important;
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover *,
    section[data-testid="stSidebar"] button[kind="secondary"]:hover * {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"],
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
    section[data-testid="stSidebar"] .stButton > button[data-testid^="stBaseButton-primary"],
    section[data-testid="stSidebar"] .stButton > button[data-testid^="stBaseButton-primary"]:hover {
        background: #FFFFFF !important;
        border-color: #FFFFFF !important;
        color: var(--sp-navy) !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"] *,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] p,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] span,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover *,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover p,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover span {
        color: var(--sp-navy) !important;
    }

    /* FINAL metric cards — beat page-level light text on nested p/span */
    html body [data-testid="stMetric"],
    html body [data-testid="stMetric"] *,
    html body [data-testid="stMetricLabel"],
    html body [data-testid="stMetricLabel"] *,
    html body [data-testid="stMetricLabel"] p,
    html body [data-testid="stMetricLabel"] span,
    html body [data-testid="stMetricLabel"] div,
    html body [data-testid="stMetricValue"],
    html body [data-testid="stMetricValue"] *,
    html body [data-testid="stMetricValue"] p,
    html body [data-testid="stMetricValue"] span,
    html body [data-testid="stMetricValue"] div,
    html body [data-testid="stMain"] [data-testid="stMetric"] [data-testid="stMarkdownContainer"] p,
    html body [data-testid="stMain"] [data-testid="stMetric"] p,
    html body [data-testid="stMain"] [data-testid="stMetric"] span,
    html body [data-testid="stMain"] [data-testid="stMetric"] div {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        opacity: 1 !important;
    }

    html body [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 3px solid #083C5D !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.09) !important;
    }

    html body [data-testid="stMetricLabel"],
    html body [data-testid="stMetricLabel"] p,
    html body [data-testid="stMetricLabel"] span {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
    }

    html body [data-testid="stMetricValue"],
    html body [data-testid="stMetricValue"] *,
    html body [data-testid="stMetricValue"] p,
    html body [data-testid="stMetricValue"] span,
    html body [data-testid="stMetricValue"] div {
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h1,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h2,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h3,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] li,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] span,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] div,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] label,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"],
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"],
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] p,
    [data-testid="stMain"] [data-testid="stExpander"] h1,
    [data-testid="stMain"] [data-testid="stExpander"] h2,
    [data-testid="stMain"] [data-testid="stExpander"] h3,
    [data-testid="stMain"] [data-testid="stExpander"] p,
    [data-testid="stMain"] [data-testid="stExpander"] span,
    [data-testid="stMain"] [data-testid="stExpander"] summary,
    [data-testid="stMain"] [data-testid="stAlert"] p,
    [data-testid="stMain"] [data-testid="stAlert"] span {
        color: #083C5D !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h3,
    [data-testid="stMain"] [data-testid="stExpander"] h3,
    [data-testid="stMain"] [data-testid="stExpander"] summary {
        font-weight: 650 !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] .stButton > button p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] .stButton > button span,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] button[kind="secondary"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] button[kind="secondary"] span {
        color: #0B4F71 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] button[kind="primary"] p,
    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] button[kind="primary"] span {
        color: #0B4F71 !important;
        font-weight: 700 !important;
    }

    html body [data-testid="stMain"] .sp-hero .sp-kicker,
    html body [data-testid="stMain"] .sp-hero h1,
    html body [data-testid="stMain"] .sp-hero h1 *,
    html body [data-testid="stMain"] .sp-landing-hero h1,
    html body [data-testid="stMain"] .sp-landing-hero h1 *,
    html body [data-testid="stMain"] .sp-landing-kicker,
    html body [data-testid="stMain"] .sp-landing-kicker * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    html body [data-testid="stMain"] .sp-landing-kicker,
    html body [data-testid="stMain"] .sp-landing-kicker * {
        color: #BDEBFA !important;
        -webkit-text-fill-color: #BDEBFA !important;
    }

    html body [data-testid="stMain"] .sp-hero p,
    html body [data-testid="stMain"] .sp-hero p *,
    html body [data-testid="stMain"] .sp-landing-headline,
    html body [data-testid="stMain"] .sp-landing-headline *,
    html body [data-testid="stMain"] .sp-landing-desc,
    html body [data-testid="stMain"] .sp-landing-desc * {
        color: #EAF6FC !important;
        -webkit-text-fill-color: #EAF6FC !important;
        font-weight: 500 !important;
    }

    html body [data-testid="stMain"] .sp-landing-headline,
    html body [data-testid="stMain"] .sp-landing-headline * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 650 !important;
    }

    html body [data-testid="stMain"] .sp-landing-welcome-title,
    html body [data-testid="stMain"] .sp-landing-welcome-title *,
    html body [data-testid="stMain"] .sp-landing-feature h3,
    html body [data-testid="stMain"] .sp-landing-feature h3 *,
    html body [data-testid="stMain"] .sp-landing-purpose h2,
    html body [data-testid="stMain"] .sp-landing-purpose h2 * {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
    }

    html body [data-testid="stMain"] .sp-landing-welcome-copy,
    html body [data-testid="stMain"] .sp-landing-welcome-copy *,
    html body [data-testid="stMain"] .sp-landing-feature p,
    html body [data-testid="stMain"] .sp-landing-feature p *,
    html body [data-testid="stMain"] .sp-landing-purpose p,
    html body [data-testid="stMain"] .sp-landing-purpose p *,
    html body [data-testid="stMain"] .sp-landing-contact p,
    html body [data-testid="stMain"] .sp-landing-contact p * {
        color: #4A5D6B !important;
        -webkit-text-fill-color: #4A5D6B !important;
        font-weight: 500 !important;
    }

    html body [data-testid="stMain"] .sp-landing-contact-title,
    html body [data-testid="stMain"] .sp-landing-contact-title * {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        font-weight: 700 !important;
    }

    html body [data-testid="stMain"] .sp-landing-contact a,
    html body [data-testid="stMain"] .sp-landing-contact a:visited {
        color: #018FC7 !important;
        -webkit-text-fill-color: #018FC7 !important;
        font-weight: 650 !important;
        text-decoration: none !important;
    }

    html body [data-testid="stMain"] .sp-page-header h1,
    html body [data-testid="stMain"] .sp-page-header h1 * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    html body [data-testid="stMain"] .sp-page-header p,
    html body [data-testid="stMain"] .sp-page-header p * {
        color: #EAF6FC !important;
        -webkit-text-fill-color: #EAF6FC !important;
        font-weight: 500 !important;
    }

    /* FINAL TYPOGRAPHY — wins over earlier rules and Streamlit defaults */
    html, :root, .stApp {
        --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        --sp-font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    html body .stApp,
    html body [data-testid="stMain"],
    html body [data-testid="stSidebar"],
    html body [data-testid="stHeader"],
    html body [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    html body .stApp h1,
    html body .stApp h2,
    html body .stApp h3,
    html body .stApp h4,
    html body .stApp p,
    html body .stApp li,
    html body .stApp label,
    html body .stApp span:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body .stApp div:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body .stApp a,
    html body .stApp button,
    html body .stApp input,
    html body .stApp textarea,
    html body .stApp select,
    html body [data-testid="stMain"] h1,
    html body [data-testid="stMain"] h2,
    html body [data-testid="stMain"] h3,
    html body [data-testid="stMain"] h4,
    html body [data-testid="stMain"] p,
    html body [data-testid="stMain"] li,
    html body [data-testid="stMain"] label,
    html body [data-testid="stSidebar"] h1,
    html body [data-testid="stSidebar"] h2,
    html body [data-testid="stSidebar"] h3,
    html body [data-testid="stSidebar"] p,
    html body [data-testid="stSidebar"] label,
    html body [data-testid="stMarkdownContainer"],
    html body [data-testid="stMarkdownContainer"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body [data-testid="stMetric"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body [data-testid="stButton"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body [data-testid="stCaptionContainer"],
    html body [data-testid="stCaptionContainer"] *,
    html body [data-testid="stWidgetLabel"],
    html body [data-testid="stWidgetLabel"] *,
    html body [data-testid="stAlert"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body [data-testid="stExpander"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body [data-testid="stTabs"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body [data-baseweb="input"],
    html body [data-baseweb="input"] *,
    html body [data-baseweb="select"],
    html body [data-baseweb="select"] *,
    html body [data-baseweb="textarea"],
    html body [data-baseweb="textarea"] *,
    html body [data-testid="stVerticalBlockBorderWrapper"] *:not([data-testid="stIconMaterial"]):not(svg):not(path):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body .stButton > button,
    html body .stButton > button *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body .stLinkButton > a,
    html body .stLinkButton > a * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    html body .stApp h1,
    html body [data-testid="stMain"] h1,
    html body [data-testid="stSidebar"] h1 {
        font-weight: 800 !important;
    }

    html body .stApp h2,
    html body [data-testid="stMain"] h2,
    html body [data-testid="stSidebar"] h2 {
        font-weight: 750 !important;
    }

    html body .stApp h3,
    html body .stApp h4,
    html body [data-testid="stMain"] h3,
    html body [data-testid="stMain"] h4,
    html body [data-testid="stSidebar"] h3,
    html body [data-testid="stMain"] [data-testid="stExpander"] summary,
    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] h3 {
        font-weight: 700 !important;
    }

    html body .stApp p,
    html body .stApp li,
    html body [data-testid="stMain"] p,
    html body [data-testid="stMain"] li,
    html body [data-testid="stMarkdownContainer"] p,
    html body [data-testid="stAlert"] p {
        font-weight: 500 !important;
    }

    html body .stApp label,
    html body [data-testid="stMain"] label,
    html body [data-testid="stWidgetLabel"],
    html body [data-testid="stWidgetLabel"] p,
    html body [data-testid="stCaptionContainer"],
    html body [data-testid="stCaptionContainer"] p {
        font-weight: 600 !important;
    }

    html body .stApp button,
    html body .stApp button *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body [data-testid="stButton"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    html body .stButton > button,
    html body .stButton > button *,
    html body .stLinkButton > a,
    html body .stLinkButton > a *,
    html body [data-testid="stFormSubmitButton"] button,
    html body [data-testid="stFormSubmitButton"] button *,
    html body [data-testid="stDownloadButton"] button,
    html body [data-testid="stDownloadButton"] button * {
        font-weight: 700 !important;
    }

    html body [data-testid="stMetricLabel"],
    html body [data-testid="stMetricLabel"] *,
    html body [data-testid="stMetricLabel"] p,
    html body [data-testid="stMetricLabel"] span {
        font-weight: 600 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    html body [data-testid="stMetricValue"],
    html body [data-testid="stMetricValue"] *,
    html body [data-testid="stMetricValue"] p,
    html body [data-testid="stMetricValue"] span,
    html body [data-testid="stMetricValue"] div {
        font-weight: 750 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    html body [data-testid="stMain"] .sp-hero h1,
    html body [data-testid="stMain"] .sp-hero h1 *,
    html body [data-testid="stMain"] .sp-page-header h1,
    html body [data-testid="stMain"] .sp-page-header h1 *,
    html body [data-testid="stMain"] .sp-landing-hero h1,
    html body [data-testid="stMain"] .sp-landing-hero h1 * {
        font-weight: 800 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    html body [data-testid="stMain"] .sp-hero p,
    html body [data-testid="stMain"] .sp-hero p *,
    html body [data-testid="stMain"] .sp-page-header p,
    html body [data-testid="stMain"] .sp-page-header p *,
    html body [data-testid="stMain"] .sp-landing-desc,
    html body [data-testid="stMain"] .sp-landing-desc * {
        font-weight: 500 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    html body [data-testid="stMain"] .sp-landing-purpose h2,
    html body [data-testid="stMain"] .sp-landing-purpose h2 * {
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        font-size: 1.18rem !important;
        font-weight: 750 !important;
        margin-top: 0 !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.35 !important;
    }

    html, body, .stApp,
    [data-testid="stMain"],
    [data-testid="stSidebar"],
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    [data-testid="stMetric"] *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    button,
    button *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]),
    input,
    textarea,
    select,
    label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    h1 {
        font-weight: 800 !important;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3, h4 {
        font-weight: 700 !important;
    }

    p, li {
        font-weight: 500 !important;
    }

    button, button *:not([data-testid="stIconMaterial"]):not([class*="material-symbols"]):not([class*="material-icons"]) {
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        font-weight: 700 !important;
    }

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p {
        font-weight: 550 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] .stButton > button span,
    [data-testid="stSidebar"] .stButton > button div {
        font-weight: 650 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    [data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"] *,
    [class*="material-symbols"],
    [class*="material-icons"],
    [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"],
    [data-testid="stHeader"] [data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapsedControl"] span,
    [data-testid="stHeader"] button:first-of-type span {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Symbols Sharp" !important;
        font-weight: 400 !important;
        font-style: normal !important;
        font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24 !important;
        letter-spacing: normal !important;
        line-height: 1 !important;
        text-transform: none !important;
        -webkit-font-smoothing: antialiased !important;
    }

    html body [data-testid="stMain"] .st-key-dash_journey_metrics [data-testid="stMetric"] {
        background: #F7FBFE !important;
        background-color: #F7FBFE !important;
        border: 2px solid #8A97A3 !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08) !important;
        padding: 1.5rem 1.45rem !important;
        cursor: default !important;
        transform: none !important;
        filter: none !important;
        transition: none !important;
    }

    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"],
    html body [data-testid="stMain"] [data-testid="stMetric"],
    html body [data-testid="stMain"] [data-testid="stAlert"],
    html body [data-testid="stMain"] [data-testid="stExpander"],
    html body [data-testid="stMain"] [data-testid="stForm"] {
        cursor: default !important;
        transform: none !important;
    }

    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"]:hover,
    html body [data-testid="stMain"] [data-testid="stMetric"]:hover,
    html body [data-testid="stMain"] [data-testid="stAlert"]:hover,
    html body [data-testid="stMain"] [data-testid="stExpander"]:hover,
    html body [data-testid="stMain"] [data-testid="stForm"]:hover {
        transform: none !important;
        filter: none !important;
        cursor: default !important;
    }

    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"]:hover {
        background: #FFFFFF !important;
        border-color: #083C5D !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08) !important;
        transform: none !important;
        filter: none !important;
        cursor: default !important;
    }

    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"]:has(.sp-info-card):hover,
    html body [data-testid="stMain"] .st-key-profile_cards [data-testid="stVerticalBlockBorderWrapper"]:hover {
        background: #FFFFFF !important;
        border-color: #083C5D !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08) !important;
        transform: none !important;
        filter: none !important;
        cursor: default !important;
    }

    html body [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child) [data-testid="stVerticalBlockBorderWrapper"]:hover {
        background: #F7FBFE !important;
        border-color: #0B4F71 !important;
        box-shadow: 0 10px 24px rgba(8, 60, 93, 0.09) !important;
        transform: none !important;
        filter: none !important;
        cursor: default !important;
    }

    html body [data-testid="stMain"] [data-testid="stMetric"]:hover {
        background: #FFFFFF !important;
        border-color: #083C5D !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.09) !important;
        transform: none !important;
        filter: none !important;
        cursor: default !important;
    }

    html body [data-testid="stMain"] .st-key-dash_journey_metrics [data-testid="stMetric"]:hover {
        background: #F7FBFE !important;
        background-color: #F7FBFE !important;
        border: 2px solid #8A97A3 !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08) !important;
        transform: none !important;
        filter: none !important;
        cursor: default !important;
        transition: none !important;
    }

    html body [data-testid="stMain"] .stButton > button:hover,
    html body [data-testid="stMain"] button[kind="secondary"]:hover,
    html body [data-testid="stMain"] button[kind="primary"]:hover,
    html body [data-testid="stMain"] button[data-testid^="stBaseButton"]:hover,
    html body [data-testid="stMain"] .stLinkButton > a:hover,
    html body [data-testid="stMain"] [data-testid="stDownloadButton"] button:hover,
    html body [data-testid="stMain"] [data-testid="stFormSubmitButton"] button:hover,
    html body [data-testid="stMain"] [data-testid="stPageLink"] a:hover,
    html body [data-testid="stMain"] [data-testid="stPageLink-NavLink"]:hover,
    html body [data-testid="stSidebar"] .stButton > button:hover,
    html body [data-testid="stSidebar"] button[kind="secondary"]:hover,
    html body [data-testid="stSidebar"] button[kind="primary"]:hover,
    html body .sp-contact-email:hover {
        cursor: pointer !important;
    }


    /* ============================================================
       FINAL POLISH: STATIC INFO CARDS + SIDEBAR LOGO ALIGNMENT
       ============================================================ */

    /* NYC should use the same tight tracking as the rest of the logo. */
    html body [data-testid="stSidebar"] .sp-sidebar-title .sp-title-nyc {
        letter-spacing: 0 !important;
        word-spacing: 0 !important;
        font-stretch: normal !important;
        text-align: center !important;
    }

    /* Keep the top title centered and let the underline follow its width. */
    html body [data-testid="stSidebar"] .sp-sidebar-brand {
        width: max-content !important;
        max-width: 100% !important;
    }

    html body [data-testid="stSidebar"] .sp-sidebar-title {
        width: max-content !important;
        max-width: 100% !important;
        align-items: stretch !important;
    }

    html body [data-testid="stSidebar"] .sp-sidebar-title .sp-title-line {
        width: max-content !important;
        max-width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        justify-content: center !important;
    }

    /* Slightly longer line so it visually lines up with the full brand title. */
    html body [data-testid="stSidebar"] .sp-sidebar-accent {
        width: calc(100% + 0.6rem) !important;
        max-width: none !important;
        height: 5px !important;
        margin-left: -0.3rem !important;
        margin-top: 0.5rem !important;
        border-radius: 999px !important;
    }

    /* Non-interactive information cards should never react visually to hover. */
    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"],
    html body [data-testid="stMain"] [data-testid="stMetric"],
    html body [data-testid="stMain"] [data-testid="stAlert"],
    html body [data-testid="stMain"] [data-testid="stForm"] {
        cursor: default !important;
        transition: none !important;
        transform: none !important;
        filter: none !important;
    }

    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"]:hover {
        background: #FFFFFF !important;
        border: 3px solid #083C5D !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08) !important;
        transform: none !important;
        filter: none !important;
        opacity: 1 !important;
        cursor: default !important;
        transition: none !important;
    }

    html body [data-testid="stMain"] [data-testid="stMetric"]:hover {
        background: #FFFFFF !important;
        border: 3px solid #083C5D !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.09) !important;
        transform: none !important;
        filter: none !important;
        opacity: 1 !important;
        cursor: default !important;
        transition: none !important;
    }

    /* Dashboard journey metrics match Continue Your Journey card chrome. */
    html body [data-testid="stMain"] .st-key-dash_journey_metrics [data-testid="stMetric"],
    html body [data-testid="stMain"] .st-key-dash_journey_metrics [data-testid="stMetric"]:hover {
        background: #F7FBFE !important;
        background-color: #F7FBFE !important;
        border: 2px solid #8A97A3 !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08) !important;
        transform: none !important;
        filter: none !important;
        cursor: default !important;
        transition: none !important;
        opacity: 1 !important;
    }

    /* These specific light cards should remain light and static as well. */
    html body [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child) [data-testid="stVerticalBlockBorderWrapper"],
    html body [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child) [data-testid="stVerticalBlockBorderWrapper"]:hover {
        background: #F7FBFE !important;
        border: 3px solid #0B4F71 !important;
        box-shadow: 0 10px 24px rgba(8, 60, 93, 0.09) !important;
        transform: none !important;
        filter: none !important;
        cursor: default !important;
        transition: none !important;
    }

    /* Real controls keep the pointer cursor. */
    html body .stButton button,
    html body .stLinkButton a,
    html body a[href],
    html body [data-testid="stSidebar"] button,
    html body [data-testid="stFormSubmitButton"] button,
    html body [data-testid="stDownloadButton"] button {
        cursor: pointer !important;
    }

    html body [data-testid="stMain"]
    [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child)
    > div
    > [data-testid="stVerticalBlock"][height="100%"],
    html body [data-testid="stMain"]
    [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child)
    > div
    > [data-testid="stVerticalBlock"][height="100%"]:hover {
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }

    html body [data-testid="stMain"]
    .st-key-dash_continue_journey
    [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child)
    > div
    > [data-testid="stVerticalBlock"][height="100%"],
    html body [data-testid="stMain"]
    .st-key-dash_continue_journey
    [data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child)
    > div
    > [data-testid="stVerticalBlock"][height="100%"]:hover {
        border: 2px solid #8A97A3 !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 22px rgba(8, 60, 93, 0.08) !important;
    }

    html body [data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
        position: relative !important;
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        min-height: 50px !important;
        height: 50px !important;
        padding: 0.35rem 0.4rem 0.2rem 0.4rem !important;
        margin: 0 !important;
        background: transparent !important;
        overflow: visible !important;
    }

    html body [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
    html body [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button,
    html body [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] [role="button"],
    html body [data-testid="stSidebar"] [data-testid="stSidebarHeader"] button {
        width: 42px !important;
        height: 42px !important;
        min-width: 42px !important;
        min-height: 42px !important;
        max-width: 42px !important;
        max-height: 42px !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: #0B1F33 !important;
        background-color: #0B1F33 !important;
        color: #FFFFFF !important;
        border: 1px solid #0B1F33 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.24) !important;
        flex: 0 0 42px !important;
        position: relative !important;
        top: auto !important;
        right: auto !important;
        left: auto !important;
        z-index: 6 !important;
        overflow: hidden !important;
    }

    html body [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] svg,
    html body [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
    html body [data-testid="stSidebar"] [data-testid="stSidebarHeader"] button svg,
    html body [data-testid="stSidebar"] [data-testid="stSidebarHeader"] button [data-testid="stIconMaterial"],
    html body [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] span,
    html body [data-testid="stSidebar"] [data-testid="stSidebarHeader"] button span {
        width: 22px !important;
        height: 22px !important;
        min-width: 22px !important;
        min-height: 22px !important;
        font-size: 22px !important;
        line-height: 1 !important;
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
    }

    html body [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(.sp-sidebar-brand),
    html body [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(.sp-sidebar-brand) *:not(.sp-sidebar-accent),
    html body [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(.sp-sidebar-brand) pre,
    html body [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(.sp-sidebar-brand) code,
    html body [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.sp-sidebar-brand),
    html body [data-testid="stSidebar"] .sp-sidebar-brand,
    html body [data-testid="stSidebar"] .sp-sidebar-title,
    html body [data-testid="stSidebar"] .sp-title-line,
    html body [data-testid="stSidebar"] .sp-title-line span,
    html body [data-testid="stSidebar"] .sp-title-blue,
    html body [data-testid="stSidebar"] .sp-title-yellow,
    html body [data-testid="stSidebar"] .sp-title-nyc {
        background: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
        outline: none !important;
    }

    html body [data-testid="stSidebar"] .sp-sidebar-brand {
        width: max-content !important;
        max-width: 100% !important;
        margin: 0.2rem auto 0.55rem auto !important;
        padding: 0 !important;
        align-items: center !important;
        text-align: center !important;
    }

    html body [data-testid="stSidebar"] .sp-sidebar-title {
        width: max-content !important;
        max-width: 100% !important;
        align-items: center !important;
        text-align: center !important;
    }

    html body [data-testid="stSidebar"] .sp-sidebar-title .sp-title-blue {
        color: #72D2F2 !important;
        -webkit-text-fill-color: #72D2F2 !important;
        font-weight: 800 !important;
        padding: 0 !important;
    }

    html body [data-testid="stSidebar"] .sp-sidebar-title .sp-title-yellow {
        color: #F4C542 !important;
        -webkit-text-fill-color: #F4C542 !important;
        font-weight: 800 !important;
        padding: 0 !important;
    }

    html body [data-testid="stSidebar"] .sp-sidebar-title .sp-title-nyc,
    html body [data-testid="stSidebar"] .sp-sidebar-title .sp-title-nyc * {
        display: block !important;
        width: max-content !important;
        max-width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        letter-spacing: 0 !important;
        word-spacing: 0 !important;
        font-stretch: normal !important;
        text-align: center !important;
        color: #72D2F2 !important;
        -webkit-text-fill-color: #72D2F2 !important;
        font-weight: 800 !important;
        background: transparent !important;
        padding: 0 !important;
    }

    html body [data-testid="stSidebar"] .sp-sidebar-accent,
    html body [data-testid="stSidebar"] .sp-sidebar-brand .sp-sidebar-accent,
    html body [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(.sp-sidebar-brand) .sp-sidebar-accent {
        width: 100% !important;
        max-width: 100% !important;
        height: 4px !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        background: #72D2F2 !important;
        background-color: #72D2F2 !important;
        border-radius: 999px !important;
    }

    html body [data-testid="stSidebarCollapsedControl"],
    html body [data-testid="stSidebarCollapsedControl"] button,
    html body [data-testid="stSidebarCollapsedControl"] [role="button"] {
        width: 48px !important;
        height: 48px !important;
        min-width: 48px !important;
        min-height: 48px !important;
        max-width: 48px !important;
        max-height: 48px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: fixed !important;
        top: 0.75rem !important;
        left: 0.75rem !important;
        background: #0B1F33 !important;
        background-color: #0B1F33 !important;
        color: #FFFFFF !important;
        border: 1px solid #0B1F33 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.24) !important;
    }

    html body [data-testid="stSidebarCollapsedControl"] svg,
    html body [data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"],
    html body [data-testid="stSidebarCollapsedControl"] span,
    html body [data-testid="stSidebarCollapsedControl"] button svg,
    html body [data-testid="stSidebarCollapsedControl"] button [data-testid="stIconMaterial"],
    html body [data-testid="stSidebarCollapsedControl"] button span {
        width: 26px !important;
        height: 26px !important;
        min-width: 26px !important;
        min-height: 26px !important;
        font-size: 26px !important;
        line-height: 1 !important;
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
    }

    html body [data-testid="stMain"] .st-key-project_equipment_expander,
    html body [data-testid="stMain"] .st-key-project_equipment_expander [data-testid="stExpander"],
    html body [data-testid="stMain"] .st-key-project_equipment_expander details {
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        height: auto !important;
        min-height: 0 !important;
        overflow: visible !important;
    }

    html body [data-testid="stMain"] .st-key-project_equipment_expander summary,
    html body [data-testid="stMain"] .st-key-project_equipment_expander [data-testid="stExpanderHeader"],
    html body [data-testid="stMain"] .st-key-project_equipment_expander [data-testid="stBaseButton-headerNoPadding"] {
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        height: auto !important;
        min-height: 2.75rem !important;
        margin: 0 !important;
        padding: 0.7rem 0.95rem !important;
        line-height: 1.35 !important;
        white-space: normal !important;
        overflow: visible !important;
        transform: none !important;
    }

    html body [data-testid="stMain"] .st-key-project_equipment_expander [data-testid="stExpanderDetails"],
    html body [data-testid="stMain"] .st-key-project_equipment_expander [data-testid="stExpanderContent"],
    html body [data-testid="stMain"] .st-key-project_equipment_expander details > div {
        position: relative !important;
        display: block !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0.15rem 0.95rem 0.95rem 0.95rem !important;
        overflow: visible !important;
        transform: none !important;
    }

    html body [data-testid="stMain"] .st-key-project_equipment_choices,
    html body [data-testid="stMain"] .st-key-project_equipment_choices [data-testid="stVerticalBlock"],
    html body [data-testid="stMain"] .st-key-project_equipment_choices [data-testid="stElementContainer"] {
        height: auto !important;
        min-height: 0 !important;
        overflow: visible !important;
    }

    html body [data-testid="stMain"] .st-key-project_equipment_choices [data-testid="stWidgetLabel"],
    html body [data-testid="stMain"] .st-key-project_equipment_choices [data-testid="stWidgetLabel"] p,
    html body [data-testid="stMain"] .st-key-project_equipment_choices label {
        position: relative !important;
        display: block !important;
        float: none !important;
        height: auto !important;
        min-height: auto !important;
        margin: 0 0 0.4rem 0 !important;
        padding: 0 !important;
        line-height: 1.35 !important;
        white-space: normal !important;
        overflow: visible !important;
        transform: none !important;
    }

    html body [data-testid="stMain"] .st-key-project_equipment_choices [data-baseweb="select"],
    html body [data-testid="stMain"] .st-key-project_equipment_choices [data-baseweb="select"] > div,
    html body [data-testid="stMain"] .st-key-project_equipment_choices [data-baseweb="input"],
    html body [data-testid="stMain"] .st-key-project_equipment_choices [data-baseweb="input"] > div {
        min-height: 42px !important;
        height: auto !important;
        padding-top: 0.4rem !important;
        padding-bottom: 0.4rem !important;
        padding-left: 0.7rem !important;
        padding-right: 0.7rem !important;
        box-sizing: border-box !important;
        align-items: center !important;
    }

    [data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"] *,
    [class*="material-symbols"],
    [class*="material-icons"],
    [data-testid="stExpander"] [data-testid="stIconMaterial"],
    [data-testid="stExpander"] [data-testid="stIconMaterial"] *,
    html body [data-testid="stIconMaterial"],
    html body [data-testid="stIconMaterial"] *,
    html body [class*="material-symbols"],
    html body [class*="material-icons"],
    html body .stApp [data-testid="stIconMaterial"],
    html body .stApp [data-testid="stIconMaterial"] *,
    html body .stApp [class*="material-symbols"],
    html body .stApp [class*="material-icons"],
    html body [data-testid="stExpander"] [data-testid="stIconMaterial"],
    html body [data-testid="stExpander"] [data-testid="stIconMaterial"] *,
    html body [data-testid="stExpander"] [class*="material-symbols"],
    html body [data-testid="stExpander"] [class*="material-icons"],
    html body [data-testid="stExpander"] span[class*="material-symbols"],
    html body [data-testid="stExpander"] span[class*="material-icons"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Symbols Sharp" !important;
        font-weight: 400 !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        line-height: 1 !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: "liga" !important;
        -webkit-font-smoothing: antialiased !important;
        font-feature-settings: "liga" !important;
    }

    html body .stApp [data-testid="stMain"] [class*="st-key-college_category_label"],
    html body .stApp [data-testid="stMain"] [class*="st-key-college_category_label"] p,
    html body .stApp [data-testid="stMain"] [class*="st-key-college_category_label"] span,
    html body .stApp [data-testid="stMain"] [class*="st-key-college_category_label"] div,
    html body .stApp [data-testid="stMain"] [class*="st-key-college_category_label"] [data-testid="stMarkdownContainer"],
    html body .stApp [data-testid="stMain"] [class*="st-key-college_category_label"] [data-testid="stMarkdownContainer"] p,
    html body .stApp [data-testid="stMain"] [class*="st-key-college_category_label"] [data-testid="stMarkdownContainer"] span,
    html body .stApp [data-testid="stMain"] [class*="st-key-college_category_label"] [data-testid="stMarkdownContainer"] strong,
    html body .stApp [data-testid="stMain"] .college-category-label,
    html body .stApp [data-testid="stMain"] p.college-category-label,
    html body .stApp [data-testid="stMain"] [data-testid="stMarkdownContainer"] p.college-category-label {
        display: block !important;
        text-align: left !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        line-height: 1.3 !important;
        letter-spacing: 0.01em !important;
        margin-top: 0.45rem !important;
        margin-bottom: 0.5rem !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding: 0 !important;
        color: #083C5D !important;
        background: none !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        font-family: Inter, "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif !important;
    }

    html body [data-testid="stMain"] .college-plain-stat,
    html body [data-testid="stMain"] .college-plain-stat:hover,
    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] .college-plain-stat,
    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] .college-plain-stat:hover {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 1px solid #AAB4BE !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        padding: 0.75rem 0.85rem !important;
        margin: 0 !important;
        min-height: 0 !important;
        height: auto !important;
        width: 100% !important;
        box-sizing: border-box !important;
        display: block !important;
        align-self: flex-start !important;
    }

    html body [data-testid="stMain"] [data-testid="stElementContainer"]:has(.college-plain-stat),
    html body [data-testid="stMain"] [data-testid="stMarkdownContainer"]:has(.college-plain-stat),
    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stElementContainer"]:has(.college-plain-stat),
    html body [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"]:has(.college-plain-stat) {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: 0 !important;
        height: auto !important;
        flex: 0 0 auto !important;
    }

    html body [data-testid="stMain"] .college-plain-stat-label {
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        margin: 0 0 0.45rem 0 !important;
        line-height: 1.35 !important;
    }

    html body [data-testid="stMain"] .college-plain-stat-value {
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        line-height: 1.25 !important;
        margin: 0 !important;
    }

    html body [data-testid="stMain"] .college-plain-stat-value .college-competition-star-filled,
    html body [data-testid="stMain"] .college-competition-star-filled {
        color: #F4C542 !important;
        -webkit-text-fill-color: #F4C542 !important;
    }

    html body [data-testid="stMain"] .college-plain-stat-value .college-competition-star-empty,
    html body [data-testid="stMain"] .college-competition-star-empty {
        color: #C5CED6 !important;
        -webkit-text-fill-color: #C5CED6 !important;
    }

    html body [data-testid="stMain"] .college-plain-stat-body {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #083C5D !important;
        -webkit-text-fill-color: #083C5D !important;
        line-height: 1.4 !important;
        margin: 0 !important;
    }

    html body [data-testid="stMain"] .college-plain-stat-caption {
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        color: #5A6A78 !important;
        -webkit-text-fill-color: #5A6A78 !important;
        margin: 0.35rem 0 0 0 !important;
        line-height: 1.35 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def render_page_header(
    title,
    subtitle="",
    kicker=""
):
    title_safe = html_module.escape(
        str(title)
    )
    kicker_html = ""

    if kicker:
        kicker_safe = html_module.escape(
            str(kicker)
        )
        kicker_html = (
            f'<div class="sp-kicker">'
            f'{kicker_safe}</div>'
        )

    subtitle_html = ""

    if subtitle:
        subtitle_safe = html_module.escape(
            str(subtitle)
        )
        subtitle_html = (
            f'<p>{subtitle_safe}</p>'
        )

    header_html = (
        f'<div class="sp-page-header">'
        f'{kicker_html}'
        f'<h1>{title_safe}</h1>'
        f'{subtitle_html}'
        f'</div>'
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True
    )


def sidebar_nav_button(
    label,
    page_name,
    key
):
    is_active = (
        st.session_state.current_page
        == page_name
    )

    if st.button(
        label,
        use_container_width=True,
        icon=None,
        type=(
            "primary"
            if is_active
            else "secondary"
        ),
        key=key,
    ):

        st.session_state.current_page = (
            page_name
        )

        st.rerun()




# ============================================================
# SUPABASE
# ============================================================

@st.cache_resource
def init_supabase():
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["service_key"]
    )


try:
    supabase = init_supabase()
    supabase_connected = True

except Exception:
    logger.exception(
        "Supabase client initialization failed"
    )
    supabase = None
    supabase_connected = False


# ============================================================
# LOCAL DATABASES
# ============================================================


try:
    opportunities = pd.read_csv("data/opportunities.csv")
except Exception:
    opportunities = pd.DataFrame()

# ------------------------------------------------------------
# CURATED OPPORTUNITY EXPANSION
# These records give the Opportunities page a stronger mix of
# selective programs, internships, research, paid work, and
# accessible NYC opportunities.
# ------------------------------------------------------------

extra_opportunities = [
    {
        "name": "Research Science Institute (RSI) at MIT",
        "organization": "Center for Excellence in Education / MIT",
        "description": "Free six-week summer STEM program for rising seniors combining advanced coursework with original mentored research.",
        "opportunity_type": "Research",
        "fields": "Engineering;Computer Science;Mathematics;Physics;Biology;Chemistry;Research",
        "grades": "11",
        "age_range": "No simple age range publicly specified — rising seniors",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 deadline was December 10, 2025",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "50 U.S. students selected from 1,500+ U.S. applicants in published CEE guidance",
        "internship_potential": "Yes — intensive mentored research experience",
        "format": "Residential — MIT, Cambridge, Massachusetts",
        "paid_status": "Not paid / Free Program",
        "requirements": "Current 11th grader; application, recommendations, transcript; standardized scores if available",
        "url": "https://www.cee.org/research-science-institute"
    },
    {
        "name": "Carnegie Mellon SAMS",
        "organization": "Carnegie Mellon University",
        "description": "Free six-week residential STEM program with rigorous academics, project work, and community-building.",
        "opportunity_type": "Summer Program",
        "fields": "Engineering;Computer Science;Mathematics;Science;STEM",
        "grades": "11",
        "age_range": "16+ by program start",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Program is offered at no cost to selected students",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 deadline was February 1",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "No — intensive academic/project-based STEM program",
        "format": "Residential — Pittsburgh, Pennsylvania",
        "paid_status": "Not paid / Free Program",
        "requirements": "Current 11th grader; age 16+ by start; U.S. citizen or permanent resident",
        "url": "https://www.cmu.edu/pre-college/academic-programs/sams.html"
    },
    {
        "name": "Columbia Engineering the Next Generation (ENG)",
        "organization": "Columbia Engineering",
        "description": "Paid six-week summer engineering research program for rising NYC seniors working with Columbia researchers and mentors.",
        "opportunity_type": "Research",
        "fields": "Engineering;Computer Science;Biomedical Engineering;Environmental Engineering;AI;Data Science",
        "grades": "11",
        "age_range": "Check official work-eligibility requirements",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — paid engineering research experience",
        "format": "In person — Columbia University, NYC",
        "paid_status": "Paid — 2026 FoR stipend listed at $17/hour, 25 hours/week",
        "requirements": "Current 11th grader/rising NYC senior; NYC school; legally allowed to work in NYC; FoR requires prior work or volunteer experience",
        "url": "https://outreach.engineering.columbia.edu/eng"
    },
    {
        "name": "Rockefeller University Jumpstart + SSRP",
        "organization": "The Rockefeller University / RockEDU",
        "description": "NYC research pathway combining spring laboratory preparation with full-time summer research; Jumpstart supports 16 students.",
        "opportunity_type": "Research",
        "fields": "Biology;Biomedical Science;Laboratory Research;Data Analysis;Science",
        "grades": "11;12",
        "age_range": "16+ by program start",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "2027 date not yet announced; 2026 Jumpstart deadline was January 2",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported; Jumpstart supports 16 students",
        "internship_potential": "Yes — spring preparation plus full-time summer laboratory research",
        "format": "In person — Rockefeller University, NYC",
        "paid_status": "Check official 2027 program information",
        "requirements": "NYC high school junior or senior; age 16+ at start; full spring/summer commitment; selected applicants interview",
        "url": "https://www.rockefeller.edu/outreach/lab-jumpstart/"
    },
    {
        "name": "Columbia University Science Honors Program (SHP)",
        "organization": "Columbia University",
        "description": "Highly selective academic-year Saturday program offering advanced mathematics and science courses taught by Columbia researchers.",
        "opportunity_type": "Academic-Year Program",
        "fields": "Mathematics;Physics;Chemistry;Biology;Computer Science;Engineering;Science",
        "grades": "10;11;12",
        "age_range": "No simple age range publicly specified — grade-based eligibility",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "$900/year for new students beginning Fall 2026",
        "financial_aid": "Program fee waivers may be available for documented financial hardship",
        "application_status": "Future Cycle",
        "deadline": "Next cycle date not yet announced; applications typically open in early February",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "No — advanced academic enrichment",
        "format": "In person — Saturdays at Columbia University",
        "paid_status": "Not paid",
        "requirements": "Apply in grades 9–11 for following year; live within 75 miles; application, essay, transcript, recommendation, entrance exam",
        "url": "https://outreach.engineering.columbia.edu/SHP"
    },
    {
        "name": "AMNH Science Research Mentoring Program (SRMP)",
        "organization": "American Museum of Natural History",
        "description": "Paid year-long NYC research program where students conduct original research with AMNH-affiliated scientists.",
        "opportunity_type": "Research",
        "fields": "Biology;Earth Science;Astronomy;Data Science;Computer Science;Natural Sciences;Research",
        "grades": "10;11",
        "age_range": "No simple age range publicly specified — current 10th or 11th graders",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "Class of 2028 applications expected Winter 2027",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — year-long mentored original research",
        "format": "In person — American Museum of Natural History, NYC",
        "paid_status": "$2,500 stipend upon completion of research and program requirements",
        "requirements": "NYC student in current grade 10 or 11; passing classes; must meet AMNH prior-program or partner-school/program eligibility",
        "url": "https://www.amnh.org/learn-teach/teens/science-research-mentoring-program"
    },
    {
        "name": "New York Academy of Sciences Junior Academy",
        "organization": "New York Academy of Sciences",
        "description": (
            "A free global virtual STEM innovation program where students ages "
            "13–17 join international teams and work with STEM mentors to develop "
            "solutions to real-world problems through 10-week Innovation Challenges."
        ),
        "opportunity_type": "Research",
        "fields": "Engineering;Computer Science;Science;Technology;Innovation;Research;Design Thinking",
        "grades": "9;10;11;12",
        "age_range": "13–17 during the program",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed — program is completely free",
        "application_status": "Fall 2026 Closed — Decisions August 31, 2026",
        "deadline": "Fall 2026 applications: April 1–July 9, 2026; future recruitment dates should be confirmed with NYAS",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported; NYAS states it receives thousands of applications worldwide",
        "internship_potential": "No — international team-based STEM innovation, research, design, and mentorship",
        "format": "Virtual / Global — Launchpad platform",
        "paid_status": "Not paid / Free Program",
        "requirements": (
            "Age 13–17 during the program; strong interest in STEM; comfortable "
            "reading, writing, and communicating in English; parental/guardian "
            "consent; ability to work on an international team; approximately "
            "3–4 hours per week during challenge periods."
        ),
        "url": "https://www.nyas.org/learning/high-school-research-programs/the-junior-academy/"
    },
    {
        "name": "MITES Summer",
        "age_range": "No simple age range publicly specified — rising seniors",
        "organization": "MIT",
        "description": (
            "A six-week residential STEM program for rising high school "
            "seniors featuring rigorous courses, hands-on projects, "
            "mentorship, and college admissions guidance."
        ),
        "opportunity_type": "Summer Program",
        "fields": "Engineering;Computer Science;Mathematics;Science",
        "grades": "11",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "2027 date not yet announced",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "No — academic STEM enrichment",
        "format": "Residential",
        "paid_status": "Unpaid / Free Program",
        "requirements": "Rising senior; application; recommendations; academic information",
        "url": "https://mites.mit.edu/discover-mites/faq-for-prospective-students/faqs-mites-semester-and-mites-summer/"
    },
    {
        "name": "Columbia Engineering SHAPE",
        "age_range": "14–18",
        "organization": "Columbia University",
        "description": (
            "A selective pre-college engineering program where high school "
            "students study engineering and technology through intensive "
            "courses, projects, and collaboration."
        ),
        "opportunity_type": "Summer Program",
        "fields": "Engineering;Computer Science;Biomedical Engineering;Technology",
        "grades": "9;10;11;12",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Tuition-based",
        "financial_aid": "Available",
        "application_status": "Future Cycle",
        "deadline": "2027 date not yet announced",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "No — project-based pre-college program",
        "format": "Commuter / Residential",
        "paid_status": "Not paid",
        "requirements": "Application; essays; transcript/report card; recommendation; resume",
        "url": "https://outreach.engineering.columbia.edu/shape/apply"
    },
    {
        "name": "NASA GISS / CCRI High School Research",
        "age_range": "Varies by project — check official eligibility",
        "organization": "NASA Goddard Institute for Space Studies",
        "description": (
            "Research opportunities in the NYC area where selected high "
            "school students can work with NASA-supported research teams "
            "on climate and Earth science projects."
        ),
        "opportunity_type": "Research",
        "fields": "Earth Science;Climate Science;Data Science;Computer Science;Research",
        "grades": "10;11;12",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Check Official Site",
        "deadline": "Check official site for next cycle",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — research internship experience",
        "format": "NYC / project dependent",
        "paid_status": "Varies by project",
        "requirements": "Project-specific; some opportunities require U.S. citizenship and GPA eligibility",
        "url": "https://www.giss.nasa.gov/edu/intern/"
    },
    {
        "name": "NASA Glenn High School Engineering Institute",
        "age_range": "16+ by program start",
        "organization": "NASA Glenn Research Center",
        "description": (
            "A one-week engineering institute where students use the "
            "engineering design process to build and test prototypes "
            "connected to NASA aerospace and space missions."
        ),
        "opportunity_type": "Summer Program",
        "fields": "Engineering;Aerospace;Mechanical Engineering;Electrical Engineering",
        "grades": "11;12",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "2027 date not yet announced",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "No — engineering work-based learning experience",
        "format": "In person — Cleveland, Ohio",
        "paid_status": "Not paid",
        "requirements": "Upcoming junior/senior; age requirement; GPA threshold; recommendation; citizenship/LPR eligibility",
        "url": "https://www.nasa.gov/learning-resources/for-students-grades-9-12/nasa-glenn-high-school-engineering-institute/"
    },
    {
        "name": "Learn & Earn",
        "age_range": "16–21",
        "organization": "NYC Department of Youth & Community Development",
        "description": (
            "A year-round NYC program combining academic support, college "
            "preparation, career exploration, work-readiness training, "
            "leadership activities, and a paid summer internship."
        ),
        "opportunity_type": "Internship",
        "fields": "Engineering;Computer Science;Healthcare;Business;Career Exploration",
        "grades": "11;12",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Seasonal",
        "deadline": "Enrollment typically September 1–30",
        "selectivity": "Eligibility Based",
        "selectivity_stars": 2,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — paid six-week summer internship",
        "format": "NYC / In person",
        "paid_status": "Paid internship component",
        "requirements": "NYC junior/senior; age and income/eligibility requirements apply",
        "url": "https://www.nyc.gov/site/dycd/services/jobs-internships/learn-and-earn.page"
    },
    {
        "name": "Work, Learn & Grow",
        "age_range": "16–21",
        "organization": "NYC Department of Youth & Community Development",
        "description": (
            "A paid NYC work-based learning program that can include "
            "college coursework, career exploration, academic support, "
            "and internships during the school year."
        ),
        "opportunity_type": "Internship",
        "fields": "Engineering;Computer Science;Architecture;Healthcare;Career Exploration",
        "grades": "10;11;12",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Eligibility Based",
        "deadline": "Check official site for current cycle",
        "selectivity": "Eligibility Based",
        "selectivity_stars": 2,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — paid work experience / internships",
        "format": "NYC / In person",
        "paid_status": "Paid",
        "requirements": "NYC youth; age, school, and prior-program eligibility can apply",
        "url": "https://www.nyc.gov/site/dycd/services/jobs-internships/work-learn-grow-employment-program.page"
    },
    {
        "name": "NYC Summer Youth Employment Program (SYEP)",
        "age_range": "14–24",
        "organization": "NYC Department of Youth & Community Development",
        "description": (
            "NYC's large youth employment program connecting young people "
            "with paid summer work experience and career exploration across "
            "many industries, including technology and STEM-related fields."
        ),
        "opportunity_type": "Internship",
        "fields": "Computer Science;Engineering;Healthcare;Business;Career Exploration",
        "grades": "9;10;11;12",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Seasonal",
        "deadline": "Check official site for next application cycle",
        "selectivity": "Accessible / Lottery or Placement Based",
        "selectivity_stars": 1,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — paid summer work experience",
        "format": "NYC",
        "paid_status": "Paid",
        "requirements": "NYC youth; program-specific age and work eligibility requirements",
        "url": "https://www.nyc.gov/site/dycd/services/jobs-internships/summer-youth-employment-program-faqs.page"
    },
    {
        "name": "STEM Matters NYC",
        "age_range": "Varies by program and grade",
        "organization": "New York City Public Schools",
        "description": (
            "Free STEM enrichment opportunities for NYC students, including "
            "high school programs in areas such as engineering, aerospace, "
            "marine science, mechanics, ecology, and other STEM fields."
        ),
        "opportunity_type": "Summer Program",
        "fields": "Engineering;Science;Aerospace;Environmental Science;STEM",
        "grades": "9;10;11;12",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Seasonal",
        "deadline": "Check official site for upcoming programs",
        "selectivity": "Moderately Competitive",
        "selectivity_stars": 3,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "No — STEM enrichment",
        "format": "NYC / In person",
        "paid_status": "Not paid",
        "requirements": "NYC student; eligibility varies by individual program",
        "url": "https://www.schools.nyc.gov/learning/subjects/stem"
    },
    {
        "name": "NYU Tandon ARISE",
        "organization": "New York University Tandon School of Engineering",
        "description": "Free 10-week NYC summer research program combining research-skills training with six weeks of hands-on work in NYU faculty labs.",
        "opportunity_type": "Research",
        "fields": "Engineering;Computer Science;Robotics;Biomedical Engineering;Environmental Science;Data Science;Research",
        "grades": "10;11",
        "age_range": "Rising juniors and seniors",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed — program is free",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 deadline was February 27, 2026 at 5 PM",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — approximately 150 hours of lab research plus possible continued research collaboration",
        "format": "Hybrid + In person — NYU Tandon, Brooklyn, NYC",
        "paid_status": "Paid — 2026 participants received a $2,000 stipend",
        "requirements": "NYC resident attending an NYC school; rising junior or senior; full 10-week commitment",
        "url": "https://k12stem.engineering.nyu.edu/programs/arise"
    },
    {
        "name": "Simons Summer Research Program",
        "organization": "Stony Brook University",
        "description": "Six-week mentored research program where high school juniors join active university research teams in science, mathematics, and engineering.",
        "opportunity_type": "Research",
        "fields": "Engineering;Computer Science;Mathematics;Physics;Biology;Chemistry;Research",
        "grades": "11",
        "age_range": "16+ by program start",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Check official cycle details",
        "financial_aid": "Check official cycle details",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 deadline was February 5, 2026",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — full-time mentored university research",
        "format": "In person — Stony Brook University, Long Island, NY",
        "paid_status": "Check official cycle details",
        "requirements": "Current 11th grader; U.S. citizen or permanent resident; age 16+ by program start; school nomination required",
        "url": "https://www.stonybrook.edu/simons/"
    },
    {
        "name": "MSK HOPP Summer Student Program",
        "organization": "Memorial Sloan Kettering Cancer Center",
        "description": "Eight-week cancer research internship placing high school juniors in translational biomedical research projects with MSK scientists.",
        "opportunity_type": "Research",
        "fields": "Biology;Cancer Research;Biomedical Science;Medicine;Laboratory Research",
        "grades": "11",
        "age_range": "14+ by program start",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "Next cycle date not yet announced; 2026 application closed February 6, 2026",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "HOPP reports sponsoring over 20 students annually; applicant count not publicly reported",
        "internship_potential": "Yes — independent mentored cancer research project",
        "format": "In person — Memorial Sloan Kettering, Manhattan, NYC",
        "paid_status": "Paid — 2026 stipend was $1,200",
        "requirements": "Current high school junior; live in NY/NJ/CT within 25 miles of MSK main campus; legally authorized to work in U.S.; 3.5 science GPA; full eight-week commitment",
        "url": "https://www.mskcc.org/education-training/summer-student"
    },
    {
        "name": "Columbia BRAINYAC",
        "organization": "Columbia University Zuckerman Institute",
        "description": "Immersive neuroscience apprenticeship where NYC high school students train and then conduct mentored research in Columbia neuroscience laboratories.",
        "opportunity_type": "Research",
        "fields": "Neuroscience;Biology;Biomedical Science;Psychology;Research",
        "grades": "10;11",
        "age_range": "Grade-based eligibility",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "2027 Cycle Opens October 2026",
        "deadline": "2027 applications expected to open October 2026; deadline not yet posted",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — intensive mentored neuroscience laboratory research",
        "format": "In person — Columbia University, NYC",
        "paid_status": "Paid stipend — amount not publicly listed on current program page",
        "requirements": "NYC resident in grade 10 or 11 and enrolled in an eligible partner program/school such as S-PREP, BioBus, Lang Youth Medical, Columbia Secondary School, or Double Discovery Center",
        "url": "https://zuckermaninstitute.columbia.edu/brainyac"
    },
    {
        "name": "MSK Bridge to Biostats Summer Program",
        "organization": "Memorial Sloan Kettering Cancer Center",
        "description": "Paid six-week summer program introducing NYC high school students to biostatistics, cancer data science, computing, and quantitative research.",
        "opportunity_type": "Research",
        "fields": "Data Science;Statistics;Computer Science;Cancer Research;Biostatistics;Mathematics",
        "grades": "9;10;11",
        "age_range": "Rising sophomore through rising senior",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 application closed February 27, 2026",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — paid experiential learning in biostatistics and cancer data science",
        "format": "In person — Midtown Manhattan, NYC",
        "paid_status": "Paid — current program page confirms paid participation; amount not publicly listed",
        "requirements": "NYC resident attending school in NYC; rising sophomore through rising senior; interest in math/computing/data science; recommendation and transcript",
        "url": "https://www.mskcc.org/education-training/bridge-to-biostats-summer-program-b2bsp"
    },
    {
        "name": "Columbia YES in THE HEIGHTS",
        "organization": "Columbia University Herbert Irving Comprehensive Cancer Center",
        "description": "Eight-week cancer research internship matching high school scholars with Columbia research groups for hands-on biomedical research.",
        "opportunity_type": "Research",
        "fields": "Cancer Research;Biology;Biomedical Science;Medicine;Laboratory Research",
        "grades": "10;11;12",
        "age_range": "High school students — check current cycle requirements",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — eight-week cancer research internship",
        "format": "In person — Columbia University Irving Medical Center, NYC",
        "paid_status": "Check official 2027 cycle details",
        "requirements": "Application materials include cover letter, resume, and full summer commitment; verify grade and neighborhood eligibility for current cycle",
        "url": "https://www.cancer.columbia.edu/education/educational-opportunities/high-school-and-undergraduate-programs/yes-heights-program"
    },
    {
        "name": "Columbia Secondary School Field Research Program (SSFRP)",
        "organization": "Columbia University Lamont-Doherty Earth Observatory",
        "description": "Six-week field and laboratory research program where students investigate ecology, earth science, environmental processes, and the Piermont Marsh.",
        "opportunity_type": "Research",
        "fields": "Environmental Science;Earth Science;Ecology;Climate Science;Biology;Research",
        "grades": "9;10;11;12",
        "age_range": "16+ by internship start",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 deadline was March 2, 2026",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — six weeks of field and laboratory research with Columbia mentors",
        "format": "In person — Lamont-Doherty Earth Observatory, Palisades, NY",
        "paid_status": "Check official 2027 cycle details",
        "requirements": "Currently enrolled high school student; age 16+ by start; able to commute; full six-week commitment",
        "url": "https://lamont.columbia.edu/education-outreach/student-summer-opportunities-SSFRP"
    },
    {
        "name": "Columbia BrainSTORM Mentorship Program",
        "organization": "Columbia University Irving Medical Center — Department of Neurology",
        "description": "Year-long neuroscience mentorship program connecting high school students with research and educational experiences in neurology and brain science.",
        "opportunity_type": "Research",
        "fields": "Neuroscience;Neurology;Medicine;Biomedical Science;Research",
        "grades": "9;10;11;12",
        "age_range": "High school students nationwide",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "2026–27 cohort closed; Columbia currently says applications for the June 2027–May 2028 cohort will open in Fall 2027",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — long-term neuroscience mentorship and research exposure",
        "format": "Mentorship program — see current cohort details",
        "paid_status": "Not publicly listed",
        "requirements": "High school student in grades 9–12; application includes research interests, personal statement, and resume/CV",
        "url": "https://www.neurology.columbia.edu/education/additional-educational-programs/brain-seminar-teens-and-opportunities-research-mentorship-brainstorm"
    },
    {
        "name": "MSK Science Enrichment Program (SEP)",
        "organization": "Memorial Sloan Kettering Cancer Center",
        "description": "Ten-month science enrichment and cancer-research pathway including an eight-week biomedical or computational lab internship at MSK.",
        "opportunity_type": "Research",
        "fields": "Cancer Research;Biology;Biomedical Science;Computational Biology;Medicine",
        "grades": "11",
        "age_range": "High school juniors",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Partner-School Nomination",
        "deadline": "Current cycle timing depends on participating partner schools",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — eight-week biomedical or computational laboratory internship",
        "format": "In person — Memorial Sloan Kettering, NYC",
        "paid_status": "Paid — current program page lists a total $4,200 stipend",
        "requirements": "High school junior; completed a full year of biology; must be nominated by an MSK SEP partner school",
        "url": "https://www.mskcc.org/education-training/science-enrichment"
    },
    {
        "name": "Rockefeller Summer Neuroscience Program (SNP)",
        "organization": "The Rockefeller University / RockEDU",
        "description": "Free two-week hands-on neuroscience program for NYC public high school students featuring experiments, mentorship, and student-designed research.",
        "opportunity_type": "Research",
        "fields": "Neuroscience;Biology;Biomedical Science;Experimental Design;Research",
        "grades": "10;11;12",
        "age_range": "16+ by program start",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "All necessary equipment, supplies, and meals are covered",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 deadline was March 15, 2026",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Research-focused course — students design experiments with mentors",
        "format": "In person — Rockefeller University, Manhattan, NYC",
        "paid_status": "Not paid / Free Program",
        "requirements": "Must attend an NYC public high school and be at least 16 years old by program start",
        "url": "https://www.rockefeller.edu/outreach/snp/"
    },
    {
        "name": "CUNY STEM Research Academy",
        "organization": "The City University of New York / College Now",
        "description": "Two-semester NYC public-school research pathway with a spring research course followed by a competitive summer placement in a CUNY faculty laboratory.",
        "opportunity_type": "Research",
        "fields": "Science;Engineering;Computer Science;Mathematics;Laboratory Research;Research",
        "grades": "10;11",
        "age_range": "Grade-based eligibility varies by CUNY campus",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "2027 campus-specific dates not yet announced",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Varies by campus; CCNY selected 25 students for Spring 2026 and 10 continued to summer research",
        "internship_potential": "Yes — selected students conduct summer research with CUNY faculty",
        "format": "In person — participating CUNY campuses",
        "paid_status": "Check individual CUNY campus for current stipend details",
        "requirements": "NYC public high school student; requirements vary by campus and may include GPA, Regents scores, transcript, and writing sample",
        "url": "https://www.cuny.edu/academics/current-initiatives/k16/stem-research-academy/"
    },
    {
        "name": "BioBus High School Junior Scientist Internship",
        "organization": "BioBus",
        "description": "Paid NYC internship where students develop independent science research projects, build laboratory skills, and co-teach science programs for younger students.",
        "opportunity_type": "Research",
        "fields": "Biology;Laboratory Research;Science Communication;Education;Research",
        "grades": "9;10;11;12",
        "age_range": "High school students — program-specific eligibility applies",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "yes",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "2026–27 Closed",
        "deadline": "2026–27 season closed; next application date not yet announced",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported; BioBus reported a record number of 2026–27 applications",
        "internship_potential": "Yes — independent research plus science teaching/mentorship",
        "format": "In person — Harlem citywide placements and Lower East Side/Chinatown placements",
        "paid_status": "Paid hourly internship",
        "requirements": "NYC high school student; specific location/program eligibility applies",
        "url": "https://www.biobus.org/internship/"
    },
    {
        "name": "Princeton AI4ALL",
        "organization": "Princeton University",
        "description": "Free residential AI program for low-income rising 11th graders combining lectures, mentorship, ethical AI discussions, and hands-on research projects.",
        "opportunity_type": "Research",
        "fields": "Artificial Intelligence;Computer Science;Machine Learning;Data Science;Research",
        "grades": "10",
        "age_range": "Rising 11th graders",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Tuition, housing, meals, and program field trip are covered",
        "application_status": "Future Cycle",
        "deadline": "Next cycle date should be confirmed on official site",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "No — research-project-based AI summer program",
        "format": "Residential — Princeton University, New Jersey",
        "paid_status": "Not paid / Free Program",
        "requirements": "Rising 11th grader living and attending high school in U.S. or Puerto Rico; must meet Princeton AI4ALL low-income criteria",
        "url": "https://ai4all.princeton.edu/about"
    },
    {
        "name": "NASA GeneLab for High Schools (GL4HS)",
        "organization": "NASA Ames Research Center",
        "description": "Four-week intensive training program in space life sciences, bioinformatics, omics data, and computational biology.",
        "opportunity_type": "Research",
        "fields": "Bioinformatics;Computational Biology;Space Biology;Data Science;Biology;Research",
        "grades": "10;11;12",
        "age_range": "Rising juniors, rising seniors, and eligible incoming college freshmen",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "Next cycle date not yet announced",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Research training — authentic space-biology and bioinformatics analysis",
        "format": "Virtual",
        "paid_status": "Not paid / Free Program",
        "requirements": "U.S. citizen or permanent resident attending a U.S. high school; rising junior/senior; 3.0+ unweighted GPA; at least one high school biology course; reliable computer/internet",
        "url": "https://www.nasa.gov/ames/genelab-for-high-schools/"
    },
    {
        "name": "NASA STEM Enhancement in Earth Science (SEES) High School Summer Intern",
        "organization": "NASA / UT Austin Center for Space Research",
        "description": "Nationally competitive research internship where high school students analyze NASA Earth and space data with scientists and engineers.",
        "opportunity_type": "Research",
        "fields": "Earth Science;Climate Science;Astronomy;Remote Sensing;Data Science;Space Science;Research",
        "grades": "10;11",
        "age_range": "Typically current 10th and 11th graders",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Check official cycle details",
        "financial_aid": "Check official cycle details",
        "application_status": "Future Cycle",
        "deadline": "Next cycle date not yet announced",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — authentic NASA-supported data research and field investigation",
        "format": "Virtual + selected in-person components depending on project",
        "paid_status": "Check official cycle details",
        "requirements": "High school sophomore or junior; current citizenship/eligibility requirements should be confirmed each cycle",
        "url": "https://science.nasa.gov/sciact-team/stem-enhancement-in-earth-science/"
    },
    {
        "name": "Boston University RISE Internship",
        "organization": "Boston University",
        "description": "Six-week full-time laboratory research program for rising seniors working approximately 40 hours per week with BU research mentors.",
        "opportunity_type": "Research",
        "fields": "Engineering;Computer Science;Physics;Biology;Chemistry;Neuroscience;Biomedical Engineering;Research",
        "grades": "11",
        "age_range": "Rising seniors",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Tuition required",
        "financial_aid": "Financial aid application available; verify current cycle",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 application deadline was February 4, 2026",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported; BU states RISE places up to about 100 students in STEM labs",
        "internship_potential": "Yes — approximately 40 hours/week of mentored research",
        "format": "Residential or Commuter — Boston University",
        "paid_status": "Not paid / Tuition-based Program",
        "requirements": "Current high school junior entering senior year; U.S. citizen or permanent resident; application, transcript, essay, and recommendation",
        "url": "https://www.bu.edu/summer/high-school-programs/rise-internship-practicum/"
    },
    {
        "name": "George Mason Aspiring Scientists Summer Internship Program (ASSIP)",
        "organization": "George Mason University",
        "description": "Eight-week full-time research internship where high school and undergraduate students work with faculty on hypothesis-driven STEM research.",
        "opportunity_type": "Research",
        "fields": "Biology;Chemistry;Computer Science;Engineering;Medicine;Neuroscience;Physics;Research",
        "grades": "10;11;12",
        "age_range": "15+",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Check official 2027 cycle details",
        "financial_aid": "Check official 2027 cycle details",
        "application_status": "2027 Opens Fall 2026",
        "deadline": "2027 application opens Fall 2026; deadline not yet posted",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — full-time faculty-mentored STEM research and three college credits",
        "format": "In person and/or approved research-site placements — George Mason University",
        "paid_status": "Check official 2027 placement details",
        "requirements": "Students age 15+; application and mentor matching; exact eligibility varies by research placement",
        "url": "https://science.gmu.edu/assip"
    },
    {
        "name": "Stanford Institutes of Medicine Summer Research Program (SIMR)",
        "organization": "Stanford Medicine",
        "description": "Eight-week biomedical research internship where high school juniors and seniors conduct hands-on research with Stanford mentors.",
        "opportunity_type": "Research",
        "fields": "Biomedical Science;Immunology;Cancer Research;Neuroscience;Bioinformatics;Stem Cell Biology;Bioengineering",
        "grades": "11;12",
        "age_range": "16+ by program start",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free to participate; application fee may apply",
        "financial_aid": "Application fee waivers available",
        "application_status": "2027 Opens December 18, 2026",
        "deadline": "Applications for SIMR 2027 are scheduled to become available December 18, 2026; deadline not yet posted",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — eight weeks of mentored biomedical research",
        "format": "In person — Stanford University, California",
        "paid_status": "Paid — Stanford states interns earn at least a $500 stipend",
        "requirements": "High school junior or senior; 16+ by program start; living and attending high school in U.S.; U.S. citizen or permanent resident",
        "url": "https://med.stanford.edu/simr.html"
    },
    {
        "name": "UCSB Research Mentorship Program (RMP)",
        "organization": "University of California, Santa Barbara",
        "description": "Competitive six-week research program pairing high school students with graduate, postdoctoral, or faculty mentors on interdisciplinary university-level research.",
        "opportunity_type": "Research",
        "fields": "Engineering;Computer Science;Biology;Physics;Chemistry;Mathematics;Social Science;Research",
        "grades": "9;10;11",
        "age_range": "Primarily current 10th and 11th graders; exceptional 9th graders considered",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Tuition required",
        "financial_aid": "Check current UCSB pre-college scholarship/aid options",
        "application_status": "Future Cycle",
        "deadline": "Next cycle date not yet announced",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "No — intensive mentor-guided university research program",
        "format": "Residential — UC Santa Barbara, California",
        "paid_status": "Not paid / Tuition-based Program",
        "requirements": "High school student in grade 10 or 11; outstanding 9th graders may be considered; minimum 3.80 weighted academic GPA; full program commitment",
        "url": "https://www.summer.ucsb.edu/programs/research-mentorship-program/overview"
    },
    {
        "name": "Princeton Laboratory Learning Program (LLP)",
        "organization": "Princeton University",
        "description": "Free full-time summer research experience placing local New Jersey high school students in ongoing Princeton science and engineering research projects.",
        "opportunity_type": "Research",
        "fields": "Engineering;Physics;Chemistry;Biology;Computer Science;Science;Research",
        "grades": "10;11;12",
        "age_range": "High school students — project-specific age requirements apply",
        "boroughs_served": "",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 application window was February 15–March 15, 2026",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — full-time research alongside Princeton faculty and research staff",
        "format": "In person — Princeton University, New Jersey",
        "paid_status": "Unpaid / Free Research Experience",
        "requirements": "Local New Jersey high school student; no housing or transportation provided; project-specific requirements apply",
        "url": "https://scienceoutreach.princeton.edu/laboratory-learning-program"
    },
    {
        "name": "Brookhaven National Laboratory High School Research Program (HSRP)",
        "organization": "Brookhaven National Laboratory / U.S. Department of Energy",
        "description": "Highly competitive six-week commuter research program where students collaborate with Brookhaven scientists, engineers, and technical staff on active STEM projects.",
        "opportunity_type": "Research",
        "fields": "Physics;Engineering;Computer Science;Materials Science;Biology;Environmental Science;Nuclear Science;Research",
        "grades": "11;12",
        "age_range": "16+ by program start",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Housing and transportation are not provided",
        "application_status": "Future Cycle",
        "deadline": "Summer 2027 date not yet announced; 2026 application closed March 20, 2026",
        "selectivity": "Highly Competitive",
        "selectivity_stars": 4,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Yes — six weeks of collaborative research at a U.S. national laboratory",
        "format": "In person / Commuter — Brookhaven National Laboratory, Upton, NY",
        "paid_status": "Check official 2027 cycle details",
        "requirements": "Recommended after completion of 11th grade; age 16+; U.S. citizen or permanent resident; health insurance; two recommendations; able to commute daily",
        "url": "https://www.bnl.gov/education/programs/program.php?q=219"
    },
    {
        "name": "Cold Spring Harbor Laboratory Partners for the Future",
        "organization": "Cold Spring Harbor Laboratory",
        "description": "Academic-year biomedical research program where nominated Long Island high school seniors work directly in Cold Spring Harbor Laboratory research groups.",
        "opportunity_type": "Research",
        "fields": "Biology;Genetics;Genomics;Neuroscience;Cancer Research;Biomedical Science;Research",
        "grades": "11;12",
        "age_range": "Students entering senior year",
        "boroughs_served": "",
        "bronx_priority": "no",
        "cost": "Free",
        "financial_aid": "Not needed",
        "application_status": "School Nomination",
        "deadline": "Current nomination/application dates should be confirmed with CSHL",
        "selectivity": "Extremely Competitive",
        "selectivity_stars": 5,
        "acceptance_rate": "Not publicly reported; each participating school science chair may nominate up to two students",
        "internship_potential": "Yes — hands-on biomedical research in CSHL laboratories",
        "format": "In person — Cold Spring Harbor Laboratory, Long Island, NY",
        "paid_status": "Check official current-cycle details",
        "requirements": "Long Island high school student entering senior year; must be nominated by school science chairperson",
        "url": "https://www.cshl.edu/education/partners-for-the-future/"
    },

]

extra_df = pd.DataFrame(
    extra_opportunities
)

if opportunities.empty:
    opportunities = extra_df.copy()
else:
    # Ensure older CSV rows support the new Opportunity 2.0 fields.
    opportunity_defaults = {
        "selectivity": "Not rated yet",
        "selectivity_stars": 0,
        "acceptance_rate": "Not publicly reported",
        "internship_potential": "Not specified",
        "format": "Check official site",
        "paid_status": "Check official site",
        "requirements": "Check official site",
        "deadline": "Check official site",
        "age_range": "Check official eligibility"
    }

    for column, default_value in opportunity_defaults.items():
        if column not in opportunities.columns:
            opportunities[column] = default_value

    # Avoid duplicates if a program already exists in the CSV.
    existing_names = set(
        opportunities["name"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    extra_df = extra_df[
        ~extra_df["name"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(
            existing_names
        )
    ]

    opportunities = pd.concat(
        [
            opportunities,
            extra_df
        ],
        ignore_index=True
    )


try:
    careers = pd.read_csv("data/careers.csv")
except Exception:
    careers = pd.DataFrame()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_salary(value):

    if pd.isna(value):
        return "Data unavailable"

    try:
        return f"${int(float(value)):,}"

    except Exception:
        return "Data unavailable"


def list_to_text(items):
    return json.dumps(
        items,
        ensure_ascii=False
    )


def text_to_list(value):

    if value is None:
        return []

    try:

        result = json.loads(value)

        if isinstance(result, list):
            return result

        return []

    except Exception:
        return []


def safe_http_url(value):

    if value is None:
        return None

    try:

        if pd.isna(value):
            return None

    except (TypeError, ValueError):
        pass

    text = str(value).strip()

    if not text:
        return None

    if text.lower() in {
        "nan",
        "none",
        "null",
        "nat"
    }:
        return None

    if not (
        text.startswith("http://")
        or
        text.startswith("https://")
    ):
        return None

    return text


def valid_choice_defaults(saved_values, options):

    if not saved_values:
        return []

    allowed = set(options)

    return [
        item
        for item in saved_values
        if item in allowed
    ]


def safe_int(value, default, minimum=None, maximum=None):

    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default

    if minimum is not None:
        number = max(minimum, number)

    if maximum is not None:
        number = min(maximum, number)

    return number


def parse_college_acceptance_rate(rate):
    """Return a numeric overall acceptance-rate percentage, or None."""

    if rate is None:
        return None

    if isinstance(rate, bool):
        return None

    if isinstance(rate, (int, float)):
        value = float(rate)
        if value != value:
            return None
        if value < 0 or value > 100:
            return None
        return value

    text = str(rate).strip()
    if not text:
        return None

    match = re.search(r"(\d+(?:\.\d+)?)", text.replace(",", ""))
    if not match:
        return None

    try:
        value = float(match.group(1))
    except (TypeError, ValueError):
        return None

    if value < 0 or value > 100:
        return None

    return value


def college_selectivity_from_acceptance_rate(rate):
    """Star rating from overall college acceptance rate. Same rule for every college."""

    parsed = parse_college_acceptance_rate(rate)

    if parsed is None:
        return None, "Not rated"

    if parsed < 25:
        return 5, "Extremely Competitive"
    if parsed < 46:
        return 4, "Highly Competitive"
    if parsed < 60:
        return 3, "Competitive"
    if parsed <= 80:
        return 2, "Moderately Competitive"
    return 1, "More Accessible"


def supabase_can_write():

    if supabase_connected:
        return True

    st.error(
        "Your data could not be saved because the database is unavailable. "
        "Please try again in a moment."
    )

    return False


def log_supabase_exception(action):

    logger.exception(
        "Supabase %s failed",
        action
    )


def mutation_row_count(response):

    if response is None:
        return 0

    data = getattr(
        response,
        "data",
        None
    )

    if isinstance(data, list):
        return len(data)

    if data:
        return 1

    count = getattr(
        response,
        "count",
        None
    )

    if isinstance(count, int):
        return count

    return 0


def is_missing_conflict_target(error):

    text = str(error).lower()

    return (
        "on conflict" in text
        or
        "no unique" in text
        or
        "unique or exclusion constraint" in text
        or
        "42p10" in text
    )


def is_unique_violation(error):

    text = str(error).lower()

    return (
        "duplicate key" in text
        or
        "unique constraint" in text
        or
        "23505" in text
    )


def supabase_upsert(
    table_name,
    payload,
    on_conflict,
    ignore_duplicates=False
):

    return (
        supabase
        .table(table_name)
        .upsert(
            payload,
            on_conflict=on_conflict,
            ignore_duplicates=ignore_duplicates
        )
        .execute()
    )


def get_google_user():

    try:
        user_sub = st.user.get("sub")
    except Exception:
        user_sub = None

    try:
        email = st.user.get("email")
    except Exception:
        email = None

    try:
        google_name = st.user.get("name")
    except Exception:
        google_name = None

    return (
        str(user_sub) if user_sub else None,
        str(email) if email else "",
        str(google_name) if google_name else ""
    )


def load_profile(user_sub):

    if not supabase_connected:
        return None

    try:

        response = (
            supabase
            .table("student_profiles")
            .select("*")
            .eq("user_sub", user_sub)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        row = response.data[0]

        return {
            "id": row.get("id"),

            "first_name":
                row.get("first_name", ""),

            "middle_name":
                row.get("middle_name", ""),

            "last_name":
                row.get("last_name", ""),

            "age":
                safe_int(
                    row.get("age", 15),
                    15,
                    13,
                    19
                ),

            "grade":
                row.get("grade", "9"),

            "borough":
                row.get("borough", "Bronx"),

            "interests":
                text_to_list(
                    row.get("interests")
                ),

            "experience_areas":
                text_to_list(
                    row.get("experience_areas")
                ),

            "goals":
                text_to_list(
                    row.get("goals")
                ),

            "exploration_stage":
                row.get(
                    "exploration_stage",
                    "I am just starting to explore STEM."
                ),

            "confidence":
                safe_int(
                    row.get("confidence", 5),
                    5,
                    1,
                    10
                ),

            "weekly_time":
                row.get(
                    "weekly_time",
                    "2–5 hours"
                ),

            "financial_support":
                row.get(
                    "financial_support",
                    False
                )
        }

    except Exception:

        log_supabase_exception(
            "load_profile"
        )

        st.error(
            "We could not load your saved profile."
        )

        return None


def save_profile(
    user_sub,
    email,
    profile
):

    if not supabase_can_write():
        return False

    now = datetime.now(
        timezone.utc
    ).isoformat()

    update_data = {
        "first_name":
            profile["first_name"],

        "middle_name":
            profile["middle_name"],

        "last_name":
            profile["last_name"],

        "age":
            int(profile["age"]),

        "grade":
            profile["grade"],

        "borough":
            profile["borough"],

        "interests":
            list_to_text(
                profile["interests"]
            ),

        "experience_areas":
            list_to_text(
                profile["experience_areas"]
            ),

        "goals":
            list_to_text(
                profile["goals"]
            ),

        "exploration_stage":
            profile["exploration_stage"],

        "confidence":
            int(profile["confidence"]),

        "weekly_time":
            profile["weekly_time"],

        "financial_support":
            bool(
                profile["financial_support"]
            ),

        "updated_at":
            now
    }

    insert_data = {
        "user_sub":
            user_sub,

        "email":
            email,

        **update_data,

        "created_at":
            now
    }

    try:

        updated = (
            supabase
            .table("student_profiles")
            .update(update_data)
            .eq("user_sub", user_sub)
            .execute()
        )

        if mutation_row_count(updated) > 0:
            return True

        try:

            upserted = supabase_upsert(
                "student_profiles",
                insert_data,
                "user_sub"
            )

            if mutation_row_count(upserted) > 0:
                return True

            st.error(
                "Your profile could not be saved."
            )

            return False

        except Exception as upsert_error:

            if not is_missing_conflict_target(
                upsert_error
            ):
                raise

            inserted = (
                supabase
                .table("student_profiles")
                .insert(insert_data)
                .execute()
            )

            if mutation_row_count(inserted) > 0:
                return True

            st.error(
                "Your profile could not be saved."
            )

            return False

    except Exception as error:

        if is_unique_violation(error):

            retried = (
                supabase
                .table("student_profiles")
                .update(update_data)
                .eq("user_sub", user_sub)
                .execute()
            )

            if mutation_row_count(retried) > 0:
                return True

        log_supabase_exception(
            "save_profile"
        )

        st.error(
            "Your profile could not be saved."
        )

        return False


# ============================================================
# SAVED OPPORTUNITIES / APPLICATION TRACKER
# ============================================================

APPLICATION_STATUSES = [
    "Saved",
    "Planning to Apply",
    "Applying",
    "Applied",
    "Accepted",
    "Waitlisted",
    "Not Selected"
]


def load_saved_opportunities(user_sub):

    if not supabase_connected:
        return []

    try:

        response = (
            supabase
            .table("saved_opportunities")
            .select("*")
            .eq("user_sub", user_sub)
            .order("saved_at", desc=True)
            .execute()
        )

        return response.data or []

    except Exception:

        log_supabase_exception(
            "load_saved_opportunities"
        )

        st.error(
            "We could not load your saved opportunities."
        )

        return []


def save_opportunity(user_sub, opportunity_name):

    if not supabase_can_write():
        return False

    now = datetime.now(
        timezone.utc
    ).isoformat()

    payload = {
        "user_sub":
            user_sub,

        "opportunity_name":
            opportunity_name,

        "status":
            "Saved",

        "notes":
            "",

        "saved_at":
            now,

        "updated_at":
            now
    }

    try:

        existing = (
            supabase
            .table("saved_opportunities")
            .select("id")
            .eq("user_sub", user_sub)
            .eq("opportunity_name", opportunity_name)
            .limit(1)
            .execute()
        )

        if existing.data:
            return True

        try:

            supabase_upsert(
                "saved_opportunities",
                payload,
                "user_sub,opportunity_name",
                ignore_duplicates=True
            )

            return True

        except Exception as upsert_error:

            if not is_missing_conflict_target(
                upsert_error
            ):
                raise

            inserted = (
                supabase
                .table("saved_opportunities")
                .insert(payload)
                .execute()
            )

            if mutation_row_count(inserted) > 0:
                return True

            st.error(
                "This opportunity could not be saved."
            )

            return False

    except Exception as error:

        if is_unique_violation(error):
            return True

        log_supabase_exception(
            "save_opportunity"
        )

        st.error(
            "This opportunity could not be saved."
        )

        return False


def update_saved_opportunity(
    user_sub,
    saved_id,
    status,
    notes
):

    if not supabase_can_write():
        return False

    try:

        updated = (
            supabase
            .table("saved_opportunities")
            .update({
                "status":
                    status,

                "notes":
                    notes,

                "updated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat()
            })
            .eq("id", saved_id)
            .eq("user_sub", user_sub)
            .execute()
        )

        if mutation_row_count(updated) > 0:
            return True

        st.error(
            "Your application tracker could not be updated."
        )

        return False

    except Exception:

        log_supabase_exception(
            "update_saved_opportunity"
        )

        st.error(
            "Your application tracker could not be updated."
        )

        return False


def delete_saved_opportunity(user_sub, saved_id):

    if not supabase_can_write():
        return False

    try:

        deleted = (
            supabase
            .table("saved_opportunities")
            .delete()
            .eq("id", saved_id)
            .eq("user_sub", user_sub)
            .execute()
        )

        if mutation_row_count(deleted) > 0:
            return True

        st.error(
            "This opportunity could not be removed."
        )

        return False

    except Exception:

        log_supabase_exception(
            "delete_saved_opportunity"
        )

        st.error(
            "This opportunity could not be removed."
        )

        return False


def saved_opportunity_names(user_sub):

    saved = load_saved_opportunities(
        user_sub
    )

    return {
        str(item.get("opportunity_name", ""))
        for item in saved
    }



# ============================================================
# FAVORITE COLLEGES
# ============================================================

def load_favorite_colleges(user_sub):

    if not supabase_connected:
        return []

    try:

        response = (
            supabase
            .table("favorite_colleges")
            .select("*")
            .eq("user_sub", user_sub)
            .order("rank_order")
            .execute()
        )

        return response.data or []

    except Exception:

        log_supabase_exception(
            "load_favorite_colleges"
        )

        st.error(
            "We could not load your favorite colleges."
        )

        return []


def add_favorite_college(
    user_sub,
    college_name
):

    if not supabase_can_write():
        return False

    try:

        existing = (
            supabase
            .table("favorite_colleges")
            .select("id")
            .eq("user_sub", user_sub)
            .eq("college_name", college_name)
            .limit(1)
            .execute()
        )

        if existing.data:
            return True

        current = load_favorite_colleges(
            user_sub
        )

        next_rank = len(current) + 1

        now = datetime.now(
            timezone.utc
        ).isoformat()

        payload = {
            "user_sub":
                user_sub,

            "college_name":
                college_name,

            "rank_order":
                next_rank,

            "notes":
                "",

            "saved_at":
                now,

            "updated_at":
                now
        }

        try:

            supabase_upsert(
                "favorite_colleges",
                payload,
                "user_sub,college_name",
                ignore_duplicates=True
            )

            return True

        except Exception as upsert_error:

            if not is_missing_conflict_target(
                upsert_error
            ):
                raise

            inserted = (
                supabase
                .table("favorite_colleges")
                .insert(payload)
                .execute()
            )

            if mutation_row_count(inserted) > 0:
                return True

            st.error(
                "This college could not be added to your favorites."
            )

            return False

    except Exception as error:

        if is_unique_violation(error):
            return True

        log_supabase_exception(
            "add_favorite_college"
        )

        st.error(
            "This college could not be added to your favorites."
        )

        return False


def update_favorite_college_notes(
    user_sub,
    favorite_id,
    notes
):

    if not supabase_can_write():
        return False

    try:

        updated = (
            supabase
            .table("favorite_colleges")
            .update({
                "notes":
                    notes,

                "updated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat()
            })
            .eq("id", favorite_id)
            .eq("user_sub", user_sub)
            .execute()
        )

        if mutation_row_count(updated) > 0:
            return True

        st.error(
            "Your college notes could not be updated."
        )

        return False

    except Exception:

        log_supabase_exception(
            "update_favorite_college_notes"
        )

        st.error(
            "Your college notes could not be updated."
        )

        return False


def reorder_favorite_colleges(
    user_sub,
    favorite_id,
    direction
):

    if not supabase_can_write():
        return False

    favorites = load_favorite_colleges(
        user_sub
    )

    if not favorites:
        return False

    current_index = next(
        (
            index
            for index, item
            in enumerate(favorites)
            if item["id"] == favorite_id
        ),
        None
    )

    if current_index is None:
        return False

    if (
        direction == "up"
        and
        current_index == 0
    ):
        return True

    if (
        direction == "down"
        and
        current_index
        == len(favorites) - 1
    ):
        return True

    swap_index = (
        current_index - 1
        if direction == "up"
        else current_index + 1
    )

    current_item = favorites[
        current_index
    ]

    swap_item = favorites[
        swap_index
    ]

    try:

        first_update = (
            supabase
            .table("favorite_colleges")
            .update({
                "rank_order":
                    swap_item[
                        "rank_order"
                    ],

                "updated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat()
            })
            .eq(
                "id",
                current_item["id"]
            )
            .eq(
                "user_sub",
                user_sub
            )
            .execute()
        )

        second_update = (
            supabase
            .table("favorite_colleges")
            .update({
                "rank_order":
                    current_item[
                        "rank_order"
                    ],

                "updated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat()
            })
            .eq(
                "id",
                swap_item["id"]
            )
            .eq(
                "user_sub",
                user_sub
            )
            .execute()
        )

        if (
            mutation_row_count(first_update) > 0
            and
            mutation_row_count(second_update) > 0
        ):
            return True

        st.error(
            "Your favorite college order could not be updated."
        )

        return False

    except Exception:

        log_supabase_exception(
            "reorder_favorite_colleges"
        )

        st.error(
            "Your favorite college order could not be updated."
        )

        return False


def remove_favorite_college(
    user_sub,
    favorite_id
):

    if not supabase_can_write():
        return False

    try:

        deleted = (
            supabase
            .table("favorite_colleges")
            .delete()
            .eq("id", favorite_id)
            .eq("user_sub", user_sub)
            .execute()
        )

        if mutation_row_count(deleted) < 1:

            st.error(
                "This college could not be removed from your favorites."
            )

            return False

        # Re-number remaining favorites so the order stays clean.
        remaining = load_favorite_colleges(
            user_sub
        )

        for index, item in enumerate(
            remaining,
            start=1
        ):

            if item.get(
                "rank_order"
            ) != index:

                ranked = (
                    supabase
                    .table("favorite_colleges")
                    .update({
                        "rank_order":
                            index,

                        "updated_at":
                            datetime.now(
                                timezone.utc
                            ).isoformat()
                    })
                    .eq(
                        "id",
                        item["id"]
                    )
                    .eq(
                        "user_sub",
                        user_sub
                    )
                    .execute()
                )

                if mutation_row_count(ranked) < 1:

                    st.error(
                        "This college could not be removed from your favorites."
                    )

                    return False

        return True

    except Exception:

        log_supabase_exception(
            "remove_favorite_college"
        )

        st.error(
            "This college could not be removed from your favorites."
        )

        return False



# ============================================================
# USER FEEDBACK / REVIEWS
# ============================================================

def load_user_feedback(user_sub):

    if not supabase_connected:
        return None

    try:

        response = (
            supabase
            .table("user_feedback")
            .select("*")
            .eq("user_sub", user_sub)
            .limit(1)
            .execute()
        )

        if response.data:
            return response.data[0]

        return None

    except Exception:

        log_supabase_exception(
            "load_user_feedback"
        )

        return None


def save_user_feedback(
    user_sub,
    email,
    feedback
):

    if not supabase_can_write():
        return False

    now = datetime.now(
        timezone.utc
    ).isoformat()

    update_data = {
        "rating":
            int(
                feedback[
                    "rating"
                ]
            ),

        "ease_of_use":
            int(
                feedback[
                    "ease_of_use"
                ]
            ),

        "overall_feeling":
            feedback[
                "overall_feeling"
            ],

        "favorite_features":
            list_to_text(
                feedback[
                    "favorite_features"
                ]
            ),

        "improvements":
            feedback[
                "improvements"
            ],

        "additional_comments":
            feedback[
                "additional_comments"
            ],

        "would_recommend":
            feedback[
                "would_recommend"
            ],

        "updated_at":
            now
    }

    insert_data = {
        "user_sub":
            user_sub,

        "email":
            email,

        **update_data,

        "created_at":
            now
    }

    try:

        updated = (
            supabase
            .table("user_feedback")
            .update(update_data)
            .eq("user_sub", user_sub)
            .execute()
        )

        if mutation_row_count(updated) > 0:
            return True

        try:

            upserted = supabase_upsert(
                "user_feedback",
                insert_data,
                "user_sub"
            )

            if mutation_row_count(upserted) > 0:
                return True

            st.error(
                "Your feedback could not be saved."
            )

            return False

        except Exception as upsert_error:

            if not is_missing_conflict_target(
                upsert_error
            ):
                raise

            inserted = (
                supabase
                .table("user_feedback")
                .insert(insert_data)
                .execute()
            )

            if mutation_row_count(inserted) > 0:
                return True

            st.error(
                "Your feedback could not be saved."
            )

            return False

    except Exception as error:

        if is_unique_violation(error):

            retried = (
                supabase
                .table("user_feedback")
                .update(update_data)
                .eq("user_sub", user_sub)
                .execute()
            )

            if mutation_row_count(retried) > 0:
                return True

        log_supabase_exception(
            "save_user_feedback"
        )

        st.error(
            "Your feedback could not be saved."
        )

        return False



# ============================================================
# ADMIN DASHBOARD
# ============================================================

def get_admin_emails():

    try:

        configured = st.secrets.get(
            "admin_emails",
            []
        )

        if isinstance(
            configured,
            str
        ):

            return {
                configured.strip().lower()
            }

        return {
            str(email).strip().lower()
            for email in configured
            if str(email).strip()
        }

    except Exception:

        return set()


def is_admin_user(email):

    admin_emails = get_admin_emails()

    return (
        str(email).strip().lower()
        in admin_emails
    )


def load_admin_metrics():

    if not supabase_connected:

        return {
            "profiles": [],
            "feedback": [],
            "saved_opportunities": [],
            "favorite_colleges": []
        }

    data = {
        "profiles": [],
        "feedback": [],
        "saved_opportunities": [],
        "favorite_colleges": []
    }

    table_map = {
        "profiles":
            "student_profiles",

        "feedback":
            "user_feedback",

        "saved_opportunities":
            "saved_opportunities",

        "favorite_colleges":
            "favorite_colleges"
    }

    for key, table_name in table_map.items():

        try:

            response = (
                supabase
                .table(
                    table_name
                )
                .select("*")
                .execute()
            )

            data[
                key
            ] = response.data or []

        except Exception:

            log_supabase_exception(
                f"load_admin_metrics:{table_name}"
            )

            data[
                key
            ] = []

    return data



# ============================================================
# GOOGLE CALENDAR LINKS
# ============================================================

def parse_confirmed_deadline(value):

    if value is None or pd.isna(value):
        return None

    raw = str(value).strip()

    if not raw:
        return None

    lower = raw.lower()

    # Do not create calendar events from estimated or unannounced dates.
    blocked_phrases = [
        "not yet announced",
        "future cycle",
        "expected",
        "typically",
        "check official",
        "see official",
        "varies",
        "seasonal",
        "next cycle",
        "future recruitment",
        "date not yet announced"
    ]

    if any(
        phrase in lower
        for phrase in blocked_phrases
    ):
        return None

    # Prefer a full Month DD, YYYY date when it appears in a longer string.
    month_pattern = (
        r"(January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+\d{1,2},\s+\d{4}"
    )

    match = re.search(
        month_pattern,
        raw,
        flags=re.IGNORECASE
    )

    if match:

        parsed = pd.to_datetime(
            match.group(0),
            errors="coerce"
        )

        if pd.notna(parsed):
            return parsed.to_pydatetime()

    # Fall back to a direct parse only for simple date-like strings.
    parsed = pd.to_datetime(
        raw,
        errors="coerce"
    )

    if pd.notna(parsed):
        return parsed.to_pydatetime()

    return None


def google_calendar_deadline_url(
    opportunity_name,
    deadline_value,
    official_url="",
    organization=""
):

    deadline_dt = parse_confirmed_deadline(
        deadline_value
    )

    official_url = safe_http_url(
        official_url
    ) or ""

    if deadline_dt is None:
        return None

    start_date = deadline_dt.strftime(
        "%Y%m%d"
    )

    # Google Calendar all-day events use an exclusive end date.
    end_date = (
        deadline_dt
        +
        pd.Timedelta(
            days=1
        )
    ).strftime(
        "%Y%m%d"
    )

    title = (
        f"{opportunity_name} Application Deadline"
    )

    details_parts = [
        f"Application deadline for {opportunity_name}."
    ]

    if organization:
        details_parts.append(
            f"Organization: {organization}"
        )

    if official_url:
        details_parts.append(
            f"Official program page: {official_url}"
        )

    details_parts.append(
        "Added from STEM Pathways NYC. Confirm the final deadline on the official program website."
    )

    details = "\n".join(
        details_parts
    )

    return (
        "https://calendar.google.com/calendar/render"
        "?action=TEMPLATE"
        f"&text={quote_plus(title)}"
        f"&dates={start_date}/{end_date}"
        f"&details={quote_plus(details)}"
    )



# ============================================================
# GOOGLE LOGIN
# ============================================================

if not st.user.is_logged_in:

    st.markdown(
        """
        <div class="sp-landing-hero">
            <div class="sp-landing-kicker">For NYC High School Students</div>
            <h1>STEM Pathways NYC</h1>
            <p class="sp-landing-headline">Find your path. Build your future.</p>
            <p class="sp-landing-desc">
                STEM Pathways NYC helps New York City high school students discover STEM careers,
                colleges, research programs, internships, projects, and opportunities
                — then turn those interests into a clear next step.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container(
        key="landing_welcome"
    ):

        st.markdown(
            '<div class="sp-landing-welcome-title">'
            'Start building your STEM pathway</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sp-landing-welcome-copy">'
            'Sign in to personalize your recommendations, save programs, '
            'track applications, and build a college list in one place.'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "Continue with Google",
            type="primary",
            width="stretch",
            key="google_continue"
        ):
            st.login("google")

    st.markdown(
        """
        <div class="sp-landing-lower">
            <div class="sp-landing-features">
                <div class="sp-landing-feature">
                    <h3>Discover Opportunities</h3>
                    <p>Find research programs, internships, scholarships, and STEM experiences available to students across New York City.</p>
                </div>
                <div class="sp-landing-feature">
                    <h3>Explore Colleges</h3>
                    <p>Discover colleges, majors, and programs that fit your goals and preferences.</p>
                </div>
                <div class="sp-landing-feature">
                    <h3>Build Your Path</h3>
                    <p>Track projects, applications, favorites, deadlines, and your STEM progress.</p>
                </div>
            </div>
            <div class="sp-landing-purpose">
                <h2>Built for NYC students who want more access to STEM opportunities.</h2>
                <p>STEM Pathways NYC was created to make it easier for New York City high school students to find programs, explore careers, and plan their next steps.</p>
            </div>
            <div class="sp-landing-footer">
                <div class="sp-landing-contact">
                    <div class="sp-landing-contact-title">✉️ Questions or feedback?</div>
                    <p>Have a suggestion, found a problem, or want to share feedback about STEM Pathways NYC? I'd love to hear from you.</p>
                    <a href="mailto:danlopez0911@gmail.com">danlopez0911@gmail.com</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# LOGGED-IN USER
# ============================================================

user_sub, user_email, google_name = (
    get_google_user()
)


if not user_sub:

    st.error(
        "Google login succeeded, but the app could not retrieve "
        "your account identifier."
    )

    if st.button(
        "Sign Out"
    ):
        st.logout()

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "profile_loaded" not in st.session_state:
    st.session_state.profile_loaded = False

if "profile_completed" not in st.session_state:
    st.session_state.profile_completed = False

if "student_profile" not in st.session_state:
    st.session_state.student_profile = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "career_results" not in st.session_state:
    st.session_state.career_results = None


# ============================================================
# AUTOMATIC PROFILE LOAD
# ============================================================

if not st.session_state.profile_loaded:

    saved_profile = load_profile(
        user_sub
    )

    if saved_profile:

        st.session_state.student_profile = (
            saved_profile
        )

        st.session_state.profile_completed = (
            True
        )

    else:

        st.session_state.profile_completed = (
            False
        )

    st.session_state.profile_loaded = True


# ============================================================
# PROFILE FORM
# ============================================================

if not st.session_state.profile_completed:

    existing_profile = (
        st.session_state.student_profile
    )

    render_page_header(
        "Create Your STEM Explorer Profile",
        (
            "Answer a few questions so STEM Pathways NYC can personalize "
            "your career, major, project, and opportunity recommendations."
        ),
        kicker="Profile Setup"
    )

    st.write(
        f"Signed in as **{user_email}**"
    )

    st.divider()

    # --------------------------------------------------------
    # ABOUT YOU
    # --------------------------------------------------------

    st.header(
        "1. About You"
    )

    col1, col2 = st.columns(2)

    with col1:

        first_name = st.text_input(
            "First name",
            value=existing_profile.get(
                "first_name",
                ""
            )
        )

    with col2:

        last_name = st.text_input(
            "Last name",
            value=existing_profile.get(
                "last_name",
                ""
            )
        )

    middle_name = st.text_input(
        "Middle name (optional)",
        value=existing_profile.get(
            "middle_name",
            ""
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        age = st.number_input(
            "Age",
            min_value=13,
            max_value=19,
            value=safe_int(
                existing_profile.get(
                    "age",
                    15
                ),
                15,
                13,
                19
            ),
            step=1
        )

    grade_options = [
        "9",
        "10",
        "11",
        "12"
    ]

    current_grade = str(
        existing_profile.get(
            "grade",
            "9"
        )
    )

    with col2:

        grade = st.selectbox(
            "Grade",
            grade_options,
            index=(
                grade_options.index(
                    current_grade
                )
                if current_grade
                in grade_options
                else 0
            )
        )

    borough_options = [
        "Bronx",
        "Manhattan",
        "Brooklyn",
        "Queens",
        "Staten Island"
    ]

    current_borough = (
        existing_profile.get(
            "borough",
            "Bronx"
        )
    )

    with col3:

        borough = st.selectbox(
            "Borough",
            borough_options,
            index=(
                borough_options.index(
                    current_borough
                )
                if current_borough
                in borough_options
                else 0
            )
        )

    st.divider()

    # --------------------------------------------------------
    # INTERESTS
    # --------------------------------------------------------

    st.header(
        "2. Your STEM Interests"
    )

    interest_options = [
        "Engineering",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Computer Engineering",
        "Computer Science",
        "Artificial Intelligence",
        "Data Science",
        "Biomedical Engineering",
        "Biology",
        "Physics",
        "Mathematics",
        "Environmental Science",
        "Robotics",
        "Not sure yet"
    ]

    interests = st.multiselect(
        "Which STEM fields currently interest you?",
        interest_options,
        default=valid_choice_defaults(
            existing_profile.get(
                "interests",
                []
            ),
            interest_options
        )
    )

    experience_options = [
        "Coding",
        "Electronics",
        "Circuit Design",
        "CAD / 3D Design",
        "3D Printing",
        "Robotics",
        "Scientific Research",
        "Engineering Projects",
        "Data Analysis",
        "Math Competitions",
        "Science Competitions",
        "None yet"
    ]

    experience_areas = st.multiselect(
        "Which STEM activities have you tried?",
        experience_options,
        default=valid_choice_defaults(
            existing_profile.get(
                "experience_areas",
                []
            ),
            experience_options
        )
    )

    st.divider()

    # --------------------------------------------------------
    # GOALS
    # --------------------------------------------------------

    st.header(
        "3. Your Goals"
    )

    goal_options = [
        "Build STEM projects",
        "Learn technical skills",
        "Explore STEM careers",
        "Find summer programs",
        "Find internships",
        "Participate in research",
        "Take college courses",
        "Enter competitions",
        "Prepare for a STEM major"
    ]

    goals = st.multiselect(
        "What would you like to do next?",
        goal_options,
        default=valid_choice_defaults(
            existing_profile.get(
                "goals",
                []
            ),
            goal_options
        )
    )

    stage_options = [
        "I am just starting to explore STEM.",
        "I have a few STEM interests but I am still exploring.",
        "I know which STEM fields interest me.",
        "I have experience and want to develop more advanced skills.",
        "I already have a specific STEM career or major in mind."
    ]

    current_stage = (
        existing_profile.get(
            "exploration_stage",
            stage_options[0]
        )
    )

    exploration_stage = st.radio(
        "Where are you currently in your STEM journey?",
        stage_options,
        index=(
            stage_options.index(
                current_stage
            )
            if current_stage
            in stage_options
            else 0
        )
    )

    confidence = st.slider(
        "How confident are you about your current STEM interests?",
        1,
        10,
        safe_int(
            existing_profile.get(
                "confidence",
                5
            ),
            5,
            1,
            10
        )
    )

    weekly_options = [
        "Less than 2 hours",
        "2–5 hours",
        "5–10 hours",
        "10+ hours"
    ]

    current_weekly = (
        existing_profile.get(
            "weekly_time",
            "2–5 hours"
        )
    )

    weekly_time = st.selectbox(
        "How much time would you like to spend exploring STEM each week?",
        weekly_options,
        index=(
            weekly_options.index(
                current_weekly
            )
            if current_weekly
            in weekly_options
            else 1
        )
    )

    financial_support = st.checkbox(
        "Prioritize free opportunities or programs offering financial aid",
        value=bool(
            existing_profile.get(
                "financial_support",
                False
            )
        )
    )

    st.divider()

    if st.button(
        "Save My STEM Profile",
        type="primary",
        use_container_width=True
    ):

        if not first_name.strip():

            st.warning(
                "Please enter your first name."
            )

        elif not last_name.strip():

            st.warning(
                "Please enter your last name."
            )

        elif not interests:

            st.warning(
                "Please choose at least one STEM interest."
            )

        elif not goals:

            st.warning(
                "Please choose at least one goal."
            )

        else:

            profile = {

                "first_name":
                    first_name.strip(),

                "middle_name":
                    middle_name.strip(),

                "last_name":
                    last_name.strip(),

                "age":
                    age,

                "grade":
                    grade,

                "borough":
                    borough,

                "interests":
                    interests,

                "experience_areas":
                    experience_areas,

                "goals":
                    goals,

                "exploration_stage":
                    exploration_stage,

                "confidence":
                    confidence,

                "weekly_time":
                    weekly_time,

                "financial_support":
                    financial_support
            }

            saved = save_profile(
                user_sub,
                user_email,
                profile
            )

            if saved:

                st.session_state.student_profile = (
                    profile
                )

                st.session_state.profile_completed = (
                    True
                )

                st.session_state.current_page = (
                    "Dashboard"
                )

                st.success(
                    "Your STEM profile has been saved."
                )

                st.rerun()

    st.divider()

    if st.button(
        "Sign Out"
    ):
        st.logout()

    st.stop()


# ============================================================
# PROFILE
# ============================================================

profile = st.session_state.student_profile


if profile.get("middle_name"):

    full_name = (
        f"{profile['first_name']} "
        f"{profile['middle_name']} "
        f"{profile['last_name']}"
    )

else:

    full_name = (
        f"{profile['first_name']} "
        f"{profile['last_name']}"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sp-sidebar-brand">'
        '<div class="sp-sidebar-title">'
        '<div class="sp-title-line">'
        '<span class="sp-title-blue">STEM</span>'
        '<span class="sp-title-yellow">Pathways</span>'
        '</div>'
        '<div class="sp-title-nyc">NYC</div>'
        '<div class="sp-sidebar-accent"></div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(full_name)

    st.markdown(
        '<div class="sp-sidebar-meta">'
        f"Grade {html_module.escape(str(profile['grade']))}"
        "  •  "
        f"{html_module.escape(str(profile['borough']))}"
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"[{user_email}](mailto:{user_email})"
    )

    st.divider()

    st.markdown(
        '<div class="sp-nav-section">HOME</div>',
        unsafe_allow_html=True
    )

    sidebar_nav_button("Dashboard", "Dashboard", "nav_v3_dashboard")
    sidebar_nav_button("My STEM Pathway", "My STEM Pathway", "nav_v3_stem_pathway")

    st.divider()

    st.markdown(
        '<div class="sp-nav-section">DISCOVER</div>',
        unsafe_allow_html=True
    )

    sidebar_nav_button("Opportunities", "Opportunities", "nav_v3_opportunities")
    sidebar_nav_button("Deadline Calendar", "Deadline Calendar", "nav_v3_deadline_calendar")
    sidebar_nav_button("College Suggestions", "College Suggestions", "nav_v3_college_suggestions")
    sidebar_nav_button("Project Explorer", "Projects", "nav_v3_projects")
    sidebar_nav_button("Resources", "Resources", "nav_v3_resources")

    st.divider()

    st.markdown(
        '<div class="sp-nav-section">MY PROGRESS</div>',
        unsafe_allow_html=True
    )

    sidebar_nav_button("My Applications", "My Applications", "nav_v3_applications")
    sidebar_nav_button("Favorite Colleges", "My Favorite Colleges", "nav_v3_favorite_colleges")

    st.divider()

    st.markdown(
        '<div class="sp-nav-section">TOOLS</div>',
        unsafe_allow_html=True
    )

    sidebar_nav_button("GPA Calculator", "GPA Calculator", "nav_v3_gpa_calculator")

    st.divider()

    st.markdown(
        '<div class="sp-nav-section">ACCOUNT</div>',
        unsafe_allow_html=True
    )

    sidebar_nav_button("Feedback", "Feedback", "nav_v3_feedback")
    sidebar_nav_button("My Profile", "My Profile", "nav_v3_my_profile")

    if st.button(
        "Sign Out",
        key="nav_v3_sign_out",
        icon=None,
        use_container_width=True
    ):

        st.logout()

    if is_admin_user(
        user_email
    ):

        st.divider()

        st.markdown(
            '<div class="sp-nav-section">ADMIN</div>',
            unsafe_allow_html=True
        )

        sidebar_nav_button("Admin Dashboard", "Admin Dashboard", "nav_v3_admin_dashboard")

    st.divider()

    st.markdown(
        """
        <div class="sp-contact-card">
            <div class="sp-contact-title">Contact</div>
            <div class="sp-contact-text">
                Have feedback, questions, or suggestions?
            </div>
            <a class="sp-contact-email" href="mailto:danlopez0911@gmail.com">
                danlopez0911@gmail.com
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Explore • Build • Discover"
    )


page = st.session_state.current_page


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    # --------------------------------------------------------
    # LOAD PERSONAL DASHBOARD DATA
    # --------------------------------------------------------

    dashboard_saved_apps = load_saved_opportunities(
        user_sub
    )

    dashboard_favorites = load_favorite_colleges(
        user_sub
    )

    primary_interest = (
        profile["interests"][0]
        if profile.get(
            "interests"
        )
        else
        "Exploring STEM"
    )

    application_status_counts = {}

    for item in dashboard_saved_apps:

        status = str(
            item.get(
                "status",
                "Saved"
            )
        ).strip()

        application_status_counts[
            status
        ] = (
            application_status_counts.get(
                status,
                0
            )
            + 1
        )

    active_applications = sum(
        application_status_counts.get(
            status,
            0
        )
        for status in [
            "Planning to Apply",
            "Applying"
        ]
    )

    submitted_applications = sum(
        application_status_counts.get(
            status,
            0
        )
        for status in [
            "Applied",
            "Accepted",
            "Waitlisted",
            "Not Selected"
        ]
    )

    # --------------------------------------------------------
    # NEXT SAVED DEADLINE
    # --------------------------------------------------------

    next_saved_deadline = None

    if (
        dashboard_saved_apps
        and
        not opportunities.empty
    ):

        saved_name_set = {
            str(
                item.get(
                    "opportunity_name",
                    ""
                )
            )
            for item in dashboard_saved_apps
        }

        deadline_candidates = []

        for _, opportunity in opportunities.iterrows():

            opportunity_name = str(
                opportunity.get(
                    "name",
                    ""
                )
            )

            if (
                opportunity_name
                not in saved_name_set
            ):

                continue

            parsed_deadline = parse_confirmed_deadline(
                opportunity.get(
                    "deadline"
                )
            )

            if parsed_deadline is None:

                continue

            if parsed_deadline.tzinfo is None:

                parsed_deadline = (
                    parsed_deadline.replace(
                        tzinfo=timezone.utc
                    )
                )

            days_left = (
                parsed_deadline.date()
                -
                datetime.now(
                    timezone.utc
                ).date()
            ).days

            if days_left >= 0:

                deadline_candidates.append(
                    (
                        parsed_deadline,
                        days_left,
                        opportunity_name,
                        str(
                            opportunity.get(
                                "organization",
                                ""
                            )
                        )
                    )
                )

        if deadline_candidates:

            deadline_candidates.sort(
                key=lambda item:
                    item[0]
            )

            next_saved_deadline = (
                deadline_candidates[0]
            )

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="sp-hero">
            <div class="sp-kicker">Your personalized STEM workspace</div>
            <h1>Welcome back, {profile['first_name']} 👋</h1>
            <p>
                Explore careers, discover colleges and opportunities,
                build projects, and keep your STEM journey organized in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # JOURNEY SNAPSHOT
    # --------------------------------------------------------

    st.header(
        "Your STEM Journey"
    )

    st.markdown(
        '<div class="sp-section-subtitle">A quick snapshot of where you are right now.</div>',
        unsafe_allow_html=True
    )

    dash_metrics = st.container(
        key="dash_journey_metrics"
    )

    journey1, journey2, journey3, journey4 = (
        dash_metrics.columns(4)
    )

    with journey1:

        st.metric(
            "Primary Interest",
            primary_interest
        )

    with journey2:

        st.metric(
            "Saved Programs",
            len(
                dashboard_saved_apps
            )
        )

    with journey3:

        st.metric(
            "Favorite Colleges",
            len(
                dashboard_favorites
            )
        )

    with journey4:

        st.metric(
            "Applications Submitted",
            submitted_applications
        )

    # --------------------------------------------------------
    # NEXT DEADLINE BANNER
    # --------------------------------------------------------

    if next_saved_deadline:

        deadline_dt, days_left, program_name, organization = (
            next_saved_deadline
        )

        if days_left == 0:

            deadline_message = (
                "Due today"
            )

        elif days_left == 1:

            deadline_message = (
                "1 day remaining"
            )

        else:

            deadline_message = (
                f"{days_left} days remaining"
            )

        with st.container(
            border=True
        ):

            deadline_col1, deadline_col2 = (
                st.columns(
                    [4, 1]
                )
            )

            with deadline_col1:

                st.subheader(
                    "Your Next Saved Deadline"
                )

                st.write(
                    f"**{program_name}**"
                )

                if organization:

                    st.caption(
                        organization
                    )

                st.write(
                    deadline_dt.strftime(
                        "%B %d, %Y"
                    ).replace(
                        " 0",
                        " "
                    )
                )

            with deadline_col2:

                st.metric(
                    "Time Left",
                    deadline_message
                )

            if st.button(
                "Open Deadline Calendar",
                key="dashboard_deadline_calendar",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "Deadline Calendar"
                )

                st.rerun()

    elif dashboard_saved_apps:

        st.info(
            "You have saved opportunities, but none currently have a "
            "specific upcoming deadline in the database."
        )

    else:

        st.info(
            "Save opportunities you care about and their upcoming deadlines "
            "will appear here automatically."
        )

    st.divider()

    # --------------------------------------------------------
    # CONTINUE YOUR JOURNEY
    # --------------------------------------------------------

    st.header(
        "Continue Your Journey"
    )

    st.markdown(
        '<div class="sp-section-subtitle">Choose what you want to work on next.</div>',
        unsafe_allow_html=True
    )

    journey_cards = st.container(
        key="dash_continue_journey"
    )

    action_row1 = journey_cards.columns(3)

    with action_row1[0]:

        with st.container(
            border=True
        ):

            st.subheader(
                "Explore Your Path"
            )

            st.write(
                "Discover majors, careers, salary data, skills, and "
                "possible STEM directions."
            )

            if st.button(
                "Open My STEM Pathway",
                key="dashboard_pathway_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "My STEM Pathway"
                )

                st.rerun()

    with action_row1[1]:

        with st.container(
            border=True
        ):

            st.subheader(
                "Discover Colleges"
            )

            st.write(
                "Answer simple questions and find colleges connected "
                "to your interests and preferences."
            )

            if st.button(
                "Find College Matches",
                key="dashboard_colleges_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "College Suggestions"
                )

                st.rerun()

    with action_row1[2]:

        with st.container(
            border=True
        ):

            st.subheader(
                "Build Something"
            )

            st.write(
                "Get personalized project ideas based on what you want "
                "to create and the tools you have."
            )

            if st.button(
                "Explore Projects",
                key="dashboard_projects_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "Projects"
                )

                st.rerun()

    action_row2 = journey_cards.columns(3)

    with action_row2[0]:

        with st.container(
            border=True
        ):

            st.subheader(
                "Find Opportunities"
            )

            st.write(
                "Discover programs, research, internships, courses, "
                "and scholarships."
            )

            if st.button(
                "Browse Opportunities",
                key="dashboard_opportunities_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "Opportunities"
                )

                st.rerun()

    with action_row2[1]:

        with st.container(
            border=True
        ):

            st.subheader(
                "Track Applications"
            )

            if active_applications:

                st.write(
                    f"You currently have **{active_applications}** "
                    f"application(s) in progress."
                )

            elif dashboard_saved_apps:

                st.write(
                    f"You have **{len(dashboard_saved_apps)}** saved "
                    "opportunity/opportunities."
                )

            else:

                st.write(
                    "Save opportunities and manage your application "
                    "progress in one place."
                )

            if st.button(
                "Open My Applications",
                key="dashboard_applications_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "My Applications"
                )

                st.rerun()

    with action_row2[2]:

        with st.container(
            border=True
        ):

            st.subheader(
                "Review Your College List"
            )

            if dashboard_favorites:

                top_favorite = (
                    dashboard_favorites[0].get(
                        "college_name",
                        "Your top college"
                    )
                )

                st.write(
                    f"Your current #1 favorite is **{top_favorite}**."
                )

            else:

                st.write(
                    "Save colleges you like and arrange them in your "
                    "personal order."
                )

            if st.button(
                "Open Favorite Colleges",
                key="dashboard_favorites_v2",
                use_container_width=True
            ):

                st.session_state.current_page = (
                    "My Favorite Colleges"
                )

                st.rerun()

    st.divider()

    # --------------------------------------------------------
    # YOUR CURRENT DIRECTION
    # --------------------------------------------------------

    st.header(
        "Your Current Direction"
    )

    direction_col1, direction_col2 = (
        st.columns(
            [2, 1]
        )
    )

    with direction_col1:

        with st.container(
            border=True
        ):

            st.subheader(
                primary_interest
            )

            st.write(
                "This is currently your primary STEM interest. "
                "It can change as you explore new fields and experiences."
            )

            st.write(
                f"**Exploration stage:** "
                f"{profile['exploration_stage']}"
            )

            st.write(
                f"**Weekly STEM goal:** "
                f"{profile['weekly_time']}"
            )

    with direction_col2:

        with st.container(
            border=True
        ):

            st.subheader(
                "Quick Profile"
            )

            st.write(
                f"**Grade:** {profile['grade']}"
            )

            st.write(
                f"**Borough:** {profile['borough']}"
            )

            st.write(
                f"**Interest confidence:** "
                f"{profile['confidence']}/10"
            )

            if profile.get(
                "financial_support"
            ):

                st.write(
                    "**Opportunity preference:** "
                    "Free / financially supported"
                )

    # --------------------------------------------------------
    # INTERESTS
    # --------------------------------------------------------

    st.divider()

    st.header(
        "Your STEM Interests"
    )

    if profile.get(
        "interests"
    ):

        interest_pills = "".join(
            [
                f'<span class="sp-pill">{interest}</span>'
                for interest
                in profile[
                    "interests"
                ]
            ]
        )

        st.markdown(
            interest_pills,
            unsafe_allow_html=True
        )

    if st.button(
        "Update My Profile",
        key="dashboard_edit_profile_v2"
    ):

        st.session_state.profile_completed = (
            False
        )

        st.rerun()


# ============================================================
# STEM PATHWAY
# ============================================================

elif page == "My STEM Pathway":

    render_page_header(
        "My STEM Pathway",
        (
            "Answer the Career Explorer questions to discover "
            "STEM fields, majors, and careers that may fit you."
        )
    )

    st.info(
        "These recommendations are designed to support exploration, "
        "not determine what you must study or become."
    )

    st.divider()

    st.header(
        "Discover Your STEM Direction"
    )

    preferred_work = st.selectbox(
        "Which type of work sounds most interesting?",
        [
            "Building physical machines or products",
            "Designing electronics and circuits",
            "Programming software",
            "Working with data and artificial intelligence",
            "Solving healthcare problems",
            "Conducting scientific research",
            "Working with mathematics and models",
            "Improving the environment",
            "Building robots and automated systems",
            "I am not sure yet"
        ]
    )

    favorite_activity = st.selectbox(
        "Which activity sounds most enjoyable?",
        [
            "Designing something in CAD",
            "Building a circuit",
            "Writing a program",
            "Analyzing a dataset",
            "Running an experiment",
            "Building a robot",
            "Solving difficult math problems",
            "Designing a healthcare device",
            "Studying the environment",
            "I am not sure yet"
        ]
    )

    programming_score = st.slider(
        "How much do you enjoy programming?",
        1,
        10,
        5
    )

    hands_on_score = st.slider(
        "How much do you enjoy building physical things?",
        1,
        10,
        5
    )

    math_score = st.slider(
        "How much do you enjoy mathematics?",
        1,
        10,
        5
    )

    electronics_score = st.slider(
        "How interested are you in electronics and circuits?",
        1,
        10,
        5
    )

    science_score = st.slider(
        "How interested are you in science and research?",
        1,
        10,
        5
    )

    data_score = st.slider(
        "How interested are you in data, statistics, or AI?",
        1,
        10,
        5
    )

    preferred_environment = st.selectbox(
        "Which environment sounds most appealing?",
        [
            "Technology company",
            "Engineering design company",
            "Engineering laboratory",
            "Research laboratory",
            "Hospital or healthcare technology",
            "Manufacturing company",
            "University or research institution",
            "Environmental organization",
            "I am not sure yet"
        ]
    )

    # ========================================================
    # CAREER DATABASE
    # ========================================================

    career_database = {

        "Engineering": {

            "majors": [
                "Engineering",
                "Industrial Engineering",
                "Civil Engineering",
                "Systems Engineering"
            ],

            "careers": [
                "Civil Engineer",
                "Industrial Engineer",
                "Systems Engineer",
                "Materials Engineer",
                "Aerospace Engineer"
            ]
        },

        "Electrical Engineering": {

            "majors": [
                "Electrical Engineering",
                "Electrical and Computer Engineering"
            ],

            "careers": [
                "Electrical Engineer",
                "Electronics Engineer",
                "Power Systems Engineer",
                "Controls Engineer",
                "RF Engineer",
                "Semiconductor Engineer",
                "Hardware Engineer"
            ]
        },

        "Mechanical Engineering": {

            "majors": [
                "Mechanical Engineering",
                "Aerospace Engineering",
                "Mechatronics"
            ],

            "careers": [
                "Mechanical Engineer",
                "Aerospace Engineer",
                "Automotive Engineer",
                "Manufacturing Engineer",
                "Product Design Engineer",
                "Mechatronics Engineer",
                "Robotics Engineer"
            ]
        },

        "Computer Engineering": {

            "majors": [
                "Computer Engineering",
                "Electrical and Computer Engineering"
            ],

            "careers": [
                "Computer Hardware Engineer",
                "Embedded Systems Engineer",
                "Firmware Engineer",
                "FPGA Engineer",
                "Hardware Engineer",
                "Robotics Engineer",
                "Systems Engineer"
            ]
        },

        "Computer Science": {

            "majors": [
                "Computer Science",
                "Software Engineering",
                "Cybersecurity"
            ],

            "careers": [
                "Software Developer",
                "Backend Developer",
                "Frontend Developer",
                "Full-Stack Developer",
                "Cybersecurity Analyst",
                "Cloud Engineer",
                "Database Architect",
                "Systems Developer"
            ]
        },

        "Artificial Intelligence": {

            "majors": [
                "Computer Science",
                "Artificial Intelligence",
                "Data Science"
            ],

            "careers": [
                "Machine Learning Engineer",
                "AI Engineer",
                "Data Scientist",
                "Computer Vision Engineer",
                "NLP Engineer",
                "AI Research Scientist",
                "Machine Learning Researcher"
            ]
        },

        "Data Science": {

            "majors": [
                "Data Science",
                "Statistics",
                "Computer Science",
                "Applied Mathematics"
            ],

            "careers": [
                "Data Scientist",
                "Data Analyst",
                "Data Engineer",
                "Operations Research Analyst",
                "Statistician",
                "Business Intelligence Analyst",
                "Quantitative Analyst"
            ]
        },

        "Biomedical Engineering": {

            "majors": [
                "Biomedical Engineering",
                "Bioengineering"
            ],

            "careers": [
                "Biomedical Engineer",
                "Medical Device Engineer",
                "Biomechanical Engineer",
                "Clinical Engineer",
                "Rehabilitation Engineer",
                "Healthcare Technology Engineer"
            ]
        },

        "Biology": {

            "majors": [
                "Biology",
                "Biochemistry",
                "Molecular Biology",
                "Biotechnology"
            ],

            "careers": [
                "Biologist",
                "Microbiologist",
                "Biochemist",
                "Biological Technician",
                "Geneticist",
                "Medical Scientist",
                "Biotechnology Researcher"
            ]
        },

        "Physics": {

            "majors": [
                "Physics",
                "Applied Physics",
                "Engineering Physics"
            ],

            "careers": [
                "Physicist",
                "Optical Engineer",
                "Nuclear Engineer",
                "Aerospace Engineer",
                "Research Scientist",
                "Medical Physicist"
            ]
        },

        "Mathematics": {

            "majors": [
                "Mathematics",
                "Applied Mathematics",
                "Statistics",
                "Actuarial Science"
            ],

            "careers": [
                "Mathematician",
                "Statistician",
                "Actuary",
                "Operations Research Analyst",
                "Data Scientist",
                "Quantitative Analyst"
            ]
        },

        "Environmental Science": {

            "majors": [
                "Environmental Science",
                "Environmental Engineering",
                "Earth Science"
            ],

            "careers": [
                "Environmental Scientist",
                "Environmental Engineer",
                "Hydrologist",
                "Conservation Scientist",
                "Environmental Consultant",
                "Climate Data Analyst"
            ]
        },

        "Robotics": {

            "majors": [
                "Robotics Engineering",
                "Mechanical Engineering",
                "Computer Engineering",
                "Electrical Engineering",
                "Mechatronics"
            ],

            "careers": [
                "Robotics Engineer",
                "Mechatronics Engineer",
                "Controls Engineer",
                "Automation Engineer",
                "Embedded Systems Engineer",
                "Computer Vision Engineer"
            ]
        }
    }

    # ========================================================
    # SCORING
    # ========================================================

    scores = {

        "Engineering": 0,
        "Electrical Engineering": 0,
        "Mechanical Engineering": 0,
        "Computer Engineering": 0,
        "Computer Science": 0,
        "Artificial Intelligence": 0,
        "Data Science": 0,
        "Biomedical Engineering": 0,
        "Biology": 0,
        "Physics": 0,
        "Mathematics": 0,
        "Environmental Science": 0,
        "Robotics": 0
    }

    for interest in profile["interests"]:

        if interest in scores:
            scores[interest] += 20

    scores["Computer Science"] += (
        programming_score * 2
    )

    scores["Computer Engineering"] += (
        programming_score * 1.5
    )

    scores["Artificial Intelligence"] += (
        programming_score * 2
    )

    scores["Data Science"] += (
        programming_score * 1.5
    )

    scores["Robotics"] += (
        programming_score
    )

    scores["Mechanical Engineering"] += (
        hands_on_score * 2
    )

    scores["Electrical Engineering"] += (
        hands_on_score
    )

    scores["Computer Engineering"] += (
        hands_on_score
    )

    scores["Robotics"] += (
        hands_on_score * 2
    )

    scores["Engineering"] += (
        hands_on_score
    )

    scores["Mathematics"] += (
        math_score * 2
    )

    scores["Physics"] += (
        math_score * 1.5
    )

    scores["Data Science"] += (
        math_score
    )

    scores["Artificial Intelligence"] += (
        math_score
    )

    scores["Electrical Engineering"] += (
        math_score
    )

    scores["Mechanical Engineering"] += (
        math_score
    )

    scores["Electrical Engineering"] += (
        electronics_score * 2
    )

    scores["Computer Engineering"] += (
        electronics_score * 2
    )

    scores["Robotics"] += (
        electronics_score * 1.5
    )

    scores["Biology"] += (
        science_score * 2
    )

    scores["Biomedical Engineering"] += (
        science_score * 1.5
    )

    scores["Physics"] += (
        science_score * 1.5
    )

    scores["Environmental Science"] += (
        science_score * 1.5
    )

    scores["Data Science"] += (
        data_score * 2
    )

    scores["Artificial Intelligence"] += (
        data_score * 2
    )

    scores["Computer Science"] += (
        data_score
    )

    scores["Mathematics"] += (
        data_score
    )

    work_mapping = {

        "Building physical machines or products":
            "Mechanical Engineering",

        "Designing electronics and circuits":
            "Electrical Engineering",

        "Programming software":
            "Computer Science",

        "Working with data and artificial intelligence":
            "Artificial Intelligence",

        "Solving healthcare problems":
            "Biomedical Engineering",

        "Conducting scientific research":
            "Biology",

        "Working with mathematics and models":
            "Mathematics",

        "Improving the environment":
            "Environmental Science",

        "Building robots and automated systems":
            "Robotics"
    }

    if preferred_work in work_mapping:

        scores[
            work_mapping[
                preferred_work
            ]
        ] += 25

    activity_mapping = {

        "Designing something in CAD":
            "Mechanical Engineering",

        "Building a circuit":
            "Electrical Engineering",

        "Writing a program":
            "Computer Science",

        "Analyzing a dataset":
            "Data Science",

        "Running an experiment":
            "Biology",

        "Building a robot":
            "Robotics",

        "Solving difficult math problems":
            "Mathematics",

        "Designing a healthcare device":
            "Biomedical Engineering",

        "Studying the environment":
            "Environmental Science"
    }

    if favorite_activity in activity_mapping:

        scores[
            activity_mapping[
                favorite_activity
            ]
        ] += 20

    environment_mapping = {

        "Technology company":
            "Computer Science",

        "Engineering design company":
            "Mechanical Engineering",

        "Engineering laboratory":
            "Electrical Engineering",

        "Research laboratory":
            "Physics",

        "Hospital or healthcare technology":
            "Biomedical Engineering",

        "Manufacturing company":
            "Mechanical Engineering",

        "University or research institution":
            "Biology",

        "Environmental organization":
            "Environmental Science"
    }

    if preferred_environment in environment_mapping:

        scores[
            environment_mapping[
                preferred_environment
            ]
        ] += 15

    # ========================================================
    # GENERATE RESULTS
    # ========================================================

    if st.button(
        "Generate My STEM Recommendations",
        type="primary",
        use_container_width=True
    ):

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        st.session_state.career_results = (
            ranked[:3]
        )

    if st.session_state.career_results:

        top_three = (
            st.session_state.career_results
        )

        max_score_value = (
            top_three[0][1]
        )

        st.divider()

        st.header(
            "Your STEM Direction"
        )

        for index, (
            field,
            score
        ) in enumerate(
            top_three,
            start=1
        ):

            percentage = round(
                (
                    score /
                    max_score_value
                ) * 100
            )

            major_info = (
                career_database[
                    field
                ]
            )

            with st.container(
                border=True
            ):

                st.subheader(
                    f"#{index} {field}"
                )

                st.metric(
                    "Exploration Match",
                    f"{percentage}%"
                )

                st.write(
                    "**Majors to explore:**"
                )

                for major in (
                    major_info["majors"]
                ):

                    st.write(
                        f"• {major}"
                    )

        top_field = (
            top_three[0][0]
        )

        top_info = (
            career_database[
                top_field
            ]
        )

        st.divider()

        st.header(
            "Recommended Major Direction"
        )

        st.subheader(
            top_info["majors"][0]
        )

        st.info(
            "This is a starting point for exploration, not a final decision."
        )

        st.divider()

        st.header(
            "Specific Careers to Explore"
        )

        career_columns = st.columns(2)

        for index, career_name in enumerate(
            top_info["careers"]
        ):

            with career_columns[
                index % 2
            ]:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        career_name
                    )

                    if careers.empty:

                        st.info(
                            "Career database unavailable."
                        )

                        continue

                    career_match = careers[
                        careers["career"]
                        .astype(str)
                        .str.lower()
                        == career_name.lower()
                    ]

                    if career_match.empty:

                        st.info(
                            "Detailed career data is being added."
                        )

                        continue

                    career_data = (
                        career_match.iloc[0]
                    )

                    st.caption(
                        f"Recommended major: "
                        f"{career_data['recommended_major']}"
                    )

                    st.write(
                        career_data[
                            "description"
                        ]
                    )

                    st.markdown(
                        "#### Salary & Career Pay"
                    )

                    salary_col1, salary_col2 = (
                        st.columns(2)
                    )

                    with salary_col1:

                        st.metric(
                            "Early-Career Benchmark",
                            format_salary(
                                career_data[
                                    "early_career_salary"
                                ]
                            )
                        )

                        st.caption(
                            "U.S. 25th percentile"
                        )

                    with salary_col2:

                        st.metric(
                            "Typical Salary",
                            format_salary(
                                career_data[
                                    "median_salary"
                                ]
                            )
                        )

                        st.caption(
                            "U.S. median"
                        )

                    salary_col3, salary_col4 = (
                        st.columns(2)
                    )

                    with salary_col3:

                        st.metric(
                            "Experienced Benchmark",
                            format_salary(
                                career_data[
                                    "experienced_salary"
                                ]
                            )
                        )

                        st.caption(
                            "U.S. 75th percentile"
                        )

                    with salary_col4:

                        st.metric(
                            "NYC / NY Average",
                            format_salary(
                                career_data[
                                    "average_salary"
                                ]
                            )
                        )

                        st.caption(
                            "Local mean annual wage"
                        )

                    st.markdown(
                        "#### Typical Education"
                    )

                    st.write(
                        career_data[
                            "education"
                        ]
                    )

                    st.markdown(
                        "#### Skills to Explore"
                    )

                    for skill in str(
                        career_data["skills"]
                    ).split(";"):

                        st.write(
                            f"• {skill.strip()}"
                        )

                    if (
                        "salary_mapping_note"
                        in career_data.index
                        and
                        pd.notna(
                            career_data[
                                "salary_mapping_note"
                            ]
                        )
                        and
                        str(
                            career_data[
                                "salary_mapping_note"
                            ]
                        ).strip()
                    ):

                        st.info(
                            career_data[
                                "salary_mapping_note"
                            ]
                        )

                        if (
                            "source_url"
                            in career_data.index
                            and
                            safe_http_url(
                                career_data[
                                    "source_url"
                                ]
                            )
                        ):

                            st.link_button(
                                "View Official BLS Source",
                                safe_http_url(
                                    career_data[
                                        "source_url"
                                    ]
                                ),
                                use_container_width=True
                            )

        st.divider()

        st.caption(
            "Salary benchmarks represent wage distributions, not "
            "guaranteed salaries after a specific number of years."
        )


# ============================================================
# OPPORTUNITIES
# ============================================================

elif page == "Opportunities":

    render_page_header(
        "Opportunities",
        (
            "Discover programs, internships, research, courses, "
            "competitions, scholarships, and paid work experiences — "
            "with selectivity and eligibility information to help you choose."
        )
    )

    st.divider()

    if opportunities.empty:

        st.warning(
            "The opportunities database is currently unavailable."
        )

    else:

        with st.form(
            "opportunity_search_form",
            clear_on_submit=False
        ):
            opportunity_types = st.multiselect(
                "Filter by opportunity type",
                sorted(
                    opportunities[
                        "opportunity_type"
                    ]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                ),
                key="opportunity_filter_types"
            )

            research_area_filter = st.multiselect(
                "Research Area",
                [
                    "Artificial Intelligence",
                    "Computer Science",
                    "Engineering",
                    "Biomedical Science",
                    "Biology",
                    "Neuroscience",
                    "Cancer Research",
                    "Data Science",
                    "Mathematics",
                    "Physics",
                    "Chemistry",
                    "Environmental Science",
                    "Earth / Climate Science",
                    "Bioinformatics / Computational Biology",
                    "Medicine / Health",
                    "Robotics",
                    "Space Science",
                    "General STEM / Interdisciplinary"
                ],
                key="opportunity_filter_research_areas"
            )

            selectivity_filter = st.multiselect(
                "Filter by selectivity",
                [
                    "Accessible / Lottery or Placement Based",
                    "Eligibility Based",
                    "Moderately Competitive",
                    "Highly Competitive",
                    "Extremely Competitive"
                ],
                key="opportunity_filter_selectivity"
            )

            student_age = st.selectbox(
                "Your age",
                [
                    "Any age",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19+"
                ],
                help=(
                    "Age and grade are checked separately because some programs "
                    "require students to be a certain age even if they are in the eligible grade."
                ),
                key="opportunity_filter_age"
            )

            search_opportunities = st.form_submit_button(
                "Search / Update Results",
                use_container_width=True,
                type="primary"
            )

        if search_opportunities:

            st.session_state[
                "opportunity_search_submitted"
            ] = True

            st.session_state[
                "opportunity_search_types"
            ] = opportunity_types

            st.session_state[
                "opportunity_search_selectivity"
            ] = selectivity_filter

            st.session_state[
                "opportunity_search_age"
            ] = student_age

            st.session_state[
                "opportunity_search_research_areas"
            ] = research_area_filter

        active_types = st.session_state.get(
            "opportunity_search_types",
            []
        )

        active_selectivity = st.session_state.get(
            "opportunity_search_selectivity",
            []
        )

        active_age = st.session_state.get(
            "opportunity_search_age",
            "Any age"
        )

        active_research_areas = st.session_state.get(
            "opportunity_search_research_areas",
            []
        )

        search_submitted = st.session_state.get(
            "opportunity_search_submitted",
            False
        )


        def selectivity_to_stars(
            opportunity
        ):

            raw_stars = pd.to_numeric(
                opportunity.get(
                    "selectivity_stars",
                    0
                ),
                errors="coerce"
            )

            if (
                pd.notna(
                    raw_stars
                )
                and
                int(
                    raw_stars
                )
                > 0
            ):

                stars = max(
                    1,
                    min(
                        5,
                        int(
                            raw_stars
                        )
                    )
                )

            else:

                label = str(
                    opportunity.get(
                        "selectivity",
                        ""
                    )
                ).strip().lower()

                if (
                    "extremely competitive"
                    in label
                ):
                    stars = 5

                elif (
                    "highly competitive"
                    in label
                ):
                    stars = 4

                elif (
                    "moderately competitive"
                    in label
                    or
                    "competitive"
                    in label
                ):
                    stars = 3

                elif (
                    "eligibility based"
                    in label
                ):
                    stars = 2

                elif (
                    "accessible"
                    in label
                    or
                    "lottery"
                    in label
                    or
                    "placement based"
                    in label
                ):
                    stars = 1

                else:
                    # Legacy opportunities without a rating get a neutral
                    # middle rating instead of displaying "Not rated".
                    stars = 3

            return (
                "★" * stars
                +
                "☆" * (
                    5 - stars
                )
            )


        def age_matches(
            age_value,
            selected_age
        ):

            if selected_age == "Any age":
                return True

            age_text = str(
                age_value
            ).strip().lower()

            # Unknown/variable age requirements should not be silently excluded.
            if (
                not age_text
                or
                age_text == "nan"
                or
                any(
                    phrase in age_text
                    for phrase in [
                        "check official",
                        "varies",
                        "not publicly",
                        "no simple age"
                    ]
                )
            ):
                return True

            try:

                age_num = (
                    19
                    if selected_age == "19+"
                    else int(
                        selected_age
                    )
                )

            except Exception:
                return True

            # Handle ranges such as 14–18 or 16-21.
            range_match = re.search(
                r"(\d{1,2})\s*[–-]\s*(\d{1,2})",
                age_text
            )

            if range_match:

                minimum = int(
                    range_match.group(1)
                )

                maximum = int(
                    range_match.group(2)
                )

                return (
                    minimum
                    <= age_num
                    <= maximum
                )

            # Handle requirements such as 16+.
            plus_match = re.search(
                r"(\d{1,2})\s*\+",
                age_text
            )

            if plus_match:

                return (
                    age_num
                    >= int(
                        plus_match.group(1)
                    )
                )

            # Handle a single explicit age.
            numbers = [
                int(value)
                for value in re.findall(
                    r"\b\d{1,2}\b",
                    age_text
                )
            ]

            if len(
                numbers
            ) == 1:

                return (
                    age_num
                    == numbers[0]
                )

            return True

        def research_areas_from_fields(
            fields_value
        ):

            tokens = [
                item.strip().lower()
                for item in str(
                    fields_value or ""
                ).split(";")
                if item.strip()
            ]

            areas = set()

            def token_matches(
                *needles
            ):

                for token in tokens:

                    for needle in needles:

                        if (
                            token == needle
                            or
                            needle in token
                        ):
                            return True

                return False

            if (
                token_matches(
                    "artificial intelligence",
                    "machine learning"
                )
                or
                "ai" in tokens
            ):
                areas.add(
                    "Artificial Intelligence"
                )

            if token_matches(
                "computer science"
            ):
                areas.add(
                    "Computer Science"
                )

            if token_matches(
                "engineering"
            ):
                areas.add(
                    "Engineering"
                )

            if token_matches(
                "biomedical",
                "bioengineering"
            ):
                areas.add(
                    "Biomedical Science"
                )

            if token_matches(
                "biology"
            ):
                areas.add(
                    "Biology"
                )

            if token_matches(
                "neuroscience",
                "neurology"
            ):
                areas.add(
                    "Neuroscience"
                )

            if token_matches(
                "cancer"
            ):
                areas.add(
                    "Cancer Research"
                )

            if token_matches(
                "data science",
                "data analysis",
                "statistics",
                "biostatistics"
            ):
                areas.add(
                    "Data Science"
                )

            if (
                token_matches(
                    "mathematics"
                )
                or
                "math" in tokens
            ):
                areas.add(
                    "Mathematics"
                )

            if token_matches(
                "physics"
            ):
                areas.add(
                    "Physics"
                )

            if token_matches(
                "chemistry"
            ):
                areas.add(
                    "Chemistry"
                )

            if token_matches(
                "environmental",
                "ecology"
            ):
                areas.add(
                    "Environmental Science"
                )

            if token_matches(
                "earth science",
                "climate",
                "remote sensing"
            ):
                areas.add(
                    "Earth / Climate Science"
                )

            if token_matches(
                "bioinformatics",
                "computational biology"
            ):
                areas.add(
                    "Bioinformatics / Computational Biology"
                )

            if token_matches(
                "medicine",
                "health",
                "immunology",
                "genetics",
                "genomics",
                "stem cell"
            ):
                areas.add(
                    "Medicine / Health"
                )

            if token_matches(
                "robotics"
            ):
                areas.add(
                    "Robotics"
                )

            if token_matches(
                "space",
                "aerospace",
                "astronomy"
            ):
                areas.add(
                    "Space Science"
                )

            general_tokens = {
                "stem",
                "science",
                "research",
                "technology",
                "innovation",
                "design thinking",
                "laboratory research",
                "career exploration",
                "natural sciences",
                "nuclear science",
                "materials science",
                "social science",
                "education",
                "science communication",
                "experimental design"
            }

            if any(
                token in general_tokens
                for token in tokens
            ):
                areas.add(
                    "General STEM / Interdisciplinary"
                )

            return areas

        def is_eligible(
            opportunity
        ):

            eligible_grades = [
                item.strip()
                for item in str(
                    opportunity["grades"]
                ).split(";")
            ]

            boroughs_served = [
                item.strip()
                for item in str(
                    opportunity[
                        "boroughs_served"
                    ]
                ).split(";")
            ]

            return (
                profile["grade"]
                in eligible_grades
                and
                profile["borough"]
                in boroughs_served
            )

        def calculate_match(
            opportunity
        ):

            score = 0
            max_score = 0
            reasons = []

            fields = [
                item.strip()
                for item in str(
                    opportunity["fields"]
                ).split(";")
            ]

            boroughs_served = [
                item.strip()
                for item in str(
                    opportunity[
                        "boroughs_served"
                    ]
                ).split(";")
            ]

            max_score += 40

            if any(
                interest in fields
                for interest in profile[
                    "interests"
                ]
            ):

                score += 40

                reasons.append(
                    "Your STEM interests align with this opportunity."
                )

            max_score += 15

            if profile[
                "financial_support"
            ]:

                cost = str(
                    opportunity[
                        "cost"
                    ]
                ).lower()

                aid = str(
                    opportunity[
                        "financial_aid"
                    ]
                ).lower()

                if (
                    cost == "free"
                    or
                    aid == "available"
                ):

                    score += 15

                    reasons.append(
                        "This opportunity is free or offers financial support."
                    )

            else:

                score += 15

            max_score += 15

            if (
                profile["borough"]
                in boroughs_served
            ):

                score += 15

                reasons.append(
                    f"This opportunity serves students in the "
                    f"{profile['borough']}."
                )

            if (
                profile["borough"]
                == "Bronx"
            ):

                max_score += 10

                if str(
                    opportunity[
                        "bronx_priority"
                    ]
                ).lower() == "yes":

                    score += 10

                    reasons.append(
                        "This opportunity has a specific focus on Bronx students."
                    )

            return (
                round(
                    (
                        score /
                        max_score
                    ) * 100
                ),
                reasons
            )


        # ----------------------------------------------------
        # SEARCH RESULTS
        # ----------------------------------------------------

        if not search_submitted:

            st.info(
                "Choose your filters above, then press **Search Opportunities**."
            )

        else:

            search_results = []

            for _, opportunity in opportunities.iterrows():

                if (
                    active_types
                    and
                    str(
                        opportunity.get(
                            "opportunity_type",
                            ""
                        )
                    )
                    not in active_types
                ):

                    continue

                if (
                    active_selectivity
                    and
                    str(
                        opportunity.get(
                            "selectivity",
                            "Not rated yet"
                        )
                    )
                    not in active_selectivity
                ):

                    continue

                if not age_matches(
                    opportunity.get(
                        "age_range",
                        "Check official eligibility"
                    ),
                    active_age
                ):

                    continue

                if (
                    active_research_areas
                    and
                    not set(
                        active_research_areas
                    ).intersection(
                        research_areas_from_fields(
                            opportunity.get(
                                "fields",
                                ""
                            )
                        )
                    )
                ):

                    continue

                # Use the student's profile for personalization, but do not
                # hide a search result solely because the saved profile grade
                # may reflect the student's current rather than entering grade.
                try:

                    score, reasons = (
                        calculate_match(
                            opportunity
                        )
                    )

                except Exception:

                    score = 50
                    reasons = []

                search_results.append(
                    (
                        score,
                        reasons,
                        opportunity
                    )
                )

            search_results.sort(
                key=lambda item:
                    item[0],
                reverse=True
            )

            st.header(
                "Search Results"
            )

            st.caption(
                f"{len(search_results)} "
                f"{'opportunity' if len(search_results) == 1 else 'opportunities'} found."
            )

            modify_col, reset_col = st.columns(2)

            with modify_col:

                if st.button(
                    "Change My Search",
                    key="opportunity_change_search",
                    use_container_width=True
                ):

                    st.session_state[
                        "opportunity_search_submitted"
                    ] = False

                    st.rerun()

            with reset_col:

                if st.button(
                    "Clear Filters",
                    key="opportunity_clear_filters",
                    use_container_width=True
                ):

                    for key in [
                        "opportunity_filter_types",
                        "opportunity_filter_selectivity",
                        "opportunity_filter_age",
                        "opportunity_filter_research_areas",
                        "opportunity_search_types",
                        "opportunity_search_selectivity",
                        "opportunity_search_age",
                        "opportunity_search_research_areas"
                    ]:

                        st.session_state.pop(
                            key,
                            None
                        )

                    st.session_state[
                        "opportunity_search_submitted"
                    ] = False

                    st.rerun()

            if not search_results:

                st.warning(
                    "No opportunities matched every filter. Try removing one "
                    "selectivity level, opportunity type, or research area and search again."
                )

            for (
                result_index,
                (
                    score,
                    reasons,
                    opportunity
                )
            ) in enumerate(search_results):

                with st.container(
                    border=True
                ):

                    title_col, match_col = st.columns(
                        [4, 1]
                    )

                    with title_col:

                        st.subheader(
                            opportunity[
                                "name"
                            ]
                        )

                        st.caption(
                            opportunity.get(
                                "organization",
                                ""
                            )
                        )

                    with match_col:

                        st.metric(
                            "Profile Match",
                            f"{score}%"
                        )

                    st.write(
                        opportunity.get(
                            "description",
                            ""
                        )
                    )

                    details1, details2, details3 = st.columns(3)

                    with details1:

                        st.write(
                            f"**Type:** "
                            f"{opportunity.get('opportunity_type', 'Not listed')}"
                        )

                        st.write(
                            f"**Grades:** "
                            f"{opportunity.get('grades', 'Check eligibility')}"
                        )

                        st.write(
                            f"**Ages:** "
                            f"{opportunity.get('age_range', 'Check official eligibility')}"
                        )

                    with details2:

                        search_star_display = (
                            selectivity_to_stars(
                                opportunity
                            )
                        )

                        st.write(
                            f"**Selectivity:** "
                            f"{search_star_display}"
                        )


                        st.write(
                            f"**Acceptance Rate:** "
                            f"{opportunity.get('acceptance_rate', 'Not publicly reported')}"
                        )

                        st.write(
                            f"**Paid:** "
                            f"{opportunity.get('paid_status', 'Check official site')}"
                        )

                    with details3:

                        st.write(
                            f"**Deadline:** "
                            f"{opportunity.get('deadline', 'Check official site')}"
                        )

                        st.write(
                            f"**Format:** "
                            f"{opportunity.get('format', 'Check official site')}"
                        )

                        st.write(
                            f"**Internship Potential:** "
                            f"{opportunity.get('internship_potential', 'Not specified')}"
                        )

                    with st.expander(
                        "Why this may match you"
                    ):

                        if reasons:

                            for reason in reasons:

                                st.write(
                                    f"• {reason}"
                                )

                        else:

                            st.write(
                                "This result matches the filters you selected."
                            )

                        st.write(
                            f"**Requirements:** "
                            f"{opportunity.get('requirements', 'Check official site')}"
                        )

                    calendar_url = google_calendar_deadline_url(
                        str(
                            opportunity[
                                "name"
                            ]
                        ),
                        opportunity.get(
                            "deadline"
                        ),
                        str(
                            opportunity.get(
                                "url",
                                ""
                            )
                        ),
                        str(
                            opportunity.get(
                                "organization",
                                ""
                            )
                        )
                    )

                    official_url = safe_http_url(
                        opportunity.get(
                            "url"
                        )
                    )

                    if calendar_url:

                        action1, action2, action3 = st.columns(3)

                    else:

                        action1, action2 = st.columns(2)

                    with action1:

                        if st.button(
                            "Save Opportunity",
                            key=f"search_save_{result_index}_{opportunity['name']}",
                            use_container_width=True
                        ):

                            if save_opportunity(
                                user_sub,
                                str(
                                    opportunity[
                                        "name"
                                    ]
                                )
                            ):

                                st.success(
                                    "Saved to My Applications."
                                )

                    if calendar_url:

                        with action2:

                            st.link_button(
                                "Add to Google Calendar",
                                calendar_url,
                                use_container_width=True
                            )

                        with action3:

                            if official_url:

                                st.link_button(
                                    "View Official Opportunity",
                                    official_url,
                                    use_container_width=True
                                )

                    else:

                        with action2:

                            if official_url:

                                st.link_button(
                                    "View Official Opportunity",
                                    official_url,
                                    use_container_width=True
                                )

            st.divider()

            st.divider()

            st.caption(
                "Profile Match measures fit with your interests and preferences; "
                "it is not an admission probability. Always confirm age, grade, "
                "deadline, and eligibility requirements on the official website."
            )

            if st.button(
                "Search Again",
                key="opportunity_search_again_bottom",
                use_container_width=True
            ):

                st.session_state[
                    "opportunity_search_submitted"
                ] = False

                st.rerun()

        # ----------------------------------------------------
        # RECOMMENDED FOR YOU
        # ----------------------------------------------------

        st.divider()

        st.header(
            "Recommended for You"
        )

        st.write(
            "These are personalized suggestions based on your saved profile, "
            "including your STEM interests, grade, borough, age, and support preferences."
        )

        recommended_results = []

        for _, recommended_opportunity in opportunities.iterrows():

            try:

                if not is_eligible(
                    recommended_opportunity
                ):

                    continue

            except Exception:

                pass

            try:

                profile_age = str(
                    profile.get(
                        "age",
                        "Any age"
                    )
                )

                if not age_matches(
                    recommended_opportunity.get(
                        "age_range",
                        "Check official eligibility"
                    ),
                    profile_age
                ):

                    continue

            except Exception:

                pass

            try:

                recommended_score, recommended_reasons = (
                    calculate_match(
                        recommended_opportunity
                    )
                )

            except Exception:

                recommended_score = 50
                recommended_reasons = []

            recommended_results.append(
                (
                    recommended_score,
                    recommended_reasons,
                    recommended_opportunity
                )
            )

        recommended_results.sort(
            key=lambda item:
                item[0],
            reverse=True
        )

        if not recommended_results:

            st.info(
                "No personalized recommendations are available yet. "
                "Try updating your profile interests."
            )

        for (
            rec_index,
            (
                recommended_score,
                recommended_reasons,
                recommended_opportunity
            )
        ) in enumerate(recommended_results[:4]):

            with st.container(
                border=True
            ):

                rec_title_col, rec_match_col = st.columns(
                    [4, 1]
                )

                with rec_title_col:

                    st.subheader(
                        recommended_opportunity[
                            "name"
                        ]
                    )

                    st.caption(
                        recommended_opportunity.get(
                            "organization",
                            ""
                        )
                    )

                with rec_match_col:

                    st.metric(
                        "Your Match",
                        f"{recommended_score}%"
                    )

                st.write(
                    recommended_opportunity.get(
                        "description",
                        ""
                    )
                )

                rec1, rec2, rec3 = st.columns(3)

                with rec1:

                    st.write(
                        f"**Type:** "
                        f"{recommended_opportunity.get('opportunity_type', 'Not listed')}"
                    )

                    st.write(
                        f"**Grades:** "
                        f"{recommended_opportunity.get('grades', 'Check eligibility')}"
                    )

                    st.write(
                        f"**Ages:** "
                        f"{recommended_opportunity.get('age_range', 'Check official eligibility')}"
                    )

                with rec2:

                    rec_star_display = (
                        selectivity_to_stars(
                            recommended_opportunity
                        )
                    )

                    st.write(
                        f"**Selectivity:** "
                        f"{rec_star_display}"
                    )


                    st.write(
                        f"**Acceptance Rate:** "
                        f"{recommended_opportunity.get('acceptance_rate', 'Not publicly reported')}"
                    )

                with rec3:

                    st.write(
                        f"**Paid:** "
                        f"{recommended_opportunity.get('paid_status', 'Check official site')}"
                    )

                    st.write(
                        f"**Deadline:** "
                        f"{recommended_opportunity.get('deadline', 'Check official site')}"
                    )

                    st.write(
                        f"**Internship Potential:** "
                        f"{recommended_opportunity.get('internship_potential', 'Not specified')}"
                    )

                with st.expander(
                    "Why this is recommended"
                ):

                    if recommended_reasons:

                        for reason in recommended_reasons:

                            st.write(
                                f"• {reason}"
                            )

                    else:

                        st.write(
                            "This opportunity fits information in your saved profile."
                        )

                    st.write(
                        f"**Requirements:** "
                        f"{recommended_opportunity.get('requirements', 'Check official site')}"
                    )

                recommended_calendar_url = google_calendar_deadline_url(
                    str(
                        recommended_opportunity[
                            "name"
                        ]
                    ),
                    recommended_opportunity.get(
                        "deadline"
                    ),
                    str(
                        recommended_opportunity.get(
                            "url",
                            ""
                        )
                    ),
                    str(
                        recommended_opportunity.get(
                            "organization",
                            ""
                        )
                    )
                )

                recommended_official_url = safe_http_url(
                    recommended_opportunity.get(
                        "url"
                    )
                )

                if recommended_calendar_url:

                    rec_action1, rec_action2, rec_action3 = st.columns(3)

                else:

                    rec_action1, rec_action2 = st.columns(2)

                with rec_action1:

                    if st.button(
                        "Save Opportunity",
                        key=f"recommended_save_{rec_index}_{recommended_opportunity['name']}",
                        use_container_width=True
                    ):

                        if save_opportunity(
                            user_sub,
                            str(
                                recommended_opportunity[
                                    "name"
                                ]
                            )
                        ):

                            st.success(
                                "Saved to My Applications."
                            )

                if recommended_calendar_url:

                    with rec_action2:

                        st.link_button(
                            "Add to Google Calendar",
                            recommended_calendar_url,
                            use_container_width=True
                        )

                    with rec_action3:

                        if recommended_official_url:

                            st.link_button(
                                "View Official Opportunity",
                                recommended_official_url,
                                use_container_width=True
                            )

                else:

                    with rec_action2:

                        if recommended_official_url:

                            st.link_button(
                                "View Official Opportunity",
                                recommended_official_url,
                                use_container_width=True
                            )


# ============================================================
# DEADLINE CALENDAR
# ============================================================

elif page == "Deadline Calendar":

    render_page_header(
        "Deadline Calendar",
        "Track upcoming STEM program and application deadlines in one place."
    )

    st.info(
        "Dates come from the STEM Pathways NYC opportunities database. "
        "Always confirm the final deadline on the official program website before submitting."
    )

    st.divider()

    if opportunities.empty:

        st.warning(
            "The opportunities database is currently unavailable."
        )

    else:

        # ----------------------------------------------------
        # HELPERS
        # ----------------------------------------------------

        def parse_deadline_value(value):

            if value is not None:

                try:

                    if "closed" in str(value).lower():
                        return None

                except Exception:
                    pass

            return parse_confirmed_deadline(
                value
            )


        def deadline_status(
            deadline_dt,
            today_dt
        ):

            days_left = (
                deadline_dt.date()
                -
                today_dt.date()
            ).days

            if days_left < 0:
                return "Closed", days_left

            if days_left == 0:
                return "Due Today", days_left

            if days_left <= 7:
                return "Due Soon", days_left

            if days_left <= 30:
                return "This Month", days_left

            return "Upcoming", days_left


        def format_deadline_date(
            deadline_dt
        ):

            return deadline_dt.strftime(
                "%B %d, %Y"
            ).replace(
                " 0",
                " "
            )


        now_local = datetime.now(
            timezone.utc
        )

        # ----------------------------------------------------
        # SAVED APPLICATIONS
        # ----------------------------------------------------

        saved_items = load_saved_opportunities(
            user_sub
        )

        saved_names = {
            str(
                item.get(
                    "opportunity_name",
                    ""
                )
            )
            for item in saved_items
        }

        # ----------------------------------------------------
        # BUILD DEADLINE DATA
        # ----------------------------------------------------

        deadline_rows = []

        for _, opportunity in opportunities.iterrows():

            deadline_dt = parse_deadline_value(
                opportunity.get(
                    "deadline"
                )
            )

            if deadline_dt is None:
                continue

            # Make timezone-naive dates safe to compare.
            if deadline_dt.tzinfo is None:

                compare_deadline = deadline_dt.replace(
                    tzinfo=timezone.utc
                )

            else:

                compare_deadline = deadline_dt.astimezone(
                    timezone.utc
                )

            status, days_left = deadline_status(
                compare_deadline,
                now_local
            )

            deadline_rows.append(
                {
                    "name":
                        str(
                            opportunity.get(
                                "name",
                                "Opportunity"
                            )
                        ),

                    "organization":
                        str(
                            opportunity.get(
                                "organization",
                                ""
                            )
                        ),

                    "type":
                        str(
                            opportunity.get(
                                "opportunity_type",
                                ""
                            )
                        ),

                    "fields":
                        str(
                            opportunity.get(
                                "fields",
                                ""
                            )
                        ),

                    "deadline":
                        compare_deadline,

                    "deadline_text":
                        format_deadline_date(
                            compare_deadline
                        ),

                    "days_left":
                        days_left,

                    "status":
                        status,

                    "saved":
                        str(
                            opportunity.get(
                                "name",
                                ""
                            )
                        )
                        in saved_names,

                    "url":
                        safe_http_url(
                            opportunity.get(
                                "url"
                            )
                        )
                        or
                        "",

                    "cost":
                        str(
                            opportunity.get(
                                "cost",
                                ""
                            )
                        ),

                    "application_status":
                        str(
                            opportunity.get(
                                "application_status",
                                ""
                            )
                        )
                }
            )

        deadline_rows.sort(
            key=lambda item:
                item["deadline"]
        )

        # ----------------------------------------------------
        # FILTERS
        # ----------------------------------------------------

        st.header(
            "Find Upcoming Deadlines"
        )

        filter_col1, filter_col2, filter_col3 = (
            st.columns(3)
        )

        with filter_col1:

            calendar_view = st.selectbox(
                "Show",
                [
                    "Upcoming deadlines",
                    "My saved opportunities",
                    "All dated opportunities",
                    "Past deadlines"
                ],
                key="deadline_calendar_view"
            )

        with filter_col2:

            type_options = sorted(
                {
                    item["type"]
                    for item in deadline_rows
                    if item["type"]
                }
            )

            selected_types = st.multiselect(
                "Opportunity type",
                type_options,
                key="deadline_calendar_types"
            )

        with filter_col3:

            field_filter = st.text_input(
                "Search field or keyword",
                placeholder="Engineering, AI, research...",
                key="deadline_calendar_search"
            )

        filtered_deadlines = []

        for item in deadline_rows:

            if (
                calendar_view
                ==
                "Upcoming deadlines"
                and
                item["days_left"] < 0
            ):
                continue

            if (
                calendar_view
                ==
                "My saved opportunities"
                and
                not item["saved"]
            ):
                continue

            if (
                calendar_view
                ==
                "Past deadlines"
                and
                item["days_left"] >= 0
            ):
                continue

            if (
                selected_types
                and
                item["type"]
                not in selected_types
            ):
                continue

            if field_filter.strip():

                search_text = (
                    item["name"]
                    +
                    " "
                    +
                    item["organization"]
                    +
                    " "
                    +
                    item["fields"]
                ).lower()

                if (
                    field_filter.strip().lower()
                    not in search_text
                ):
                    continue

            filtered_deadlines.append(
                item
            )

        # ----------------------------------------------------
        # SNAPSHOT
        # ----------------------------------------------------

        upcoming_only = [
            item
            for item in deadline_rows
            if item["days_left"] >= 0
        ]

        due_30 = [
            item
            for item in upcoming_only
            if item["days_left"] <= 30
        ]

        saved_upcoming = [
            item
            for item in upcoming_only
            if item["saved"]
        ]

        snapshot1, snapshot2, snapshot3, snapshot4 = (
            st.columns(4)
        )

        with snapshot1:

            st.metric(
                "Upcoming",
                len(
                    upcoming_only
                )
            )

        with snapshot2:

            st.metric(
                "Next 30 Days",
                len(
                    due_30
                )
            )

        with snapshot3:

            st.metric(
                "Saved With Deadlines",
                len(
                    saved_upcoming
                )
            )

        with snapshot4:

            if upcoming_only:

                st.metric(
                    "Next Deadline",
                    upcoming_only[0][
                        "deadline"
                    ].strftime(
                        "%b %d"
                    )
                )

            else:

                st.metric(
                    "Next Deadline",
                    "None listed"
                )

        st.divider()

        # ----------------------------------------------------
        # MONTHLY GROUPED CALENDAR
        # ----------------------------------------------------

        if not filtered_deadlines:

            st.info(
                "No deadlines match the filters you selected."
            )

        else:

            month_groups = {}

            for item in filtered_deadlines:

                month_key = (
                    item["deadline"].strftime(
                        "%Y-%m"
                    )
                )

                month_groups.setdefault(
                    month_key,
                    []
                ).append(
                    item
                )

            for month_key, month_items in month_groups.items():

                month_label = (
                    month_items[0][
                        "deadline"
                    ].strftime(
                        "%B %Y"
                    )
                )

                st.header(
                    month_label
                )

                for item in month_items:

                    with st.container(
                        border=True
                    ):

                        title_col, countdown_col = (
                            st.columns(
                                [4, 1]
                            )
                        )

                        with title_col:

                            st.subheader(
                                item['name']
                            )

                            st.caption(
                                f"{item['organization']} • {item['type']}"
                            )

                        with countdown_col:

                            if item["days_left"] < 0:

                                st.metric(
                                    "Status",
                                    "Closed"
                                )

                            elif item["days_left"] == 0:

                                st.metric(
                                    "Time Left",
                                    "Today"
                                )

                            elif item["days_left"] == 1:

                                st.metric(
                                    "Time Left",
                                    "1 day"
                                )

                            else:

                                st.metric(
                                    "Time Left",
                                    f"{item['days_left']} days"
                                )

                        details1, details2, details3 = (
                            st.columns(3)
                        )

                        with details1:

                            st.write(
                                f"**Deadline:** "
                                f"{item['deadline_text']}"
                            )

                        with details2:

                            st.write(
                                f"**Status:** "
                                f"{item['status']}"
                            )

                        with details3:

                            st.write(
                                f"**Cost:** "
                                f"{item['cost']}"
                            )

                        if item[
                            "application_status"
                        ]:

                            st.caption(
                                f"Program note: "
                                f"{item['application_status']}"
                            )

                        if item["fields"]:

                            st.write(
                                "**Fields:** "
                                +
                                item["fields"]
                            )

                        deadline_calendar_url = google_calendar_deadline_url(
                            item["name"],
                            item["deadline"],
                            item.get(
                                "url",
                                ""
                            ),
                            item.get(
                                "organization",
                                ""
                            )
                        )

                        if deadline_calendar_url:

                            action1, action2, action3 = (
                                st.columns(3)
                            )

                        else:

                            action1, action2 = (
                                st.columns(2)
                            )

                        with action1:

                            if not item["saved"]:

                                if st.button(
                                    "Save to My Applications",
                                    key=f"calendar_save_{item['name']}_{item['deadline_text']}",
                                    use_container_width=True
                                ):

                                    if save_opportunity(
                                        user_sub,
                                        item["name"]
                                    ):

                                        st.success(
                                            "Saved to My Applications."
                                        )

                                        st.rerun()

                            else:

                                st.success(
                                    "Saved in My Applications"
                                )

                        if deadline_calendar_url:

                            with action2:

                                st.link_button(
                                    "Add to Google Calendar",
                                    deadline_calendar_url,
                                    use_container_width=True
                                )

                            with action3:

                                if item["url"]:

                                    st.link_button(
                                        "View Official Program",
                                        item["url"],
                                        use_container_width=True
                                    )

                        else:

                            with action2:

                                if item["url"]:

                                    st.link_button(
                                        "View Official Program",
                                        item["url"],
                                        use_container_width=True
                                    )

                st.divider()

        # ----------------------------------------------------
        # UNDATED PROGRAMS
        # ----------------------------------------------------

        undated_count = len(
            opportunities
        ) - len(
            deadline_rows
        )

        if undated_count > 0:

            with st.expander(
                f"{undated_count} opportunities do not yet have a specific date"
            ):

                st.write(
                    "Some programs have future cycles, rolling dates, or deadlines "
                    "that have not yet been announced. They remain available on the "
                    "Opportunities page and should be checked on their official websites."
                )

        st.caption(
            "Deadline information may change. STEM Pathways NYC helps organize dates, "
            "but the official program website is always the final source."
        )





# ============================================================
# COLLEGE SUGGESTIONS
# ============================================================

elif page == "College Suggestions":

    render_page_header(
        "College & Major Discovery",
        (
            "Answer a few simple questions about what you enjoy. "
            "STEM Pathways NYC will suggest fields, majors, and colleges "
            "that may be worth exploring."
        )
    )

    st.info(
        "Match score measures how well a college fits your interests and preferences. "
        "It is NOT your chance of admission."
    )

    st.divider()

    # --------------------------------------------------------
    # SIMPLE INTEREST QUESTIONS
    # --------------------------------------------------------

    st.header("1. Explore What You Might Like")

    q1 = st.multiselect(
        "What kinds of things sound interesting to you?",
        [
            "Building or fixing things",
            "Computers and technology",
            "Coding or making apps",
            "Robots and electronics",
            "Math and solving puzzles",
            "Science and experiments",
            "Medicine and the human body",
            "Nature, climate, and the environment",
            "Working with data and patterns",
            "Designing or creating new things",
            "I'm not sure yet"
        ],
        key="college_discovery_interests_v2"
    )

    q2 = st.selectbox(
        "Which school subject do you enjoy most?",
        [
            "I'm not sure",
            "Math",
            "Science",
            "Computer Science / Technology",
            "Biology",
            "Physics",
            "A mix of math and science"
        ],
        key="college_discovery_subject_v2"
    )

    q3 = st.selectbox(
        "What type of work sounds most enjoyable?",
        [
            "I'm not sure",
            "Building something with my hands",
            "Working on a computer",
            "Solving difficult problems",
            "Designing new products or systems",
            "Running experiments or doing research",
            "Helping people through science or technology",
            "Analyzing information and finding patterns"
        ],
        key="college_discovery_work_v2"
    )

    q4 = st.selectbox(
        "Would you rather work mostly with...",
        [
            "I'm not sure",
            "Hardware, machines, or physical objects",
            "Software and computers",
            "People and healthcare",
            "Numbers and data",
            "Science and research",
            "The environment",
            "A mix of hardware and software"
        ],
        key="college_discovery_environment_v2"
    )

    q5 = st.select_slider(
        "How much do you enjoy math?",
        options=[
            "Not much",
            "A little",
            "It's okay",
            "I like it",
            "I really like it"
        ],
        value="It's okay",
        key="college_discovery_math_v2"
    )

    # --------------------------------------------------------
    # OPTIONAL COLLEGE PREFERENCES
    # --------------------------------------------------------

    with st.expander("2. College Preferences (optional)"):

        college_location = st.selectbox(
            "Where would you be interested in going to college?",
            [
                "I'm open to anywhere",
                "NYC / close to home",
                "Northeast U.S.",
                "Anywhere in the U.S."
            ],
            key="college_discovery_location_v2"
        )

        college_setting = st.selectbox(
            "What kind of college environment sounds best?",
            [
                "I'm not sure",
                "City / urban",
                "Traditional college campus",
                "Small college",
                "Large university"
            ],
            key="college_discovery_setting_v2"
        )

        research_priority = st.checkbox(
            "Research opportunities are important to me",
            value=True,
            key="college_discovery_research_v2"
        )

        aid_priority = st.checkbox(
            "Financial aid / affordability is very important to me",
            value=bool(profile.get("financial_support", False)),
            key="college_discovery_aid_v2"
        )

    # --------------------------------------------------------
    # FIELD DISCOVERY SCORING
    # --------------------------------------------------------

    field_scores = {
        "Engineering": 0,
        "Electrical Engineering": 0,
        "Mechanical Engineering": 0,
        "Computer Engineering": 0,
        "Computer Science": 0,
        "Artificial Intelligence": 0,
        "Data Science": 0,
        "Biomedical Engineering": 0,
        "Biology": 0,
        "Physics": 0,
        "Mathematics": 0,
        "Environmental Science": 0,
        "Robotics": 0
    }

    def add_points(fields, points):
        for field in fields:
            if field in field_scores:
                field_scores[field] += points

    for answer in q1:
        if answer == "Building or fixing things":
            add_points(["Mechanical Engineering", "Engineering", "Robotics"], 5)
        elif answer == "Computers and technology":
            add_points(["Computer Science", "Computer Engineering", "Artificial Intelligence"], 5)
        elif answer == "Coding or making apps":
            add_points(["Computer Science", "Artificial Intelligence", "Data Science"], 6)
        elif answer == "Robots and electronics":
            add_points(["Robotics", "Electrical Engineering", "Computer Engineering"], 6)
        elif answer == "Math and solving puzzles":
            add_points(["Mathematics", "Physics", "Data Science", "Engineering"], 5)
        elif answer == "Science and experiments":
            add_points(["Biology", "Physics", "Biomedical Engineering", "Environmental Science"], 5)
        elif answer == "Medicine and the human body":
            add_points(["Biomedical Engineering", "Biology"], 6)
        elif answer == "Nature, climate, and the environment":
            add_points(["Environmental Science", "Biology"], 6)
        elif answer == "Working with data and patterns":
            add_points(["Data Science", "Artificial Intelligence", "Mathematics"], 6)
        elif answer == "Designing or creating new things":
            add_points(["Engineering", "Mechanical Engineering", "Robotics"], 5)

    subject_map = {
        "Math": ["Mathematics", "Data Science", "Engineering", "Physics"],
        "Science": ["Biology", "Physics", "Environmental Science", "Biomedical Engineering"],
        "Computer Science / Technology": ["Computer Science", "Computer Engineering", "Artificial Intelligence", "Robotics"],
        "Biology": ["Biology", "Biomedical Engineering", "Environmental Science"],
        "Physics": ["Physics", "Electrical Engineering", "Mechanical Engineering", "Engineering"],
        "A mix of math and science": ["Engineering", "Biomedical Engineering", "Physics", "Data Science"]
    }

    add_points(subject_map.get(q2, []), 4)

    work_map = {
        "Building something with my hands": ["Mechanical Engineering", "Robotics", "Engineering"],
        "Working on a computer": ["Computer Science", "Artificial Intelligence", "Data Science", "Computer Engineering"],
        "Solving difficult problems": ["Mathematics", "Physics", "Engineering", "Computer Science"],
        "Designing new products or systems": ["Mechanical Engineering", "Electrical Engineering", "Computer Engineering", "Engineering"],
        "Running experiments or doing research": ["Biology", "Physics", "Biomedical Engineering", "Environmental Science"],
        "Helping people through science or technology": ["Biomedical Engineering", "Biology", "Engineering"],
        "Analyzing information and finding patterns": ["Data Science", "Artificial Intelligence", "Mathematics"]
    }

    add_points(work_map.get(q3, []), 4)

    environment_map = {
        "Hardware, machines, or physical objects": ["Mechanical Engineering", "Electrical Engineering", "Robotics"],
        "Software and computers": ["Computer Science", "Artificial Intelligence", "Data Science"],
        "People and healthcare": ["Biomedical Engineering", "Biology"],
        "Numbers and data": ["Data Science", "Mathematics", "Artificial Intelligence"],
        "Science and research": ["Physics", "Biology", "Environmental Science"],
        "The environment": ["Environmental Science", "Biology"],
        "A mix of hardware and software": ["Computer Engineering", "Robotics", "Electrical Engineering"]
    }

    add_points(environment_map.get(q4, []), 4)

    math_points = {
        "Not much": 0,
        "A little": 1,
        "It's okay": 2,
        "I like it": 3,
        "I really like it": 4
    }[q5]

    add_points(
        [
            "Engineering",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Computer Engineering",
            "Computer Science",
            "Artificial Intelligence",
            "Data Science",
            "Physics",
            "Mathematics",
            "Robotics"
        ],
        math_points
    )

    # --------------------------------------------------------
    # COLLEGE DATABASE
    # --------------------------------------------------------

    college_catalog = [
        {
            "name": "MIT",
            "location": "Cambridge, MA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Physics", "Mathematics", "Robotics"
            ],
            "admit_rate": 4.5,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://ir.mit.edu/projects/2024-25-common-data-set/",
            "research": True
        },
        {
            "name": "Stanford University",
            "location": "Stanford, CA",
            "region": "West",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Data Science",
                "Biomedical Engineering", "Biology", "Physics", "Mathematics", "Robotics"
            ],
            "admit_rate": 3.8,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://irds.stanford.edu/data-findings/cds",
            "research": True
        },
        {
            "name": "Carnegie Mellon University",
            "location": "Pittsburgh, PA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Computer Engineering",
                "Computer Science", "Artificial Intelligence", "Data Science",
                "Mathematics", "Robotics"
            ],
            "admit_rate": 11.1,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.cmu.edu/ira/CDS/",
            "research": True
        },
        {
            "name": "UC Berkeley",
            "location": "Berkeley, CA",
            "region": "West",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Data Science",
                "Biomedical Engineering", "Biology", "Physics", "Mathematics",
                "Environmental Science"
            ],
            "admit_rate": 11.0,
            "rate_label": "2026 first-year overall",
            "source_url": "https://admissions.berkeley.edu/apply-to-berkeley/student-profile/",
            "research": True
        },
        {
            "name": "Georgia Tech",
            "location": "Atlanta, GA",
            "region": "South",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Physics", "Mathematics", "Robotics"
            ],
            "admit_rate": 13.3,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://irp.gatech.edu/files/CDS/CDS_2025-2026_FINAL_R4_03JUN2026.pdf",
            "research": True
        },
        {
            "name": "University of Michigan",
            "location": "Ann Arbor, MI",
            "region": "Midwest",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Physics", "Mathematics",
                "Environmental Science", "Robotics"
            ],
            "admit_rate": 16.4,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://obp.umich.edu/wp-content/uploads/pubdata/factsfigures/firstyearsprofile_umaa_2025.pdf",
            "research": True
        },
        {
            "name": "Purdue University",
            "location": "West Lafayette, IN",
            "region": "Midwest",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Physics", "Mathematics", "Robotics"
            ],
            "admit_rate": 49.9,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.purdue.edu/idata/wp-content/uploads/2025/06/CDS_2024-2025.pdf",
            "research": True
        },
        {
            "name": "Cornell University",
            "location": "Ithaca, NY",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science", "Robotics"
            ],
            "admit_rate": 7.9,
            "rate_label": "Fall 2023 overall",
            "source_url": "https://irp.cornell.edu/common-data-set",
            "research": True
        },
        {
            "name": "Columbia University",
            "location": "New York, NY",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science"
            ],
            "admit_rate": 3.9,
            "rate_label": "Class of 2027 overall",
            "source_url": "https://undergrad.admissions.columbia.edu/",
            "research": True
        },
        {
            "name": "Princeton University",
            "location": "Princeton, NJ",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Small",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Physics",
                "Mathematics", "Biology", "Environmental Science"
            ],
            "admit_rate": 4.4,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://profile.princeton.edu/admission-and-costs",
            "research": True
        },
        {
            "name": "Harvard University",
            "location": "Cambridge, MA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science"
            ],
            "admit_rate": 4.2,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://college.harvard.edu/admissions/admissions-statistics",
            "research": True
        },
        {
            "name": "Duke University",
            "location": "Durham, NC",
            "region": "South",
            "setting": "Traditional college campus",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Data Science",
                "Biomedical Engineering", "Biology", "Mathematics"
            ],
            "admit_rate": 5.2,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://admissions.duke.edu/",
            "research": True
        },
        {
            "name": "Johns Hopkins University",
            "location": "Baltimore, MD",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science"
            ],
            "admit_rate": 6.4,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://oira.jhu.edu/wp-content/uploads/CDS_2024-2025_JHU-2.pdf",
            "research": True
        },
        {
            "name": "Caltech",
            "location": "Pasadena, CA",
            "region": "West",
            "setting": "Small college",
            "size": "Small",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Artificial Intelligence", "Physics",
                "Mathematics", "Biology"
            ],
            "admit_rate": 3.1,
            "rate_label": "Fall 2023 overall",
            "source_url": "https://iro.caltech.edu/",
            "research": True
        },
        {
            "name": "The Cooper Union",
            "location": "New York, NY",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Small",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering"
            ],
            "admit_rate": 13.0,
            "rate_label": "2024-25 overall",
            "source_url": "https://cooper.edu/admissions/faq",
            "research": True
        },
        {
            "name": "NYU Tandon",
            "location": "Brooklyn, NY",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Robotics"
            ],
            "admit_rate": 13.0,
            "rate_label": "NYU university-wide",
            "source_url": "https://bulletins.nyu.edu/nyu/enrollment-graduation-statistics/",
            "research": True
        },
        {
            "name": "Stevens Institute of Technology",
            "location": "Hoboken, NJ",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Physics", "Mathematics",
                "Robotics"
            ],
            "admit_rate": 51.0,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.stevens.edu/discover-stevens/stevens-by-the-numbers/facts-statistics",
            "research": True
        },
        {
            "name": "CCNY",
            "location": "New York, NY",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Biomedical Engineering",
                "Biology", "Physics", "Mathematics", "Environmental Science"
            ],
            "admit_rate": 60.0,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.ccny.cuny.edu/sites/default/files/2025-03/20250324_FINAL%20CDS-2024-2025.pdf",
            "research": True
        },
        {
            "name": "Stony Brook University",
            "location": "Stony Brook, NY",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Biology", "Physics",
                "Mathematics", "Environmental Science"
            ],
            "admit_rate": 48.2,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.stonybrook.edu/irpe/factbook/common-data-set.html",
            "research": True
        },
        {
            "name": "CUNY City Tech",
            "location": "Brooklyn, NY",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Data Science",
                "Mathematics", "Physics"
            ],
            "admit_rate": 80.3,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.citytech.cuny.edu/consumer-info/",
            "research": True
        },
        {
            "name": "UMass Lowell",
            "location": "Lowell, MA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Artificial Intelligence",
                "Data Science", "Biomedical Engineering", "Physics", "Mathematics",
                "Robotics"
            ],
            "admit_rate": 83.0,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.uml.edu/docs/CDS_2024-2025%20Final_tcm18-403507.pdf",
            "research": True
        },
        {
            "name": "Western New England University",
            "location": "Springfield, MA",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Data Science",
                "Biomedical Engineering", "Mathematics"
            ],
            "admit_rate": 83.5,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://wne.edu/institutional-research/doc/WNE-CDS-2024-25-FINAL.pdf",
            "research": True
        },
        {
            "name": "UMass Boston",
            "location": "Boston, MA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Large",
            "fields": [
                "Computer Science", "Data Science", "Mathematics", "Physics"
            ],
            "admit_rate": 85.5,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.umb.edu/media/umassboston/editor-uploads/institutional-research-assessment-planning/TABLE7-Undergraduate--Admissions.pdf",
            "research": True
        },
        {
            "name": "Wentworth Institute of Technology",
            "location": "Boston, MA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Data Science",
                "Biomedical Engineering", "Mathematics", "Robotics"
            ],
            "admit_rate": 87.8,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://wit.edu/sites/default/files/2026-02/Common%20Data%20Set%202025-2026%20%281%29.pdf",
            "research": True
        },
        {
            "name": "University of New Hampshire",
            "location": "Durham, NH",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Data Science",
                "Biomedical Engineering", "Physics", "Mathematics", "Environmental Science"
            ],
            "admit_rate": 88.2,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.unh.edu/institutional-research/sites/default/files/media/2025-07/CDS-2024-2025_7.18.25.pdf",
            "research": True
        },
        {
            "name": "UMass Dartmouth",
            "location": "Dartmouth, MA",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Large",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Data Science",
                "Biomedical Engineering", "Physics", "Mathematics"
            ],
            "admit_rate": 90.6,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.umassd.edu/media/umassdartmouth/institutional-research/Data_Book_Fall24_Final-v2_6.26.25.pdf",
            "research": True
        },
        {
            "name": "Wilkes University",
            "location": "Wilkes-Barre, PA",
            "region": "Northeast",
            "setting": "City / urban",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Science", "Data Science", "Physics", "Mathematics",
                "Environmental Science"
            ],
            "admit_rate": 94.0,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.wilkes.edu/about-wilkes/offices-and-administration/institutional-research/_assets/fact-book-2025-26.pdf",
            "research": True
        },
        {
            "name": "University of Pittsburgh at Johnstown",
            "location": "Johnstown, PA",
            "region": "Northeast",
            "setting": "Traditional college campus",
            "size": "Medium",
            "fields": [
                "Engineering", "Electrical Engineering", "Mechanical Engineering",
                "Computer Engineering", "Computer Science", "Data Science",
                "Mathematics", "Physics"
            ],
            "admit_rate": 94.8,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://ir.pitt.edu/sites/default/files/assets/2024-2025_CDS_Johnstown.pdf",
            "research": True
        }
    ]

    # --------------------------------------------------------
    # COMPETITIVENESS
    # --------------------------------------------------------

    def competitiveness_from_rate(rate):
        return college_selectivity_from_acceptance_rate(rate)

    def college_list_category(stars):
        if stars is None:
            return None
        if stars >= 4:
            return "Reach"
        if stars >= 2:
            return "Target"
        if stars == 1:
            return "Safety"
        return None

    def college_category_display_label(category):
        return {
            "Reach": "🎯 REACH",
            "Target": "✅ TARGET",
            "Safety": "🛡️ SAFETY"
        }.get(category, category)

    # --------------------------------------------------------
    # PERSONALIZED COLLEGE MATCH
    # --------------------------------------------------------

    def college_match_score(college, top_fields):

        score = 0
        max_score = 100
        reasons = []

        # Field fit: up to 50 points
        field_points = 0

        for rank, (field, field_score) in enumerate(top_fields, start=1):
            if field in college["fields"]:
                bonus = max(22 - ((rank - 1) * 5), 7)
                field_points += bonus

        field_points = min(field_points, 50)
        score += field_points

        if field_points >= 35:
            reasons.append("Very strong match with your top STEM interests.")
        elif field_points >= 20:
            reasons.append("Good match with several of your STEM interests.")

        # Location fit: up to 20 points
        if college_location == "NYC / close to home":
            if college["location"] in ["New York, NY", "Brooklyn, NY", "Hoboken, NJ"]:
                score += 20
                reasons.append("Matches your preference to stay in or near NYC.")
            elif college["region"] == "Northeast":
                score += 10

        elif college_location == "Northeast U.S.":
            if college["region"] == "Northeast":
                score += 20
                reasons.append("Matches your Northeast location preference.")

        elif college_location in ["I'm open to anywhere", "Anywhere in the U.S."]:
            score += 12

        # Campus setting: up to 15 points
        if college_setting == "I'm not sure":
            score += 8
        elif college_setting == college["setting"]:
            score += 15
            reasons.append("Matches the type of college environment you selected.")
        elif (
            college_setting == "Large university"
            and college["size"] == "Large"
        ):
            score += 15
        elif (
            college_setting == "Small college"
            and college["size"] == "Small"
        ):
            score += 15
        else:
            score += 4

        # Research: up to 10 points
        if research_priority:
            if college.get("research"):
                score += 10
                reasons.append("Offers a strong research-oriented environment.")
        else:
            score += 5

        # Affordability preference: 5 points for local public-ish option,
        # otherwise do not pretend to know individualized net price.
        if aid_priority:
            if college["name"] in ["CCNY", "Stony Brook University"]:
                score += 5
                reasons.append("May be worth exploring as a lower-cost public option.")
        else:
            score += 5

        return min(round(score), max_score), reasons

    if st.button(
        "Discover My Best-Fit Colleges",
        type="primary",
        use_container_width=True
    ):

        ranked_fields = sorted(
            field_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_fields = ranked_fields[:4]

        results = []

        for college in college_catalog:
            match_score, reasons = college_match_score(
                college,
                top_fields
            )

            stars, competitive_label = competitiveness_from_rate(
                college["admit_rate"]
            )

            results.append({
                "college": college,
                "match_score": match_score,
                "reasons": reasons,
                "stars": stars,
                "competitive_label": competitive_label
            })

        results.sort(
            key=lambda item: item["match_score"],
            reverse=True
        )

        st.session_state["college_discovery_results_v3"] = top_fields
        st.session_state["college_match_results_v3"] = results
        st.rerun()

    discovery_results = st.session_state.get(
        "college_discovery_results_v3"
    )

    college_results = st.session_state.get(
        "college_match_results_v3"
    )

    if discovery_results and college_results:

        st.divider()

        st.header("Your Top STEM Directions")

        top_field_score = max(
            discovery_results[0][1],
            1
        )

        field_columns = st.columns(4)

        for index, (field, score) in enumerate(discovery_results):

            with field_columns[index]:

                with st.container(border=True):

                    st.subheader(
                        f"#{index + 1}"
                    )

                    st.write(
                        f"**{field}**"
                    )

                    relative = round(
                        (score / top_field_score) * 100
                    )

                    st.metric(
                        "Interest Match",
                        f"{relative}%"
                    )

        st.divider()

        st.header("Best College Matches")

        st.write(
            "Colleges are scored first by how well they match your STEM interests "
            "and preferences. Your strongest matches are then grouped as "
            "**Reach**, **Target**, or **Safety** using selectivity stars. "
            "Within each group, schools are ranked by your personalized **match score**."
        )

        def college_has_intended_field(result):
            college_fields = result["college"].get("fields", [])
            return any(
                field in college_fields
                for field, _
                in discovery_results
            )

        def is_strong_personalized_match(result):
            if not college_has_intended_field(result):
                return False
            return result.get("match_score", 0) >= 40

        def render_college_match_card(
            result,
            rank,
            category,
            category_key
        ):
            college = result["college"]
            match_score = result["match_score"]
            reasons = result["reasons"]
            stars, competitive_label = competitiveness_from_rate(
                college.get("admit_rate")
            )

            with st.container(border=True):

                st.subheader(
                    f"{rank}. {college['name']}"
                )

                st.caption(
                    f"{college['location']} • {college['setting']} • {college['size']}"
                )

                category_label = college_category_display_label(
                    category
                )
                category_label_key = (
                    "college_category_label_"
                    f"{category_key}_{rank}_"
                    + re.sub(
                        r"[^A-Za-z0-9]+",
                        "_",
                        str(college["name"])
                    )
                )

                with st.container(
                    key=category_label_key
                ):
                    st.markdown(
                        category_label
                    )

                info1, info2, info3, info4 = st.columns(4)

                with info1:

                    if college["admit_rate"] is not None:

                        admit_rate_value = (
                            f"{college['admit_rate']:.1f}%"
                        )

                    else:

                        admit_rate_value = "See source"

                    admit_rate_caption = ""

                    if college.get("rate_label"):

                        admit_rate_caption = (
                            '<div class="college-plain-stat-caption">'
                            + html_module.escape(
                                str(college["rate_label"])
                            )
                            + "</div>"
                        )

                    st.markdown(
                        '<div class="college-plain-stat">'
                        '<div class="college-plain-stat-label">'
                        "Recent Admit Rate"
                        "</div>"
                        '<div class="college-plain-stat-value">'
                        f"{admit_rate_value}"
                        "</div>"
                        f"{admit_rate_caption}"
                        "</div>",
                        unsafe_allow_html=True
                    )

                with info2:

                    if stars is not None:

                        star_display = (
                            (
                                '<span class="college-competition-star-filled">'
                                "★"
                                "</span>"
                            ) * stars
                            +
                            (
                                '<span class="college-competition-star-empty">'
                                "☆"
                                "</span>"
                            ) * (5 - stars)
                        )

                        competition_caption = (
                            '<div class="college-plain-stat-caption">'
                            + html_module.escape(
                                str(competitive_label)
                            )
                            + "</div>"
                        )

                        st.markdown(
                            '<div class="college-plain-stat">'
                            '<div class="college-plain-stat-label">'
                            "Competition"
                            "</div>"
                            '<div class="college-plain-stat-value">'
                            f"{star_display}"
                            "</div>"
                            f"{competition_caption}"
                            "</div>",
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            '<div class="college-plain-stat">'
                            '<div class="college-plain-stat-label">'
                            "Competition"
                            "</div>"
                            '<div class="college-plain-stat-value">'
                            "Not rated"
                            "</div>"
                            "</div>",
                            unsafe_allow_html=True
                        )

                with info3:

                    matching_fields = [
                        field
                        for field, _
                        in discovery_results
                        if field in college["fields"]
                    ]

                    if matching_fields:
                        matching_fields_value = " • ".join(
                            matching_fields[:4]
                        )
                    else:
                        matching_fields_value = "General STEM option"

                    st.markdown(
                        '<div class="college-plain-stat">'
                        '<div class="college-plain-stat-label">'
                        "Matching fields"
                        "</div>"
                        '<div class="college-plain-stat-body">'
                        + html_module.escape(
                            matching_fields_value
                        )
                        + "</div>"
                        "</div>",
                        unsafe_allow_html=True
                    )

                with info4:

                    st.markdown(
                        '<div class="college-plain-stat">'
                        '<div class="college-plain-stat-label">'
                        "Your Match"
                        "</div>"
                        '<div class="college-plain-stat-value">'
                        f"{match_score}%"
                        "</div>"
                        "</div>",
                        unsafe_allow_html=True
                    )

                with st.expander(
                    "Why this school matches you"
                ):

                    if reasons:
                        for reason in reasons:
                            st.write(
                                f"• {reason}"
                            )
                    else:
                        st.write(
                            "This school is included as a STEM option "
                            "but has fewer direct matches with your current answers."
                        )

                favorite_action1, favorite_action2 = st.columns(2)

                with favorite_action1:

                    if st.button(
                        "Save College",
                        key=(
                            f"favorite_college_{category_key}_"
                            f"{rank}_{college['name']}"
                        ),
                        width="stretch"
                    ):

                        if add_favorite_college(
                            user_sub,
                            college["name"]
                        ):

                            st.success(
                                "College saved to My Favorite Colleges."
                            )

                with favorite_action2:

                    college_source_url = safe_http_url(
                        college.get(
                            "source_url"
                        )
                    )

                    if college_source_url:

                        st.link_button(
                            "View Admissions / Data Source",
                            college_source_url,
                            width="stretch"
                        )

        grouped_matches = {
            "Reach": [],
            "Target": [],
            "Safety": []
        }

        for result in college_results:

            if not is_strong_personalized_match(result):
                continue

            stars, _ = competitiveness_from_rate(
                result["college"].get("admit_rate")
            )
            category = college_list_category(stars)

            if category:
                grouped_matches[category].append(result)

        category_sections = [
            (
                "Reach",
                "reach",
                "🎯 Reach Schools",
                "Your strongest-matching colleges with 4–5 selectivity stars.",
                7,
                None
            ),
            (
                "Target",
                "target",
                "✅ Target Schools",
                "Your strongest-matching colleges with 2–3 selectivity stars.",
                7,
                None
            ),
            (
                "Safety",
                "safety",
                "🛡️ Safety Schools",
                "Your strongest-matching colleges with 1 selectivity star.",
                6,
                (
                    "We need more colleges in our database that match "
                    "your interests and have higher admission rates."
                )
            )
        ]

        for (
            category,
            category_key,
            section_title,
            section_caption,
            max_schools,
            empty_message
        ) in category_sections:

            section_results = grouped_matches[category][
                :max_schools
            ]

            st.subheader(section_title)

            st.write(section_caption)

            if section_results:

                for rank, result in enumerate(
                    section_results,
                    start=1
                ):

                    render_college_match_card(
                        result,
                        rank,
                        category,
                        category_key
                    )

            elif empty_message:

                st.info(empty_message)

            else:

                st.write(
                    "No strong matches in this category for your "
                    "current interests and preferences."
                )

        st.divider()

        st.caption(
            "Important: admit rates are recent institution- or school-level figures "
            "where official data was available. Some colleges admit by school or residency, "
            "so a single percentage may not describe every applicant. Competitiveness stars "
            "are a STEM Pathways NYC category based on the displayed admit rate. "
            "Match score reflects your interests and preferences only — it is not an admission chance."
        )


# ============================================================
# MY FAVORITE COLLEGES
# ============================================================

elif page == "My Favorite Colleges":

    render_page_header(
        "My Favorite Colleges",
        (
            "Build your own college list, keep the schools you like, "
            "and arrange them in your personal order."
        )
    )

    st.info(
        "Your favorite order is based on your personal preferences. "
        "The competitiveness rating and admission data are informational "
        "and do not predict your individual chance of admission."
    )

    st.divider()

    # --------------------------------------------------------
    # COLLEGE DETAILS USED IN FAVORITES
    # --------------------------------------------------------

    favorite_college_catalog = {
        "MIT": {
            "location": "Cambridge, MA",
            "admit_rate": 4.5,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://ir.mit.edu/projects/2024-25-common-data-set/"
        },
        "Stanford University": {
            "location": "Stanford, CA",
            "admit_rate": 3.8,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://irds.stanford.edu/data-findings/cds"
        },
        "Carnegie Mellon University": {
            "location": "Pittsburgh, PA",
            "admit_rate": 11.1,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.cmu.edu/ira/CDS/"
        },
        "UC Berkeley": {
            "location": "Berkeley, CA",
            "admit_rate": 11.0,
            "rate_label": "2026 first-year overall",
            "source_url": "https://admissions.berkeley.edu/apply-to-berkeley/student-profile/"
        },
        "Georgia Tech": {
            "location": "Atlanta, GA",
            "admit_rate": 13.3,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://irp.gatech.edu/files/CDS/CDS_2025-2026_FINAL_R4_03JUN2026.pdf"
        },
        "University of Michigan": {
            "location": "Ann Arbor, MI",
            "admit_rate": 16.4,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://obp.umich.edu/wp-content/uploads/pubdata/factsfigures/firstyearsprofile_umaa_2025.pdf"
        },
        "Purdue University": {
            "location": "West Lafayette, IN",
            "admit_rate": 49.9,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.purdue.edu/idata/wp-content/uploads/2025/06/CDS_2024-2025.pdf"
        },
        "Cornell University": {
            "location": "Ithaca, NY",
            "admit_rate": 7.9,
            "rate_label": "Fall 2023 overall",
            "source_url": "https://irp.cornell.edu/common-data-set"
        },
        "Columbia University": {
            "location": "New York, NY",
            "admit_rate": 3.9,
            "rate_label": "Class of 2027 overall",
            "source_url": "https://undergrad.admissions.columbia.edu/"
        },
        "Princeton University": {
            "location": "Princeton, NJ",
            "admit_rate": 4.4,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://profile.princeton.edu/admission-and-costs"
        },
        "Harvard University": {
            "location": "Cambridge, MA",
            "admit_rate": 4.2,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://college.harvard.edu/admissions/admissions-statistics"
        },
        "Duke University": {
            "location": "Durham, NC",
            "admit_rate": 5.2,
            "rate_label": "Class of 2029 overall",
            "source_url": "https://admissions.duke.edu/"
        },
        "Johns Hopkins University": {
            "location": "Baltimore, MD",
            "admit_rate": 6.4,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://oira.jhu.edu/wp-content/uploads/CDS_2024-2025_JHU-2.pdf"
        },
        "Caltech": {
            "location": "Pasadena, CA",
            "admit_rate": 3.1,
            "rate_label": "Fall 2023 overall",
            "source_url": "https://iro.caltech.edu/"
        },
        "The Cooper Union": {
            "location": "New York, NY",
            "admit_rate": 13.0,
            "rate_label": "2024-25 overall",
            "source_url": "https://cooper.edu/admissions/faq"
        },
        "NYU Tandon": {
            "location": "Brooklyn, NY",
            "admit_rate": 13.0,
            "rate_label": "NYU university-wide",
            "source_url": "https://bulletins.nyu.edu/nyu/enrollment-graduation-statistics/"
        },
        "Stevens Institute of Technology": {
            "location": "Hoboken, NJ",
            "admit_rate": 51.0,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.stevens.edu/discover-stevens/stevens-by-the-numbers/facts-statistics"
        },
        "CCNY": {
            "location": "New York, NY",
            "admit_rate": 60.0,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.ccny.cuny.edu/sites/default/files/2025-03/20250324_FINAL%20CDS-2024-2025.pdf"
        },
        "Stony Brook University": {
            "location": "Stony Brook, NY",
            "admit_rate": 48.2,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.stonybrook.edu/irpe/factbook/common-data-set.html"
        },
        "CUNY City Tech": {
            "location": "Brooklyn, NY",
            "admit_rate": 80.3,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.citytech.cuny.edu/consumer-info/"
        },
        "UMass Lowell": {
            "location": "Lowell, MA",
            "admit_rate": 83.0,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.uml.edu/docs/CDS_2024-2025%20Final_tcm18-403507.pdf"
        },
        "Western New England University": {
            "location": "Springfield, MA",
            "admit_rate": 83.5,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://wne.edu/institutional-research/doc/WNE-CDS-2024-25-FINAL.pdf"
        },
        "UMass Boston": {
            "location": "Boston, MA",
            "admit_rate": 85.5,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.umb.edu/media/umassboston/editor-uploads/institutional-research-assessment-planning/TABLE7-Undergraduate--Admissions.pdf"
        },
        "Wentworth Institute of Technology": {
            "location": "Boston, MA",
            "admit_rate": 87.8,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://wit.edu/sites/default/files/2026-02/Common%20Data%20Set%202025-2026%20%281%29.pdf"
        },
        "University of New Hampshire": {
            "location": "Durham, NH",
            "admit_rate": 88.2,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.unh.edu/institutional-research/sites/default/files/media/2025-07/CDS-2024-2025_7.18.25.pdf"
        },
        "UMass Dartmouth": {
            "location": "Dartmouth, MA",
            "admit_rate": 90.6,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://www.umassd.edu/media/umassdartmouth/institutional-research/Data_Book_Fall24_Final-v2_6.26.25.pdf"
        },
        "Wilkes University": {
            "location": "Wilkes-Barre, PA",
            "admit_rate": 94.0,
            "rate_label": "Fall 2025 overall",
            "source_url": "https://www.wilkes.edu/about-wilkes/offices-and-administration/institutional-research/_assets/fact-book-2025-26.pdf"
        },
        "University of Pittsburgh at Johnstown": {
            "location": "Johnstown, PA",
            "admit_rate": 94.8,
            "rate_label": "Fall 2024 overall",
            "source_url": "https://ir.pitt.edu/sites/default/files/assets/2024-2025_CDS_Johnstown.pdf"
        }
    }

    def favorite_competitiveness(rate):
        return college_selectivity_from_acceptance_rate(rate)

    # Recover the most recent personalized college matches from this session.
    last_match_lookup = {}

    for result in st.session_state.get(
        "college_match_results_v3",
        []
    ):

        college_info = result.get(
            "college",
            {}
        )

        college_name = college_info.get(
            "name"
        )

        if college_name:

            last_match_lookup[
                college_name
            ] = result.get(
                "match_score"
            )

    favorite_colleges = load_favorite_colleges(
        user_sub
    )

    if not favorite_colleges:

        st.header(
            "Your favorites list is empty"
        )

        st.write(
            "Go to **College Suggestions** and click "
            "**Save College** on schools you want to remember."
        )

        if st.button(
            "Explore College Suggestions",
            type="primary",
            use_container_width=True
        ):

            st.session_state.current_page = (
                "College Suggestions"
            )

            st.rerun()

    else:

        st.header(
            "Your Ranked College List"
        )

        st.caption(
            "Use the arrows to move schools up or down. "
            "#1 is currently your favorite."
        )

        for index, favorite in enumerate(
            favorite_colleges,
            start=1
        ):

            favorite_id = favorite[
                "id"
            ]

            college_name = favorite[
                "college_name"
            ]

            college_info = (
                favorite_college_catalog.get(
                    college_name,
                    {}
                )
            )

            admit_rate = (
                college_info.get(
                    "admit_rate"
                )
            )

            stars, competition_label = (
                favorite_competitiveness(
                    admit_rate
                )
            )

            personal_match = (
                last_match_lookup.get(
                    college_name
                )
            )

            with st.container(
                border=True
            ):

                title_col, rank_col = (
                    st.columns(
                        [4, 1]
                    )
                )

                with title_col:

                    st.subheader(
                        college_name
                    )

                    if college_info.get(
                        "location"
                    ):

                        st.caption(
                            college_info[
                                "location"
                            ]
                        )

                with rank_col:

                    st.metric(
                        "Your Rank",
                        f"#{index}"
                    )

                stat1, stat2, stat3 = (
                    st.columns(3)
                )

                with stat1:

                    if admit_rate is not None:

                        st.metric(
                            "Recent Admit Rate",
                            f"{admit_rate:.1f}%"
                        )

                    else:

                        st.metric(
                            "Recent Admit Rate",
                            "See source"
                        )

                    if college_info.get(
                        "rate_label"
                    ):

                        st.caption(
                            college_info[
                                "rate_label"
                            ]
                        )

                with stat2:

                    if stars is not None:

                        star_display = (
                            "★" * stars
                            +
                            "☆" * (
                                5 - stars
                            )
                        )

                        st.metric(
                            "Competition",
                            star_display
                        )

                        st.caption(
                            competition_label
                        )

                    else:

                        st.metric(
                            "Competition",
                            "Not rated"
                        )

                with stat3:

                    if personal_match is not None:

                        st.metric(
                            "Your Last Match",
                            f"{personal_match}%"
                        )

                        st.caption(
                            "Fit score, not admission chance"
                        )

                    else:

                        st.metric(
                            "Your Last Match",
                            "Run discovery"
                        )

                        st.caption(
                            "Use College Suggestions to calculate your fit"
                        )

                notes_value = st.text_area(
                    "Why do you like this school? (optional)",
                    value=(
                        favorite.get(
                            "notes",
                            ""
                        )
                        or
                        ""
                    ),
                    placeholder=(
                        "Example: Strong Computer Engineering, "
                        "close to NYC, research opportunities..."
                    ),
                    key=f"favorite_college_notes_{favorite_id}"
                )

                move_col1, move_col2, save_col, remove_col = (
                    st.columns(4)
                )

                with move_col1:

                    if st.button(
                        "Move Up",
                        key=f"favorite_up_{favorite_id}",
                        disabled=(
                            index == 1
                        ),
                        use_container_width=True
                    ):

                        if reorder_favorite_colleges(
                            user_sub,
                            favorite_id,
                            "up"
                        ):

                            st.rerun()

                with move_col2:

                    if st.button(
                        "Move Down",
                        key=f"favorite_down_{favorite_id}",
                        disabled=(
                            index
                            ==
                            len(
                                favorite_colleges
                            )
                        ),
                        use_container_width=True
                    ):

                        if reorder_favorite_colleges(
                            user_sub,
                            favorite_id,
                            "down"
                        ):

                            st.rerun()

                with save_col:

                    if st.button(
                        "Save Notes",
                        key=f"favorite_save_notes_{favorite_id}",
                        use_container_width=True
                    ):

                        if update_favorite_college_notes(
                            user_sub,
                            favorite_id,
                            notes_value
                        ):

                            st.success(
                                "Notes saved."
                            )

                with remove_col:

                    if st.button(
                        "Remove",
                        key=f"favorite_remove_{favorite_id}",
                        use_container_width=True
                    ):

                        st.session_state[
                            "confirm_remove_favorite_college"
                        ] = favorite_id

                if safe_http_url(
                    college_info.get(
                        "source_url"
                    )
                ):

                    st.link_button(
                        "View Admissions / Data Source",
                        safe_http_url(
                            college_info.get(
                                "source_url"
                            )
                        ),
                        use_container_width=True
                    )

                if (
                    st.session_state.get(
                        "confirm_remove_favorite_college"
                    )
                    ==
                    favorite_id
                ):

                    st.warning(
                        f"Remove {college_name} from your favorites?"
                    )

                    confirm_col1, confirm_col2 = (
                        st.columns(2)
                    )

                    with confirm_col1:

                        if st.button(
                            "Yes, Remove",
                            key=f"favorite_confirm_remove_{favorite_id}",
                            use_container_width=True
                        ):

                            if remove_favorite_college(
                                user_sub,
                                favorite_id
                            ):

                                st.session_state.pop(
                                    "confirm_remove_favorite_college",
                                    None
                                )

                                st.rerun()

                    with confirm_col2:

                        if st.button(
                            "Cancel",
                            key=f"favorite_cancel_remove_{favorite_id}",
                            use_container_width=True
                        ):

                            st.session_state.pop(
                                "confirm_remove_favorite_college",
                                None
                            )

                            st.rerun()

        st.divider()

        st.caption(
            "Tip: Your favorites can change as you learn more. "
            "Move schools whenever your priorities change. "
            "Admission rates and competitiveness categories are informational only."
        )


# ============================================================
# MY APPLICATIONS
# ============================================================

elif page == "My Applications":

    render_page_header(
        "My Applications",
        (
            "Save opportunities you are interested in and track your "
            "progress from discovery through the application process."
        )
    )

    st.info(
        "Your tracker is private to your signed-in account. "
        "Saving an opportunity does not submit an application."
    )

    st.divider()

    saved_items = load_saved_opportunities(
        user_sub
    )

    if not saved_items:

        st.header(
            "No saved opportunities yet"
        )

        st.write(
            "Go to the Opportunities page and select "
            "**Save Opportunity** on any program you want to track."
        )

        if st.button(
            "Explore Opportunities",
            type="primary",
            use_container_width=True
        ):

            st.session_state.current_page = (
                "Opportunities"
            )

            st.rerun()

    else:

        # ----------------------------------------------------
        # APPLICATION SNAPSHOT
        # ----------------------------------------------------

        st.header(
            "Application Snapshot"
        )

        total_saved = len(
            saved_items
        )

        applied_count = sum(
            1
            for item in saved_items
            if item.get("status")
            in [
                "Applied",
                "Accepted",
                "Waitlisted",
                "Not Selected"
            ]
        )

        accepted_count = sum(
            1
            for item in saved_items
            if item.get("status")
            == "Accepted"
        )

        planning_count = sum(
            1
            for item in saved_items
            if item.get("status")
            in [
                "Planning to Apply",
                "Applying"
            ]
        )

        metric1, metric2, metric3, metric4 = (
            st.columns(4)
        )

        with metric1:

            st.metric(
                "Saved",
                total_saved
            )

        with metric2:

            st.metric(
                "Planning / Applying",
                planning_count
            )

        with metric3:

            st.metric(
                "Submitted",
                applied_count
            )

        with metric4:

            st.metric(
                "Accepted",
                accepted_count
            )

        st.divider()

        # ----------------------------------------------------
        # STATUS FILTER
        # ----------------------------------------------------

        filter_status = st.multiselect(
            "Filter by application status",
            APPLICATION_STATUSES,
            default=[]
        )

        filtered_items = [
            item
            for item in saved_items
            if (
                not filter_status
                or
                item.get(
                    "status",
                    "Saved"
                )
                in filter_status
            )
        ]

        for saved_item in filtered_items:

            saved_name = str(
                saved_item.get(
                    "opportunity_name",
                    "Saved Opportunity"
                )
            )

            current_status = (
                saved_item.get(
                    "status",
                    "Saved"
                )
                or
                "Saved"
            )

            current_notes = (
                saved_item.get(
                    "notes",
                    ""
                )
                or
                ""
            )

            opportunity_match = (
                opportunities[
                    opportunities[
                        "name"
                    ]
                    .astype(str)
                    == saved_name
                ]
                if (
                    not opportunities.empty
                    and
                    "name"
                    in opportunities.columns
                )
                else pd.DataFrame()
            )

            with st.container(
                border=True
            ):

                st.subheader(
                    saved_name
                )

                if not opportunity_match.empty:

                    opportunity_data = (
                        opportunity_match.iloc[0]
                    )

                    st.caption(
                        str(
                            opportunity_data.get(
                                "organization",
                                ""
                            )
                        )
                    )

                    top1, top2, top3 = (
                        st.columns(3)
                    )

                    with top1:

                        st.write(
                            f"**Type:** "
                            f"{opportunity_data.get('opportunity_type', 'Not listed')}"
                        )

                    with top2:

                        st.write(
                            f"**Cost:** "
                            f"{opportunity_data.get('cost', 'Not listed')}"
                        )

                    with top3:

                        if (
                            "selectivity"
                            in opportunity_data.index
                            and
                            pd.notna(
                                opportunity_data[
                                    "selectivity"
                                ]
                            )
                        ):

                            try:

                                stars = (
                                    "★"
                                    * int(
                                        opportunity_data[
                                            "selectivity"
                                        ]
                                    )
                                    +
                                    "☆"
                                    * (
                                        5
                                        -
                                        int(
                                            opportunity_data[
                                                "selectivity"
                                            ]
                                        )
                                    )
                                )

                                st.write(
                                    f"**Selectivity:** {stars}"
                                )

                            except Exception:

                                pass

                    if (
                        "deadline"
                        in opportunity_data.index
                        and
                        pd.notna(
                            opportunity_data[
                                "deadline"
                            ]
                        )
                    ):

                        st.write(
                            f"**Deadline:** "
                            f"{opportunity_data['deadline']}"
                        )

                    if (
                        "application_status"
                        in opportunity_data.index
                        and
                        pd.notna(
                            opportunity_data[
                                "application_status"
                            ]
                        )
                    ):

                        st.write(
                            f"**Program status:** "
                            f"{opportunity_data['application_status']}"
                        )

                st.divider()

                status_col, notes_col = (
                    st.columns(
                        [1, 2]
                    )
                )

                with status_col:

                    selected_status = st.selectbox(
                        "Application Status",
                        APPLICATION_STATUSES,
                        index=(
                            APPLICATION_STATUSES.index(
                                current_status
                            )
                            if current_status
                            in APPLICATION_STATUSES
                            else 0
                        ),
                        key=f"application_status_{saved_item['id']}"
                    )

                with notes_col:

                    selected_notes = st.text_area(
                        "Notes",
                        value=current_notes,
                        placeholder=(
                            "Example: Ask teacher for recommendation, "
                            "finish essay, request transcript..."
                        ),
                        key=f"application_notes_{saved_item['id']}"
                    )

                action1, action2, action3 = (
                    st.columns(
                        [1, 1, 1]
                    )
                )

                with action1:

                    if st.button(
                        "Save Changes",
                        key=f"save_tracker_{saved_item['id']}",
                        type="primary",
                        use_container_width=True
                    ):

                        if update_saved_opportunity(
                            user_sub,
                            saved_item["id"],
                            selected_status,
                            selected_notes
                        ):

                            st.success(
                                "Application tracker updated."
                            )

                            st.rerun()

                with action2:

                    if not opportunity_match.empty:

                        opportunity_url = safe_http_url(
                            opportunity_match.iloc[0].get(
                                "url"
                            )
                        )

                        if opportunity_url:

                            st.link_button(
                                "Official Website",
                                opportunity_url,
                                use_container_width=True
                            )

                with action3:

                    if st.button(
                        "Remove",
                        key=f"remove_tracker_{saved_item['id']}",
                        use_container_width=True
                    ):

                        st.session_state[
                            "confirm_remove_saved_id"
                        ] = saved_item[
                            "id"
                        ]

                if (
                    st.session_state.get(
                        "confirm_remove_saved_id"
                    )
                    ==
                    saved_item[
                        "id"
                    ]
                ):

                    st.warning(
                        "Remove this opportunity from My Applications?"
                    )

                    confirm1, confirm2 = (
                        st.columns(2)
                    )

                    with confirm1:

                        if st.button(
                            "Yes, Remove",
                            key=f"confirm_remove_{saved_item['id']}",
                            use_container_width=True
                        ):

                            if delete_saved_opportunity(
                                user_sub,
                                saved_item["id"]
                            ):

                                st.session_state.pop(
                                    "confirm_remove_saved_id",
                                    None
                                )

                                st.rerun()

                    with confirm2:

                        if st.button(
                            "Cancel",
                            key=f"cancel_remove_{saved_item['id']}",
                            use_container_width=True
                        ):

                            st.session_state.pop(
                                "confirm_remove_saved_id",
                                None
                            )

                            st.rerun()





# ============================================================
# PROJECTS
# ============================================================

elif page == "Projects":

    render_page_header(
        "Project Explorer",
        (
            "Not sure what to build? Tell us what sounds interesting and "
            "we'll suggest hands-on STEM projects that match what you want to create."
        )
    )

    st.divider()

    # --------------------------------------------------------
    # PROJECT DATABASE
    # --------------------------------------------------------

    project_catalog = [
        {
            "title": "Smart Room Lighting System",
            "fields": ["Electrical Engineering", "Computer Engineering", "Robotics"],
            "create": ["A physical device", "Something that makes everyday life easier", "Something with lights or electronics"],
            "level": "Beginner",
            "time": "1–2 weeks",
            "hours": "5–10 hours",
            "style": ["Building with my hands", "Coding", "Testing and experimenting"],
            "equipment": ["Computer", "Arduino / microcontroller", "Breadboard / basic electronics"],
            "cost": "Low",
            "description": "Build a lighting system that reacts automatically to the amount of light in a room.",
            "skills": ["Circuits", "Sensors", "Arduino", "C/C++", "Prototyping"],
            "materials": ["Arduino-compatible board", "Photoresistor", "LEDs", "Resistors", "Breadboard", "Jumper wires"],
            "steps": [
                "Learn how a photoresistor changes with light.",
                "Build and test the sensor circuit.",
                "Read sensor values with the microcontroller.",
                "Program LEDs to react to different light levels.",
                "Test the system in multiple lighting conditions.",
                "Document the final design and what you would improve."
            ],
            "portfolio": "Designed and programmed an automatic lighting prototype using a light sensor, microcontroller, and custom circuit logic."
        },
        {
            "title": "1D LED Pong Game",
            "fields": ["Electrical Engineering", "Computer Engineering", "Computer Science"],
            "create": ["A game", "A physical device", "Something with lights or electronics"],
            "level": "Intermediate",
            "time": "1–2 weeks",
            "hours": "8–15 hours",
            "style": ["Building with my hands", "Coding", "Solving logic problems"],
            "equipment": ["Computer", "Arduino / microcontroller", "Breadboard / basic electronics"],
            "cost": "Low",
            "description": "Create a physical Pong-style game using a row of LEDs, buttons, timing logic, and scoring.",
            "skills": ["Digital logic", "Embedded programming", "Circuit design", "Debugging"],
            "materials": ["Microcontroller", "LEDs", "Push buttons", "Resistors", "Breadboard", "Jumper wires"],
            "steps": [
                "Design the rules and game states.",
                "Wire the LED playing field and buttons.",
                "Program the moving LED.",
                "Add player input and collision timing.",
                "Create scoring and reset logic.",
                "Test difficulty and document the final system."
            ],
            "portfolio": "Built a physical LED Pong game integrating circuit design, player inputs, timing logic, and embedded programming."
        },
        {
            "title": "Mini Smart Home Security System",
            "fields": ["Electrical Engineering", "Computer Engineering", "Cybersecurity", "Robotics"],
            "create": ["A physical device", "Something that makes everyday life easier", "Something with sensors"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Building with my hands", "Coding", "Testing and experimenting"],
            "equipment": ["Computer", "Arduino / microcontroller", "Breadboard / basic electronics"],
            "cost": "Low–Medium",
            "description": "Build a prototype alarm that detects motion or an opened door and triggers an alert.",
            "skills": ["Sensors", "Embedded systems", "Circuit design", "Programming", "System testing"],
            "materials": ["Microcontroller", "Motion or magnetic sensor", "Buzzer", "LED", "Breadboard", "Wires"],
            "steps": [
                "Define what the system should detect.",
                "Test the sensor independently.",
                "Build the alarm circuit.",
                "Program normal and alert states.",
                "Add a reset or arm/disarm feature.",
                "Test false alarms and document improvements."
            ],
            "portfolio": "Developed a sensor-based home security prototype with programmable alarm states and real-world system testing."
        },
        {
            "title": "Reaction-Time Tester",
            "fields": ["Electrical Engineering", "Computer Engineering", "Biomedical Engineering"],
            "create": ["A physical device", "Something related to health or the human body", "Something with lights or electronics"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "3–6 hours",
            "style": ["Building with my hands", "Coding", "Testing and experimenting"],
            "equipment": ["Computer", "Arduino / microcontroller", "Breadboard / basic electronics"],
            "cost": "Low",
            "description": "Build a device that measures how quickly a person reacts after a light turns on.",
            "skills": ["Timing", "Microcontrollers", "Data collection", "Circuits"],
            "materials": ["Microcontroller", "LED", "Button", "Breadboard", "Resistors"],
            "steps": [
                "Create a random delay before the LED turns on.",
                "Wire an LED and response button.",
                "Measure elapsed time after the signal.",
                "Display or record reaction times.",
                "Test multiple users.",
                "Analyze variation in the results."
            ],
            "portfolio": "Designed a microcontroller-based reaction-time tester and collected human response data for analysis."
        },
        {
            "title": "Assistive Grip Device",
            "fields": ["Mechanical Engineering", "Biomedical Engineering", "Engineering"],
            "create": ["A physical device", "Something related to health or the human body", "Something that helps people"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Building with my hands", "Designing in CAD", "Testing and experimenting"],
            "equipment": ["Computer", "CAD software", "3D printer"],
            "cost": "Low–Medium",
            "description": "Design an inexpensive device that makes gripping or holding an everyday object easier.",
            "skills": ["CAD", "Human-centered design", "Prototyping", "Mechanical design", "Iteration"],
            "materials": ["CAD software", "Cardboard or 3D-print material", "Fasteners", "Everyday test objects"],
            "steps": [
                "Choose a specific gripping challenge.",
                "Research existing assistive products.",
                "Sketch several concepts.",
                "Model the best concept in CAD.",
                "Prototype and test it.",
                "Use feedback to create an improved version."
            ],
            "portfolio": "Designed and iterated an assistive mechanical device using human-centered design, CAD, prototyping, and user testing."
        },
        {
            "title": "Rubber-Band Powered Car",
            "fields": ["Mechanical Engineering", "Physics", "Engineering"],
            "create": ["A physical device", "Something that moves", "Something I can build cheaply"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "2–5 hours",
            "style": ["Building with my hands", "Testing and experimenting", "Solving logic problems"],
            "equipment": ["Basic household materials"],
            "cost": "Very Low",
            "description": "Design a small vehicle powered only by stored elastic energy and optimize it for distance.",
            "skills": ["Mechanics", "Energy", "Design iteration", "Measurement"],
            "materials": ["Cardboard", "Rubber bands", "Bottle caps or wheels", "Axles", "Tape"],
            "steps": [
                "Sketch a drivetrain concept.",
                "Build the chassis and axles.",
                "Create the rubber-band drive.",
                "Measure travel distance.",
                "Change one design variable at a time.",
                "Graph your results and identify the best design."
            ],
            "portfolio": "Engineered and optimized a rubber-band powered vehicle through iterative testing and quantitative performance analysis."
        },
        {
            "title": "Robotic Gripper",
            "fields": ["Mechanical Engineering", "Robotics", "Electrical Engineering"],
            "create": ["A robot", "A physical device", "Something that moves"],
            "level": "Advanced",
            "time": "1–2 months",
            "hours": "20+ hours",
            "style": ["Building with my hands", "Designing in CAD", "Coding"],
            "equipment": ["Computer", "Arduino / microcontroller", "CAD software", "3D printer"],
            "cost": "Medium",
            "description": "Design a motorized gripper capable of picking up several differently shaped objects.",
            "skills": ["CAD", "Mechanisms", "Servo control", "Embedded programming", "Iteration"],
            "materials": ["Microcontroller", "Servo motor", "3D printed or laser-cut parts", "Fasteners", "Wires"],
            "steps": [
                "Study common gripper mechanisms.",
                "Define target objects and constraints.",
                "Design the mechanism in CAD.",
                "Fabricate and assemble the gripper.",
                "Program servo movement.",
                "Test grip strength and redesign weak points."
            ],
            "portfolio": "Designed, fabricated, and programmed a robotic gripper using CAD, servo control, and iterative mechanical testing."
        },
        {
            "title": "Personal Portfolio Website",
            "fields": ["Computer Science", "Web Development"],
            "create": ["A website or app", "Something useful for school or my future", "Something creative"],
            "level": "Beginner",
            "time": "1–2 weeks",
            "hours": "5–10 hours",
            "style": ["Coding", "Designing a user experience", "Working mostly on a computer"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Build a personal website that showcases your projects, skills, experiences, and goals.",
            "skills": ["HTML", "CSS", "Web design", "GitHub", "Communication"],
            "materials": ["Computer", "Code editor", "GitHub account"],
            "steps": [
                "Plan the pages and content.",
                "Create the HTML structure.",
                "Style the site with CSS.",
                "Add project cards and an About section.",
                "Make the layout mobile-friendly.",
                "Publish and ask others for feedback."
            ],
            "portfolio": "Designed and deployed a responsive personal portfolio website showcasing technical projects, skills, and experiences."
        },
        {
            "title": "Study Planner Web App",
            "fields": ["Computer Science", "Web Development", "Software Engineering"],
            "create": ["A website or app", "Something useful for school or my future", "Something that helps people"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Coding", "Designing a user experience", "Solving logic problems"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Create an app where students can enter assignments, deadlines, and study goals.",
            "skills": ["Python or JavaScript", "UI design", "Data storage", "Software design"],
            "materials": ["Computer", "Streamlit or web framework", "GitHub"],
            "steps": [
                "Interview students about planning problems.",
                "Choose the minimum useful features.",
                "Build assignment and deadline inputs.",
                "Create a dashboard.",
                "Add saving or persistent storage.",
                "Test with real users and improve the interface."
            ],
            "portfolio": "Developed a student planning web application with deadline tracking, persistent data, and user-centered interface design."
        },
        {
            "title": "Local Opportunity Finder",
            "fields": ["Computer Science", "Data Science", "Software Engineering"],
            "create": ["A website or app", "Something that helps people", "Something useful for school or my future"],
            "level": "Advanced",
            "time": "1–2 months",
            "hours": "20+ hours",
            "style": ["Coding", "Working with data", "Designing a user experience"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Build a searchable tool that helps students discover internships, programs, scholarships, or community resources.",
            "skills": ["Python", "Databases", "Search/filtering", "Product design", "Data cleaning"],
            "materials": ["Computer", "Python", "Database or CSV", "GitHub"],
            "steps": [
                "Define the target student group.",
                "Create a structured opportunity dataset.",
                "Build filters and search.",
                "Add eligibility and deadline fields.",
                "Test recommendations with students.",
                "Document limitations and future improvements."
            ],
            "portfolio": "Built a data-driven opportunity discovery platform with structured filtering and student-focused recommendation features."
        },
        {
            "title": "Movie Recommendation Engine",
            "fields": ["Data Science", "Artificial Intelligence", "Computer Science"],
            "create": ["An AI project", "A website or app", "Something with data"],
            "level": "Intermediate",
            "time": "1–2 weeks",
            "hours": "8–15 hours",
            "style": ["Coding", "Working with data", "Solving logic problems"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Create a program that recommends movies based on genres, ratings, or similarities between users.",
            "skills": ["Python", "Pandas", "Recommendation systems", "Data analysis"],
            "materials": ["Computer", "Python", "Public movie dataset"],
            "steps": [
                "Load and clean a movie dataset.",
                "Explore ratings and genres.",
                "Create a simple recommendation rule.",
                "Build a similarity-based recommender.",
                "Evaluate sample recommendations.",
                "Create a simple interface for users."
            ],
            "portfolio": "Developed a Python recommendation engine using structured movie data, similarity metrics, and interactive user preferences."
        },
        {
            "title": "Image Classification Model",
            "fields": ["Artificial Intelligence", "Computer Science", "Data Science"],
            "create": ["An AI project", "Something with data", "Something creative"],
            "level": "Advanced",
            "time": "2–4 weeks",
            "hours": "15–25 hours",
            "style": ["Coding", "Working with data", "Testing and experimenting"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Train a machine-learning model to recognize categories of images and evaluate where it makes mistakes.",
            "skills": ["Python", "Machine learning", "Model evaluation", "Data preparation"],
            "materials": ["Computer", "Python notebook environment", "Open image dataset"],
            "steps": [
                "Choose a safe public image dataset.",
                "Prepare training and test data.",
                "Build a baseline classifier.",
                "Train and evaluate the model.",
                "Analyze incorrect predictions.",
                "Explain limitations and possible improvements."
            ],
            "portfolio": "Trained and evaluated an image classification model, analyzing prediction errors and model limitations."
        },
        {
            "title": "NYC Data Story",
            "fields": ["Data Science", "Mathematics", "Environmental Science"],
            "create": ["Something with data", "Something that helps my community", "A research project"],
            "level": "Beginner",
            "time": "1–2 weeks",
            "hours": "5–10 hours",
            "style": ["Working with data", "Researching", "Working mostly on a computer"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Use a public NYC dataset to investigate a question about transportation, environment, education, or another community issue.",
            "skills": ["Python", "Data visualization", "Statistics", "Research questions", "Communication"],
            "materials": ["Computer", "Python or spreadsheet software", "NYC Open Data"],
            "steps": [
                "Choose a community question.",
                "Find a relevant public dataset.",
                "Clean the data.",
                "Create at least three visualizations.",
                "Interpret patterns carefully.",
                "Present a conclusion and limitations."
            ],
            "portfolio": "Analyzed a public NYC dataset using Python and data visualization to investigate a community-focused research question."
        },
        {
            "title": "Air Quality Data Dashboard",
            "fields": ["Environmental Science", "Data Science", "Computer Science"],
            "create": ["Something with data", "Something that helps my community", "A website or app"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Coding", "Working with data", "Researching"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Create an interactive dashboard that explores air-quality patterns across locations or time.",
            "skills": ["Python", "Data visualization", "Environmental analysis", "Dashboard design"],
            "materials": ["Computer", "Public air-quality dataset", "Streamlit"],
            "steps": [
                "Choose an air-quality dataset.",
                "Identify useful pollutants and measurements.",
                "Clean and summarize the data.",
                "Build charts and filters.",
                "Add explanations for nontechnical users.",
                "Publish the dashboard and document limitations."
            ],
            "portfolio": "Created an interactive air-quality dashboard using public environmental data, Python, and visual analytics."
        },
        {
            "title": "Plant Growth Experiment",
            "fields": ["Biology", "Environmental Science"],
            "create": ["A research project", "Something involving biology", "Something I can build cheaply"],
            "level": "Beginner",
            "time": "2–4 weeks",
            "hours": "5–10 hours",
            "style": ["Testing and experimenting", "Researching", "Working with data"],
            "equipment": ["Basic household materials"],
            "cost": "Very Low",
            "description": "Design a controlled experiment testing how one environmental variable affects plant growth.",
            "skills": ["Experimental design", "Measurement", "Biology", "Data analysis"],
            "materials": ["Seeds", "Containers", "Growing medium", "Ruler", "Chosen experimental variable"],
            "steps": [
                "Write a testable research question.",
                "Identify independent and dependent variables.",
                "Create control and experimental groups.",
                "Collect measurements consistently.",
                "Graph the results.",
                "Write a conclusion that discusses limitations."
            ],
            "portfolio": "Designed and conducted a controlled plant-growth experiment, collecting and analyzing quantitative biological data."
        },
        {
            "title": "Low-Cost Water Filter Investigation",
            "fields": ["Environmental Science", "Engineering", "Chemistry"],
            "create": ["A research project", "Something that helps my community", "A physical device"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "8–15 hours",
            "style": ["Building with my hands", "Testing and experimenting", "Researching"],
            "equipment": ["Basic household materials"],
            "cost": "Low",
            "description": "Compare safe model filtration materials to study how engineering design changes water clarity. Do not drink filtered test water.",
            "skills": ["Experimental design", "Environmental engineering", "Measurement", "Iteration"],
            "materials": ["Bottles", "Gravel", "Sand", "Filter material", "Prepared non-potable test water"],
            "steps": [
                "Research the purpose of filtration layers.",
                "Define a safe test method.",
                "Build multiple filter designs.",
                "Measure changes in clarity or another safe indicator.",
                "Compare designs.",
                "Explain why filtration alone does not necessarily make water safe to drink."
            ],
            "portfolio": "Investigated low-cost water filtration designs through controlled testing and comparative environmental engineering analysis."
        },
        {
            "title": "Heart-Rate Data Investigation",
            "fields": ["Biomedical Engineering", "Biology", "Data Science"],
            "create": ["Something related to health or the human body", "Something with data", "A research project"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "3–6 hours",
            "style": ["Working with data", "Testing and experimenting", "Researching"],
            "equipment": ["Computer", "Phone sensors / wearable (optional)"],
            "cost": "Free",
            "description": "Explore how heart rate changes during safe everyday activities using your own measurements or a public dataset.",
            "skills": ["Physiology", "Data collection", "Statistics", "Visualization"],
            "materials": ["Timer or wearable", "Computer or spreadsheet"],
            "steps": [
                "Choose a simple question about heart rate.",
                "Create a consistent measurement procedure.",
                "Collect or obtain non-sensitive sample data.",
                "Calculate summary statistics.",
                "Graph the results.",
                "Discuss variation without making medical conclusions."
            ],
            "portfolio": "Conducted a quantitative heart-rate investigation using structured data collection, visualization, and statistical analysis."
        },
        {
            "title": "Bridge Design Challenge",
            "fields": ["Civil Engineering", "Mechanical Engineering", "Physics"],
            "create": ["A physical device", "Something I can build cheaply", "A research project"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "3–6 hours",
            "style": ["Building with my hands", "Testing and experimenting", "Solving logic problems"],
            "equipment": ["Basic household materials"],
            "cost": "Very Low",
            "description": "Design a lightweight model bridge and test how much load it can support.",
            "skills": ["Structures", "Forces", "Engineering design", "Testing"],
            "materials": ["Craft sticks or paper", "Glue or tape", "Weights", "Scale"],
            "steps": [
                "Research basic bridge structures.",
                "Set size and material constraints.",
                "Sketch your design.",
                "Build the bridge.",
                "Test increasing loads safely.",
                "Calculate strength-to-weight performance and redesign."
            ],
            "portfolio": "Designed and load-tested a model bridge, applying structural concepts and iterative engineering optimization."
        },
        {
            "title": "Solar Oven Optimization",
            "fields": ["Environmental Science", "Mechanical Engineering", "Physics"],
            "create": ["A physical device", "Something involving energy", "Something I can build cheaply"],
            "level": "Beginner",
            "time": "Weekend",
            "hours": "3–6 hours",
            "style": ["Building with my hands", "Testing and experimenting", "Working with data"],
            "equipment": ["Basic household materials"],
            "cost": "Very Low",
            "description": "Build a small solar heating device and test how design choices affect temperature.",
            "skills": ["Energy", "Heat transfer", "Experimental design", "Optimization"],
            "materials": ["Cardboard box", "Foil", "Clear covering", "Dark paper", "Thermometer"],
            "steps": [
                "Research heat absorption and reflection.",
                "Build a baseline solar oven.",
                "Measure temperature over time.",
                "Change one design feature.",
                "Compare performance.",
                "Document the most effective design."
            ],
            "portfolio": "Built and optimized a solar heating prototype using experimental data and heat-transfer principles."
        },
        {
            "title": "Interactive Physics Simulator",
            "fields": ["Physics", "Computer Science", "Mathematics"],
            "create": ["A website or app", "Something useful for school or my future", "A simulation"],
            "level": "Intermediate",
            "time": "2–4 weeks",
            "hours": "10–20 hours",
            "style": ["Coding", "Solving logic problems", "Designing a user experience"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Build an interactive simulation for projectile motion, collisions, circuits, or another physics concept.",
            "skills": ["Python", "Physics modeling", "Mathematics", "Visualization"],
            "materials": ["Computer", "Python", "Streamlit or plotting library"],
            "steps": [
                "Choose one physics model.",
                "Write the governing equations.",
                "Verify calculations with sample values.",
                "Build adjustable user inputs.",
                "Visualize the simulated result.",
                "Explain assumptions and limitations."
            ],
            "portfolio": "Developed an interactive physics simulation translating mathematical models into adjustable visual software."
        },
        {
            "title": "Budget Optimization Tool",
            "fields": ["Industrial Engineering", "Data Science", "Mathematics", "Computer Science"],
            "create": ["A website or app", "Something with data", "Something that solves an optimization problem"],
            "level": "Advanced",
            "time": "2–4 weeks",
            "hours": "15–25 hours",
            "style": ["Coding", "Working with data", "Solving logic problems"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Create a tool that allocates a limited budget across competing needs while respecting user-defined constraints.",
            "skills": ["Optimization", "Python", "Linear programming", "Data modeling", "UI design"],
            "materials": ["Computer", "Python", "Optimization library"],
            "steps": [
                "Define a realistic allocation problem.",
                "Identify decision variables and constraints.",
                "Write an objective function.",
                "Implement the optimization model.",
                "Build inputs for different scenarios.",
                "Explain tradeoffs and test edge cases."
            ],
            "portfolio": "Built an optimization tool using mathematical programming to allocate limited resources under real-world constraints."
        },
        {
            "title": "Emergency Response Location Model",
            "fields": ["Industrial Engineering", "Data Science", "Mathematics"],
            "create": ["Something with data", "Something that helps my community", "Something that solves an optimization problem"],
            "level": "Advanced",
            "time": "1–2 months",
            "hours": "20+ hours",
            "style": ["Coding", "Working with data", "Solving logic problems"],
            "equipment": ["Computer"],
            "cost": "Free",
            "description": "Build a simplified model that chooses service locations to improve coverage or response time using public or synthetic data.",
            "skills": ["Operations research", "Optimization", "Python", "Data analysis", "Model assumptions"],
            "materials": ["Computer", "Python", "Public or synthetic location data"],
            "steps": [
                "Define the service-area problem.",
                "Create or clean location data.",
                "Choose a coverage or distance objective.",
                "Implement a simplified optimization model.",
                "Compare multiple scenarios.",
                "Explain ethical limitations and what real deployment would require."
            ],
            "portfolio": "Developed a facility-location optimization model to evaluate service coverage and resource-allocation tradeoffs."
        }
    ]

    # --------------------------------------------------------
    # DISCOVERY QUESTIONS
    # --------------------------------------------------------

    st.header("What do you want to create?")

    create_choices = st.multiselect(
        "Choose anything that sounds exciting.",
        [
            "A physical device",
            "A robot",
            "A game",
            "A website or app",
            "An AI project",
            "Something with data",
            "A research project",
            "Something related to health or the human body",
            "Something involving biology",
            "Something involving energy",
            "Something with sensors",
            "Something with lights or electronics",
            "Something that moves",
            "A simulation",
            "Something that solves an optimization problem",
            "Something that helps people",
            "Something that helps my community",
            "Something that makes everyday life easier",
            "Something useful for school or my future",
            "Something creative",
            "Something I can build cheaply",
            "Surprise me"
        ],
        key="project_create_choices"
    )

    project_field = st.multiselect(
        "Are there any STEM areas you want to explore?",
        [
            "I'm not sure yet",
            "Engineering",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Computer Engineering",
            "Civil Engineering",
            "Industrial Engineering",
            "Biomedical Engineering",
            "Robotics",
            "Computer Science",
            "Software Engineering",
            "Web Development",
            "Artificial Intelligence",
            "Data Science",
            "Cybersecurity",
            "Biology",
            "Environmental Science",
            "Physics",
            "Mathematics",
            "Chemistry"
        ],
        key="project_field_choices"
    )

    project_style = st.multiselect(
        "How would you like to spend most of your time?",
        [
            "Building with my hands",
            "Coding",
            "Working with data",
            "Designing in CAD",
            "Testing and experimenting",
            "Researching",
            "Solving logic problems",
            "Designing a user experience",
            "Working mostly on a computer"
        ],
        key="project_style_choices"
    )

    project_skill = st.selectbox(
        "What is your current skill level?",
        [
            "Beginner — I'm just getting started",
            "Intermediate — I've completed a few projects",
            "Advanced — I'm comfortable building independently"
        ],
        help="This helps prioritize projects that fit your current experience.",
        key="project_skill_choice"
    )

    col1, col2 = st.columns(2)

    with col1:
        project_level = st.selectbox(
            "How challenging should the project be?",
            [
                "Any level",
                "Beginner",
                "Intermediate",
                "Advanced"
            ],
            key="project_level_choice"
        )

    with col2:
        project_time = st.selectbox(
            "How long do you want to work on it?",
            [
                "Any amount of time",
                "Weekend",
                "1–2 weeks",
                "2–4 weeks",
                "1–2 months"
            ],
            key="project_time_choice"
        )

    with st.expander(
        "What equipment do you have? (optional)",
        key="project_equipment_expander"
    ):

        equipment = st.multiselect(
            "Select everything you can access.",
            [
                "Computer",
                "Basic household materials",
                "Arduino / microcontroller",
                "Breadboard / basic electronics",
                "CAD software",
                "3D printer",
                "Raspberry Pi",
                "Phone sensors / wearable (optional)"
            ],
            key="project_equipment_choices"
        )

        budget = st.selectbox(
            "How much would you prefer to spend?",
            [
                "Any budget",
                "Free only",
                "Very low cost",
                "Low cost",
                "Low–Medium is okay",
                "Medium is okay"
            ],
            key="project_budget_choice"
        )

    # --------------------------------------------------------
    # MATCHING
    # --------------------------------------------------------

    def project_match(project):

        score = 0
        reasons = []

        if create_choices:
            overlap = len(
                set(create_choices)
                &
                set(project["create"])
            )

            score += min(
                overlap * 14,
                42
            )

            if overlap:
                reasons.append(
                    "Matches what you said you want to create."
                )

        selected_fields = [
            item
            for item in project_field
            if item != "I'm not sure yet"
        ]

        if selected_fields:
            overlap = len(
                set(selected_fields)
                &
                set(project["fields"])
            )

            score += min(
                overlap * 12,
                30
            )

            if overlap:
                reasons.append(
                    "Connects to STEM fields you want to explore."
                )

        if project_style:
            overlap = len(
                set(project_style)
                &
                set(project["style"])
            )

            score += min(
                overlap * 8,
                24
            )

            if overlap:
                reasons.append(
                    "Fits the way you said you like to work."
                )

        if (
            project_level == "Any level"
            or project_level == project["level"]
        ):
            score += 12

        # Use the student's current experience to favor realistic projects.
        skill_target = {
            "Beginner — I'm just getting started": "Beginner",
            "Intermediate — I've completed a few projects": "Intermediate",
            "Advanced — I'm comfortable building independently": "Advanced"
        }.get(
            project_skill,
            "Beginner"
        )

        level_rank = {
            "Beginner": 1,
            "Intermediate": 2,
            "Advanced": 3
        }

        skill_rank = level_rank.get(
            skill_target,
            1
        )

        project_rank = level_rank.get(
            project["level"],
            1
        )

        if project_rank == skill_rank:
            score += 16
            reasons.append(
                "Matches your current skill level."
            )
        elif project_rank < skill_rank:
            score += 10
            reasons.append(
                "Should be manageable with your current experience."
            )
        elif project_rank == skill_rank + 1:
            score += 3
        else:
            score -= 10

        if (
            project_time == "Any amount of time"
            or project_time == project["time"]
        ):
            score += 10

        if equipment:
            required = set(
                project["equipment"]
            )

            available = set(
                equipment
            )

            equipment_overlap = len(
                required & available
            )

            if required:
                score += round(
                    12
                    *
                    equipment_overlap
                    /
                    len(required)
                )

        # If the user hasn't made many selections yet, keep useful
        # projects visible rather than producing meaningless zeroes.
        if not create_choices:
            score += 10

        if not selected_fields:
            score += 8

        if not project_style:
            score += 6

        return score, reasons

    if st.button(
        "Find Projects for Me",
        type="primary",
        use_container_width=True
    ):

        ranked_projects = []

        for project in project_catalog:

            score, reasons = project_match(
                project
            )

            ranked_projects.append(
                {
                    "project": project,
                    "score": score,
                    "reasons": reasons
                }
            )

        ranked_projects.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        st.session_state[
            "project_recommendations"
        ] = ranked_projects

        st.rerun()

    recommendations = st.session_state.get(
        "project_recommendations"
    )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if recommendations:

        st.divider()

        st.header("Your Best Project Matches")

        st.caption(
            "Projects are ordered by how closely they match your answers. "
            "You can still explore any project that sounds interesting."
        )

        top_score = max(
            recommendations[0]["score"],
            1
        )

        for rank, item in enumerate(
            recommendations[:12],
            start=1
        ):

            project = item["project"]

            relative_match = min(
                round(
                    item["score"]
                    /
                    top_score
                    *
                    100
                ),
                100
            )

            with st.container(
                border=True
            ):

                title_col, match_col = (
                    st.columns(
                        [4, 1]
                    )
                )

                with title_col:

                    st.subheader(
                        f"{rank}. {project['title']}"
                    )

                    st.caption(
                        " • ".join(
                            project["fields"][:3]
                        )
                    )

                with match_col:

                    st.metric(
                        "Project Match",
                        f"{relative_match}%"
                    )

                meta1, meta2, meta3, meta4 = (
                    st.columns(4)
                )

                with meta1:
                    st.write(
                        f"**Level**\n\n{project['level']}"
                    )

                with meta2:
                    st.write(
                        f"**Timeline**\n\n{project['time']}"
                    )

                with meta3:
                    st.write(
                        f"**Workload**\n\n{project['hours']}"
                    )

                with meta4:
                    st.write(
                        f"**Cost**\n\n{project['cost']}"
                    )

                st.write(
                    project["description"]
                )

                st.write(
                    "**Skills you'll build:** "
                    +
                    " • ".join(
                        project["skills"]
                    )
                )

                with st.expander(
                    "See materials and project roadmap"
                ):

                    st.write(
                        "**What you'll need**"
                    )

                    for material in project[
                        "materials"
                    ]:
                        st.write(
                            f"• {material}"
                        )

                    st.write(
                        "**Suggested roadmap**"
                    )

                    for step_number, step in enumerate(
                        project["steps"],
                        start=1
                    ):
                        st.write(
                            f"{step_number}. {step}"
                        )

                    st.write(
                        "**Possible portfolio description**"
                    )

                    st.write(
                        project["portfolio"]
                    )

                if item["reasons"]:

                    st.caption(
                        "Why it matches: "
                        +
                        " ".join(
                            item["reasons"]
                        )
                    )

        st.divider()

        st.info(
            "Next upgrade: students will be able to save a project, press "
            "'Start Project,' track milestones, and move completed projects "
            "into a personal STEM portfolio."
        )

    else:

        st.divider()

        st.header("Examples of What You Can Build")

        example_cols = st.columns(3)

        for index, project in enumerate(
            project_catalog[:6]
        ):

            with example_cols[
                index % 3
            ]:

                with st.container(
                    border=True
                ):

                    st.caption(
                        project["level"]
                    )

                    st.subheader(
                        project["title"]
                    )

                    st.write(
                        project["description"]
                    )

                    st.caption(
                        f"{project['time']} • {project['cost']} cost"
                    )

    st.divider()

    st.caption(
        "STEM Pathways NYC • Explore • Build • Discover"
    )


# ============================================================
# RESOURCES
# ============================================================

elif page == "Resources":

    render_page_header(
        "Resources",
        "Build the skills you need using free and accessible learning resources."
    )

    st.divider()

    resource_row1 = st.columns(2, gap="medium")

    with resource_row1[0]:

        with st.container(
            border=True
        ):

            st.markdown(
                '<div class="sp-info-card"></div>',
                unsafe_allow_html=True
            )

            st.subheader(
                "Programming"
            )

            st.write(
                "Python • GitHub • Web Development • Data Analysis"
            )

            st.caption(
                "Build programming skills that can support software, "
                "data science, AI, and engineering projects."
            )

    with resource_row1[1]:

        with st.container(
            border=True
        ):

            st.markdown(
                '<div class="sp-info-card"></div>',
                unsafe_allow_html=True
            )

            st.subheader(
                "Research"
            )

            st.write(
                "Experimental Design • Data Collection • "
                "Scientific Writing • Analysis"
            )

            st.caption(
                "Learn the fundamentals needed to investigate questions "
                "and communicate scientific findings."
            )

    resource_row2 = st.columns(2, gap="medium")

    with resource_row2[0]:

        with st.container(
            border=True
        ):

            st.markdown(
                '<div class="sp-info-card"></div>',
                unsafe_allow_html=True
            )

            st.subheader(
                "Engineering"
            )

            st.write(
                "CAD • Electronics • Circuit Design • Arduino • Prototyping"
            )

            st.caption(
                "Develop practical engineering skills through design "
                "and hands-on experimentation."
            )

    with resource_row2[1]:

        with st.container(
            border=True
        ):

            st.markdown(
                '<div class="sp-info-card"></div>',
                unsafe_allow_html=True
            )

            st.subheader(
                "Career Exploration"
            )

            st.write(
                "STEM Majors • Engineering Fields • "
                "Research Careers • Technical Careers"
            )

            st.caption(
                "Compare possible majors and careers before deciding "
                "which directions you want to explore further."
            )


# ============================================================
# GPA CALCULATOR & CONVERTER
# ============================================================

elif page == "GPA Calculator":

    # --------------------------------------------------------
    # GPA SESSION STATE + RESET HELPERS
    # --------------------------------------------------------

    if "gpa_calculation_result" not in st.session_state:
        st.session_state.gpa_calculation_result = None

    if "gpa_results_confirmed" not in st.session_state:
        st.session_state.gpa_results_confirmed = False

    if "gpa_show_restart_confirmation" not in st.session_state:
        st.session_state.gpa_show_restart_confirmation = False

    def reset_gpa_tools():
        keys_to_remove = [
            key
            for key in list(st.session_state.keys())
            if key.startswith("gpa_")
        ]

        for key in keys_to_remove:
            del st.session_state[key]

    render_page_header(
        "GPA Calculator & Converter",
        (
            "Estimate your unweighted and weighted GPA, then convert between "
            "a 4.0 scale and a 100-point average."
        )
    )

    st.info(
        "GPA policies vary by high school, college, and university. "
        "Weighted GPA and scale conversions on this page are estimates "
        "for planning purposes, not official transcript calculations."
    )

    st.divider()

    calculator_tab, converter_tab = st.tabs(
        [
            "Course GPA Calculator",
            "GPA Scale Converter"
        ]
    )

    # --------------------------------------------------------
    # COURSE GPA CALCULATOR
    # --------------------------------------------------------

    with calculator_tab:

        st.header(
            "Calculate Your GPA"
        )

        st.write(
            "Enter your courses, letter grades, course levels, and credits. "
            "The calculator will estimate both unweighted and weighted GPA."
        )

        # Dynamic course list: starts with 5 courses and allows up to 15.
        if "gpa_course_ids" not in st.session_state:
            st.session_state.gpa_course_ids = [0, 1, 2, 3, 4]

        if "gpa_next_course_id" not in st.session_state:
            st.session_state.gpa_next_course_id = 5

        course_control_col1, course_control_col2 = st.columns([1, 2])

        with course_control_col1:
            if st.button(
                "Add Course",
                use_container_width=True,
                key="gpa_add_course",
                disabled=len(st.session_state.gpa_course_ids) >= 15
            ):
                new_course_id = st.session_state.gpa_next_course_id
                st.session_state.gpa_course_ids.append(new_course_id)
                st.session_state.gpa_next_course_id += 1
                st.session_state.gpa_results_confirmed = False
                st.rerun()

        with course_control_col2:
            st.caption(
                f"{len(st.session_state.gpa_course_ids)} of 15 courses added"
            )

        if len(st.session_state.gpa_course_ids) >= 15:
            st.info(
                "You reached the 15-course maximum. Remove a course if you want to add a different one."
            )

        grade_points = {
            "A+": 4.0,
            "A": 4.0,
            "A-": 3.7,
            "B+": 3.3,
            "B": 3.0,
            "B-": 2.7,
            "C+": 2.3,
            "C": 2.0,
            "C-": 1.7,
            "D+": 1.3,
            "D": 1.0,
            "F": 0.0
        }

        level_bonus = {
            "Regular": 0.0,
            "Honors": 0.5,
            "AP / IB": 1.0,
            "Dual Enrollment": 1.0
        }

        course_rows = []

        st.markdown(
            "#### Your Courses"
        )

        for display_index, course_id in enumerate(
            list(st.session_state.gpa_course_ids),
            start=1
        ):

            with st.container(
                border=True
            ):

                title_col, remove_col = st.columns([4, 1])

                with title_col:
                    st.caption(
                        f"Course {display_index}"
                    )

                with remove_col:
                    if st.button(
                        "Remove",
                        key=f"gpa_remove_course_{course_id}",
                        use_container_width=True,
                        disabled=len(st.session_state.gpa_course_ids) <= 1
                    ):
                        st.session_state.gpa_course_ids.remove(course_id)

                        for course_key in [
                            f"gpa_course_name_{course_id}",
                            f"gpa_letter_grade_{course_id}",
                            f"gpa_course_level_{course_id}",
                            f"gpa_credits_{course_id}",
                        ]:
                            st.session_state.pop(course_key, None)

                        st.session_state.gpa_calculation_result = None
                        st.session_state.gpa_results_confirmed = False
                        st.rerun()

                name_col, grade_col, level_col, credit_col = st.columns(
                    [2.4, 1, 1.6, 1]
                )

                with name_col:

                    course_name = st.text_input(
                        "Course",
                        value="",
                        placeholder="e.g. AP Biology",
                        key=f"gpa_course_name_{course_id}"
                    )

                with grade_col:

                    letter_grade = st.selectbox(
                        "Grade",
                        list(grade_points.keys()),
                        index=1,
                        key=f"gpa_letter_grade_{course_id}"
                    )

                with level_col:

                    course_level = st.selectbox(
                        "Level",
                        list(level_bonus.keys()),
                        key=f"gpa_course_level_{course_id}"
                    )

                with credit_col:

                    credits = st.number_input(
                        "Credits",
                        min_value=0.25,
                        max_value=4.0,
                        value=1.0,
                        step=0.25,
                        key=f"gpa_credits_{course_id}"
                    )

                course_rows.append(
                    {
                        "name": course_name.strip() or f"Course {display_index}",
                        "grade": letter_grade,
                        "level": course_level,
                        "credits": float(credits)
                    }
                )

        if st.button(
            "Calculate My GPA",
            type="primary",
            use_container_width=True,
            key="gpa_calculate_course_gpa"
        ):

            total_credits = sum(
                course["credits"]
                for course in course_rows
            )

            if total_credits <= 0:

                st.warning(
                    "Please enter at least one course with credits."
                )

            else:

                unweighted_quality_points = sum(
                    grade_points[course["grade"]]
                    * course["credits"]
                    for course in course_rows
                )

                weighted_quality_points = sum(
                    (
                        grade_points[course["grade"]]
                        + level_bonus[course["level"]]
                    )
                    * course["credits"]
                    for course in course_rows
                )

                unweighted_gpa = (
                    unweighted_quality_points
                    / total_credits
                )

                weighted_gpa = (
                    weighted_quality_points
                    / total_credits
                )

                if unweighted_gpa >= 4.0:
                    estimated_100 = "93–100"
                elif unweighted_gpa >= 3.7:
                    estimated_100 = "90–92"
                elif unweighted_gpa >= 3.3:
                    estimated_100 = "87–89"
                elif unweighted_gpa >= 3.0:
                    estimated_100 = "83–86"
                elif unweighted_gpa >= 2.7:
                    estimated_100 = "80–82"
                elif unweighted_gpa >= 2.3:
                    estimated_100 = "77–79"
                elif unweighted_gpa >= 2.0:
                    estimated_100 = "73–76"
                elif unweighted_gpa >= 1.7:
                    estimated_100 = "70–72"
                elif unweighted_gpa >= 1.3:
                    estimated_100 = "67–69"
                elif unweighted_gpa >= 1.0:
                    estimated_100 = "65–66"
                else:
                    estimated_100 = "Below 65"

                calculation_rows = []

                for course in course_rows:

                    base = grade_points[
                        course["grade"]
                    ]

                    weighted = (
                        base
                        + level_bonus[
                            course["level"]
                        ]
                    )

                    calculation_rows.append(
                        {
                            "Course": course["name"],
                            "Grade": course["grade"],
                            "Level": course["level"],
                            "Credits": course["credits"],
                            "Unweighted Points": round(base, 2),
                            "Weighted Points": round(weighted, 2)
                        }
                    )

                st.session_state.gpa_calculation_result = {
                    "unweighted_gpa": unweighted_gpa,
                    "weighted_gpa": weighted_gpa,
                    "estimated_100": estimated_100,
                    "calculation_rows": calculation_rows
                }

                st.session_state.gpa_results_confirmed = False

        if st.session_state.gpa_calculation_result:

            result = st.session_state.gpa_calculation_result

            st.divider()

            st.subheader(
                "Your Estimated Results"
            )

            result_col1, result_col2, result_col3 = st.columns(3)

            with result_col1:

                st.metric(
                    "Unweighted GPA",
                    f"{result['unweighted_gpa']:.2f} / 4.00"
                )

            with result_col2:

                st.metric(
                    "Estimated Weighted GPA",
                    f"{result['weighted_gpa']:.2f}"
                )

            with result_col3:

                st.metric(
                    "Approx. 100-Point Range",
                    result["estimated_100"]
                )

            st.caption(
                "Weighted estimate used here: Regular +0.0, Honors +0.5, "
                "AP/IB +1.0, Dual Enrollment +1.0. Your school may use a different system."
            )

            with st.expander(
                "See course-by-course calculation"
            ):

                st.dataframe(
                    pd.DataFrame(
                        result["calculation_rows"]
                    ),
                    use_container_width=True,
                    hide_index=True
                )

            st.divider()

            if st.session_state.gpa_results_confirmed:

                st.success(
                    "GPA results confirmed. You can still restart the calculator "
                    "below if you want to try different courses or grades."
                )

            else:

                st.write(
                    "If these courses and grades look correct, confirm your results. "
                    "Nothing is saved to your official school record."
                )

                if st.button(
                    "Confirm My GPA Results",
                    type="primary",
                    use_container_width=True,
                    key="gpa_confirm_results"
                ):

                    st.session_state.gpa_results_confirmed = True
                    st.rerun()

    # --------------------------------------------------------
    # GPA SCALE CONVERTER
    # --------------------------------------------------------

    with converter_tab:

        st.header(
            "GPA Scale Converter"
        )

        st.write(
            "Use this tool when you know your GPA on one scale and want an "
            "approximate equivalent on another."
        )

        conversion_direction = st.radio(
            "Convert from",
            [
                "4.0 GPA → 100-Point Scale",
                "100-Point Average → 4.0 GPA"
            ],
            horizontal=True,
            key="gpa_conversion_direction"
        )

        st.divider()

        if conversion_direction == "4.0 GPA → 100-Point Scale":

            four_point_gpa = st.number_input(
                "Enter your GPA on a 4.0 scale",
                min_value=0.0,
                max_value=4.0,
                value=3.50,
                step=0.01,
                format="%.2f",
                key="gpa_four_point_input"
            )

            if four_point_gpa >= 4.0:
                hundred_range = "93–100"
                letter_equivalent = "A / A+"
            elif four_point_gpa >= 3.7:
                hundred_range = "90–92"
                letter_equivalent = "A-"
            elif four_point_gpa >= 3.3:
                hundred_range = "87–89"
                letter_equivalent = "B+"
            elif four_point_gpa >= 3.0:
                hundred_range = "83–86"
                letter_equivalent = "B"
            elif four_point_gpa >= 2.7:
                hundred_range = "80–82"
                letter_equivalent = "B-"
            elif four_point_gpa >= 2.3:
                hundred_range = "77–79"
                letter_equivalent = "C+"
            elif four_point_gpa >= 2.0:
                hundred_range = "73–76"
                letter_equivalent = "C"
            elif four_point_gpa >= 1.7:
                hundred_range = "70–72"
                letter_equivalent = "C-"
            elif four_point_gpa >= 1.3:
                hundred_range = "67–69"
                letter_equivalent = "D+"
            elif four_point_gpa >= 1.0:
                hundred_range = "65–66"
                letter_equivalent = "D"
            else:
                hundred_range = "Below 65"
                letter_equivalent = "F"

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    "Estimated 100-Point Equivalent",
                    hundred_range
                )

            with result_col2:

                st.metric(
                    "Approximate Letter Grade",
                    letter_equivalent
                )

        else:

            hundred_average = st.number_input(
                "Enter your average on a 100-point scale",
                min_value=0.0,
                max_value=100.0,
                value=90.0,
                step=0.1,
                format="%.1f",
                key="gpa_hundred_point_input"
            )

            if hundred_average >= 93:
                converted_gpa = 4.0
                letter_equivalent = "A / A+"
            elif hundred_average >= 90:
                converted_gpa = 3.7
                letter_equivalent = "A-"
            elif hundred_average >= 87:
                converted_gpa = 3.3
                letter_equivalent = "B+"
            elif hundred_average >= 83:
                converted_gpa = 3.0
                letter_equivalent = "B"
            elif hundred_average >= 80:
                converted_gpa = 2.7
                letter_equivalent = "B-"
            elif hundred_average >= 77:
                converted_gpa = 2.3
                letter_equivalent = "C+"
            elif hundred_average >= 73:
                converted_gpa = 2.0
                letter_equivalent = "C"
            elif hundred_average >= 70:
                converted_gpa = 1.7
                letter_equivalent = "C-"
            elif hundred_average >= 67:
                converted_gpa = 1.3
                letter_equivalent = "D+"
            elif hundred_average >= 65:
                converted_gpa = 1.0
                letter_equivalent = "D"
            else:
                converted_gpa = 0.0
                letter_equivalent = "F"

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    "Estimated 4.0 GPA",
                    f"{converted_gpa:.1f} / 4.0"
                )

            with result_col2:

                st.metric(
                    "Approximate Letter Grade",
                    letter_equivalent
                )

        st.divider()

        st.markdown(
            "#### Approximate Conversion Guide"
        )

        conversion_table = pd.DataFrame(
            [
                ["93–100", "A / A+", "4.0"],
                ["90–92", "A-", "3.7"],
                ["87–89", "B+", "3.3"],
                ["83–86", "B", "3.0"],
                ["80–82", "B-", "2.7"],
                ["77–79", "C+", "2.3"],
                ["73–76", "C", "2.0"],
                ["70–72", "C-", "1.7"],
                ["67–69", "D+", "1.3"],
                ["65–66", "D", "1.0"],
                ["Below 65", "F", "0.0"]
            ],
            columns=[
                "100-Point Range",
                "Letter Grade",
                "Approx. 4.0 GPA"
            ]
        )

        st.dataframe(
            conversion_table,
            use_container_width=True,
            hide_index=True
        )

        st.warning(
            "There is no universal official conversion between a 4.0 GPA "
            "and a 100-point average. Colleges may recalculate grades using "
            "their own methods, so use these results only as an estimate."
        )

    # --------------------------------------------------------
    # CONFIRM / RESTART AREA
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Finished?"
    )

    st.write(
        "If you entered something incorrectly or want to test a different set "
        "of grades, you can restart the GPA tools without affecting your profile."
    )

    if not st.session_state.gpa_show_restart_confirmation:

        if st.button(
            "Start Over",
            use_container_width=True,
            key="gpa_restart_request"
        ):

            st.session_state.gpa_show_restart_confirmation = True
            st.rerun()

    else:

        st.warning(
            "Start over? This will clear the courses, grades, calculator results, "
            "and converter inputs on this page."
        )

        restart_col1, restart_col2 = st.columns(2)

        with restart_col1:

            if st.button(
                "Yes, Start Over",
                type="primary",
                use_container_width=True,
                key="gpa_restart_confirm",
                on_click=reset_gpa_tools
            ):
                pass

        with restart_col2:

            if st.button(
                "Cancel",
                use_container_width=True,
                key="gpa_restart_cancel"
            ):

                st.session_state.gpa_show_restart_confirmation = False
                st.rerun()


# ============================================================
# ADMIN DASHBOARD
# ============================================================

elif page == "Admin Dashboard":

    if not is_admin_user(
        user_email
    ):

        st.error(
            "You do not have permission to view this page."
        )

        st.stop()

    render_page_header(
        "Admin Dashboard",
        (
            "Review platform activity, user feedback, and early usage trends "
            "for STEM Pathways NYC."
        )
    )

    st.warning(
        "This dashboard contains user-submitted information. "
        "Use it only to improve the platform and avoid sharing personally identifiable data publicly."
    )

    st.divider()

    admin_data = load_admin_metrics()

    profiles = admin_data[
        "profiles"
    ]

    feedback_rows = admin_data[
        "feedback"
    ]

    saved_rows = admin_data[
        "saved_opportunities"
    ]

    favorite_rows = admin_data[
        "favorite_colleges"
    ]

    # --------------------------------------------------------
    # PLATFORM OVERVIEW
    # --------------------------------------------------------

    st.header(
        "Platform Overview"
    )

    review_count = len(
        feedback_rows
    )

    avg_rating = 0

    if review_count:

        ratings = [
            safe_int(
                row.get(
                    "rating",
                    0
                ),
                0
            )
            for row in feedback_rows
            if row.get(
                "rating"
            )
            is not None
        ]

        if ratings:

            avg_rating = (
                sum(
                    ratings
                )
                /
                len(
                    ratings
                )
            )

    recommend_yes = sum(
        1
        for row in feedback_rows
        if str(
            row.get(
                "would_recommend",
                ""
            )
        ).strip().lower()
        ==
        "yes"
    )

    recommend_rate = (
        round(
            (
                recommend_yes
                /
                review_count
            )
            * 100
        )
        if review_count
        else 0
    )

    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )

    with metric1:

        st.metric(
            "Student Profiles",
            len(
                profiles
            )
        )

    with metric2:

        st.metric(
            "Feedback Responses",
            review_count
        )

    with metric3:

        st.metric(
            "Average Rating",
            (
                f"{avg_rating:.1f} / 5"
                if review_count
                else "No data"
            )
        )

    with metric4:

        st.metric(
            "Would Recommend",
            (
                f"{recommend_rate}%"
                if review_count
                else "No data"
            )
        )

    metric5, metric6 = (
        st.columns(2)
    )

    with metric5:

        st.metric(
            "Saved Opportunities",
            len(
                saved_rows
            )
        )

    with metric6:

        st.metric(
            "Favorite Colleges",
            len(
                favorite_rows
            )
        )

    st.divider()

    # --------------------------------------------------------
    # FEEDBACK ANALYTICS
    # --------------------------------------------------------

    st.header(
        "Feedback Analytics"
    )

    if not feedback_rows:

        st.info(
            "No feedback has been submitted yet."
        )

    else:

        ease_scores = [
            int(
                row.get(
                    "ease_of_use",
                    0
                )
                or 0
            )
            for row in feedback_rows
            if row.get(
                "ease_of_use"
            )
            is not None
        ]

        avg_ease = (
            sum(
                ease_scores
            )
            /
            len(
                ease_scores
            )
            if ease_scores
            else 0
        )

        rating_counts = {
            rating: 0
            for rating in range(
                1,
                6
            )
        }

        for row in feedback_rows:

            try:

                rating_counts[
                    int(
                        row.get(
                            "rating",
                            0
                        )
                    )
                ] += 1

            except Exception:

                pass

        feedback_col1, feedback_col2 = (
            st.columns(2)
        )

        with feedback_col1:

            st.metric(
                "Average Ease of Use",
                f"{avg_ease:.1f} / 5"
            )

            st.markdown(
                "#### Rating Distribution"
            )

            for rating in range(
                5,
                0,
                -1
            ):

                stars = (
                    "★"
                    * rating
                    +
                    "☆"
                    * (
                        5 - rating
                    )
                )

                st.write(
                    f"**{stars}** — "
                    f"{rating_counts[rating]} response(s)"
                )

        with feedback_col2:

            st.markdown(
                "#### Recommendation"
            )

            recommend_counts = {
                "Yes": 0,
                "Maybe": 0,
                "No": 0
            }

            for row in feedback_rows:

                answer = str(
                    row.get(
                        "would_recommend",
                        ""
                    )
                ).strip()

                if answer in recommend_counts:

                    recommend_counts[
                        answer
                    ] += 1

            for answer, count in recommend_counts.items():

                st.write(
                    f"**{answer}:** {count}"
                )

        st.divider()

        # ----------------------------------------------------
        # POPULAR FEATURES
        # ----------------------------------------------------

        st.header(
            "Most Useful Features"
        )

        feature_counts = {}

        for row in feedback_rows:

            features = text_to_list(
                row.get(
                    "favorite_features"
                )
            )

            for feature in features:

                feature_counts[
                    feature
                ] = (
                    feature_counts.get(
                        feature,
                        0
                    )
                    + 1
                )

        if feature_counts:

            feature_rankings = sorted(
                feature_counts.items(),
                key=lambda item:
                    item[1],
                reverse=True
            )

            for rank, (
                feature,
                count
            ) in enumerate(
                feature_rankings,
                start=1
            ):

                st.write(
                    f"**#{rank} {feature}** — "
                    f"{count} vote(s)"
                )

        else:

            st.info(
                "Users have not selected favorite features yet."
            )

        st.divider()

        # ----------------------------------------------------
        # WRITTEN FEEDBACK
        # ----------------------------------------------------

        st.header(
            "Recent Written Feedback"
        )

        sorted_feedback = sorted(
            feedback_rows,
            key=lambda row:
                str(
                    row.get(
                        "updated_at",
                        row.get(
                            "created_at",
                            ""
                        )
                    )
                ),
            reverse=True
        )

        for row in sorted_feedback[:20]:

            rating = int(
                row.get(
                    "rating",
                    0
                )
                or 0
            )

            stars = (
                "★"
                * rating
                +
                "☆"
                * (
                    5 - rating
                )
            )

            with st.container(
                border=True
            ):

                feedback_top1, feedback_top2 = (
                    st.columns(2)
                )

                with feedback_top1:

                    st.write(
                        f"**Rating:** {stars}"
                    )

                with feedback_top2:

                    st.write(
                        f"**Recommend:** "
                        f"{row.get('would_recommend', 'Not answered')}"
                    )

                improvement_text = str(
                    row.get(
                        "improvements",
                        ""
                    )
                    or
                    ""
                ).strip()

                comments_text = str(
                    row.get(
                        "additional_comments",
                        ""
                    )
                    or
                    ""
                ).strip()

                if improvement_text:

                    st.markdown(
                        "**What should improve**"
                    )

                    st.write(
                        improvement_text
                    )

                if comments_text:

                    st.markdown(
                        "**Additional comments**"
                    )

                    st.write(
                        comments_text
                    )

                if (
                    not improvement_text
                    and
                    not comments_text
                ):

                    st.caption(
                        "No written comments submitted."
                    )

    st.divider()

    # --------------------------------------------------------
    # APPLICATION / COLLEGE ACTIVITY
    # --------------------------------------------------------

    st.header(
        "Student Activity"
    )

    application_status_counts = {}

    for row in saved_rows:

        status = str(
            row.get(
                "status",
                "Saved"
            )
        ).strip()

        application_status_counts[
            status
        ] = (
            application_status_counts.get(
                status,
                0
            )
            + 1
        )

    if application_status_counts:

        st.markdown(
            "#### Application Tracker Status"
        )

        for status, count in sorted(
            application_status_counts.items(),
            key=lambda item:
                item[1],
            reverse=True
        ):

            st.write(
                f"**{status}:** {count}"
            )

    else:

        st.info(
            "No saved application activity yet."
        )

    st.divider()

    # --------------------------------------------------------
    # PRIVACY-SAFE EXPORT VIEW
    # --------------------------------------------------------

    with st.expander(
        "View feedback data"
    ):

        if feedback_rows:

            feedback_df = pd.DataFrame(
                feedback_rows
            )

            safe_columns = [
                column
                for column in [
                    "rating",
                    "ease_of_use",
                    "overall_feeling",
                    "favorite_features",
                    "improvements",
                    "additional_comments",
                    "would_recommend",
                    "created_at",
                    "updated_at"
                ]
                if column
                in feedback_df.columns
            ]

            st.dataframe(
                feedback_df[
                    safe_columns
                ],
                use_container_width=True,
                hide_index=True
            )

            csv_export = (
                feedback_df[
                    safe_columns
                ]
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8"
                )
            )

            st.download_button(
                "Download Feedback CSV",
                data=csv_export,
                file_name="stem_pathways_feedback.csv",
                mime="text/csv",
                use_container_width=True
            )

        else:

            st.write(
                "No feedback data available."
            )

    st.caption(
        "Admin dashboard data is intended for product improvement and should be handled responsibly."
    )





# ============================================================
# FEEDBACK
# ============================================================

elif page == "Feedback":

    render_page_header(
        "Share Your Feedback",
        (
            "Help improve STEM Pathways NYC by telling us what worked, "
            "what felt confusing, and what you would like to see next."
        )
    )

    st.info(
        "Your feedback is used to improve the platform. "
        "You can return and update your response later."
    )

    st.divider()

    existing_feedback = load_user_feedback(
        user_sub
    ) or {}

    # --------------------------------------------------------
    # STAR RATING
    # --------------------------------------------------------

    st.header(
        "Overall Experience"
    )

    rating_options = {
        "★☆☆☆☆  1 — Poor": 1,
        "★★☆☆☆  2 — Fair": 2,
        "★★★☆☆  3 — Good": 3,
        "★★★★☆  4 — Very Good": 4,
        "★★★★★  5 — Excellent": 5
    }

    existing_rating = int(
        existing_feedback.get(
            "rating",
            5
        )
        or 5
    )

    default_rating_label = next(
        (
            label
            for label, value
            in rating_options.items()
            if value
            ==
            existing_rating
        ),
        "★★★★★  5 — Excellent"
    )

    rating_label = st.radio(
        "How would you rate STEM Pathways NYC overall?",
        list(
            rating_options.keys()
        ),
        index=list(
            rating_options.keys()
        ).index(
            default_rating_label
        ),
        key="feedback_rating"
    )

    rating = rating_options[
        rating_label
    ]

    st.metric(
        "Your Rating",
        "★" * rating
        +
        "☆" * (
            5 - rating
        )
    )

    # --------------------------------------------------------
    # EASE OF USE / FEELING
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        existing_ease = int(
            existing_feedback.get(
                "ease_of_use",
                4
            )
            or 4
        )

        ease_of_use = st.slider(
            "How easy is the website to use?",
            1,
            5,
            existing_ease,
            help=(
                "1 = very difficult to navigate, "
                "5 = very easy to navigate"
            ),
            key="feedback_ease"
        )

    with col2:

        feeling_options = [
            "I really like it",
            "I like it",
            "It's okay",
            "I'm unsure about it",
            "I don't like it yet"
        ]

        saved_feeling = (
            existing_feedback.get(
                "overall_feeling",
                "I really like it"
            )
            or
            "I really like it"
        )

        overall_feeling = st.selectbox(
            "How do you feel about the website overall?",
            feeling_options,
            index=(
                feeling_options.index(
                    saved_feeling
                )
                if saved_feeling
                in feeling_options
                else 0
            ),
            key="feedback_feeling"
        )

    st.divider()

    # --------------------------------------------------------
    # FAVORITE FEATURES
    # --------------------------------------------------------

    st.header(
        "What Is Working?"
    )

    feature_options = [
        "Dashboard",
        "My STEM Pathway",
        "Career recommendations",
        "Salary information",
        "Opportunities",
        "Deadline Calendar",
        "College Suggestions",
        "College match scores",
        "Favorite Colleges",
        "Application Tracker",
        "Project Explorer",
        "GPA Calculator",
        "Resources",
        "Profile"
    ]

    saved_features = text_to_list(
        existing_feedback.get(
            "favorite_features"
        )
    )

    favorite_features = st.multiselect(
        "Which parts of STEM Pathways NYC have been most useful to you?",
        feature_options,
        default=[
            feature
            for feature
            in saved_features
            if feature
            in feature_options
        ],
        key="feedback_features"
    )

    st.divider()

    # --------------------------------------------------------
    # IMPROVEMENTS
    # --------------------------------------------------------

    st.header(
        "What Should We Improve?"
    )

    improvements = st.text_area(
        "What felt confusing, difficult, missing, or could be better?",
        value=(
            existing_feedback.get(
                "improvements",
                ""
            )
            or
            ""
        ),
        placeholder=(
            "Example: I want more filters for colleges, "
            "the sidebar feels crowded, or I want more beginner projects..."
        ),
        height=140,
        key="feedback_improvements"
    )

    additional_comments = st.text_area(
        "Anything else you want us to know? (optional)",
        value=(
            existing_feedback.get(
                "additional_comments",
                ""
            )
            or
            ""
        ),
        placeholder=(
            "Share ideas, feature requests, or anything you liked."
        ),
        height=120,
        key="feedback_comments"
    )

    recommend_options = [
        "Yes",
        "Maybe",
        "No"
    ]

    saved_recommend = (
        existing_feedback.get(
            "would_recommend",
            "Yes"
        )
        or
        "Yes"
    )

    would_recommend = st.radio(
        "Would you recommend STEM Pathways NYC to another student?",
        recommend_options,
        index=(
            recommend_options.index(
                saved_recommend
            )
            if saved_recommend
            in recommend_options
            else 0
        ),
        horizontal=True,
        key="feedback_recommend"
    )

    st.divider()

    if st.button(
        "Submit Feedback",
        type="primary",
        use_container_width=True
    ):

        feedback_payload = {
            "rating":
                rating,

            "ease_of_use":
                ease_of_use,

            "overall_feeling":
                overall_feeling,

            "favorite_features":
                favorite_features,

            "improvements":
                improvements.strip(),

            "additional_comments":
                additional_comments.strip(),

            "would_recommend":
                would_recommend
        }

        if save_user_feedback(
            user_sub,
            user_email,
            feedback_payload
        ):

            st.success(
                "Thank you — your feedback has been saved."
            )

            st.balloons()

    if existing_feedback:

        st.caption(
            "You have already submitted feedback before. "
            "Submitting again will update your existing response."
        )





# ============================================================
# PROFILE
# ============================================================

elif page == "My Profile":

    render_page_header(
        "My Profile",
        full_name,
        kicker="STEM Explorer Profile"
    )

    st.success(
        "Your profile is saved to your account."
    )

    st.divider()

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "Age",
            profile["age"]
        )

    with col2:

        st.metric(
            "Grade",
            profile["grade"]
        )

    with col3:

        st.metric(
            "Borough",
            profile["borough"]
        )

    with col4:

        st.metric(
            "Confidence",
            f"{profile['confidence']}/10"
        )

    st.divider()

    profile_cards = st.container(
        key="profile_cards",
        gap="medium"
    )

    col1, col2 = profile_cards.columns(2, gap="medium")

    with col1:

        with st.container(
            border=True,
            height=340
        ):

            st.markdown(
                '<div class="sp-profile-card"></div>',
                unsafe_allow_html=True
            )

            st.header(
                "STEM Interests"
            )

            for interest in (
                profile["interests"]
            ):

                st.write(
                    f"• {interest}"
                )

    with col2:

        with st.container(
            border=True,
            height=340
        ):

            st.markdown(
                '<div class="sp-profile-card"></div>',
                unsafe_allow_html=True
            )

            st.header(
                "Goals"
            )

            for goal in (
                profile["goals"]
            ):

                st.write(
                    f"• {goal}"
                )

    col3, col4 = profile_cards.columns(2, gap="medium")

    with col3:

        with st.container(
            border=True,
            height=340
        ):

            st.markdown(
                '<div class="sp-profile-card"></div>',
                unsafe_allow_html=True
            )

            st.header(
                "Previous Experience"
            )

            if profile[
                "experience_areas"
            ]:

                for experience in (
                    profile[
                        "experience_areas"
                    ]
                ):

                    st.write(
                        f"• {experience}"
                    )

            else:

                st.write(
                    "No previous STEM experience selected."
                )

    with col4:

        with st.container(
            border=True,
            height=340
        ):

            st.markdown(
                '<div class="sp-profile-card"></div>',
                unsafe_allow_html=True
            )

            st.header(
                "Current Exploration Stage"
            )

            st.write(
                profile[
                    "exploration_stage"
                ]
            )

            st.write(
                f"**Weekly STEM goal:** "
                f"{profile['weekly_time']}"
            )

            if profile[
                "financial_support"
            ]:

                st.write(
                    "**Opportunity preference:** "
                    "Prioritize free or financially supported programs"
                )

    with st.container(
        key="profile_action_stack",
        gap=None,
        height="content"
    ):

        with st.container(
            key="profile_action_divider",
            height="content"
        ):

            st.divider()

        with st.container(
            horizontal=True,
            horizontal_alignment="center",
            vertical_alignment="center",
            gap=24,
            height="content",
            key="profile_actions"
        ):

            if st.button(
                "Edit My Profile",
                width=320
            ):

                st.session_state.profile_completed = (
                    False
                )

                st.rerun()

            if st.button(
                "Sign Out",
                width=320
            ):

                st.logout()


else:

    st.session_state.current_page = "Dashboard"
    st.rerun()


# ============================================================
# FOOTER
# ============================================================

if page != "My Profile":

    st.divider()

    st.caption(
        ""
    )