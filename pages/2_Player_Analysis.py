import streamlit as st
import pandas as pd
from utils.loader import load_data, get_player_career_summary
from utils.styles import apply_custom_styles, render_kpi_card
from utils.filters import render_sidebar_filters
from utils.charts import (
    plot_player_rating_timeline, plot_performance_score_timeline,
    plot_goals_vs_xg, plot_shots_vs_target, plot_radar_chart, plot_pass_accuracy_trend
)

st.set_page_config(page_title="Player Analysis | FIFA 2026", page_icon="👤", layout="wide")
theme = st.session_state.get("theme", "dark")
apply_custom_styles(theme)

df = load_data()
filtered_df = render_sidebar_filters(df)

st.title("👤 Player Deep-Dive Analysis")

all_players = sorted(filtered_df['player_name'].unique()) if len(filtered_df) > 0 and 'player_name' in filtered_df else sorted(df['player_name'].unique())

if not all_players:
    st.warning("No players available with current sidebar filters.")
    st.stop()

selected_player = st.selectbox("🎯 Select Player to Analyze", all_players, index=0)

player_matches = df[df['player_name'] == selected_player].sort_values('match_date')
summary_df = get_player_career_summary(df)
p_summary = summary_df[summary_df['player_name'] == selected_player]

if len(player_matches) == 0:
    st.warning("No match data found for selected player.")
    st.stop()

p_latest = player_matches.iloc[-1]
p_stat = p_summary.iloc[0] if len(p_summary) > 0 else p_latest

# Player Profile Card Header
st.markdown(f"""
<div class="fifa-hero">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h2>⚽ {selected_player}</h2>
            <p><strong>Team:</strong> {p_stat.get('team', 'N/A')} | <strong>Club:</strong> {p_stat.get('club_name', 'N/A')} | <strong>Nationality:</strong> {p_stat.get('nationality', 'N/A')}</p>
        </div>
        <div>
            <span class="badge badge-primary">{p_stat.get('position', 'N/A')}</span>
            <span class="badge badge-success">{p_stat.get('preferred_foot', 'N/A')} Foot</span>
            <span class="badge badge-warning">€{p_stat.get('market_value_eur', 0)/1e6:.1f}M MV</span>
        </div>
    </div>
    <div style="margin-top: 1rem; font-size: 0.9rem; color: #94a3b8;">
        Age: <strong>{p_stat.get('age', 'N/A')} yrs</strong> | Height: <strong>{p_stat.get('height_cm', 'N/A')} cm</strong> | Weight: <strong>{p_stat.get('weight_kg', 'N/A')} kg</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# Player KPI Cards Row
k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)

total_g = int(player_matches['goals'].sum()) if 'goals' in player_matches else 0
total_a = int(player_matches['assists'].sum()) if 'assists' in player_matches else 0
total_mins = int(player_matches['minutes_played'].sum()) if 'minutes_played' in player_matches else 0
total_xg = player_matches['expected_goals_xg'].sum() if 'expected_goals_xg' in player_matches else 0.0
total_xa = player_matches['expected_assists_xa'].sum() if 'expected_assists_xa' in player_matches else 0.0
mean_rating = player_matches['player_rating'].mean() if 'player_rating' in player_matches else 0.0
mean_perf = player_matches['performance_score'].mean() if 'performance_score' in player_matches else 0.0
mean_pass_acc = player_matches['pass_accuracy'].mean() if 'pass_accuracy' in player_matches else 0.0

with k1: render_kpi_card("Goals", f"{total_g}", theme=theme)
with k2: render_kpi_card("Assists", f"{total_a}", theme=theme)
with k3: render_kpi_card("Minutes", f"{total_mins:,}", theme=theme)
with k4: render_kpi_card("xG", f"{total_xg:.2f}", theme=theme)
with k5: render_kpi_card("xA", f"{total_xa:.2f}", theme=theme)
with k6: render_kpi_card("Rating", f"{mean_rating:.2f}", theme=theme)
with k7: render_kpi_card("Perf Score", f"{mean_perf:.1f}", theme=theme)
with k8: render_kpi_card("Pass Acc", f"{mean_pass_acc:.1f}%", theme=theme)

st.divider()

# Row 1: Timelines & Radar Chart
col_left, col_right = st.columns([1.2, 1])

with col_left:
    fig_rate = plot_player_rating_timeline(df, selected_player, theme=theme)
    st.plotly_chart(fig_rate, use_container_width=True)
    
    fig_perf = plot_performance_score_timeline(df, selected_player, theme=theme)
    st.plotly_chart(fig_perf, use_container_width=True)

with col_right:
    st.subheader("🕸️ 7-Axis Capability Radar")
    categories = ['Passing', 'Creativity', 'Defending', 'Offense', 'Pressure', 'Consistency', 'Clutch']
    vals = [
        float(p_stat.get('pass_accuracy', 50)),
        float(p_stat.get('creativity_score', 50)),
        float(p_stat.get('defensive_contribution', 5)) * 10,
        float(p_stat.get('offensive_contribution', 5)) * 10,
        float(p_stat.get('pressure_resistance', 50)),
        float(p_stat.get('consistency_score', 50)),
        float(p_stat.get('clutch_performance_score', 50))
    ]
    fig_radar = plot_radar_chart(categories, vals, name=selected_player, theme=theme)
    st.plotly_chart(fig_radar, use_container_width=True)

st.divider()

# Row 2: Goals vs xG & Shots vs Target
r2_c1, r2_c2 = st.columns(2)

with r2_c1:
    fig_xg = plot_goals_vs_xg(df, player_name=selected_player, theme=theme)
    st.plotly_chart(fig_xg, use_container_width=True)

with r2_c2:
    fig_shots = plot_shots_vs_target(df, selected_player, theme=theme)
    st.plotly_chart(fig_shots, use_container_width=True)

st.divider()

# Match-wise Table
st.subheader("📋 Match-wise Performance History")
display_cols = [
    'match_date', 'tournament_stage', 'team', 'opponent_team', 'match_result',
    'minutes_played', 'goals', 'assists', 'shots', 'shots_on_target',
    'pass_accuracy', 'tackles', 'distance_covered_km', 'top_speed_kmh',
    'player_rating', 'performance_score'
]
avail_disp = [c for c in display_cols if c in player_matches.columns]
st.dataframe(player_matches[avail_disp], use_container_width=True, hide_index=True)
