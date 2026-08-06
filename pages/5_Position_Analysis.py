import streamlit as st
import pandas as pd
import plotly.express as px
from utils.loader import load_data
from utils.styles import apply_custom_styles, render_kpi_card
from utils.filters import render_sidebar_filters
from utils.charts import plot_parallel_coordinates, plot_radar_chart

st.set_page_config(page_title="Position Analysis | FIFA 2026", page_icon="🎯", layout="wide")
theme = st.session_state.get("theme", "dark")
apply_custom_styles(theme)

df = load_data()
filtered_df = render_sidebar_filters(df)

st.title("🎯 Position-Based Metrics & Distribution")

POS_MAP = {
    'ST': ['Forward'], 'RW': ['Forward'], 'LW': ['Forward'],
    'CAM': ['Midfielder'], 'CM': ['Midfielder'], 'CDM': ['Midfielder'],
    'CB': ['Defender'], 'RB': ['Defender'], 'LB': ['Defender'],
    'GK': ['Goalkeeper'],
    'Forward': ['Forward'], 'Midfielder': ['Midfielder'],
    'Defender': ['Defender'], 'Goalkeeper': ['Goalkeeper']
}

positions = ["All", "Forward", "Midfielder", "Defender", "Goalkeeper", "ST", "CAM", "RW", "LW", "CM", "CDM", "CB", "RB", "LB", "GK"]
sel_pos = st.radio(" Choose Position Role:", positions, horizontal=True)

if sel_pos == "All":
    pos_df = filtered_df
else:
    target_pos = POS_MAP.get(sel_pos, [sel_pos])
    pos_df = filtered_df[filtered_df['position'].isin(target_pos)]

if len(pos_df) == 0:
    st.warning("No players found for selected position criteria.")
    st.stop()

# Position KPIs
k1, k2, k3, k4, k5, k6 = st.columns(6)

avg_rating = pos_df['player_rating'].mean() if 'player_rating' in pos_df else 0.0
avg_goals = pos_df['goals'].mean() if 'goals' in pos_df else 0.0
avg_tackles = pos_df['tackles'].mean() if 'tackles' in pos_df else 0.0
avg_pass_acc = pos_df['pass_accuracy'].mean() if 'pass_accuracy' in pos_df else 0.0
avg_xg = pos_df['expected_goals_xg'].mean() if 'expected_goals_xg' in pos_df else 0.0
avg_creativity = pos_df['creativity_score'].mean() if 'creativity_score' in pos_df else 0.0

with k1: render_kpi_card("Avg Rating", f"{avg_rating:.2f}", theme=theme)
with k2: render_kpi_card("Avg Goals/Match", f"{avg_goals:.2f}", theme=theme)
with k3: render_kpi_card("Avg Tackles", f"{avg_tackles:.2f}", theme=theme)
with k4: render_kpi_card("Pass Accuracy", f"{avg_pass_acc:.1f}%", theme=theme)
with k5: render_kpi_card("Avg xG", f"{avg_xg:.2f}", theme=theme)
with k6: render_kpi_card("Creativity Score", f"{avg_creativity:.1f}", theme=theme)

st.divider()

# Row 1: Box Plot & Violin Plot
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    fig_box = px.box(pos_df, x='position', y='player_rating', color='position',
                     title="<b>Rating Box Plot by Position</b>")
    fig_box.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_box, use_container_width=True)

with r1_c2:
    fig_violin = px.violin(pos_df, x='position', y='player_rating', color='position', box=True, points="outliers",
                           title="<b>Rating Violin Spread Plot</b>")
    fig_violin.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_violin, use_container_width=True)

st.divider()

# Row 2: Average Metrics Radar Chart & Parallel Coordinates
r2_c1, r2_c2 = st.columns([1, 1.2])

with r2_c1:
    st.subheader("🕸️ Position Benchmark Radar")
    categories = ['Passing', 'Creativity', 'Defending', 'Offense', 'Pressure', 'Consistency', 'Clutch']
    vals = [
        float(pos_df['pass_accuracy'].mean() if 'pass_accuracy' in pos_df else 50),
        float(pos_df['creativity_score'].mean() if 'creativity_score' in pos_df else 50),
        float(pos_df['defensive_contribution'].mean() if 'defensive_contribution' in pos_df else 5) * 10,
        float(pos_df['offensive_contribution'].mean() if 'offensive_contribution' in pos_df else 5) * 10,
        float(pos_df['pressure_resistance'].mean() if 'pressure_resistance' in pos_df else 50),
        float(pos_df['consistency_score'].mean() if 'consistency_score' in pos_df else 50),
        float(pos_df['clutch_performance_score'].mean() if 'clutch_performance_score' in pos_df else 50)
    ]
    fig_radar = plot_radar_chart(categories, vals, name=f"{sel_pos} Role Benchmark", theme=theme)
    st.plotly_chart(fig_radar, use_container_width=True)

with r2_c2:
    st.subheader("🔀 Multi-Metric Parallel Coordinates")
    fig_par = plot_parallel_coordinates(pos_df, theme=theme)
    st.plotly_chart(fig_par, use_container_width=True)
