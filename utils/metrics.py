import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def run_kmeans_clustering(df: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    """Performs K-Means clustering and labels players as Elite, Good, Average, or Developing."""
    feature_cols = [
        'player_rating', 'performance_score', 'goals', 'assists', 
        'pass_accuracy', 'tackles', 'distance_covered_km', 'top_speed_kmh'
    ]
    avail_cols = [c for c in feature_cols if c in df.columns]
    if len(df) < n_clusters or len(avail_cols) < 2:
        df_copy = df.copy()
        df_copy['Cluster_Label'] = 'Average'
        return df_copy

    df_clean = df.copy()
    X = df_clean[avail_cols].fillna(0)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    df_clean['Cluster'] = clusters
    
    # Map cluster index to meaningful rank (Elite, Good, Average, Developing) based on average performance_score
    cluster_means = df_clean.groupby('Cluster')['performance_score'].mean().sort_values(ascending=False)
    rank_labels = ['Elite', 'Good', 'Average', 'Developing']
    mapping = {c_id: rank_labels[i] for i, c_id in enumerate(cluster_means.index)}
    
    df_clean['Cluster_Label'] = df_clean['Cluster'].map(mapping)
    return df_clean

@st.cache_data
def run_pca_projection(df: pd.DataFrame) -> pd.DataFrame:
    """Projects multi-dimensional player stats down to 2D using PCA."""
    feature_cols = [
        'player_rating', 'performance_score', 'goals', 'assists', 'shots',
        'pass_accuracy', 'tackles', 'interceptions', 'distance_covered_km', 'top_speed_kmh'
    ]
    avail_cols = [c for c in feature_cols if c in df.columns]
    df_clean = df.copy()
    if len(df) < 5 or len(avail_cols) < 2:
        df_clean['PCA1'] = 0.0
        df_clean['PCA2'] = 0.0
        return df_clean

    X = df_clean[avail_cols].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_scaled)
    
    df_clean['PCA1'] = coords[:, 0]
    df_clean['PCA2'] = coords[:, 1]
    return df_clean

@st.cache_data
def run_rf_feature_importance(df: pd.DataFrame) -> pd.DataFrame:
    """Fits Random Forest to predict Performance Score and returns feature importances."""
    target_col = 'performance_score'
    feature_cols = [
        'player_rating', 'goals', 'assists', 'shots', 'shots_on_target',
        'expected_goals_xg', 'expected_assists_xa', 'pass_accuracy',
        'tackles', 'interceptions', 'clearances', 'distance_covered_km',
        'sprint_distance_km', 'top_speed_kmh', 'stamina_score'
    ]
    avail_cols = [c for c in feature_cols if c in df.columns]
    
    if target_col not in df.columns or len(avail_cols) < 2 or len(df) < 10:
        return pd.DataFrame({'Feature': ['No Data'], 'Importance': [0.0]})
        
    X = df[avail_cols].fillna(0)
    y = df[target_col].fillna(0)
    
    rf = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=10)
    rf.fit(X, y)
    
    imp_df = pd.DataFrame({
        'Feature': avail_cols,
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    return imp_df

@st.cache_data
def recommend_ai_players(df: pd.DataFrame, position: str = "ST", max_age: int = 35, 
                         max_market_val_m: float = 200.0, preferred_foot: str = None, 
                         min_rating: float = 6.0, min_perf: float = 50.0, top_n: int = 10) -> pd.DataFrame:
    """AI Scout Engine using Cosine Similarity against ideal benchmark stats."""
    
    scout_df = df.copy()
    
    POS_MAP = {
        'ST': ['Forward'], 'RW': ['Forward'], 'LW': ['Forward'],
        'CAM': ['Midfielder'], 'CM': ['Midfielder'], 'CDM': ['Midfielder'],
        'CB': ['Defender'], 'RB': ['Defender'], 'LB': ['Defender'],
        'GK': ['Goalkeeper'],
        'Forward': ['Forward'], 'Midfielder': ['Midfielder'],
        'Defender': ['Defender'], 'Goalkeeper': ['Goalkeeper']
    }
    
    # Filter base criteria
    if position and position != "All":
        target_positions = POS_MAP.get(position, [position])
        scout_df = scout_df[scout_df['position'].isin(target_positions)]
    if max_age:
        scout_df = scout_df[scout_df['age'] <= max_age]
    if max_market_val_m:
        scout_df = scout_df[scout_df['market_value_eur'] <= max_market_val_m * 1e6]
    if preferred_foot and preferred_foot != "Any":
        scout_df = scout_df[scout_df['preferred_foot'] == preferred_foot]
    if min_rating:
        scout_df = scout_df[scout_df['player_rating'] >= min_rating]
    if min_perf:
        scout_df = scout_df[scout_df['performance_score'] >= min_perf]
        
    if len(scout_df) == 0:
        return pd.DataFrame()
        
    num_cols = [
        'player_rating', 'performance_score', 'goals', 'assists', 
        'pass_accuracy', 'tackles', 'distance_covered_km', 'top_speed_kmh'
    ]
    avail_cols = [c for c in num_cols if c in scout_df.columns]
    
    # Group per player
    agg_dict = {
        'team': 'first',
        'club_name': 'first',
        'position': 'first',
        'age': 'first',
        'market_value_eur': 'last',
        'player_rating': 'mean',
        'performance_score': 'mean',
        'goals': 'sum',
        'assists': 'sum',
        'pass_accuracy': 'mean',
        'tackles': 'mean',
        'distance_covered_km': 'mean',
        'top_speed_kmh': 'max'
    }
    actual_dict = {k: v for k, v in agg_dict.items() if k in scout_df.columns}
    player_grouped = scout_df.groupby('player_name').agg(actual_dict).reset_index()
    
    if len(player_grouped) == 0:
        return pd.DataFrame()

    # Calculate ideal target vector (90th percentile of group)
    feature_matrix = player_grouped[avail_cols].fillna(0)
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(feature_matrix)
    
    target_vector = np.percentile(scaled_matrix, 90, axis=0).reshape(1, -1)
    sim_scores = cosine_similarity(scaled_matrix, target_vector).flatten()
    
    player_grouped['Similarity_Score'] = (sim_scores * 100).clip(0, 100).round(1)
    
    result = player_grouped.sort_values('Similarity_Score', ascending=False).head(top_n)
    return result
