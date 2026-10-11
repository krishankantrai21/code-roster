"""
app.py  –  Code Roster  |  Complete rewrite with:
  • Dark / Light mode toggle
  • All buttons + clicks working correctly
  • No text overwriting / z-index issues
  • Clean, spacious modern layout
  • Two-screen roast flow (editor → result, no scroll needed)
"""

import base64
import json
import os
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from code_analyzer import analyze_code, suggest_code_fix, calculate_health_score, SUPPORTED_LANGUAGES
from roast_engine import generate_roast, PERSONAS
from styles import get_custom_css, get_theme_tokens

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Code Roster | Cyber-Flame AI IDE",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  SESSION DEFAULTS
# ─────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "current_page" not in st.session_state:
    st.session_state.current_page = "hub"
if "roast_screen" not in st.session_state:
    st.session_state.roast_screen = "editor"
if "roast_data" not in st.session_state:
    st.session_state.roast_data = None

DARK = st.session_state.dark_mode

T = get_theme_tokens(DARK)
BG          = T['BG']
SURFACE     = T['SURFACE']
SURFACE2    = T['SURFACE2']
SURFACE3    = T['SURFACE3']
BORDER      = T['BORDER']
BORDER_GLOW = T['BORDER_GLOW']
TEXT        = T['TEXT']
TEXT_SUB    = T['TEXT_SUB']
TEXT_MUTED  = T['TEXT_MUTED']
ACCENT      = T['ACCENT']
ACCENT2     = T['ACCENT2']
ACCENT_PURPLE = T['ACCENT_PURPLE']
ACCENT_AMBER  = T['ACCENT_AMBER']
ACCENT_GREEN  = T['ACCENT_GREEN']

# ─────────────────────────────────────────────
#  GLOBAL CSS INJECTION (CYBER-FLAME GLASS)
# ─────────────────────────────────────────────
st.markdown(get_custom_css(DARK), unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CACHED LOADERS
# ─────────────────────────────────────────────
@st.cache_resource
def load_trained_model():
    path = "models/best_student_performance_model.joblib"
    return joblib.load(path) if os.path.exists(path) else None

@st.cache_data
def load_metadata():
    path = "models/model_metadata.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@st.cache_data
def load_model_comparison():
    path = "reports/model_comparison.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@st.cache_data
def load_eval_report():
    path = "reports/evaluation_report.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@st.cache_data
def load_feature_importance():
    path = "reports/feature_importance.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# ─────────────────────────────────────────────
#  GLOBAL TOP NAVIGATION BAR (SIDEBAR REMOVED)
# ─────────────────────────────────────────────
logo_path = "assets/code_roster_logo.jpg"
logo_b64 = ""
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f_img:
        logo_b64 = base64.b64encode(f_img.read()).decode("utf-8")

if st.session_state.current_page == "hub":
    top_brand_col, top_theme_col = st.columns([3.8, 1.2])
    with top_brand_col:
        img_html = f'<img src="data:image/jpeg;base64,{logo_b64}" class="cr-nav-logo" alt="Code Roster Logo"/>' if logo_b64 else '🔥'
        st.markdown(f"""
        <div class="cr-navbar-brand">
          <div class="cr-nav-logo-box">
            {img_html}
          </div>
          <div>
            <div class="cr-nav-title">CODE ROSTER</div>
            <div class="cr-nav-subtitle">CYBERNETIC AST CODE CRITIC · ML PERFORMANCE LAB</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with top_theme_col:
        top_mode_label = "☀️ Switch to Light Mode" if DARK else "🌙 Switch to Dark Mode"
        if st.button(top_mode_label, key="top_global_theme_toggle_btn", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
else:
    nav_brand_col, nav_home_col, nav_theme_col = st.columns([2.5, 2.2, 1.3])
    with nav_brand_col:
        img_html = f'<img src="data:image/jpeg;base64,{logo_b64}" class="cr-nav-logo" alt="Code Roster Logo"/>' if logo_b64 else '🔥'
        st.markdown(f"""
        <div class="cr-navbar-brand">
          <div class="cr-nav-logo-box" style="width:38px;height:38px;">
            {img_html}
          </div>
          <div>
            <div class="cr-nav-title" style="font-size:1.2rem;">CODE ROSTER</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with nav_home_col:
        if st.button("🏠 Return to Home Hub", key="top_nav_home_hub_btn", use_container_width=True, type="primary"):
            st.session_state.current_page = "hub"
            st.rerun()
    with nav_theme_col:
        sub_mode_label = "☀️ Light Mode" if DARK else "🌙 Dark Mode"
        if st.button(sub_mode_label, key="top_sub_theme_toggle_btn", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

st.markdown(f"<div style='height:1px;background:{BORDER};margin:10px 0 24px;opacity:0.5;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SAMPLE CODES (per language)
# ─────────────────────────────────────────────
SAMPLE_CODES = {
    "Python": '''\
def find_common_items(list_a, list_b, cache=[]):
    """Finds common elements between lists."""
    result = ""
    for a in list_a:
        for b in list_b:
            if a == b:
                if a == None:
                    continue
                result += str(a) + ","
    return result
''',
    "JavaScript": '''\
function findDuplicates(arr1, arr2) {
    var duplicates = "";
    for (var i = 0; i < arr1.length; i++) {
        for (var j = 0; j < arr2.length; j++) {
            if (arr1[i] == arr2[j]) {
                duplicates += arr1[i];
            }
        }
    }
    return duplicates;
}
''',
    "Java": '''\
public class SearchEngine {
    public static String search(String[] listA, String[] listB) {
        String result = "";
        for (int i = 0; i < listA.length; i++) {
            for (int j = 0; j < listB.length; j++) {
                if (listA[i] == listB[j]) {
                    result += listA[i];
                }
            }
        }
        return result;
    }
}
''',
    "C++": '''\
#include <iostream>
#include <vector>
using namespace std;

void findPairs(vector<int> nums) {
    for (int i = 0; i < nums.size(); i++) {
        for (int j = 0; j < nums.size(); j++) {
            if (nums[i] == nums[j]) {
                cout << nums[i] << endl;
            }
        }
    }
}
''',
    "C": '''\
#include <stdio.h>

void search(int a[], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (a[i] == a[j]) {
                printf("%d\\n", a[i]);
            }
        }
    }
}
''',
}

LANG_EXT = {"Python": "main.py", "JavaScript": "index.js",
            "Java": "Solution.java", "C++": "main.cpp", "C": "main.c"}
LANG_ICON = {"Python": "🐍", "JavaScript": "🟨", "Java": "☕", "C++": "⚡", "C": "🔵"}


# ═══════════════════════════════════════════════════════════
#  VIEW 0 · HOME HUB (WHAT YOU WILL GET - STARTING INTERFACE)
# ═══════════════════════════════════════════════════════════
if st.session_state.current_page == "hub":
    # ── DEDICATED THEME SWITCH CONTROL ON HOME PAGE ──
    t_box_col1, t_box_col2 = st.columns([3.5, 1.5])
    with t_box_col1:
        current_mode_title = "Obsidian Cyber-Flame (Dark Mode)" if DARK else "Daylight Editorial (Light Mode)"
        current_mode_icon = "🌙" if DARK else "☀️"
        st.markdown(f"""
        <div class="cr-home-theme-box">
          <span class="cr-home-theme-icon">{current_mode_icon}</span>
          <div>
            <div class="cr-home-theme-text-title">Active Theme: <strong>{current_mode_title}</strong></div>
            <div class="cr-home-theme-text-sub">Instant visual switch with high-contrast accessibility across all modules.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with t_box_col2:
        home_btn_label = "☀️ Switch to Light Mode" if DARK else "🌙 Switch to Dark Mode"
        if st.button(home_btn_label, key="home_dedicated_theme_btn", use_container_width=True, type="primary"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="cr-hub-hero">
      <div class="cr-hub-top-icon">⚡</div>
      <div class="cr-hub-title">What You Will Get</div>
      <div class="cr-hub-sub">
        Explore our gamified AST code analyzer and machine learning student performance intelligence suite. Select any module below to launch the interactive workspace.
      </div>
    </div>
    """, unsafe_allow_html=True)

    h_col1, h_col2 = st.columns(2)

    with h_col1:
        st.markdown(f"""
        <div class="cr-hub-card">
          <div>
            <div class="cr-hub-circle-icon">🔥</div>
            <div class="cr-hub-card-title">Code Roast & Checker</div>
            <div class="cr-hub-card-desc">
              Multi-language AST syntax inspection, 4 humorous judge personas (Best Friend, Strict Manager, Professor, Savage), flame intensity gauge, and instant before/after refactoring diff generator.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch Code Roaster", key="hub_launch_roast", use_container_width=True, type="primary"):
            st.session_state.current_page = "roast"
            st.rerun()

    with h_col2:
        st.markdown(f"""
        <div class="cr-hub-card">
          <div>
            <div class="cr-hub-circle-icon">🎯</div>
            <div class="cr-hub-card-title">Student AI Predictor</div>
            <div class="cr-hub-card-desc">
              Supervised Machine Learning Logistic Regression pipeline predicting coding mastery tier with multi-class probability scores and personalized remedial action plans.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch AI Predictor", key="hub_launch_pred", use_container_width=True, type="primary"):
            st.session_state.current_page = "predictor"
            st.rerun()

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    h_col3, h_col4 = st.columns(2)

    with h_col3:
        st.markdown(f"""
        <div class="cr-hub-card">
          <div>
            <div class="cr-hub-circle-icon">📊</div>
            <div class="cr-hub-card-title">Model Evaluation Lab</div>
            <div class="cr-hub-card-desc">
              Stratified 5-Fold Cross Validation benchmark audit, interactive Confusion Matrix heatmaps, Random Forest Gini impurity feature importance ranking, and KPI telemetry.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch Evaluation Lab", key="hub_launch_eval", use_container_width=True, type="primary"):
            st.session_state.current_page = "eval"
            st.rerun()

    with h_col4:
        st.markdown(f"""
        <div class="cr-hub-card">
          <div>
            <div class="cr-hub-circle-icon">⚔️</div>
            <div class="cr-hub-card-title">Roasting Arena & Wall of Shame</div>
            <div class="cr-hub-card-desc">
              1v1 Head-to-Head Code Duels, Hall of Flame disaster archives with community burn votes (🔥, 🗑️, 😭), and unlockable Coder Badges.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch Arena & Shame", key="hub_launch_arena", use_container_width=True, type="primary"):
            st.session_state.current_page = "arena"
            st.rerun()


# ═══════════════════════════════════════════════════════════
#  VIEW 1 · CODE ROAST & CHECKER
# ═══════════════════════════════════════════════════════════
elif st.session_state.current_page == "roast":
    if st.button("⬅️ Return to Home Hub", key="roast_hub_return_btn"):
        st.session_state.current_page = "hub"
        st.rerun()

    if "user_code" not in st.session_state:
        st.session_state.user_code = SAMPLE_CODES["Python"]
    if "sel_lang" not in st.session_state:
        st.session_state.sel_lang = "Python"
    if "sel_persona" not in st.session_state:
        st.session_state.sel_persona = list(PERSONAS.keys())[0]

    # ── SCREEN A: EDITOR ──────────────────────────────────
    if st.session_state.roast_screen == "editor":

        # Header
        st.markdown(f"""
        <div class="cr-hero">
          <div style="display:flex;align-items:center;gap:16px;">
            <div style="font-size:2.2rem;background:{'rgba(255, 87, 34, 0.15)' if DARK else 'rgba(234, 88, 12, 0.12)'};
                        border:1px solid {ACCENT};border-radius:14px;padding:8px 12px;display:flex;align-items:center;justify-content:center;">
              🔥
            </div>
            <div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:900;color:{TEXT};letter-spacing:-0.5px;">
                Code Roast & Static Quality Analyzer
              </div>
              <div style="font-size:0.82rem;font-weight:600;color:{TEXT_MUTED};letter-spacing:0.3px;margin-top:2px;">
                PASTE YOUR CODE · GET ROASTED WITHOUT MERCY · DISCOVER PERFORMANCE & CLEAN FIXES
              </div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:10px;">
            <span class="cr-badge cr-badge-glow">
              <span class="a-live-dot"></span>
              AST SANDBOX SECURE
            </span>
            <span class="cr-badge">
              5 LANGUAGES READY
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Controls row (Language + Persona Dropdown)
        col_lang, col_persona = st.columns([1, 1.8])

        with col_lang:
            st.markdown(f"<div style='font-size:0.82rem;font-weight:700;color:{TEXT_SUB};margin-bottom:6px;'>🌐 PROGRAMMING LANGUAGE</div>", unsafe_allow_html=True)
            sel_lang = st.selectbox(
                "🌐 Language",
                options=SUPPORTED_LANGUAGES,
                format_func=lambda l: f"{LANG_ICON.get(l,'')} {l}",
                index=SUPPORTED_LANGUAGES.index(st.session_state.sel_lang)
                      if st.session_state.sel_lang in SUPPORTED_LANGUAGES else 0,
                key="lang_selector",
                label_visibility="collapsed",
            )
            st.session_state.sel_lang = sel_lang

        with col_persona:
            st.markdown(f"<div style='font-size:0.82rem;font-weight:700;color:{TEXT_SUB};margin-bottom:6px;'>🎭 SELECT ROAST JUDGE PERSONA (DROPDOWN)</div>", unsafe_allow_html=True)
            sel_persona = st.selectbox(
                "Roast Judge Persona",
                options=list(PERSONAS.keys()),
                format_func=lambda p: f"{PERSONAS[p]['avatar']}  {p}  —  \"{PERSONAS[p]['tagline']}\"",
                index=list(PERSONAS.keys()).index(st.session_state.sel_persona),
                key="persona_dropdown_selector",
                label_visibility="collapsed",
            )
            st.session_state.sel_persona = sel_persona

        # Selected Persona Live Preview Card
        curr_p = PERSONAS[sel_persona]
        st.markdown(f"""
        <div class="cr-persona-preview">
          <div style="display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:12px;">
              <span style="font-size:1.6rem;filter:drop-shadow(0 2px 6px rgba(0,0,0,0.5));">{curr_p['avatar']}</span>
              <div>
                <div style="font-size:0.92rem;font-weight:800;color:{TEXT};display:flex;align-items:center;gap:8px;">
                  {sel_persona}
                  <span style="font-size:0.7rem;background:{'rgba(255,87,34,0.15)' if DARK else 'rgba(234,88,12,0.1)'};color:{ACCENT};padding:2px 10px;border-radius:12px;border:1px solid {BORDER};font-weight:600;">
                    {curr_p['tagline']}
                  </span>
                </div>
                <div style="font-size:0.8rem;color:{TEXT_MUTED};margin-top:2px;">{curr_p['description']}</div>
              </div>
            </div>
            <span class="cr-badge cr-badge-glow" style="font-size:0.7rem;">
              JUDGE READY
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Flame Intensity HUD Meter
        st.markdown(f"""
        <div class="cr-flame-meter-card">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="font-size:1.2rem;display:inline-block;animation:floatBob 2.5s infinite;">🔥</span>
              <span style="font-size:0.82rem;font-weight:800;color:{ACCENT};letter-spacing:1px;">
                LIVE FLAME INTENSITY HUD GAUGE
              </span>
              <span style="font-size:0.72rem;background:{'rgba(255,87,34,0.14)' if DARK else 'rgba(234,88,12,0.1)'};color:{ACCENT};padding:2px 8px;border-radius:6px;border:1px solid {BORDER};font-weight:700;">
                MAXIMUM SIZZLE
              </span>
            </div>
            <span style="font-size:0.76rem;font-weight:700;color:{ACCENT2};font-family:'JetBrains Mono',monospace;">
              HEAT LEVEL: 96% CRITICAL ROAST
            </span>
          </div>
          <div class="cr-flame-track">
            <div class="cr-flame-fill"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # IDE Titlebar with macOS buttons
        file_name = LANG_EXT.get(sel_lang, "code.txt")
        st.markdown(f"""
        <div class="cr-ide-frame">
          <div class="cr-ide-titlebar">
            <div style="display:flex;align-items:center;gap:12px;">
              <div class="cr-ide-dots">
                <span class="cr-dot cr-dot-red"></span>
                <span class="cr-dot cr-dot-yellow"></span>
                <span class="cr-dot cr-dot-green"></span>
              </div>
              <span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:600;color:{TEXT};background:{SURFACE};padding:3px 12px;border-radius:6px;border:1px solid {BORDER};">
                📄 {file_name}
              </span>
              <span style="font-size:0.76rem;color:{TEXT_MUTED};">
                src/{file_name} &nbsp;·&nbsp; UTF-8
              </span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="font-size:0.74rem;color:{ACCENT};font-weight:700;background:{'rgba(255, 87, 34, 0.12)' if DARK else 'rgba(234, 88, 12, 0.1)'};padding:2px 10px;border-radius:6px;">
                {sel_lang.upper()} MODE
              </span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Code editor
        code_input = st.text_area(
            label="Write or paste your code here:",
            value=st.session_state.user_code,
            height=420,
            label_visibility="collapsed",
            placeholder="# Paste or type your code here...",
            key="code_editor",
        )
        st.session_state.user_code = code_input

        # Action buttons
        btn1, btn2, btn3 = st.columns([2, 1.4, 1])
        with btn1:
            roast_clicked = st.button("🔥 Roast My Code", type="primary", use_container_width=True)
        with btn2:
            load_sample = st.button("📋 Load Sample Code", use_container_width=True)
        with btn3:
            clear_btn = st.button("🗑️ Clear", use_container_width=True)

        if load_sample:
            st.session_state.user_code = SAMPLE_CODES.get(sel_lang, SAMPLE_CODES["Python"])
            st.rerun()

        if clear_btn:
            st.session_state.user_code = ""
            st.rerun()

        if roast_clicked:
            if not code_input.strip():
                st.warning("⚠️ Code box khaali hai! Pehle kuch code likhein ya sample load karein.")
            else:
                with st.spinner("🔥 Analyzing aur roasting your code..."):
                    analysis_res = analyze_code(code_input, language=sel_lang)
                    roast_res    = generate_roast(code_input, analysis_res, sel_persona, language=sel_lang)
                    health_res   = calculate_health_score(analysis_res)

                st.session_state.roast_data = {
                    "code": code_input,
                    "lang": sel_lang,
                    "persona": sel_persona,
                    "analysis": analysis_res,
                    "roast": roast_res,
                    "health": health_res,
                }
                st.session_state.roast_screen = "result"
                st.rerun()

    # ── SCREEN B: RESULT ──────────────────────────────────
    elif st.session_state.roast_screen == "result":
        data = st.session_state.roast_data
        if not data:
            st.session_state.roast_screen = "editor"
            st.rerun()

        analysis = data["analysis"]
        roast    = data["roast"]
        health   = data["health"]
        sticker  = roast["sticker"]

        # Top navigation bar
        nav_c1, nav_c2 = st.columns([1, 3])
        with nav_c1:
            if st.button("⬅️ Back to Editor", type="primary", use_container_width=True):
                st.session_state.roast_screen = "editor"
                st.rerun()
        with nav_c2:
            st.markdown(
                f"<div style='padding:10px 0;font-size:1.05rem;font-weight:700;color:{ACCENT2};'>"
                f"Roast Report &nbsp;·&nbsp; {data['lang']} &nbsp;·&nbsp; "
                f"{PERSONAS[data['persona']]['avatar']} {data['persona']}</div>",
                unsafe_allow_html=True,
            )

        st.markdown(f"<hr class='cr-divider'>", unsafe_allow_html=True)

        # Row 1: Sticker + Health
        s_col, h_col = st.columns([1.3, 1])

        with s_col:
            st.markdown(
                f'<div class="cr-sticker" style="background:{sticker["gradient"]};color:#fff;">'
                f'<div class="cr-sticker-emoji">{sticker["emoji"]}</div>'
                f'<div class="cr-sticker-title">{sticker["title"]}</div>'
                f'<div class="cr-sticker-sub">{sticker["subtitle"]}</div>'
                f'<span class="cr-sticker-tag">{sticker["tag"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with h_col:
            sc   = health["score"]
            col  = health["color"]
            tier = health["tier"]
            msg  = health["message"]
            st.markdown(
                f'<div class="cr-health">'
                f'<div style="font-size:0.8rem;font-weight:700;color:{TEXT_MUTED};margin-bottom:4px;">CODE HEALTH SCORE</div>'
                f'<div style="font-size:3.8rem;font-weight:900;color:{col};line-height:1;">{sc}'
                f'<span style="font-size:1.1rem;color:{TEXT_MUTED};">/100</span></div>'
                f'<div style="margin:8px 0;"><span style="background:{col}22;color:{col};font-weight:700;'
                f'padding:4px 14px;border-radius:20px;font-size:0.85rem;">{tier}</span></div>'
                f'<div style="font-size:0.83rem;color:{TEXT_SUB};margin-top:6px;">{msg}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            # Big-O bar
            bigo = analysis.complexity.estimated_big_o
            bigo_score = 4 if "O(n³)" in bigo else 3 if "O(n²)" in bigo else 2 if "O(n)" in bigo else 1
            st.progress(bigo_score / 4, text=f"⚡ Complexity: {bigo}")

        st.markdown(f"<hr class='cr-divider'>", unsafe_allow_html=True)

        # Row 2: Roast dialog with Audio Waveform Interceptor
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:1.5rem;">{PERSONAS[data['persona']]['avatar']}</span>
            <div>
              <div style="font-size:1.15rem;font-weight:800;color:{TEXT};">
                Roast Verdict by {data['persona']}
              </div>
              <div style="font-size:0.78rem;color:{TEXT_MUTED};">"{PERSONAS[data['persona']]['tagline']}"</div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;">
            <div class="cr-audio-wave">
              <span></span><span></span><span></span><span></span><span></span>
            </div>
            <span style="font-size:0.72rem;font-weight:800;color:{ACCENT};letter-spacing:1px;">VERDICT BROADCAST</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        roast_text_html = roast["roast_text"].replace("\n", "<br>")
        st.markdown(f'<div class="cr-roast">{roast_text_html}</div>', unsafe_allow_html=True)

        st.markdown(f"<hr class='cr-divider'>", unsafe_allow_html=True)

        # Row 3: Side-by-side diff with Dual Terminal Frames
        st.markdown(
            f"<div style='font-size:1.2rem;font-weight:800;color:{TEXT};display:flex;align-items:center;gap:8px;margin-bottom:14px;'>"
            f"<span>🔄</span><span>Code Refactoring Comparison</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        d1, d2 = st.columns(2)
        with d1:
            st.markdown(f"""
            <div class="cr-ide-frame" style="margin-bottom:6px;">
              <div class="cr-ide-titlebar" style="padding:6px 12px;">
                <div class="cr-ide-dots">
                  <span class="cr-dot cr-dot-red"></span>
                  <span class="cr-dot cr-dot-yellow"></span>
                  <span class="cr-dot cr-dot-green"></span>
                </div>
                <span style="font-size:0.75rem;font-weight:700;color:#ef4444;">❌ user@submission:~/flawed.{LANG_EXT.get(data['lang'],'txt')}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.code(data["code"], language=data["lang"].lower())
        with d2:
            st.markdown(f"""
            <div class="cr-ide-frame" style="margin-bottom:6px;">
              <div class="cr-ide-titlebar" style="padding:6px 12px;">
                <div class="cr-ide-dots">
                  <span class="cr-dot cr-dot-red"></span>
                  <span class="cr-dot cr-dot-yellow"></span>
                  <span class="cr-dot cr-dot-green"></span>
                </div>
                <span style="font-size:0.75rem;font-weight:700;color:#10b981;">✅ ast@refactor:~/clean.{LANG_EXT.get(data['lang'],'txt')}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            if roast.get("suggested_fix"):
                st.code(roast["suggested_fix"], language=data["lang"].lower())
            else:
                st.success("🎉 Code is already clean! No refactor needed.")

        st.markdown(f"<hr class='cr-divider'>", unsafe_allow_html=True)

        # Row 4: Issues
        st.markdown("#### 🔍 Detected Issues")
        if not analysis.issues:
            st.success(f"🎉 Zero anti-patterns detected in your {data['lang']} code!")
        else:
            for iss in analysis.issues:
                color_map = {
                    "Critical": "#ef4444",
                    "Warning": "#f59e0b",
                    "Optimization": "#3b82f6",
                    "Style": "#8b5cf6",
                }
                c    = color_map.get(iss.severity, "#6b7280")
                line = f"Line {iss.line}" if iss.line else "Global"
                st.markdown(
                    f'<div class="cr-issue" style="border-left:4px solid {c};">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<strong style="color:{TEXT};">[{iss.id}] {iss.title}</strong>'
                    f'<span style="background:{c}22;color:{c};font-size:0.73rem;font-weight:700;'
                    f'padding:2px 10px;border-radius:20px;">{iss.severity}</span></div>'
                    f'<div style="font-size:0.8rem;color:{TEXT_MUTED};margin:3px 0;">📍 {line}</div>'
                    f'<div style="font-size:0.9rem;color:{TEXT_SUB};margin:5px 0;">{iss.description}</div>'
                    f'<div style="font-size:0.83rem;color:{ACCENT2};">💡 <strong>Fix:</strong> {iss.suggested_fix}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown(f"<hr class='cr-divider'>", unsafe_allow_html=True)

        # Row 5: Back + Download
        back_c, dl_c = st.columns([1, 2])
        with back_c:
            if st.button("⬅️ Write New Code", use_container_width=True):
                st.session_state.roast_screen = "editor"
                st.rerun()
        with dl_c:
            report_lines = [
                f"# Code Roster Audit Report",
                f"Language: {data['lang']}",
                f"Judge: {data['persona']}",
                f"Health Score: {health['score']}/100  ({health['grade']})",
                f"Complexity: {analysis.complexity.estimated_big_o}",
                f"",
                f"## Original Code",
                f"```{data['lang'].lower()}",
                data["code"],
                f"```",
                f"",
                f"## Roast Verdict",
                roast["roast_text"],
                f"",
                f"## Issues Found",
            ]
            for iss in analysis.issues:
                report_lines.append(f"- [{iss.severity}] {iss.title} (Line {iss.line}): {iss.description}")
            report_lines += [f"", f"## Suggested Fix", f"```{data['lang'].lower()}", roast.get("suggested_fix",""), "```"]
            st.download_button(
                label="📥 Download Audit Report (.md)",
                data="\n".join(report_lines),
                file_name=f"code_roster_{data['lang'].lower()}_audit.md",
                mime="text/markdown",
                use_container_width=True,
            )


# ═══════════════════════════════════════════════════════════
#  VIEW 2 · STUDENT AI PREDICTOR
# ═══════════════════════════════════════════════════════════
elif st.session_state.current_page == "predictor":
    if st.button("⬅️ Return to Home Hub", key="pred_hub_return_btn"):
        st.session_state.current_page = "hub"
        st.rerun()

    st.markdown(f"""
    <div class="cr-hero">
      <div style="display:flex;align-items:center;gap:16px;">
        <div style="font-size:2.2rem;background:{'rgba(0, 229, 211, 0.15)' if DARK else 'rgba(2, 132, 199, 0.12)'};
                    border:1px solid {ACCENT2};border-radius:14px;padding:8px 12px;">
          🎯
        </div>
        <div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:900;color:{TEXT};letter-spacing:-0.5px;">
            Student Performance Tier Predictor
          </div>
          <div style="font-size:0.82rem;font-weight:600;color:{TEXT_MUTED};letter-spacing:0.3px;margin-top:2px;">
            SUPERVISED MACHINE LEARNING · 5-FOLD STRATIFIED CV · MACRO F1: 0.7356
          </div>
        </div>
      </div>
      <div>
        <span class="cr-badge cr-badge-glow">
          LOGISTIC REGRESSION PIPELINE
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    model_pipeline = load_trained_model()
    model_meta     = load_metadata()

    if model_pipeline is None:
        st.error("❌ Model not found. Run `python train_model.py` first.")
        st.stop()

    # Preset profiles
    st.markdown(f"**⚡ Quick Preset Profiles:**")
    pp1, pp2, pp3 = st.columns(3)

    defaults = dict(p_hours=3.0, p_prob=180, p_acc=72.0, p_streak=25, p_assign=8, p_focus=6.2, p_lang="Python")
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    with pp1:
        if st.button("🧑‍🎓 Struggling Student", use_container_width=True):
            st.session_state.p_hours=1.0; st.session_state.p_prob=40; st.session_state.p_acc=48.0
            st.session_state.p_streak=3; st.session_state.p_assign=3; st.session_state.p_focus=3.2
            st.session_state.p_lang="Python"; st.rerun()
    with pp2:
        if st.button("💻 Average Consistent Coder", use_container_width=True):
            st.session_state.p_hours=3.2; st.session_state.p_prob=195; st.session_state.p_acc=75.0
            st.session_state.p_streak=32; st.session_state.p_assign=9; st.session_state.p_focus=6.8
            st.session_state.p_lang="Java"; st.rerun()
    with pp3:
        if st.button("🌟 Top Competitive Coder", use_container_width=True):
            st.session_state.p_hours=5.8; st.session_state.p_prob=390; st.session_state.p_acc=92.0
            st.session_state.p_streak=70; st.session_state.p_assign=14; st.session_state.p_focus=9.4
            st.session_state.p_lang="C++"; st.rerun()

    st.markdown(f"<hr class='cr-divider'>", unsafe_allow_html=True)

    with st.form("predictor_form", clear_on_submit=False):
        fc1, fc2 = st.columns(2)
        with fc1:
            h    = st.slider("⏱️ Daily Coding Hours", 0.5, 8.0, float(st.session_state.p_hours), 0.1)
            p    = st.slider("🧩 Problems Solved", 5, 450, int(st.session_state.p_prob), 5)
            acc  = st.slider("🎯 Submission Accuracy (%)", 35.0, 98.0, float(st.session_state.p_acc), 0.5)
            lang = st.selectbox("💻 Primary Language", ["Python", "Java", "C++", "JavaScript"],
                                index=["Python","Java","C++","JavaScript"].index(st.session_state.p_lang))
        with fc2:
            stk  = st.slider("🔥 Consistency Streak (Days)", 1, 90, int(st.session_state.p_streak), 1)
            asn  = st.slider("📚 Lab Assignments (out of 15)", 1, 15, int(st.session_state.p_assign), 1)
            foc  = st.slider("🧠 Focus & Attendance Score", 1.0, 10.0, float(st.session_state.p_focus), 0.1)

        predict_btn = st.form_submit_button("🔮 Predict My Performance Tier", type="primary", use_container_width=True)

    if predict_btn:
        df_in = pd.DataFrame([{
            "daily_coding_hours": h, "problems_solved": p,
            "submission_accuracy": acc, "consistency_streak_days": stk,
            "assignments_completed": asn, "focus_score": foc,
            "primary_language": lang,
        }])
        pred_tier = model_pipeline.predict(df_in)[0]
        probs     = model_pipeline.predict_proba(df_in)[0]
        classes   = model_pipeline.classes_

        tier_colors = {"Needs Guidance": "#ef4444", "Competent": "#3b82f6", "Exemplary": "#10b981"}
        tc = tier_colors.get(pred_tier, ACCENT)

        st.markdown(f"<hr class='cr-divider'>", unsafe_allow_html=True)
        st.markdown("### 🏆 Prediction Result")

        r1, r2 = st.columns([1, 1.3])
        with r1:
            st.markdown(
                f'<div class="cr-pred-box" style="border-color:{tc};background:{tc}11;">'
                f'<div style="font-size:0.8rem;font-weight:700;color:{TEXT_MUTED};margin-bottom:6px;">PREDICTED TIER</div>'
                f'<div style="font-size:2rem;font-weight:900;color:{tc};">{pred_tier}</div>'
                f'<div style="font-size:0.83rem;color:{TEXT_SUB};margin-top:8px;">'
                f'Algorithm: {model_meta.get("model_name","Logistic Regression")}<br>'
                f'Track: {lang} &nbsp;|&nbsp; {h} hrs/day</div></div>',
                unsafe_allow_html=True,
            )
        with r2:
            fig = px.bar(
                x=probs, y=classes, orientation="h",
                color=classes, color_discrete_map=tier_colors,
                text=[f"{pv*100:.1f}%" for pv in probs], height=220,
            )
            fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=10,b=10),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color=TEXT, xaxis_range=[0,1])
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("**📋 Action Plan:**")
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            (st.warning if h < 2.0 else st.success)("⏱️ " + ("Increase daily practice by 45 min." if h < 2.0 else "Good daily commitment!"))
        with ac2:
            (st.warning if acc < 65.0 else st.success)("🎯 " + ("Dry-run test cases before submitting." if acc < 65.0 else "Solid submission accuracy!"))
        with ac3:
            (st.error if asn < 10 else st.success)("📚 " + ("Finish pending lab assignments!" if asn < 10 else "Lab coursework on track!"))


# ═══════════════════════════════════════════════════════════
#  VIEW 3 · MODEL EVALUATION
# ═══════════════════════════════════════════════════════════
elif st.session_state.current_page == "eval":
    if st.button("⬅️ Return to Home Hub", key="eval_hub_return_btn"):
        st.session_state.current_page = "hub"
        st.rerun()

    st.markdown(f"""
    <div class="cr-hero">
      <div style="display:flex;align-items:center;gap:16px;">
        <div style="font-size:2.2rem;background:{'rgba(168, 85, 247, 0.15)' if DARK else 'rgba(147, 51, 234, 0.12)'};
                    border:1px solid {ACCENT_PURPLE};border-radius:14px;padding:8px 12px;">
          📊
        </div>
        <div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:900;color:{TEXT};letter-spacing:-0.5px;">
            ML Model Training & Evaluation Lab
          </div>
          <div style="font-size:0.82rem;font-weight:600;color:{TEXT_MUTED};letter-spacing:0.3px;margin-top:2px;">
            STRATIFIED 5-FOLD CV · CONFUSION MATRIX · FEATURE IMPORTANCE · BALANCED ACCURACY
          </div>
        </div>
      </div>
      <div>
        <span class="cr-badge cr-badge-glow">
          1,500 TELEMETRY RECORDS
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    comp_data = load_model_comparison()
    eval_data = load_eval_report()
    fi_data   = load_feature_importance()

    # KPI Stat Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f'<div class="cr-card" style="text-align:center;padding:16px;">'
            f'<div style="font-size:0.72rem;font-weight:800;color:{TEXT_MUTED};">CV MACRO F1</div>'
            f'<div style="font-size:1.85rem;font-weight:900;color:{ACCENT2};font-family:\'Space Grotesk\',sans-serif;">0.7356</div>'
            f'<div style="font-size:0.74rem;color:{ACCENT_GREEN};">5-Fold Stratified</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f'<div class="cr-card" style="text-align:center;padding:16px;">'
            f'<div style="font-size:0.72rem;font-weight:800;color:{TEXT_MUTED};">TEST ACCURACY</div>'
            f'<div style="font-size:1.85rem;font-weight:900;color:{ACCENT};font-family:\'Space Grotesk\',sans-serif;">76.0%</div>'
            f'<div style="font-size:0.74rem;color:{TEXT_SUB};">Hold-out 300 test</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f'<div class="cr-card" style="text-align:center;padding:16px;">'
            f'<div style="font-size:0.72rem;font-weight:800;color:{TEXT_MUTED};">BEST MODEL</div>'
            f'<div style="font-size:1.4rem;font-weight:900;color:{ACCENT_PURPLE};font-family:\'Space Grotesk\',sans-serif;margin:4px 0;">Logistic Reg</div>'
            f'<div style="font-size:0.74rem;color:{TEXT_SUB};">Scikit-learn Pipeline</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f'<div class="cr-card" style="text-align:center;padding:16px;">'
            f'<div style="font-size:0.72rem;font-weight:800;color:{TEXT_MUTED};">DATA LEAKAGE</div>'
            f'<div style="font-size:1.85rem;font-weight:900;color:{ACCENT_GREEN};font-family:\'Space Grotesk\',sans-serif;">0%</div>'
            f'<div style="font-size:0.74rem;color:{ACCENT_GREEN};">Fit on Train Only</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(f"<div style='height:1px;background:{BORDER};margin:16px 0 20px;'></div>", unsafe_allow_html=True)

    if comp_data:
        st.markdown("#### 1. Model Comparison (5-Fold CV)")
        df_comp = pd.DataFrame(comp_data)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)
    else:
        st.info("Run `python train_model.py` to generate evaluation reports.")

    if eval_data and "Logistic Regression" in eval_data:
        st.markdown(f"<hr class='cr-divider'>", unsafe_allow_html=True)
        st.markdown("#### 2. Confusion Matrix (Test Set — 300 samples)")
        lr = eval_data["Logistic Regression"]
        cm     = lr["confusion_matrix"]
        labels = lr["labels"]
        fig_cm = go.Figure(go.Heatmap(
            z=cm, x=[f"Pred: {l}" for l in labels], y=[f"True: {l}" for l in labels],
            colorscale="Blues", text=cm, texttemplate="%{text}", textfont={"size":15},
        ))
        fig_cm.update_layout(height=340, margin=dict(l=20,r=20,t=20,b=20),
                             paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             font_color=TEXT)
        st.plotly_chart(fig_cm, use_container_width=True)

    if fi_data:
        st.markdown(f"<hr class='cr-divider'>", unsafe_allow_html=True)
        st.markdown("#### 3. Feature Importance (Random Forest — Gini Impurity)")
        fi_df = (pd.DataFrame(list(fi_data.items()), columns=["Feature","Importance"])
                   .sort_values("Importance", ascending=True))
        fig_fi = px.bar(fi_df, x="Importance", y="Feature", orientation="h",
                        height=300, color="Importance", color_continuous_scale="Viridis")
        fig_fi.update_layout(showlegend=False, margin=dict(l=20,r=20,t=10,b=10),
                             paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             font_color=TEXT)
        st.plotly_chart(fig_fi, use_container_width=True)


# ═══════════════════════════════════════════════════════════
#  VIEW 4 · ROASTING ARENA & WALL OF SHAME
# ═══════════════════════════════════════════════════════════
elif st.session_state.current_page == "arena":
    if st.button("⬅️ Return to Home Hub", key="arena_hub_return_btn"):
        st.session_state.current_page = "hub"
        st.rerun()

    st.markdown(f"""
    <div class="cr-hero">
      <div style="display:flex;align-items:center;gap:16px;">
        <div style="font-size:2.2rem;background:{'rgba(255, 87, 34, 0.15)' if DARK else 'rgba(234, 88, 12, 0.12)'};
                    border:1px solid {ACCENT};border-radius:14px;padding:8px 12px;">
          ⚔️
        </div>
        <div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:900;color:{TEXT};letter-spacing:-0.5px;">
            Code Roasting Arena & Wall of Shame
          </div>
          <div style="font-size:0.82rem;font-weight:600;color:{TEXT_MUTED};letter-spacing:0.3px;margin-top:2px;">
            HEAD-TO-HEAD CODE DUELS · COMMUNITY FLAME DISASTERS · UNLOCKABLE CODER BADGES
          </div>
        </div>
      </div>
      <div>
        <span class="cr-badge cr-badge-glow">
          ARENA BATTLEFIELD LIVE
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_duel, tab_shame, tab_badges = st.tabs([
        "⚔️ 1v1 Code Duel Arena",
        "🔥 Wall of Shame (Hall of Flame)",
        "🎖️ Coder Badges Gallery"
    ])

    # ─────────────────────────────────────────────────────────
    #  TAB 1: 1v1 CODE DUEL ARENA
    # ─────────────────────────────────────────────────────────
    with tab_duel:
        st.markdown(f"""
        <div style="font-size:1.1rem;font-weight:800;color:{TEXT};margin-bottom:8px;">
          🥊 Two Coders Enter. One Coder Gets Roasted.
        </div>
        <div style="font-size:0.85rem;color:{TEXT_MUTED};margin-bottom:16px;">
          Paste two rival code implementations below. The AST engine will analyze both, compare Big-O complexity, and declare a Winner while brutally roasting the loser!
        </div>
        """, unsafe_allow_html=True)

        DUEL_PRESETS = {
            "Custom Code": ("", ""),
            "⚔️ Duel 1: Nested Loops O(n²) vs Hash Set O(n)": (
                '''def find_common_slow(a, b):\n    res = []\n    for x in a:\n        for y in b:\n            if x == y:\n                res.append(x)\n    return res''',
                '''def find_common_fast(a, b):\n    set_b = set(b)\n    return [x for x in a if x in set_b]'''
            ),
            "⚔️ Duel 2: String Concatenation vs List Join": (
                '''def build_string_bad(words):\n    out = ""\n    for w in words:\n        out = out + w + ","\n    return out''',
                '''def build_string_good(words):\n    return ",".join(words)'''
            ),
            "⚔️ Duel 3: Range Check with 50 Ifs vs Modulo Bitwise": (
                '''def is_even_disaster(n):\n    if n == 0: return True\n    elif n == 1: return False\n    elif n == 2: return True\n    elif n == 3: return False\n    return False''',
                '''def is_even_clean(n):\n    return (n & 1) == 0'''
            )
        }

        sel_preset = st.selectbox("⚡ Quick Battle Matchups:", list(DUEL_PRESETS.keys()), index=1)
        preset_code_a, preset_code_b = DUEL_PRESETS[sel_preset]

        col_a, col_vs, col_b = st.columns([1, 0.15, 1])

        with col_a:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
              <span style="font-weight:800;color:#ef4444;font-size:0.95rem;">🔴 Challenger (Player 1)</span>
            </div>
            """, unsafe_allow_html=True)
            duel_code_a = st.text_area("Player 1 Code", value=preset_code_a, height=220, key="duel_a_editor", label_visibility="collapsed")

        with col_vs:
            st.markdown(f"""
            <div style="text-align:center;padding-top:80px;">
              <div class="cr-vs-badge">VS</div>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
              <span style="font-weight:800;color:#10b981;font-size:0.95rem;">🔵 Defender (Player 2)</span>
            </div>
            """, unsafe_allow_html=True)
            duel_code_b = st.text_area("Player 2 Code", value=preset_code_b, height=220, key="duel_b_editor", label_visibility="collapsed")

        if st.button("⚔️ FIGHT! Run Roast Duel & Declare Winner", type="primary", use_container_width=True):
            if not duel_code_a.strip() or not duel_code_b.strip():
                st.warning("⚠️ Both players must submit code to fight in the Arena!")
            else:
                with st.spinner("⚔️ Running AST duel inspection & crunching performance metrics..."):
                    ana_a = analyze_code(duel_code_a, language="Python")
                    ana_b = analyze_code(duel_code_b, language="Python")
                    health_a = calculate_health_score(ana_a)
                    health_b = calculate_health_score(ana_b)

                st.markdown(f"<div style='height:1px;background:{BORDER};margin:24px 0;'></div>", unsafe_allow_html=True)
                st.markdown("### 🏆 Arena Duel Verdict")

                sc_a = health_a["score"]
                sc_b = health_b["score"]

                if sc_a > sc_b:
                    winner_name = "Player 1 (Challenger) WINS!"
                    winner_color = "#10b981"
                    loser_name = "Player 2 (Defender) DEFEATED"
                    roast_msg = f"Player 2 got destroyed! Player 1 achieved a Health Score of {sc_a}/100 vs Player 2's dismal {sc_b}/100. Player 2's complexity ({ana_b.complexity.estimated_big_o}) brought shame to their CPU."
                elif sc_b > sc_a:
                    winner_name = "Player 2 (Defender) WINS!"
                    winner_color = "#10b981"
                    loser_name = "Player 1 (Challenger) DEFEATED"
                    roast_msg = f"Player 1 got crushed! Player 2 dominated with a Health Score of {sc_b}/100 while Player 1 choked at {sc_a}/100. Player 1's complexity ({ana_a.complexity.estimated_big_o}) is a crime against computer science."
                else:
                    winner_name = "STALEMATE TIE!"
                    winner_color = "#f59e0b"
                    loser_name = "Both Tied"
                    roast_msg = f"Both players tied with identical health scores of {sc_a}/100. Either both are geniuses, or both wrote equally catastrophic spaghetti!"

                st.markdown(f"""
                <div class="cr-card" style="border:2px solid {winner_color};background:{winner_color}12;text-align:center;">
                  <div style="font-size:0.85rem;font-weight:800;color:{TEXT_MUTED};letter-spacing:1px;">OFFICIAL ROAST ARENA OUTCOME</div>
                  <div style="font-family:'Space Grotesk',sans-serif;font-size:2.3rem;font-weight:900;color:{winner_color};margin:8px 0;">
                    👑 {winner_name}
                  </div>
                  <div style="font-size:1.02rem;color:{TEXT};line-height:1.6;max-width:760px;margin:0 auto;">
                    {roast_msg}
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # Head to Head Stats Comparison
                st.markdown("#### 📊 Head-to-Head Telemetry Breakdown")
                st1, st2, st3 = st.columns(3)
                with st1:
                    st.markdown(f"""
                    <div class="cr-card" style="text-align:center;padding:16px;">
                      <div style="font-size:0.75rem;font-weight:800;color:{TEXT_MUTED};">HEALTH SCORE</div>
                      <div style="font-size:1.5rem;font-weight:900;color:{TEXT};margin:6px 0;">
                        <span style="color:#ef4444;">{sc_a}</span> &nbsp;vs&nbsp; <span style="color:#10b981;">{sc_b}</span>
                      </div>
                      <div style="font-size:0.75rem;color:{TEXT_MUTED};">Player 1 vs Player 2</div>
                    </div>
                    """, unsafe_allow_html=True)
                with st2:
                    st.markdown(f"""
                    <div class="cr-card" style="text-align:center;padding:16px;">
                      <div style="font-size:0.75rem;font-weight:800;color:{TEXT_MUTED};">TIME COMPLEXITY</div>
                      <div style="font-size:1.2rem;font-weight:900;color:{ACCENT2};margin:8px 0;font-family:'JetBrains Mono';">
                        {ana_a.complexity.estimated_big_o} &nbsp;vs&nbsp; {ana_b.complexity.estimated_big_o}
                      </div>
                      <div style="font-size:0.75rem;color:{TEXT_MUTED};">Player 1 vs Player 2</div>
                    </div>
                    """, unsafe_allow_html=True)
                with st3:
                    st.markdown(f"""
                    <div class="cr-card" style="text-align:center;padding:16px;">
                      <div style="font-size:0.75rem;font-weight:800;color:{TEXT_MUTED};">ANTI-PATTERNS DETECTED</div>
                      <div style="font-size:1.5rem;font-weight:900;color:{TEXT};margin:6px 0;">
                        <span style="color:#ef4444;">{len(ana_a.issues)}</span> &nbsp;vs&nbsp; <span style="color:#10b981;">{len(ana_b.issues)}</span>
                      </div>
                      <div style="font-size:0.75rem;color:{TEXT_MUTED};">Total Flaws Found</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────
    #  TAB 2: WALL OF SHAME (HALL OF FLAME)
    # ─────────────────────────────────────────────────────────
    with tab_shame:
        st.markdown(f"""
        <div style="font-size:1.1rem;font-weight:800;color:{TEXT};margin-bottom:8px;">
          🔥 Community Wall of Shame (Hall of Flame)
        </div>
        <div style="font-size:0.85rem;color:{TEXT_MUTED};margin-bottom:18px;">
          The absolute worst coding disasters ever committed to git. Vote with reactions to give them emotional damage!
        </div>
        """, unsafe_allow_html=True)

        if "burn_votes" not in st.session_state:
            st.session_state.burn_votes = {"p1_fire": 482, "p1_trash": 129, "p1_cry": 312,
                                           "p2_fire": 395, "p2_trash": 241, "p2_cry": 510,
                                           "p3_fire": 620, "p3_trash": 88,  "p3_cry": 435}

        # Shame Item 1
        st.markdown(f"""
        <div class="cr-shame-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:1.4rem;">🍝</span>
              <strong style="font-size:1.1rem;color:{TEXT};">The Infinite If-Parity Checker</strong>
            </div>
            <span style="background:#ef444422;color:#ef4444;font-size:0.75rem;font-weight:800;padding:4px 12px;border-radius:20px;border:1px solid #ef444444;">
              HEALTH: 6/100 · SPAGHETTI LORD
            </span>
          </div>
          <div style="font-size:0.82rem;color:{TEXT_MUTED};margin-bottom:8px;">Author: Anonymous Intern · Language: Python · Issue: Hardcoded 1,000 branch conditions</div>
        </div>
        """, unsafe_allow_html=True)
        st.code('''def is_even(n):\n    if n == 0: return True\n    elif n == 1: return False\n    elif n == 2: return True\n    elif n == 3: return False\n    # ... repeated 500 more times until IDE ran out of RAM\n    return "idk bro"''', language="python")
        st.markdown(f"""
        <div class="cr-roast" style="margin-top:10px;font-size:0.92rem;line-height:1.6;">
          📢 <strong>Roast Verdict:</strong> You wrote an O(n) branching lookup tree to solve a 1-bit bitwise operation (<code>n & 1</code>). George Boole is spinning in his grave at 10,000 RPM.
        </div>
        """, unsafe_allow_html=True)

        v1, v2, v3, _ = st.columns([1, 1, 1, 3])
        with v1:
            if st.button(f"🔥 Sizzle ({st.session_state.burn_votes['p1_fire']})", key="btn_shame_1_fire"):
                st.session_state.burn_votes['p1_fire'] += 1
                st.rerun()
        with v2:
            if st.button(f"🗑️ Trash ({st.session_state.burn_votes['p1_trash']})", key="btn_shame_1_trash"):
                st.session_state.burn_votes['p1_trash'] += 1
                st.rerun()
        with v3:
            if st.button(f"😭 Cry ({st.session_state.burn_votes['p1_cry']})", key="btn_shame_1_cry"):
                st.session_state.burn_votes['p1_cry'] += 1
                st.rerun()

        st.markdown(f"<div style='height:1px;background:{BORDER};margin:22px 0;'></div>", unsafe_allow_html=True)

        # Shame Item 2
        st.markdown(f"""
        <div class="cr-shame-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:1.4rem;">⏱️</span>
              <strong style="font-size:1.1rem;color:{TEXT};">The Asynchronous "Sleep Sort"</strong>
            </div>
            <span style="background:#f59e0b22;color:#f59e0b;font-size:0.75rem;font-weight:800;padding:4px 12px;border-radius:20px;border:1px solid #f59e0b44;">
              HEALTH: 18/100 · TIME WARP KAMIKAZE
            </span>
          </div>
          <div style="font-size:0.82rem;color:{TEXT_MUTED};margin-bottom:8px;">Author: Web Dev Guru · Language: JavaScript · Issue: Time Complexity = Literal Human Time</div>
        </div>
        """, unsafe_allow_html=True)
        st.code('''function sleepSort(arr) {\n    // Why use QuickSort when setTimeout exists?\n    arr.forEach(num => {\n        setTimeout(() => console.log(num), num * 1000);\n    });\n}''', language="javascript")
        st.markdown(f"""
        <div class="cr-roast" style="margin-top:10px;font-size:0.92rem;line-height:1.6;">
          📢 <strong>Roast Verdict:</strong> Sorting <code>[1, 9999]</code> takes 2.7 literal hours of human existence. If your server gets rebooted in hour 2, your sort order is lost to the cosmos.
        </div>
        """, unsafe_allow_html=True)

        v4, v5, v6, _ = st.columns([1, 1, 1, 3])
        with v4:
            if st.button(f"🔥 Sizzle ({st.session_state.burn_votes['p2_fire']})", key="btn_shame_2_fire"):
                st.session_state.burn_votes['p2_fire'] += 1
                st.rerun()
        with v5:
            if st.button(f"🗑️ Trash ({st.session_state.burn_votes['p2_trash']})", key="btn_shame_2_trash"):
                st.session_state.burn_votes['p2_trash'] += 1
                st.rerun()
        with v6:
            if st.button(f"😭 Cry ({st.session_state.burn_votes['p2_cry']})", key="btn_shame_2_cry"):
                st.session_state.burn_votes['p2_cry'] += 1
                st.rerun()

        st.markdown(f"<div style='height:1px;background:{BORDER};margin:22px 0;'></div>", unsafe_allow_html=True)

        # Shame Item 3
        st.markdown(f"""
        <div class="cr-shame-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:1.4rem;">🕳️</span>
              <strong style="font-size:1.1rem;color:{TEXT};">The 9-Level Callback Pyramid of Doom</strong>
            </div>
            <span style="background:#8b5cf622;color:#8b5cf6;font-size:0.75rem;font-weight:800;padding:4px 12px;border-radius:20px;border:1px solid #8b5cf644;">
              HEALTH: 14/100 · ABYSS DRIFTER
            </span>
          </div>
          <div style="font-size:0.82rem;color:{TEXT_MUTED};margin-bottom:8px;">Author: Legacy Code Archaeologist · Language: JavaScript · Issue: Extreme Horizontal Drift</div>
        </div>
        """, unsafe_allow_html=True)
        st.code('''getUser(id, (u) => {\n    getOrders(u, (o) => {\n        getPayment(o, (p) => {\n            notifyBank(p, (b) => {\n                sendInvoice(b, (i) => {\n                    console.log("Finally made it here!");\n                });\n            });\n        });\n    });\n});''', language="javascript")
        st.markdown(f"""
        <div class="cr-roast" style="margin-top:10px;font-size:0.92rem;line-height:1.6;">
          📢 <strong>Roast Verdict:</strong> Your indentation has drifted so far east it needs a visa. Promises and async/await were invented specifically so humans wouldn't have to suffer reading this pyramid.
        </div>
        """, unsafe_allow_html=True)

        v7, v8, v9, _ = st.columns([1, 1, 1, 3])
        with v7:
            if st.button(f"🔥 Sizzle ({st.session_state.burn_votes['p3_fire']})", key="btn_shame_3_fire"):
                st.session_state.burn_votes['p3_fire'] += 1
                st.rerun()
        with v8:
            if st.button(f"🗑️ Trash ({st.session_state.burn_votes['p3_trash']})", key="btn_shame_3_trash"):
                st.session_state.burn_votes['p3_trash'] += 1
                st.rerun()
        with v9:
            if st.button(f"😭 Cry ({st.session_state.burn_votes['p3_cry']})", key="btn_shame_3_cry"):
                st.session_state.burn_votes['p3_cry'] += 1
                st.rerun()

    # ─────────────────────────────────────────────────────────
    #  TAB 3: CODER BADGES GALLERY
    # ─────────────────────────────────────────────────────────
    with tab_badges:
        st.markdown(f"""
        <div style="font-size:1.1rem;font-weight:800;color:{TEXT};margin-bottom:8px;">
          🎖️ Coder Badges & Achievements Gallery
        </div>
        <div style="font-size:0.85rem;color:{TEXT_MUTED};margin-bottom:20px;">
          Earn these cyber badges based on your coding style, anti-patterns, and AST optimization metrics!
        </div>
        """, unsafe_allow_html=True)

        BADGES = [
            {"icon": "🍝", "title": "Spaghetti Master", "tier": "LEGENDARY DISASTER", "color": "#ef4444",
             "desc": "Granted when AST detects nested loop depth >= 3, bringing the CPU to a crawl."},
            {"icon": "💾", "title": "Memory Leak Legend", "tier": "EPIC DANGER", "color": "#f97316",
             "desc": "Granted for accumulating global state and mutable default arguments across function calls."},
            {"icon": "☕", "title": "NullPointer Emperor", "tier": "UNHOLY DISASTER", "color": "#ec4899",
             "desc": "Granted for invoking dereferenced methods without verifying nullable input bounds."},
            {"icon": "⚡", "title": "O(1) Turbo Titan", "tier": "MYTHIC CLEAN", "color": "#00e5d3",
             "desc": "Granted for achieving optimal constant-time complexity with zero static code flaws."},
            {"icon": "🛡️", "title": "AST Pure Paladin", "tier": "EXEMPLARY PRO", "color": "#10b981",
             "desc": "Granted for scoring 95+ Health Score with zero anti-patterns across all 5 languages."},
            {"icon": "🔮", "title": "Bitwise Alchemist", "tier": "WIZARD TIER", "color": "#a855f7",
             "desc": "Granted for replacing clunky if-else branches with elegant bit-level binary operations."},
        ]

        b_c1, b_c2, b_c3 = st.columns(3)
        cols = [b_c1, b_c2, b_c3]

        for i, bg in enumerate(BADGES):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="cr-badge-card" style="margin-bottom:16px;">
                  <div style="font-size:2.8rem;margin-bottom:8px;">{bg['icon']}</div>
                  <div style="font-family:'Space Grotesk',sans-serif;font-size:1.15rem;font-weight:900;color:{TEXT};">
                    {bg['title']}
                  </div>
                  <div style="margin:8px 0;">
                    <span style="background:{bg['color']}22;color:{bg['color']};font-size:0.7rem;font-weight:800;padding:3px 12px;border-radius:14px;border:1px solid {bg['color']}44;">
                      {bg['tier']}
                    </span>
                  </div>
                  <div style="font-size:0.84rem;color:{TEXT_SUB};line-height:1.5;">
                    {bg['desc']}
                  </div>
                </div>
                """, unsafe_allow_html=True)
