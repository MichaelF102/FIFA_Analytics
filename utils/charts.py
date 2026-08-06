import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Theme palette
COLOR_NEON_CYAN = "#00f2fe"
COLOR_EMERALD = "#10b981"
COLOR_GOLD = "#fbbf24"
COLOR_PURPLE = "#8b5cf6"
COLOR_PINK = "#ec4899"
COLOR_RED = "#ef4444"
COLOR_PALETTE = [COLOR_NEON_CYAN, COLOR_EMERALD, COLOR_GOLD, COLOR_PURPLE, COLOR_PINK, COLOR_RED, "#3b82f6"]

def _apply_theme(fig, title: str = "", theme: str = "dark"):
    bg_color = "rgba(0,0,0,0)" if theme == "dark" else "rgba(255,255,255,0)"
    font_color = "#f8fafc" if theme == "dark" else "#0f172a"
    grid_color = "rgba(255,255,255,0.07)" if theme == "dark" else "rgba(0,0,0,0.07)"
    
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(family="Outfit, sans-serif", size=18, color=font_color)),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(family="Inter, sans-serif", color=font_color),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color),
        yaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=font_color))
    )
    return fig

# 1. Overview Charts
def plot_goals_by_team(df: pd.DataFrame, top_n: int = 15, theme: str = "dark"):
    team_goals = df.groupby('team')['goals'].sum().reset_index().sort_values('goals', ascending=False).head(top_n)
    fig = px.bar(team_goals, x='team', y='goals', color='goals',
                 color_continuous_scale=['#0e7490', '#00f2fe'],
                 labels={'team': 'Team', 'goals': 'Total Goals'})
    return _apply_theme(fig, f"Top {top_n} Teams by Total Goals", theme)

def plot_match_results_distribution(df: pd.DataFrame, theme: str = "dark"):
    results = df['match_result'].value_counts().reset_index()
    results.columns = ['match_result', 'count']
    fig = px.pie(results, names='match_result', values='count', hole=0.0,
                 color_discrete_sequence=[COLOR_EMERALD, COLOR_NEON_CYAN, COLOR_RED])
    return _apply_theme(fig, "Match Results Distribution", theme)

def plot_tournament_stage_distribution(df: pd.DataFrame, theme: str = "dark"):
    stages = df['tournament_stage'].value_counts().reset_index()
    stages.columns = ['tournament_stage', 'count']
    fig = px.pie(stages, names='tournament_stage', values='count', hole=0.4,
                 color_discrete_sequence=COLOR_PALETTE)
    return _apply_theme(fig, "Matches by Tournament Stage", theme)

def plot_top_scorers(df: pd.DataFrame, top_n: int = 15, theme: str = "dark"):
    top_scorers = df.groupby('player_name')['goals'].sum().reset_index().sort_values('goals', ascending=True).tail(top_n)
    fig = px.bar(top_scorers, y='player_name', x='goals', orientation='h',
                 color='goals', color_continuous_scale=['#4c1d95', '#8b5cf6', '#ec4899'],
                 labels={'player_name': 'Player', 'goals': 'Goals'})
    return _apply_theme(fig, f"Top {top_n} Goal Scorers", theme)

def plot_highest_rated_players(df: pd.DataFrame, top_n: int = 15, theme: str = "dark"):
    top_rated = df.groupby('player_name')['player_rating'].mean().reset_index().sort_values('player_rating', ascending=True).tail(top_n)
    fig = px.bar(top_rated, y='player_name', x='player_rating', orientation='h',
                 color='player_rating', color_continuous_scale=['#065f46', '#10b981', '#fbbf24'],
                 labels={'player_name': 'Player', 'player_rating': 'Average Rating'})
    return _apply_theme(fig, f"Top {top_n} Highest Rated Players", theme)

def plot_rating_by_position_box(df: pd.DataFrame, theme: str = "dark"):
    fig = px.box(df, x='position', y='player_rating', color='position',
                 color_discrete_sequence=COLOR_PALETTE,
                 labels={'position': 'Position', 'player_rating': 'Player Rating'})
    return _apply_theme(fig, "Average Player Rating by Position", theme)

def plot_market_value_distribution(df: pd.DataFrame, theme: str = "dark"):
    df_copy = df.copy()
    df_copy['mv_millions'] = df_copy['market_value_eur'] / 1e6
    fig = px.histogram(df_copy, x='mv_millions', nbins=30, color_discrete_sequence=[COLOR_NEON_CYAN],
                       labels={'mv_millions': 'Market Value (€ Millions)'})
    return _apply_theme(fig, "Market Value Distribution", theme)

def plot_correlation_heatmap(df: pd.DataFrame, theme: str = "dark"):
    numeric_cols = [
        'player_rating', 'performance_score', 'goals', 'assists', 'expected_goals_xg',
        'expected_assists_xa', 'pass_accuracy', 'tackles', 'distance_covered_km',
        'top_speed_kmh', 'creativity_score', 'consistency_score'
    ]
    avail_cols = [c for c in numeric_cols if c in df.columns]
    corr = df[avail_cols].corr()
    
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
    return _apply_theme(fig, "Feature Correlation Heatmap", theme)

# 2. Player Analysis Charts
def plot_player_rating_timeline(df: pd.DataFrame, player_name: str, theme: str = "dark"):
    p_df = df[df['player_name'] == player_name].sort_values('match_date')
    fig = px.line(p_df, x='match_date', y='player_rating', markers=True,
                  line_shape='spline', color_discrete_sequence=[COLOR_NEON_CYAN],
                  labels={'match_date': 'Match Date', 'player_rating': 'Rating'})
    return _apply_theme(fig, f"{player_name} - Rating Timeline", theme)

def plot_performance_score_timeline(df: pd.DataFrame, player_name: str, theme: str = "dark"):
    p_df = df[df['player_name'] == player_name].sort_values('match_date')
    fig = px.area(p_df, x='match_date', y='performance_score', markers=True,
                  color_discrete_sequence=[COLOR_EMERALD],
                  labels={'match_date': 'Match Date', 'performance_score': 'Performance Score'})
    return _apply_theme(fig, f"{player_name} - Performance Score Timeline", theme)

def plot_goals_vs_xg(df: pd.DataFrame, player_name: str = None, theme: str = "dark"):
    if player_name:
        sub_df = df[df['player_name'] == player_name]
    else:
        sub_df = df
    fig = px.scatter(sub_df, x='expected_goals_xg', y='goals', color='tournament_stage',
                     size='shots', hover_data=['player_name', 'opponent_team'],
                     color_discrete_sequence=COLOR_PALETTE,
                     labels={'expected_goals_xg': 'Expected Goals (xG)', 'goals': 'Actual Goals'})
    return _apply_theme(fig, "Goals vs. Expected Goals (xG)", theme)

def plot_shots_vs_target(df: pd.DataFrame, player_name: str, theme: str = "dark"):
    p_df = df[df['player_name'] == player_name]
    agg = p_df[['shots', 'shots_on_target']].sum().reset_index()
    agg.columns = ['Metric', 'Count']
    fig = px.bar(agg, x='Metric', y='Count', color='Metric', color_discrete_sequence=[COLOR_PURPLE, COLOR_NEON_CYAN])
    return _apply_theme(fig, f"{player_name} - Shots vs Shots on Target", theme)

def plot_radar_chart(categories: list, values: list, name: str = "Player", compare_values: list = None, compare_name: str = "Target", theme: str = "dark"):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=name,
        line=dict(color=COLOR_NEON_CYAN, width=2)
    ))
    if compare_values:
        fig.add_trace(go.Scatterpolar(
            r=compare_values + [compare_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=compare_name,
            line=dict(color=COLOR_GOLD, width=2)
        ))
    
    bg_color = "rgba(0,0,0,0)"
    font_color = "#f8fafc" if theme == "dark" else "#0f172a"
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.15)"),
            bgcolor=bg_color
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(family="Inter, sans-serif", color=font_color),
        showlegend=True
    )
    return fig

# 3. Team Analysis Charts
def plot_team_goals_by_match(df: pd.DataFrame, team_name: str, theme: str = "dark"):
    t_df = df[df['team'] == team_name].sort_values('match_date')
    match_goals = t_df.groupby(['match_id', 'opponent_team', 'match_date'])['goals'].sum().reset_index()
    fig = px.bar(match_goals, x='opponent_team', y='goals', color='goals',
                 color_continuous_scale=['#065f46', '#10b981'],
                 labels={'opponent_team': 'Opponent', 'goals': 'Goals Scored'})
    return _apply_theme(fig, f"{team_name} - Goals by Opponent Match", theme)

def plot_position_counts(df: pd.DataFrame, team_name: str = None, theme: str = "dark"):
    sub = df[df['team'] == team_name] if team_name else df
    counts = sub['position'].value_counts().reset_index()
    counts.columns = ['position', 'count']
    fig = px.bar(counts, x='position', y='count', color='count', color_continuous_scale=['#312e81', '#8b5cf6'])
    return _apply_theme(fig, "Position Distribution & Formation Count", theme)

# 4. Position & ML Insights Charts
def plot_position_violin(df: pd.DataFrame, theme: str = "dark"):
    fig = px.violin(df, x='position', y='player_rating', color='position', box=True, points="all",
                    color_discrete_sequence=COLOR_PALETTE)
    return _apply_theme(fig, "Rating Spread by Position (Violin Plot)", theme)

def plot_parallel_coordinates(df: pd.DataFrame, theme: str = "dark"):
    sample_df = df.sample(min(500, len(df))).copy()
    fig = px.parallel_coordinates(
        sample_df,
        dimensions=['player_rating', 'performance_score', 'pass_accuracy', 'distance_covered_km', 'top_speed_kmh'],
        color='player_rating',
        color_continuous_scale=px.colors.diverging.Tealrose
    )
    return _apply_theme(fig, "Multi-Metric Parallel Coordinates Comparison", theme)

def plot_market_vs_performance_scatter(df: pd.DataFrame, theme: str = "dark"):
    df_copy = df.copy()
    df_copy['mv_millions'] = df_copy['market_value_eur'] / 1e6
    fig = px.scatter(df_copy, x='mv_millions', y='performance_score', color='position',
                     size='player_rating', hover_data=['player_name', 'team'],
                     color_discrete_sequence=COLOR_PALETTE,
                     labels={'mv_millions': 'Market Value (€M)', 'performance_score': 'Performance Score'})
    return _apply_theme(fig, "Market Value vs Performance Score", theme)

def plot_bubble_age_perf_mv(df: pd.DataFrame, theme: str = "dark"):
    df_copy = df.copy()
    df_copy['mv_millions'] = df_copy['market_value_eur'] / 1e6
    fig = px.scatter(df_copy, x='age', y='performance_score', size='mv_millions', color='position',
                     hover_data=['player_name', 'team'], color_discrete_sequence=COLOR_PALETTE,
                     labels={'age': 'Age', 'performance_score': 'Performance Score', 'mv_millions': 'Market Value (€M)'})
    return _apply_theme(fig, "Age vs. Performance Score vs. Market Value (Bubble Chart)", theme)

def plot_kmeans_clusters(df_clustered: pd.DataFrame, theme: str = "dark"):
    fig = px.scatter(df_clustered, x='player_rating', y='performance_score', color='Cluster_Label',
                     symbol='Cluster_Label', size='market_value_eur', hover_data=['player_name', 'team', 'position'],
                     color_discrete_sequence=[COLOR_NEON_CYAN, COLOR_EMERALD, COLOR_GOLD, COLOR_PINK])
    return _apply_theme(fig, "K-Means Player Segment Clusters", theme)

def plot_pca_projection(df_pca: pd.DataFrame, theme: str = "dark"):
    fig = px.scatter(df_pca, x='PCA1', y='PCA2', color='position', hover_data=['player_name', 'team'],
                     color_discrete_sequence=COLOR_PALETTE)
    return _apply_theme(fig, "PCA 2D Player Skill Projection", theme)

def plot_rf_feature_importance(importances_df: pd.DataFrame, theme: str = "dark"):
    fig = px.bar(importances_df.head(10), x='Importance', y='Feature', orientation='h',
                 color='Importance', color_continuous_scale=['#065f46', '#10b981'])
    return _apply_theme(fig, "Random Forest Feature Importance for Performance Score", theme)

def plot_speed_vs_acceleration(df: pd.DataFrame, theme: str = "dark"):
    fig = px.scatter(df, x='accelerations', y='top_speed_kmh', color='position',
                     size='stamina_score', hover_data=['player_name', 'team'],
                     color_discrete_sequence=COLOR_PALETTE,
                     labels={'accelerations': 'Accelerations', 'top_speed_kmh': 'Top Speed (km/h)'})
    return _apply_theme(fig, "Accelerations vs Top Speed", theme)
