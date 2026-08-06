import streamlit as st
import pandas as pd
from utils.loader import load_data
from utils.styles import apply_custom_styles, render_kpi_card
from utils.filters import render_sidebar_filters
from utils.charts import (
    plot_goals_by_team, plot_match_results_distribution, plot_tournament_stage_distribution,
    plot_top_scorers, plot_highest_rated_players, plot_rating_by_position_box,
    plot_market_value_distribution, plot_correlation_heatmap
)

st.set_page_config(page_title="Overview | FIFA 2026", page_icon="📊", layout="wide")
theme = st.session_state.get("theme", "dark")
apply_custom_styles(theme)

df = load_data()
filtered_df = render_sidebar_filters(df)

st.title("📊 FIFA World Cup 2026 - Overview Dashboard")
st.caption("High-level tournament KPIs, scoring distributions, team summaries, and feature correlations.")

# KPI Cards Row
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6, kpi7, kpi8 = st.columns(8)

total_players = filtered_df['player_name'].nunique() if 'player_name' in filtered_df else 0
total_matches = filtered_df['match_id'].nunique() if 'match_id' in filtered_df else 0
total_teams = filtered_df['team'].nunique() if 'team' in filtered_df else 0
total_goals = int(filtered_df['goals'].sum()) if 'goals' in filtered_df else 0
avg_rating = filtered_df['player_rating'].mean() if 'player_rating' in filtered_df else 0.0
avg_xg = filtered_df['expected_goals_xg'].mean() if 'expected_goals_xg' in filtered_df else 0.0
avg_perf = filtered_df['performance_score'].mean() if 'performance_score' in filtered_df else 0.0
avg_pass_acc = filtered_df['pass_accuracy'].mean() if 'pass_accuracy' in filtered_df else 0.0

with kpi1:
    render_kpi_card("Players", f"{total_players:,}", badge="Total", theme=theme)
with kpi2:
    render_kpi_card("Matches", f"{total_matches:,}", badge="Matches", theme=theme)
with kpi3:
    render_kpi_card("Teams", f"{total_teams:,}", badge="Teams", theme=theme)
with kpi4:
    render_kpi_card("Goals", f"{total_goals:,}", badge="Goals", theme=theme)
with kpi5:
    render_kpi_card("Avg Rating", f"{avg_rating:.2f}", badge="Score", theme=theme)
with kpi6:
    render_kpi_card("Avg xG", f"{avg_xg:.2f}", badge="xG", theme=theme)
with kpi7:
    render_kpi_card("Perf Score", f"{avg_perf:.1f}", badge="Perf", theme=theme)
with kpi8:
    render_kpi_card("Pass Acc", f"{avg_pass_acc:.1f}%", badge="Pass", theme=theme)

st.divider()

# Row 1 Charts: Goals by Team & Distributions
row1_col1, row1_col2, row1_col3 = st.columns([1.5, 1, 1])

with row1_col1:
    fig_goals_team = plot_goals_by_team(filtered_df, top_n=15, theme=theme)
    st.plotly_chart(fig_goals_team, use_container_width=True)

with row1_col2:
    fig_results = plot_match_results_distribution(filtered_df, theme=theme)
    st.plotly_chart(fig_results, use_container_width=True)

with row1_col3:
    fig_stages = plot_tournament_stage_distribution(filtered_df, theme=theme)
    st.plotly_chart(fig_stages, use_container_width=True)

st.divider()

# Row 2 Charts: Top Performers & Position Box Plot
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    fig_scorers = plot_top_scorers(filtered_df, top_n=15, theme=theme)
    st.plotly_chart(fig_scorers, use_container_width=True)

with row2_col2:
    fig_rated = plot_highest_rated_players(filtered_df, top_n=15, theme=theme)
    st.plotly_chart(fig_rated, use_container_width=True)

st.divider()

# Row 3 Charts: Position Boxplot, Market Value & Heatmap
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    fig_box = plot_rating_by_position_box(filtered_df, theme=theme)
    st.plotly_chart(fig_box, use_container_width=True)

with row3_col2:
    fig_mv = plot_market_value_distribution(filtered_df, theme=theme)
    st.plotly_chart(fig_mv, use_container_width=True)

st.divider()

st.subheader("🔥 Correlation Analysis")
fig_corr = plot_correlation_heatmap(filtered_df, theme=theme)
st.plotly_chart(fig_corr, use_container_width=True)
