import streamlit as st
import pandas as pd
import io
from utils.loader import load_data, get_player_career_summary
from utils.styles import apply_custom_styles, render_kpi_card
from utils.filters import render_sidebar_filters
from utils.charts import plot_radar_chart

st.set_page_config(
    page_title="FIFA 2026 World Cup Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme State Management
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

# Top right theme switch in sidebar
with st.sidebar:
    st.image("assets/fifa_logo.png", use_container_width=True)
    st.title("⚽ FIFA 2026 Dashboard")
    theme_choice = st.radio("🎨 Theme Mode", ["Dark", "Light"], 
                            index=0 if st.session_state["theme"] == "dark" else 1,
                            horizontal=True)
    st.session_state["theme"] = theme_choice.lower()

apply_custom_styles(st.session_state["theme"])

# Load Dataset
df = load_data()
filtered_df = render_sidebar_filters(df)

# Hero Header
st.markdown("""
<div class="fifa-hero">
    <h1>🏆 FIFA World Cup 2026 Performance Analytics</h1>
    <p>Comprehensive player scouting, tactical match intelligence, multi-metric performance insights, and AI-driven scout recommendations for the 2026 tournament.</p>
    <p style="text-align: right;"><b>Made By Michael Fernandes</b></p>
</div>
""", unsafe_allow_html=True)

# Top Bar Features: Player Search & Comparison Expander
col_search, col_compare = st.columns([1, 1])

with col_search:
    with st.expander("🔍 Quick Player Search Autocomplete", expanded=False):
        all_players = sorted(df['player_name'].unique()) if 'player_name' in df.columns else []
        search_player = st.selectbox("Search for a player:", [""] + all_players)
        if search_player:
            player_data = df[df['player_name'] == search_player]
            if len(player_data) > 0:
                p_latest = player_data.iloc[-1]
                st.success(f"**{search_player}** ({p_latest.get('position', 'N/A')}) - {p_latest.get('team', 'N/A')}")
                st.write(f"**Age:** {p_latest.get('age', 'N/A')} | **Club:** {p_latest.get('club_name', 'N/A')} | **Foot:** {p_latest.get('preferred_foot', 'N/A')}")
                st.write(f"**Market Value:** €{p_latest.get('market_value_eur', 0)/1e6:.1f}M | **Avg Rating:** {player_data['player_rating'].mean():.2f}")

with col_compare:
    with st.expander("⚔️ Head-to-Head Player Comparison (Player A vs Player B)", expanded=False):
        p_list = sorted(df['player_name'].unique()) if 'player_name' in df.columns else []
        col_pa, col_pb = st.columns(2)
        with col_pa:
            player_a = st.selectbox("Select Player A", p_list, index=0 if len(p_list) > 0 else 0)
        with col_pb:
            player_b = st.selectbox("Select Player B", p_list, index=min(1, len(p_list)-1) if len(p_list) > 1 else 0)
            
        if player_a and player_b and player_a != player_b:
            summary_df = get_player_career_summary(df)
            pa_row = summary_df[summary_df['player_name'] == player_a]
            pb_row = summary_df[summary_df['player_name'] == player_b]
            
            if len(pa_row) > 0 and len(pb_row) > 0:
                pa_stat = pa_row.iloc[0]
                pb_stat = pb_row.iloc[0]
                
                # Side by side KPI cards
                kpi_c1, kpi_c2 = st.columns(2)
                with kpi_c1:
                    st.markdown(f"#### 🟦 {player_a}")
                    st.write(f"**Team:** {pa_stat.get('team', 'N/A')} | **Position:** {pa_stat.get('position', 'N/A')}")
                    st.write(f"**Goals:** {pa_stat.get('goals', 0)} | **Assists:** {pa_stat.get('assists', 0)}")
                    st.write(f"**Avg Rating:** {pa_stat.get('player_rating', 0):.2f}")
                with kpi_c2:
                    st.markdown(f"#### 🟨 {player_b}")
                    st.write(f"**Team:** {pb_stat.get('team', 'N/A')} | **Position:** {pb_stat.get('position', 'N/A')}")
                    st.write(f"**Goals:** {pb_stat.get('goals', 0)} | **Assists:** {pb_stat.get('assists', 0)}")
                    st.write(f"**Avg Rating:** {pb_stat.get('player_rating', 0):.2f}")
                
                categories = ['Pass Accuracy', 'Creativity', 'Defending', 'Offense', 'Pressure', 'Consistency', 'Clutch']
                vals_a = [
                    pa_stat.get('pass_accuracy', 50), pa_stat.get('creativity_score', 50),
                    pa_stat.get('defensive_contribution', 50)*10, pa_stat.get('offensive_contribution', 50)*10,
                    pa_stat.get('pressure_resistance', 50), pa_stat.get('consistency_score', 50),
                    pa_stat.get('clutch_performance_score', 50)
                ]
                vals_b = [
                    pb_stat.get('pass_accuracy', 50), pb_stat.get('creativity_score', 50),
                    pb_stat.get('defensive_contribution', 50)*10, pb_stat.get('offensive_contribution', 50)*10,
                    pb_stat.get('pressure_resistance', 50), pb_stat.get('consistency_score', 50),
                    pb_stat.get('clutch_performance_score', 50)
                ]
                radar_fig = plot_radar_chart(categories, vals_a, name=player_a, compare_values=vals_b, compare_name=player_b, theme=st.session_state["theme"])
                st.plotly_chart(radar_fig, use_container_width=True)

st.divider()

# Core Navigation Cards
st.subheader("📌 Explore Dashboard Analytics Modules")
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns(4)

with nav_c1:
    render_kpi_card("Module 1", "Overview", "KPIs & Distributions", badge="1_Overview")
    render_kpi_card("Module 5", "Position", "Box/Violin Analysis", badge="5_Position_Analysis")
with nav_c2:
    render_kpi_card("Module 2", "Player Analysis", "Profile & Radar Charts", badge="2_Player_Analysis")
    render_kpi_card("Module 6", "ML Insights", "Clustering & PCA", badge="6_Performance_Insights")
with nav_c3:
    render_kpi_card("Module 3", "Team Analysis", "Tactical & Formations", badge="3_Team_Analysis")
    render_kpi_card("Module 7", "Physical Metrics", "Speed & Stamina", badge="7_Physical_Metrics")
with nav_c4:
    render_kpi_card("Module 4", "Match Analysis", "Live Scoreboard & Stats", badge="4_Match_Analysis")
    render_kpi_card("Module 8", "AI Scout Engine", "Cosine Similarity Scout", badge="8_AI_Player_Scout")

st.divider()

# Data Exporter Section
st.subheader("📥 Export Filtered Performance Data")
exp_col1, exp_col2, exp_col3 = st.columns(3)

with exp_col1:
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📄 Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name="fifa_2026_filtered_performance.csv",
        mime="text/csv",
        use_container_width=True
    )

with exp_col2:
    buffer_excel = io.BytesIO()
    with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
        filtered_df.head(5000).to_excel(writer, index=False, sheet_name="FIFA_2026")
    excel_data = buffer_excel.getvalue()
    st.download_button(
        "📊 Download Excel Report (.xlsx)",
        data=excel_data,
        file_name="fifa_2026_performance_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with exp_col3:
    # Summary Report Text Download
    summary_text = f"""FIFA WORLD CUP 2026 PERFORMANCE SUMMARY REPORT
Total Filtered Records: {len(filtered_df):,}
Total Teams: {filtered_df['team'].nunique() if 'team' in filtered_df else 0}
Total Players: {filtered_df['player_name'].nunique() if 'player_name' in filtered_df else 0}
Total Goals Scored: {filtered_df['goals'].sum() if 'goals' in filtered_df else 0}
Average Player Rating: {filtered_df['player_rating'].mean() if 'player_rating' in filtered_df else 0:.2f}
Average Performance Score: {filtered_df['performance_score'].mean() if 'performance_score' in filtered_df else 0:.2f}
"""
    st.download_button(
        "📑 Download Text Executive Report",
        data=summary_text.encode('utf-8'),
        file_name="fifa_2026_executive_summary.txt",
        mime="text/plain",
        use_container_width=True
    )
