import pandas as pd
import numpy as np
import streamlit as st
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "fifa_world_cup_2026_player_performance.csv")

@st.cache_data(show_spinner="Loading FIFA 2026 dataset...")
def load_data(file_path: str = DATA_PATH) -> pd.DataFrame:
    """Loads and preprocesses the FIFA 2026 Player Performance dataset."""
    if not os.path.exists(file_path):
        # Fallback to root directory if data folder isn't found
        file_path = "fifa_world_cup_2026_player_performance.csv"
    
    df = pd.read_csv(file_path)
    
    # Preprocess dates
    if 'match_date' in df.columns:
        df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce')
    
    # Numeric column casting & fillna
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # Category / Text column cleaning
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        df[col] = df[col].fillna('Unknown').astype(str).str.strip()
        
    return df

@st.cache_data
def get_filter_options(df: pd.DataFrame) -> dict:
    """Extracts unique sorted options for sidebar filters."""
    options = {
        "tournament_stage": sorted(df['tournament_stage'].unique().tolist()) if 'tournament_stage' in df.columns else [],
        "nationality": sorted(df['nationality'].unique().tolist()) if 'nationality' in df.columns else [],
        "team": sorted(df['team'].unique().tolist()) if 'team' in df.columns else [],
        "opponent_team": sorted(df['opponent_team'].unique().tolist()) if 'opponent_team' in df.columns else [],
        "player": sorted(df['player_name'].unique().tolist()) if 'player_name' in df.columns else [],
        "position": sorted(df['position'].unique().tolist()) if 'position' in df.columns else [],
        "club": sorted(df['club_name'].unique().tolist()) if 'club_name' in df.columns else [],
        "preferred_foot": sorted(df['preferred_foot'].unique().tolist()) if 'preferred_foot' in df.columns else [],
        "match_result": sorted(df['match_result'].unique().tolist()) if 'match_result' in df.columns else [],
        "city": sorted(df['city'].unique().tolist()) if 'city' in df.columns else [],
        "age_min": int(df['age'].min()) if 'age' in df.columns else 16,
        "age_max": int(df['age'].max()) if 'age' in df.columns else 40,
        "market_val_min": float(df['market_value_eur'].min()) if 'market_value_eur' in df.columns else 0.0,
        "market_val_max": float(df['market_value_eur'].max()) if 'market_value_eur' in df.columns else 200000000.0,
        "rating_min": float(df['player_rating'].min()) if 'player_rating' in df.columns else 1.0,
        "rating_max": float(df['player_rating'].max()) if 'player_rating' in df.columns else 10.0,
        "perf_min": float(df['performance_score'].min()) if 'performance_score' in df.columns else 0.0,
        "perf_max": float(df['performance_score'].max()) if 'performance_score' in df.columns else 100.0,
        "date_min": df['match_date'].min().date() if 'match_date' in df.columns and not df['match_date'].isnull().all() else None,
        "date_max": df['match_date'].max().date() if 'match_date' in df.columns and not df['match_date'].isnull().all() else None,
    }
    return options

@st.cache_data
def get_player_career_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates match stats into per-player career tournament stats."""
    agg_dict = {
        'age': 'first',
        'nationality': 'first',
        'team': 'first',
        'position': 'first',
        'preferred_foot': 'first',
        'club_name': 'first',
        'market_value_eur': 'last',
        'height_cm': 'first',
        'weight_kg': 'first',
        'match_id': 'count', # Matches played
        'minutes_played': 'sum',
        'goals': 'sum',
        'assists': 'sum',
        'shots': 'sum',
        'shots_on_target': 'sum',
        'expected_goals_xg': 'sum',
        'expected_assists_xa': 'sum',
        'key_passes': 'sum',
        'successful_passes': 'sum',
        'total_passes': 'sum',
        'tackles': 'sum',
        'interceptions': 'sum',
        'clearances': 'sum',
        'distance_covered_km': 'sum',
        'sprint_distance_km': 'sum',
        'top_speed_kmh': 'max',
        'player_rating': 'mean',
        'performance_score': 'mean',
        'offensive_contribution': 'mean',
        'defensive_contribution': 'mean',
        'possession_impact': 'mean',
        'pressure_resistance': 'mean',
        'creativity_score': 'mean',
        'consistency_score': 'mean',
        'clutch_performance_score': 'mean'
    }
    
    actual_dict = {k: v for k, v in agg_dict.items() if k in df.columns}
    summary = df.groupby('player_name').agg(actual_dict).reset_index()
    if 'match_id' in summary.columns:
        summary.rename(columns={'match_id': 'matches_played'}, inplace=True)
    if 'total_passes' in summary.columns and 'successful_passes' in summary.columns:
        summary['pass_accuracy'] = np.where(summary['total_passes'] > 0, 
                                            (summary['successful_passes'] / summary['total_passes']) * 100, 0)
    return summary
