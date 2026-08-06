import streamlit as st
import pandas as pd
import plotly.express as px
from utils.loader import load_data
from utils.styles import apply_custom_styles, render_kpi_card
from utils.filters import render_sidebar_filters

st.set_page_config(page_title="Match Analysis | FIFA 2026", page_icon="⚔️", layout="wide")
theme = st.session_state.get("theme", "dark")
apply_custom_styles(theme)

df = load_data()
filtered_df = render_sidebar_filters(df)

st.title("⚔️ Match Performance Breakdown")

if 'match_id' not in filtered_df.columns:
    st.warning("Match ID column missing.")
    st.stop()

# Group match options nicely
match_ids = filtered_df['match_id'].unique()
if len(match_ids) == 0:
    st.warning("No matches available with current sidebar filters.")
    st.stop()

# Create human-readable match selectbox titles
match_options = {}
for m_id in match_ids:
    m_sub = df[df['match_id'] == m_id]
    if len(m_sub) > 0:
        team_a = m_sub['team'].iloc[0]
        team_b = m_sub['opponent_team'].iloc[0]
        stage = m_sub['tournament_stage'].iloc[0]
        label = f"{m_id}: {team_a} vs {team_b} ({stage})"
        match_options[label] = m_id

selected_label = st.selectbox("🏟️ Select Match", list(match_options.keys()), index=0)
selected_match_id = match_options[selected_label]

match_df = df[df['match_id'] == selected_match_id]

if len(match_df) == 0:
    st.warning("No data found for selected match.")
    st.stop()

team_a = match_df['team'].iloc[0]
team_b = match_df['opponent_team'].iloc[0]
stage = match_df['tournament_stage'].iloc[0]

# Calculate match score
goals_a = match_df[match_df['team'] == team_a]['goals'].sum() if 'goals' in match_df else 0
goals_b = match_df[match_df['team'] == team_b]['goals'].sum() if 'goals' in match_df else 0

# Scoreboard Component
st.markdown(f"""
<div class="scoreboard-box">
    <div style="font-size: 0.9rem; text-transform: uppercase; color: #94a3b8; font-weight: 600;">{stage}</div>
    <div style="display: flex; justify-content: center; align-items: center; gap: 2rem;">
        <div style="font-size: 1.8rem; font-weight: 700;">{team_a}</div>
        <div class="score-display">{goals_a} - {goals_b}</div>
        <div style="font-size: 1.8rem; font-weight: 700;">{team_b}</div>
    </div>
    <div style="font-size: 0.85rem; color: #10b981; margin-top: 0.5rem;">
        Stadium: {match_df['stadium'].iloc[0] if 'stadium' in match_df else 'FIFA Stadium'} | City: {match_df['city'].iloc[0] if 'city' in match_df else 'Host City'}
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Row 1: Player Ratings Bar Chart & Performance Scatter Plot
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    fig_ratings = px.bar(
        match_df.sort_values('player_rating', ascending=True),
        y='player_name', x='player_rating', color='team', orientation='h',
        title="<b>Player Match Ratings</b>", color_discrete_sequence=['#00f2fe', '#fbbf24']
    )
    fig_ratings.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_ratings, use_container_width=True)

with r1_c2:
    fig_scatter = px.scatter(
        match_df, x='expected_goals_xg', y='performance_score', size='player_rating', color='team',
        hover_data=['player_name', 'goals', 'assists'],
        title="<b>xG vs Performance Score Scatter</b>", color_discrete_sequence=['#00f2fe', '#fbbf24']
    )
    fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# Row 2: Offensive & Defensive Contributions
r2_c1, r2_c2 = st.columns(2)

with r2_c1:
    fig_off = px.bar(
        match_df.sort_values('offensive_contribution', ascending=False).head(10),
        x='player_name', y='offensive_contribution', color='team',
        title="<b>Top Offensive Contributions</b>", color_discrete_sequence=['#10b981', '#ec4899']
    )
    fig_off.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_off, use_container_width=True)

with r2_c2:
    fig_def = px.bar(
        match_df.sort_values('defensive_contribution', ascending=False).head(10),
        x='player_name', y='defensive_contribution', color='team',
        title="<b>Top Defensive Contributions</b>", color_discrete_sequence=['#8b5cf6', '#3b82f6']
    )
    fig_def.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_def, use_container_width=True)

st.divider()

# Match Statistics Table
st.subheader("📋 Match Player Performance Table")
disp_cols = [
    'player_name', 'team', 'position', 'minutes_played', 'goals', 'assists',
    'shots', 'shots_on_target', 'expected_goals_xg', 'pass_accuracy',
    'tackles', 'distance_covered_km', 'top_speed_kmh', 'player_rating', 'performance_score'
]
actual_disp = [c for c in disp_cols if c in match_df.columns]
st.dataframe(match_df[actual_disp], use_container_width=True, hide_index=True)
