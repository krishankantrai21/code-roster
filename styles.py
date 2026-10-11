"""
styles.py - Cyber-Flame Glassmorphism Design System for Code Roster
===================================================================
Ultra-Modern aesthetic with:
  • Custom Cyber-Flame / Obsidian Dark & Crisp Light Studio themes
  • Guaranteed high-contrast text in both Dark Mode & Light Mode
  • Hub Dashboard (Cards Grid matching 'What You Will Get' design)
  • Independent separate button boxes for Sidebar navigation
  • Holographic unique logo showcase frame with cybernetic badge
  • Interactive Flame Intensity HUD Meter
  • Intercepted Audio Visualizer for Roast speech
  • Modern selectbox and input controls
"""

def get_theme_tokens(dark: bool = True) -> dict:
    if dark:
        return {
            "BG": "#08090d",
            "BG_GRADIENT": "radial-gradient(ellipse at 15% 0%, rgba(255, 87, 34, 0.12) 0%, transparent 55%), radial-gradient(ellipse at 85% 15%, rgba(138, 43, 226, 0.10) 0%, transparent 50%), radial-gradient(ellipse at 50% 85%, rgba(0, 229, 211, 0.06) 0%, transparent 60%), #08090d",
            "SURFACE": "rgba(15, 18, 27, 0.88)",
            "SURFACE2": "rgba(22, 27, 40, 0.90)",
            "SURFACE3": "#1d2334",
            "BORDER": "rgba(255, 255, 255, 0.10)",
            "BORDER_GLOW": "rgba(255, 87, 34, 0.55)",
            "TEXT": "#f8fafc",
            "TEXT_SUB": "#cbd5e1",
            "TEXT_MUTED": "#94a3b8",
            "ACCENT": "#ff5722",
            "ACCENT_HOVER": "#ff7043",
            "ACCENT2": "#00e5d3",
            "ACCENT_PURPLE": "#a855f7",
            "ACCENT_AMBER": "#f59e0b",
            "ACCENT_GREEN": "#10b981",
            "CARD_SHADOW": "0 12px 32px -4px rgba(0, 0, 0, 0.55), 0 0 1px 1px rgba(255, 255, 255, 0.06)",
            "IDE_BG": "#0a0c12",
            "ROAST_BOX_BG": "linear-gradient(135deg, rgba(38, 19, 12, 0.85) 0%, rgba(20, 15, 28, 0.92) 100%)",
            "HUB_CARD_BG": "rgba(16, 20, 32, 0.85)",
            "HUB_CIRCLE_BG": "linear-gradient(135deg, rgba(255, 87, 34, 0.2), rgba(0, 229, 211, 0.15))",
        }
    else:
        return {
            "BG": "#f8fafc",
            "BG_GRADIENT": "radial-gradient(ellipse at 15% 0%, rgba(255, 87, 34, 0.06) 0%, transparent 55%), radial-gradient(ellipse at 85% 15%, rgba(99, 102, 241, 0.06) 0%, transparent 50%), #f8fafc",
            "SURFACE": "#ffffff",
            "SURFACE2": "#f1f5f9",
            "SURFACE3": "#e2e8f0",
            "BORDER": "rgba(0, 0, 0, 0.12)",
            "BORDER_GLOW": "rgba(234, 88, 12, 0.4)",
            "TEXT": "#0f172a",
            "TEXT_SUB": "#334155",
            "TEXT_MUTED": "#64748b",
            "ACCENT": "#ea580c",
            "ACCENT_HOVER": "#c2410c",
            "ACCENT2": "#0284c7",
            "ACCENT_PURPLE": "#9333ea",
            "ACCENT_AMBER": "#d97706",
            "ACCENT_GREEN": "#059669",
            "CARD_SHADOW": "0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 0 1px 1px rgba(0, 0, 0, 0.05)",
            "IDE_BG": "#f8fafc",
            "ROAST_BOX_BG": "linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)",
            "HUB_CARD_BG": "#ffffff",
            "HUB_CIRCLE_BG": "linear-gradient(135deg, rgba(234, 88, 12, 0.12), rgba(2, 132, 199, 0.12))",
        }


def get_custom_css(dark: bool = True) -> str:
    T = get_theme_tokens(dark)
    primary_shadow = "rgba(255, 87, 34, 0.42)" if dark else "rgba(234, 88, 12, 0.32)"
    primary_hover_shadow = "rgba(255, 87, 34, 0.65)" if dark else "rgba(234, 88, 12, 0.48)"
    badge_glow_bg = "rgba(255, 87, 34, 0.12)" if dark else "rgba(234, 88, 12, 0.1)"
    badge_shadow = "rgba(255, 87, 34, 0.25)" if dark else "rgba(234, 88, 12, 0.15)"
    text_color_area = "#e2e8f0" if dark else "#0f172a"
    focus_shadow = "rgba(255, 87, 34, 0.35)" if dark else "rgba(234, 88, 12, 0.2)"
    roast_shadow = "rgba(255, 87, 34, 0.18)" if dark else "rgba(234, 88, 12, 0.08)"

    return f"""
<style>
  /* ---- GOOGLE FONTS ---- */
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700;800&display=swap');

  /* ---- ROOT APPLICATION CONTAINER ---- */
  html, body, [class*="css"], .stApp {{
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
      background: {T['BG_GRADIENT']} !important;
      background-attachment: fixed !important;
      color: {T['TEXT']} !important;
  }}

  /* ---- ABSOLUTE TEXT CONTRAST IN BOTH MODES ---- */
  .stApp p, .stApp span, .stApp label,
  .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
  div[data-testid="stMarkdownContainer"] p,
  div[data-testid="stMarkdownContainer"] span,
  div[data-testid="stMarkdownContainer"] li,
  div[data-testid="stMarkdownContainer"] h1,
  div[data-testid="stMarkdownContainer"] h2,
  div[data-testid="stMarkdownContainer"] h3,
  div[data-testid="stMarkdownContainer"] h4,
  div[data-testid="stText"],
  div[data-testid="stCaptionContainer"] {{
      color: {T['TEXT']} !important;
  }}

  textarea, code, pre {{
      font-family: 'JetBrains Mono', monospace !important;
  }}

  /* ---- STREAMLIT CLEAN CHROME ---- */
  #MainMenu, footer, header {{ visibility: hidden; height: 0; }}
  .stDeployButton {{ display: none; }}

  /* ---- SCROLLBAR POLISH ---- */
  ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
  ::-webkit-scrollbar-track {{ background: transparent; }}
  ::-webkit-scrollbar-thumb {{ background: {T['SURFACE3']}; border-radius: 99px; }}
  ::-webkit-scrollbar-thumb:hover {{ background: {T['ACCENT']}; }}

  /* ---- COMPLETELY HIDE SIDEBAR & TOGGLE BUTTONS ---- */
  section[data-testid="stSidebar"],
  aside[data-testid="stSidebar"],
  div[data-testid="collapsedControl"],
  [data-testid="stSidebarCollapseButton"],
  [data-testid="stSidebarCollapsedControl"],
  button[data-testid="stSidebarExpandButton"],
  button[data-testid="baseButton-headerNoPadding"],
  button[kind="header"] {{
      display: none !important;
      visibility: hidden !important;
      width: 0 !important;
      height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      pointer-events: none !important;
  }}

  /* Full-width clean container */
  .main .block-container {{
      padding: 1.2rem 2.8rem 3.5rem !important;
      max-width: 100% !important;
  }}

  /* ---- TOP NAVIGATION BAR ---- */
  .cr-navbar-brand {{
      display: flex;
      align-items: center;
      gap: 14px;
  }}

  .cr-nav-logo-box {{
      width: 44px;
      height: 44px;
      border-radius: 12px;
      padding: 2px;
      background: linear-gradient(135deg, {T['ACCENT']}, {T['ACCENT2']});
      box-shadow: 0 4px 14px {'rgba(255, 87, 34, 0.35)' if dark else 'rgba(234, 88, 12, 0.2)'};
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      overflow: hidden;
  }}

  .cr-nav-logo {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 10px;
      display: block;
  }}

  .cr-nav-title {{
      font-family: 'Space Grotesk', sans-serif !important;
      font-size: 1.4rem !important;
      font-weight: 900 !important;
      letter-spacing: 0.8px !important;
      background: linear-gradient(135deg, #ff5722 0%, #ff8a00 50%, #00e5d3 100%);
      -webkit-background-clip: text !important;
      -webkit-text-fill-color: transparent !important;
      background-clip: text !important;
      line-height: 1.15 !important;
  }}

  .cr-nav-subtitle {{
      font-size: 0.65rem !important;
      color: {T['TEXT_MUTED']} !important;
      font-weight: 700 !important;
      letter-spacing: 1.4px !important;
      margin-top: 2px !important;
  }}

  /* ---- DEDICATED THEME CONTROL BOX ON HOME PAGE ---- */
  .cr-home-theme-box {{
      background: {T['SURFACE']} !important;
      border: 1.5px solid {T['BORDER']} !important;
      border-radius: 16px !important;
      padding: 14px 20px !important;
      display: flex !important;
      align-items: center !important;
      gap: 14px !important;
      box-shadow: {T['CARD_SHADOW']} !important;
      height: 100% !important;
  }}

  .cr-home-theme-icon {{
      font-size: 1.8rem !important;
      line-height: 1 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
  }}

  .cr-home-theme-text-title {{
      font-size: 0.95rem !important;
      font-weight: 800 !important;
      color: {T['TEXT']} !important;
      letter-spacing: 0.2px !important;
  }}

  .cr-home-theme-text-sub {{
      font-size: 0.75rem !important;
      color: {T['TEXT_SUB']} !important;
      margin-top: 2px !important;
  }}

  /* ---- UNIQUE LOGO SHOWCASE ---- */
  .cr-logo-wrapper {{
      margin-bottom: 14px;
      text-align: center;
  }}

  .cr-logo-frame {{
      position: relative;
      border-radius: 18px;
      padding: 3px;
      background: linear-gradient(135deg, {T['ACCENT']}, {T['ACCENT2']}, {T['ACCENT_PURPLE']});
      box-shadow: 0 0 24px rgba(255, 87, 34, 0.35), 0 0 10px rgba(0, 229, 211, 0.25);
      overflow: hidden;
      display: inline-block;
      width: 100%;
  }}

  .cr-logo-img {{
      width: 100%;
      height: auto;
      border-radius: 15px;
      display: block;
      filter: contrast(1.05) saturate(1.1);
  }}

  .cr-logo-tag {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      margin-top: 8px;
      font-size: 0.68rem;
      font-weight: 800;
      letter-spacing: 1.5px;
      color: {T['ACCENT2']};
      background: {'rgba(0, 229, 211, 0.08)' if dark else 'rgba(2, 132, 199, 0.08)'};
      border: 1px solid {'rgba(0, 229, 211, 0.25)' if dark else 'rgba(2, 132, 199, 0.2)'};
      padding: 4px 12px;
      border-radius: 20px;
  }}

  /* ---- BRAND TITLE & TAGLINE ---- */
  .cr-brand-container {{
      text-align: center;
      padding: 4px 0 14px;
      margin-bottom: 12px;
      border-bottom: 1px solid {T['BORDER']};
  }}

  .cr-brand-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.7rem;
      font-weight: 900;
      letter-spacing: 1.2px;
      background: linear-gradient(135deg, #ff5722 0%, #ff8a00 50%, #00e5d3 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-shadow: 0 0 20px rgba(255, 87, 34, 0.3);
  }}

  .cr-brand-tagline {{
      font-size: 0.68rem;
      color: {T['TEXT_MUTED']};
      font-weight: 800;
      letter-spacing: 1.8px;
      margin-top: 3px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
  }}

  /* ---- MAIN CONTENT WRAPPER ---- */
  .main .block-container {{
      padding: 1.6rem 2.2rem 2.5rem !important;
      max-width: 100% !important;
  }}

  /* ─────────────────────────────────────────────
     STARTING INTERFACE / HUB CARDS (MATCHING IMAGE)
     ───────────────────────────────────────────── */
  .cr-hub-hero {{
      text-align: center;
      padding: 30px 20px 38px;
      max-width: 820px;
      margin: 0 auto 28px;
  }}

  .cr-hub-top-icon {{
      width: 58px;
      height: 58px;
      border-radius: 16px;
      background: linear-gradient(135deg, {T['ACCENT']}, {T['ACCENT2']});
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 1.8rem;
      box-shadow: 0 10px 24px {'rgba(255, 87, 34, 0.35)' if dark else 'rgba(234, 88, 12, 0.25)'};
      margin-bottom: 16px;
  }}

  .cr-hub-title {{
      font-family: 'Space Grotesk', sans-serif !important;
      font-size: 2.7rem !important;
      font-weight: 900 !important;
      color: {T['TEXT']} !important;
      letter-spacing: -0.5px !important;
      margin-bottom: 12px !important;
      line-height: 1.15 !important;
  }}

  .cr-hub-sub {{
      font-size: 1.1rem !important;
      color: {T['TEXT_SUB']} !important;
      font-weight: 500 !important;
      line-height: 1.6 !important;
  }}

  .cr-hub-card {{
      background: {T['HUB_CARD_BG']} !important;
      border: 1.5px solid {T['BORDER']} !important;
      border-radius: 22px !important;
      padding: 32px 24px 26px !important;
      text-align: center !important;
      box-shadow: {T['CARD_SHADOW']} !important;
      transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
      height: 100% !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
  }}

  .cr-hub-card:hover {{
      transform: translateY(-8px) !important;
      border-color: {T['ACCENT']} !important;
      box-shadow: 0 18px 45px -5px {'rgba(255, 87, 34, 0.28)' if dark else 'rgba(234, 88, 12, 0.18)'} !important;
  }}

  .cr-hub-circle-icon {{
      width: 72px;
      height: 72px;
      border-radius: 50%;
      background: {T['HUB_CIRCLE_BG']};
      border: 2px solid {T['BORDER']};
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 2.2rem;
      margin: 0 auto 18px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
      transition: transform 0.25s ease;
  }}

  .cr-hub-card:hover .cr-hub-circle-icon {{
      transform: scale(1.1) rotate(4deg);
      border-color: {T['ACCENT']};
  }}

  .cr-hub-card-title {{
      font-family: 'Space Grotesk', sans-serif !important;
      font-size: 1.35rem !important;
      font-weight: 800 !important;
      color: {T['TEXT']} !important;
      margin-bottom: 10px !important;
  }}

  .cr-hub-card-desc {{
      font-size: 0.92rem !important;
      color: {T['TEXT_SUB']} !important;
      line-height: 1.6 !important;
      margin-bottom: 22px !important;
      min-height: 66px !important;
  }}

  /* ---- GLASS CARD COMPONENT ---- */
  .cr-card {{
      background: {T['SURFACE']};
      backdrop-filter: blur(20px) saturate(160%);
      -webkit-backdrop-filter: blur(20px) saturate(160%);
      border: 1px solid {T['BORDER']};
      border-radius: 16px;
      padding: 22px 24px;
      margin-bottom: 18px;
      box-shadow: {T['CARD_SHADOW']};
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }}

  .cr-card:hover {{
      border-color: {T['BORDER_GLOW']};
  }}

  /* ---- HEADER HERO COMPONENT ---- */
  .cr-hero {{
      background: {T['SURFACE']};
      backdrop-filter: blur(22px) saturate(180%);
      -webkit-backdrop-filter: blur(22px) saturate(180%);
      border: 1px solid {T['BORDER']};
      border-radius: 18px;
      padding: 18px 24px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: {T['CARD_SHADOW']};
      position: relative;
      overflow: hidden;
  }}

  .cr-hero::after {{
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, {T['ACCENT']}, {T['ACCENT2']}, transparent);
      opacity: 0.8;
  }}

  /* ---- HUD PILL BADGE ---- */
  .cr-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: {T['SURFACE2']};
      border: 1px solid {T['BORDER']};
      padding: 4px 12px;
      border-radius: 99px;
      font-size: 0.76rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: {T['TEXT_SUB']};
  }}

  .cr-badge-glow {{
      background: {badge_glow_bg};
      border-color: {T['ACCENT']};
      color: {T['ACCENT']};
      box-shadow: 0 0 12px {badge_shadow};
  }}

  /* ---- FLAME INTENSITY HUD METER ---- */
  .cr-flame-meter-card {{
      background: {T['SURFACE']};
      border: 1px solid {T['BORDER']};
      border-radius: 14px;
      padding: 12px 18px;
      margin-bottom: 14px;
      box-shadow: {T['CARD_SHADOW']};
  }}

  .cr-flame-track {{
      height: 7px;
      background: {'rgba(255, 255, 255, 0.08)' if dark else 'rgba(0, 0, 0, 0.08)'};
      border-radius: 99px;
      overflow: hidden;
      margin-top: 6px;
      position: relative;
  }}

  .cr-flame-fill {{
      height: 100%;
      width: 92%;
      background: linear-gradient(90deg, #ffbd2e 0%, #ff5722 50%, #ff1744 100%);
      box-shadow: 0 0 12px #ff5722;
      border-radius: 99px;
      animation: flamePulse 2s ease-in-out infinite alternate;
  }}

  @keyframes flamePulse {{
      0% {{ opacity: 0.85; filter: brightness(1); }}
      100% {{ opacity: 1; filter: brightness(1.25); }}
  }}

  /* ---- PERSONA LIVE PREVIEW CARD ---- */
  .cr-persona-preview {{
      background: {T['SURFACE2']};
      border: 1px solid {T['BORDER']};
      border-radius: 12px;
      padding: 10px 16px;
      margin-top: 8px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
      transition: all 0.2s ease;
  }}

  .cr-persona-preview:hover {{
      border-color: {T['BORDER_GLOW']};
  }}

  /* ---- IDE EDITOR FRAME ---- */
  .cr-ide-frame {{
      background: {T['IDE_BG']};
      border: 1px solid {T['BORDER']};
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 12px;
      box-shadow: {T['CARD_SHADOW']};
  }}

  .cr-ide-titlebar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 16px;
      background: {T['SURFACE2']};
      border-bottom: 1px solid {T['BORDER']};
  }}

  .cr-ide-dots {{
      display: flex;
      gap: 7px;
      align-items: center;
  }}

  .cr-dot {{
      width: 11px;
      height: 11px;
      border-radius: 50%;
      display: inline-block;
  }}

  .cr-dot-red    {{ background: #ff5f56; }}
  .cr-dot-yellow {{ background: #ffbd2e; }}
  .cr-dot-green  {{ background: #27c93f; }}

  /* ---- STICKER TROPHY CARD ---- */
  .cr-sticker {{
      border-radius: 18px;
      padding: 30px 22px;
      text-align: center;
      border: 1px solid rgba(255, 255, 255, 0.18);
      position: relative;
      overflow: hidden;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.35);
      backdrop-filter: blur(14px);
  }}

  .cr-sticker::before {{
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, transparent 60%);
      pointer-events: none;
  }}

  .cr-sticker-emoji {{
      font-size: 3.8rem;
      filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));
      animation: floatBob 3.2s ease-in-out infinite;
      display: inline-block;
  }}

  @keyframes floatBob {{
      0%, 100% {{ transform: translateY(0) rotate(0deg); }}
      50% {{ transform: translateY(-9px) rotate(2deg); }}
  }}

  .cr-sticker-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.55rem;
      font-weight: 900;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin: 8px 0 4px;
      text-shadow: 0 3px 10px rgba(0,0,0,0.3);
  }}

  .cr-sticker-sub {{
      font-size: 0.95rem;
      opacity: 0.92;
      margin-bottom: 12px;
      font-weight: 500;
  }}

  .cr-sticker-tag {{
      display: inline-block;
      background: rgba(0,0,0,0.35);
      border: 1px solid rgba(255,255,255,0.4);
      padding: 4px 16px;
      border-radius: 30px;
      font-size: 0.8rem;
      font-weight: 800;
      letter-spacing: 1px;
  }}

  /* ---- HEALTH METER CARD ---- */
  .cr-health {{
      background: {T['SURFACE']};
      backdrop-filter: blur(20px);
      border: 1px solid {T['BORDER']};
      border-radius: 18px;
      padding: 24px;
      text-align: center;
      box-shadow: {T['CARD_SHADOW']};
      display: flex;
      flex-direction: column;
      justify-content: center;
      height: 100%;
  }}

  /* ---- AUDIO WAVE INTERCEPTOR ---- */
  .cr-audio-wave {{
      display: inline-flex;
      align-items: center;
      gap: 3px;
      height: 14px;
  }}
  .cr-audio-wave span {{
      width: 3px;
      background: {T['ACCENT']};
      border-radius: 3px;
      animation: waveBar 1.2s ease-in-out infinite alternate;
  }}
  .cr-audio-wave span:nth-child(1) {{ height: 5px; animation-delay: 0.1s; }}
  .cr-audio-wave span:nth-child(2) {{ height: 12px; animation-delay: 0.3s; }}
  .cr-audio-wave span:nth-child(3) {{ height: 8px; animation-delay: 0.2s; }}
  .cr-audio-wave span:nth-child(4) {{ height: 14px; animation-delay: 0.4s; }}
  .cr-audio-wave span:nth-child(5) {{ height: 6px; animation-delay: 0.15s; }}

  @keyframes waveBar {{
      0% {{ transform: scaleY(0.4); }}
      100% {{ transform: scaleY(1.3); }}
  }}

  /* ---- ROAST VERDICT BOX ---- */
  .cr-roast {{
      background: {T['ROAST_BOX_BG']};
      border: 1px solid {'rgba(255, 87, 34, 0.35)' if dark else 'rgba(234, 88, 12, 0.3)'};
      border-left: 5px solid {T['ACCENT']};
      border-radius: 16px;
      padding: 22px 26px;
      color: {'#fff3e0' if dark else '#431407'};
      font-size: 1.05rem;
      line-height: 1.78;
      box-shadow: 0 8px 24px {roast_shadow};
      position: relative;
  }}

  /* ---- ISSUE ACCORDION CARD ---- */
  .cr-issue {{
      background: {T['SURFACE']};
      border: 1px solid {T['BORDER']};
      border-radius: 14px;
      padding: 16px 20px;
      margin-bottom: 12px;
      box-shadow: {T['CARD_SHADOW']};
      transition: transform 0.18s ease, border-color 0.18s ease;
  }}

  .cr-issue:hover {{
      transform: translateY(-2px);
      border-color: {T['BORDER_GLOW']};
  }}

  /* ---- PREDICTION KPI BOX ---- */
  .cr-pred-box {{
      border-radius: 16px;
      padding: 22px;
      border-width: 2px;
      border-style: solid;
      box-shadow: {T['CARD_SHADOW']};
  }}

  /* ---- FORM INPUTS & BUTTONS POLISH ---- */
  div[data-testid="stButton"] button {{
      border-radius: 12px !important;
      font-weight: 700 !important;
      padding: 0.55rem 1.4rem !important;
      letter-spacing: 0.3px !important;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
      border: 1px solid {T['BORDER']} !important;
  }}

  div[data-testid="stButton"] button[kind="primary"] {{
      background: linear-gradient(135deg, {T['ACCENT']} 0%, #ff8a00 100%) !important;
      color: #ffffff !important;
      border: none !important;
      box-shadow: 0 4px 18px {primary_shadow} !important;
  }}

  div[data-testid="stButton"] button[kind="primary"]:hover {{
      transform: translateY(-2px) !important;
      box-shadow: 0 6px 24px {primary_hover_shadow} !important;
  }}

  div[data-testid="stButton"] button[kind="secondary"]:hover {{
      border-color: {T['ACCENT']} !important;
      color: {T['ACCENT']} !important;
      transform: translateY(-1px) !important;
  }}

  /* ---- SELECTBOX DROPDOWN STYLING ---- */
  div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
      background: {T['SURFACE2']} !important;
      border: 1px solid {T['BORDER']} !important;
      border-radius: 12px !important;
      color: {T['TEXT']} !important;
      font-weight: 600 !important;
      transition: all 0.2s ease !important;
  }}

  div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {{
      border-color: {T['ACCENT']} !important;
  }}

  div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {{
      border-color: {T['ACCENT']} !important;
      box-shadow: 0 0 0 2px {focus_shadow} !important;
  }}

  /* ---- TEXTAREA (CODE EDITOR) ---- */
  textarea {{
      background: {T['IDE_BG']} !important;
      color: {text_color_area} !important;
      border: 1px solid {T['BORDER']} !important;
      border-radius: 12px !important;
      font-size: 0.94rem !important;
      line-height: 1.65 !important;
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.25) !important;
  }}

  textarea:focus {{
      border-color: {T['ACCENT']} !important;
      box-shadow: 0 0 0 2px {focus_shadow} !important;
  }}

  /* ---- EXPANDERS ---- */
  details {{
      background: {T['SURFACE']} !important;
      border: 1px solid {T['BORDER']} !important;
      border-radius: 12px !important;
      margin-bottom: 10px !important;
  }}

  details summary {{
      cursor: pointer !important;
      font-weight: 700 !important;
      color: {T['TEXT']} !important;
      padding: 14px 18px !important;
  }}

  details summary:hover {{
      color: {T['ACCENT']} !important;
  }}

  /* ---- PULSE GLOW ANIMATION ---- */
  @keyframes livePulse {{
      0% {{ transform: scale(0.95); opacity: 0.7; }}
      50% {{ transform: scale(1.15); opacity: 1; }}
      100% {{ transform: scale(0.95); opacity: 0.7; }}
  }}
  .a-live-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: {T['ACCENT_GREEN']};
      box-shadow: 0 0 8px {T['ACCENT_GREEN']};
      display: inline-block;
      animation: livePulse 2s infinite ease-in-out;
  }}

  /* ---- ARENA DUEL BOXES & CARDS ---- */
  .cr-duel-card {{
      background: rgba(18, 22, 34, 0.75);
      border: 1.5px solid rgba(255, 255, 255, 0.1);
      border-radius: 18px;
      padding: 20px;
      margin-bottom: 16px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.3);
  }}

  .cr-vs-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 54px;
      height: 54px;
      border-radius: 50%;
      background: linear-gradient(135deg, #ff5722 0%, #ff8a00 100%);
      color: #ffffff;
      font-weight: 900;
      font-size: 1.1rem;
      box-shadow: 0 0 20px rgba(255, 87, 34, 0.5);
      animation: vsPulse 2s ease-in-out infinite;
  }}

  @keyframes vsPulse {{
      0%, 100% {{ transform: scale(1); box-shadow: 0 0 16px rgba(255, 87, 34, 0.4); }}
      50% {{ transform: scale(1.12); box-shadow: 0 0 30px rgba(255, 87, 34, 0.8); }}
  }}

  .cr-shame-card {{
      background: rgba(18, 22, 34, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 18px;
      padding: 22px 24px;
      margin-bottom: 18px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
      transition: transform 0.2s ease, border-color 0.2s ease;
  }}

  .cr-shame-card:hover {{
      transform: translateY(-4px);
      border-color: rgba(255, 87, 34, 0.4);
  }}

  .cr-badge-card {{
      background: rgba(18, 22, 34, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 22px 20px;
      text-align: center;
      transition: all 0.25s ease;
      height: 100%;
  }}

  .cr-badge-card:hover {{
      transform: translateY(-6px);
      border-color: #00e5d3;
      box-shadow: 0 12px 30px rgba(0, 229, 211, 0.2);
  }}
</style>
"""
