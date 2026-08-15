import streamlit as st

def apply_custom_styles(theme: str = "dark"):
    """Injects custom CSS theme styling for FIFA 2026 Analytics Dashboard."""
    
    if theme == "dark":
        bg_primary = "#0b0f19"
        bg_secondary = "rgba(18, 26, 44, 0.7)"
        border_color = "rgba(0, 242, 254, 0.2)"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        accent_neon = "#00f2fe"
        accent_emerald = "#10b981"
        accent_gold = "#fbbf24"
        accent_purple = "#8b5cf6"
        card_glow = "0 8px 32px 0 rgba(0, 242, 254, 0.15)"
    else:
        bg_primary = "#f8fafc"
        bg_secondary = "rgba(255, 255, 255, 0.85)"
        border_color = "rgba(15, 23, 42, 0.12)"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        accent_neon = "#0284c7"
        accent_emerald = "#059669"
        accent_gold = "#d97706"
        accent_purple = "#7c3aed"
        card_glow = "0 8px 24px 0 rgba(15, 23, 42, 0.08)"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    h1, h2, h3, .hero-title {{
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }}

    /* Main Container Background */
    .stApp {{
        background: {bg_primary};
        color: {text_primary};
    }}

    /* Glassmorphism KPI Card */
    .fifa-kpi-card {{
        background: {bg_secondary};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: {card_glow};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}

    .fifa-kpi-card:hover {{
        transform: translateY(-4px);
        border-color: {accent_neon};
        box-shadow: 0 12px 40px 0 rgba(0, 242, 254, 0.25);
    }}

    .fifa-kpi-title {{
        font-size: 0.825rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {text_secondary};
        margin-bottom: 0.35rem;
    }}

    .fifa-kpi-val {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {text_primary};
        line-height: 1.1;
        font-family: 'Outfit', sans-serif;
    }}

    .fifa-kpi-subtitle {{
        font-size: 0.75rem;
        color: {accent_emerald};
        margin-top: 0.35rem;
        font-weight: 500;
    }}

    /* Hero Banner */
    .fifa-hero {{
        background: linear-gradient(135deg, rgba(11,15,25,0.95) 0%, rgba(26,38,66,0.9) 100%),
                    radial-gradient(circle at top right, rgba(0,242,254,0.15), transparent 40%);
        border: 1px solid {border_color};
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: {card_glow};
    }}

    .fifa-hero h1 {{
        color: #ffffff;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #ffffff 0%, {accent_neon} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .fifa-hero p {{
        color: {text_secondary};
        font-size: 1.05rem;
        max-width: 700px;
        margin: 0;
    }}

    /* Custom Badges */
    .badge {{
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 0.4rem;
    }}

    .badge-primary {{ background: rgba(0, 242, 254, 0.15); color: {accent_neon}; border: 1px solid rgba(0,242,254,0.3); }}
    .badge-success {{ background: rgba(16, 185, 129, 0.15); color: {accent_emerald}; border: 1px solid rgba(16,185,129,0.3); }}
    .badge-warning {{ background: rgba(251, 191, 36, 0.15); color: {accent_gold}; border: 1px solid rgba(251,191,36,0.3); }}
    .badge-purple {{ background: rgba(139, 92, 246, 0.15); color: {accent_purple}; border: 1px solid rgba(139,92,246,0.3); }}

    /* Scoreboard */
    .scoreboard-box {{
        background: {bg_secondary};
        border: 1px solid {border_color};
        border-radius: 20px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: {card_glow};
    }}

    .score-display {{
        font-size: 3rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        color: {accent_neon};
        margin: 0.5rem 0;
    }}

    /* Hide Default Streamlit Menu / Header padding tweak */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_kpi_card(
    title: str,
    value: str,
    subtitle: str = "",
    badge: str = "",
    theme: str = "dark"
):
    """Render a styled FIFA KPI card."""

    badge_html = (
        f'<span class="badge badge-primary">{badge}</span>'
        if badge
        else ""
    )

    subtitle_html = (
        f'<div class="fifa-kpi-subtitle">{subtitle}</div>'
        if subtitle
        else ""
    )

    html = f"""
    <div class="fifa-kpi-card">
        <div class="fifa-kpi-header">
            <div class="fifa-kpi-title">{title}</div>
            {badge_html}
        </div>

        <div class="fifa-kpi-val">{value}</div>

        {subtitle_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
