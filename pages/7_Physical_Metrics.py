import streamlit as st
import pandas as pd
import plotly.express as px
from utils.loader import load_data
from utils.styles import apply_custom_styles, render_kpi_card
from utils.filters import render_sidebar_filters
from utils.charts import plot_speed_vs_acceleration

st.set_page_config(page_title="Physical Metrics | FIFA 2026", page_icon="⚡", layout="wide")
theme = st.session_state.get("theme", "dark")
apply_custom_styles(theme)

df = load_data()
filtered_df = render_sidebar_filters(df)

st.title("⚡ Physical Performance & Fitness Dashboard")

# Physical KPIs
k1, k2, k3, k4, k5, k6 = st.columns(6)

avg_dist = filtered_df['distance_covered_km'].mean() if 'distance_covered_km' in filtered_df else 0.0
avg_sprint = filtered_df['sprint_distance_km'].mean() if 'sprint_distance_km' in filtered_df else 0.0
max_speed = filtered_df['top_speed_kmh'].max() if 'top_speed_kmh' in filtered_df else 0.0
avg_accel = filtered_df['accelerations'].mean() if 'accelerations' in filtered_df else 0.0
avg_decel = filtered_df['decelerations'].mean() if 'decelerations' in filtered_df else 0.0
avg_stamina = filtered_df['stamina_score'].mean() if 'stamina_score' in filtered_df else 0.0

with k1:
    render_kpi_card("Avg Distance", f"{avg_dist:.2f} km", theme=theme)

with k2:
    render_kpi_card("Sprint Distance", f"{avg_sprint:.2f} km", theme=theme)

with k3:
    render_kpi_card("Top Speed", f"{max_speed:.1f} km/h", theme=theme)

with k4:
    render_kpi_card("Avg Accel", f"{avg_accel:.1f}", theme=theme)

with k5:
    render_kpi_card("Avg Decel", f"{avg_decel:.1f}", theme=theme)

with k6:
    render_kpi_card("Stamina Score", f"{avg_stamina:.1f}", theme=theme)

st.divider()

# Row 1: Top Fastest Players & Distance Covered
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    fastest = filtered_df.groupby('player_name')['top_speed_kmh'].max().reset_index().sort_values('top_speed_kmh', ascending=True).tail(15)
    fig_fast = px.bar(fastest, y='player_name', x='top_speed_kmh', orientation='h',
                      color='top_speed_kmh', color_continuous_scale=['#065f46', '#10b981', '#00f2fe'],
                      title="<b>🚀 Top 15 Fastest Players (Top Speed km/h)</b>")
    fig_fast.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_fast, use_container_width=True)

with r1_c2:
    dist_df = filtered_df.groupby('player_name')['distance_covered_km'].mean().reset_index().sort_values('distance_covered_km', ascending=True).tail(15)
    fig_dist = px.bar(dist_df, y='player_name', x='distance_covered_km', orientation='h',
                      color='distance_covered_km', color_continuous_scale=['#4c1d95', '#8b5cf6'],
                      title="<b>🏃 Top 15 Highest Distance Covered (Avg km)</b>")
    fig_dist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_dist, use_container_width=True)

st.divider()

# Row 2: Sprint Distribution & Stamina by Position Box Plot
r2_c1, r2_c2 = st.columns(2)

with r2_c1:
    fig_sprint_hist = px.histogram(filtered_df, x='sprint_distance_km', nbins=30, color='position',
                                   title="<b>Sprint Distance Distribution</b>")
    fig_sprint_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_sprint_hist, use_container_width=True)

with r2_c2:
    fig_stamina_box = px.box(filtered_df, x='position', y='stamina_score', color='position',
                             title="<b>Stamina Score by Position Role</b>")
    fig_stamina_box.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_stamina_box, use_container_width=True)

st.divider()

# Row 3: Speed Distribution & Acceleration vs Performance
r3_c1, r3_c2 = st.columns(2)

with r3_c1:
    fig_speed_hist = px.histogram(filtered_df, x='top_speed_kmh', nbins=25, color_discrete_sequence=['#00f2fe'],
                                  title="<b>Top Speed Distribution (km/h)</b>")
    fig_speed_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_speed_hist, use_container_width=True)

with r3_c2:
    fig_accel_perf = plot_speed_vs_acceleration(filtered_df, theme=theme)
    st.plotly_chart(fig_accel_perf, use_container_width=True)
