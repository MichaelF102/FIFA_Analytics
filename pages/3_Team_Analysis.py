import streamlit as st
import pandas as pd
import plotly.express as px
from utils.loader import load_data
from utils.styles import apply_custom_styles, render_kpi_card
from utils.filters import render_sidebar_filters
from utils.charts import (
    plot_team_goals_by_match, plot_position_counts
)

st.set_page_config(page_title="Team Analysis | FIFA 2026", page_icon="🛡️", layout="wide")
theme = st.session_state.get("theme", "dark")
apply_custom_styles(theme)

df = load_data()
filtered_df = render_sidebar_filters(df)

st.title("🛡️ Team Tactical & Performance Analysis")

all_teams = sorted(filtered_df['team'].unique()) if len(filtered_df) > 0 and 'team' in filtered_df else sorted(df['team'].unique())

if not all_teams:
    st.warning("No teams available with current sidebar filters.")
    st.stop()

selected_team = st.selectbox(" Choose Team", all_teams, index=0)

team_df = df[df['team'] == selected_team]

if len(team_df) == 0:
    st.warning("No match data found for selected team.")
    st.stop()

# Team KPIs
k1, k2, k3, k4, k5, k6 = st.columns(6)

total_goals = int(team_df['goals'].sum()) if 'goals' in team_df else 0
total_conceded = int(team_df['goals_conceded'].sum()) if 'goals_conceded' in team_df else 0
avg_rating = team_df['player_rating'].mean() if 'player_rating' in team_df else 0.0
avg_possession = team_df['possession_impact'].mean() if 'possession_impact' in team_df else 0.0
avg_perf = team_df['performance_score'].mean() if 'performance_score' in team_df else 0.0
total_assists = int(team_df['assists'].sum()) if 'assists' in team_df else 0

with k1: render_kpi_card("Goals Scored", f"{total_goals}", theme=theme)
with k2: render_kpi_card("Goals Conceded", f"{total_conceded}", theme=theme)
with k3: render_kpi_card("Avg Rating", f"{avg_rating:.2f}", theme=theme)
with k4: render_kpi_card("Possession Impact", f"{avg_possession:.1f}", theme=theme)
with k5: render_kpi_card("Avg Performance", f"{avg_perf:.1f}", theme=theme)
with k6: render_kpi_card("Total Assists", f"{total_assists}", theme=theme)

st.divider()

# Row 1: Goals by Match & Formation Position Counts
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    fig_match_goals = plot_team_goals_by_match(df, selected_team, theme=theme)
    st.plotly_chart(fig_match_goals, use_container_width=True)

with r1_c2:
    fig_formation = plot_position_counts(df, selected_team, theme=theme)
    st.plotly_chart(fig_formation, use_container_width=True)

st.divider()

# Row 2: Top Scorers & Top Assist Providers for Team
r2_c1, r2_c2 = st.columns(2)

with r2_c1:
    top_t_scorers = team_df.groupby('player_name')['goals'].sum().reset_index().sort_values('goals', ascending=True).tail(10)
    fig_t_scorers = px.bar(top_t_scorers, y='player_name', x='goals', orientation='h',
                           color='goals', color_continuous_scale=['#065f46', '#10b981'],
                           title=f"<b>Top Scorers - {selected_team}</b>")
    fig_t_scorers.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_t_scorers, use_container_width=True)

with r2_c2:
    top_t_assists = team_df.groupby('player_name')['assists'].sum().reset_index().sort_values('assists', ascending=True).tail(10)
    fig_t_assists = px.bar(top_t_assists, y='player_name', x='assists', orientation='h',
                           color='assists', color_continuous_scale=['#4c1d95', '#8b5cf6'],
                           title=f"<b>Top Assist Providers - {selected_team}</b>")
    fig_t_assists.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_t_assists, use_container_width=True)

st.divider()

# Row 3: Team Rating Distribution & Market Value Distribution
r3_c1, r3_c2 = st.columns(2)

with r3_c1:
    fig_violin = px.violin(team_df, x='position', y='player_rating', color='position', box=True,
                            title=f"<b>Rating Distribution by Position - {selected_team}</b>")
    fig_violin.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_violin, use_container_width=True)

with r3_c2:
    team_df_mv = team_df.copy()
    team_df_mv['mv_millions'] = team_df_mv['market_value_eur'] / 1e6
    fig_mv_dist = px.histogram(team_df_mv, x='mv_millions', color='position',
                               title=f"<b>Market Value Distribution - {selected_team}</b>")
    fig_mv_dist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
    st.plotly_chart(fig_mv_dist, use_container_width=True)
