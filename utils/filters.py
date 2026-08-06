import streamlit as st
import pandas as pd
from utils.loader import get_filter_options

def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Renders the comprehensive 15-parameter sidebar filter suite and returns filtered DataFrame."""
    st.sidebar.markdown("### ⚽ Tournament Filters")
    
    options = get_filter_options(df)
    
    # Reset button
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state.clear()
        st.rerun()
        
    st.sidebar.divider()
    
    # Expanders for organized sidebar grouping
    with st.sidebar.expander("🏆 Tournament & Teams", expanded=True):
        sel_stages = st.multiselect("Tournament Stage", options["tournament_stage"], key="filter_stage")
        sel_teams = st.multiselect("Team", options["team"], key="filter_team")
        sel_opponents = st.multiselect("Opponent", options["opponent_team"], key="filter_opponent")
        sel_results = st.multiselect("Match Result", options["match_result"], key="filter_result")
        sel_cities = st.multiselect("City", options["city"], key="filter_city")

    with st.sidebar.expander("👤 Player Demographics & Club", expanded=True):
        sel_players = st.multiselect("Player Name", options["player"], key="filter_player")
        sel_nationalities = st.multiselect("Nationality", options["nationality"], key="filter_nationality")
        sel_clubs = st.multiselect("Club", options["club"], key="filter_club")
        sel_positions = st.multiselect("Position", options["position"], key="filter_position")
        sel_foot = st.multiselect("Preferred Foot", options["preferred_foot"], key="filter_foot")
        
        age_range = st.slider(
            "Age Range", 
            min_value=options["age_min"], 
            max_value=options["age_max"], 
            value=(options["age_min"], options["age_max"]),
            key="filter_age"
        )
        
        mv_range = st.slider(
            "Market Value (€M)", 
            min_value=0.0, 
            max_value=options["market_val_max"] / 1e6, 
            value=(0.0, options["market_val_max"] / 1e6),
            step=1.0,
            key="filter_mv"
        )

    with st.sidebar.expander("📊 Performance & Ratings", expanded=False):
        rating_range = st.slider(
            "Player Rating", 
            min_value=1.0, 
            max_value=10.0, 
            value=(1.0, 10.0),
            step=0.1,
            key="filter_rating"
        )
        
        perf_range = st.slider(
            "Performance Score", 
            min_value=0.0, 
            max_value=100.0, 
            value=(0.0, 100.0),
            step=1.0,
            key="filter_perf"
        )
        
        if options["date_min"] and options["date_max"]:
            date_range = st.date_input(
                "Date Range",
                value=(options["date_min"], options["date_max"]),
                min_value=options["date_min"],
                max_value=options["date_max"],
                key="filter_date"
            )
        else:
            date_range = None

    # Apply filtering
    filtered_df = df.copy()
    
    if sel_stages:
        filtered_df = filtered_df[filtered_df['tournament_stage'].isin(sel_stages)]
    if sel_teams:
        filtered_df = filtered_df[filtered_df['team'].isin(sel_teams)]
    if sel_opponents:
        filtered_df = filtered_df[filtered_df['opponent_team'].isin(sel_opponents)]
    if sel_results:
        filtered_df = filtered_df[filtered_df['match_result'].isin(sel_results)]
    if sel_cities:
        filtered_df = filtered_df[filtered_df['city'].isin(sel_cities)]
    if sel_players:
        filtered_df = filtered_df[filtered_df['player_name'].isin(sel_players)]
    if sel_nationalities:
        filtered_df = filtered_df[filtered_df['nationality'].isin(sel_nationalities)]
    if sel_clubs:
        filtered_df = filtered_df[filtered_df['club_name'].isin(sel_clubs)]
    if sel_positions:
        filtered_df = filtered_df[filtered_df['position'].isin(sel_positions)]
    if sel_foot:
        filtered_df = filtered_df[filtered_df['preferred_foot'].isin(sel_foot)]
        
    if 'age' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])]
    if 'market_value_eur' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['market_value_eur'] >= mv_range[0] * 1e6) & 
                                  (filtered_df['market_value_eur'] <= mv_range[1] * 1e6)]
    if 'player_rating' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['player_rating'] >= rating_range[0]) & 
                                  (filtered_df['player_rating'] <= rating_range[1])]
    if 'performance_score' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['performance_score'] >= perf_range[0]) & 
                                  (filtered_df['performance_score'] <= perf_range[1])]
    if date_range and isinstance(date_range, tuple) and len(date_range) == 2 and 'match_date' in filtered_df.columns:
        start_d, end_d = date_range
        filtered_df = filtered_df[(filtered_df['match_date'].dt.date >= start_d) & 
                                  (filtered_df['match_date'].dt.date <= end_d)]
        
    st.sidebar.caption(f"Filtered Records: **{len(filtered_df):,}** / {len(df):,}")
    return filtered_df
