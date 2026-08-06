import streamlit as st
import pandas as pd
from utils.loader import load_data, get_player_career_summary
from utils.styles import apply_custom_styles, render_kpi_card
from utils.filters import render_sidebar_filters
from utils.metrics import recommend_ai_players
from utils.charts import plot_radar_chart

st.set_page_config(page_title="AI Player Scout | FIFA 2026", page_icon="🤖", layout="wide")
theme = st.session_state.get("theme", "dark")
apply_custom_styles(theme)

df = load_data()

st.markdown("""
<div class="fifa-hero">
    <h1>🤖 AI Player Scout Engine</h1>
    <p>Specify target recruitment parameters and let our Cosine Similarity & Nearest Neighbors AI engine find the highest matching talent across the tournament.</p>
</div>
""", unsafe_allow_html=True)

# Interactive Form Inputs
with st.container():
    st.subheader("🎯 Configure Scouting Target Criteria")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        target_pos = st.selectbox("Target Position", ["All", "Forward", "Midfielder", "Defender", "Goalkeeper", "ST", "CAM", "RW", "LW", "CM", "CDM", "CB", "RB", "LB", "GK"], index=1)
        target_foot = st.selectbox("Preferred Foot", ["Any", "Right", "Left"], index=0)
        
    with c2:
        max_age = st.slider("Maximum Age", 16, 40, 35)
        max_mv = st.slider("Max Market Value (€M)", 1.0, 200.0, 150.0, step=5.0)
        
    with c3:
        min_rating = st.slider("Minimum Avg Rating", 1.0, 10.0, 3.0, step=0.1)
        min_perf = st.slider("Minimum Performance Score", 0.0, 100.0, 30.0, step=5.0)
        
    with c4:
        st.markdown("#### Scouting Engine")
        scout_btn = st.button("🚀 Run AI Scouting Search", use_container_width=True, type="primary")

st.divider()

# Run Recommendation Algorithm
scout_results = recommend_ai_players(
    df,
    position=target_pos,
    max_age=max_age,
    max_market_val_m=max_mv,
    preferred_foot=target_foot,
    min_rating=min_rating,
    min_perf=min_perf,
    top_n=10
)

if len(scout_results) == 0:
    st.warning("No players matched the specified AI scout parameters. Try broadening your filter ranges.")
    st.stop()

st.subheader(f"✨ Top 10 Recommended Matches ({target_pos} Role)")

# Render Scout Cards & Table
for i, row in scout_results.head(3).iterrows():
    col_card, col_radar = st.columns([1.2, 1])
    
    with col_card:
        sim_val = row['Similarity_Score']
        badge_cls = "badge-success" if sim_val >= 85 else "badge-primary"
        
        st.markdown(f"""
        <div class="fifa-kpi-card" style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0;">#{i+1} {row['player_name']}</h3>
                <span class="badge {badge_cls}" style="font-size: 1rem; padding: 0.4rem 0.8rem;">{sim_val}% AI Match</span>
            </div>
            <p style="margin: 0.5rem 0; color: #94a3b8;">
                <strong>Club:</strong> {row.get('club_name', 'N/A')} | <strong>Team:</strong> {row.get('team', 'N/A')} | <strong>Age:</strong> {row.get('age', 'N/A')}
            </p>
            <div style="display: flex; gap: 1.5rem; margin-top: 1rem;">
                <div>Avg Rating: <strong>{row.get('player_rating', 0):.2f}</strong></div>
                <div>Goals: <strong>{row.get('goals', 0)}</strong></div>
                <div>Assists: <strong>{row.get('assists', 0)}</strong></div>
                <div>Market Val: <strong>€{row.get('market_value_eur', 0)/1e6:.1f}M</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_radar:
        cats = ['Pass Accuracy', 'Rating', 'Goals', 'Assists', 'Distance', 'Top Speed']
        vals = [
            min(100, float(row.get('pass_accuracy', 50))),
            float(row.get('player_rating', 5)) * 10,
            min(100, float(row.get('goals', 0)) * 20),
            min(100, float(row.get('assists', 0)) * 20),
            min(100, float(row.get('distance_covered_km', 5)) * 5),
            min(100, float(row.get('top_speed_kmh', 25)) * 2.5)
        ]
        fig_r = plot_radar_chart(cats, vals, name=row['player_name'], theme=theme)
        st.plotly_chart(fig_r, use_container_width=True)

st.divider()

# Recommendation Table
st.subheader("📋 Complete Recommended Scout Candidates")

disp_rec = scout_results[['player_name', 'club_name', 'team', 'position', 'age', 'player_rating', 'goals', 'assists', 'market_value_eur', 'Similarity_Score']].copy()
disp_rec['market_value_eur'] = disp_rec['market_value_eur'].apply(lambda x: f"€{x/1e6:.1f}M")
disp_rec['player_rating'] = disp_rec['player_rating'].round(2)
disp_rec.rename(columns={
    'player_name': 'Player', 'club_name': 'Club', 'team': 'Team', 'position': 'Pos',
    'age': 'Age', 'player_rating': 'Rating', 'goals': 'Goals', 'assists': 'Assists',
    'market_value_eur': 'Market Value', 'Similarity_Score': 'AI Match %'
}, inplace=True)

st.dataframe(disp_rec, use_container_width=True, hide_index=True)
