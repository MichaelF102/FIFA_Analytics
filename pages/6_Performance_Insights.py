import streamlit as st
import pandas as pd
import plotly.express as px
from utils.loader import load_data
from utils.styles import apply_custom_styles
from utils.filters import render_sidebar_filters
from utils.charts import (
    plot_market_vs_performance_scatter, plot_bubble_age_perf_mv,
    plot_kmeans_clusters, plot_pca_projection, plot_rf_feature_importance
)
from utils.metrics import (
    run_kmeans_clustering, run_pca_projection, run_rf_feature_importance
)

st.set_page_config(page_title="ML Performance Insights | FIFA 2026", page_icon="🤖", layout="wide")
theme = st.session_state.get("theme", "dark")
apply_custom_styles(theme)

df = load_data()
filtered_df = render_sidebar_filters(df)

st.title("🤖 Advanced Machine Learning & Performance Insights")
st.caption("Unsupervised clustering, PCA dimensionality reduction, Random Forest feature attribution, and market valuation analysis.")

# Row 1: Market Value vs Performance Scatter & Bubble Chart
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    fig_mv_perf = plot_market_vs_performance_scatter(filtered_df, theme=theme)
    st.plotly_chart(fig_mv_perf, use_container_width=True)

with r1_c2:
    fig_bubble = plot_bubble_age_perf_mv(filtered_df, theme=theme)
    st.plotly_chart(fig_bubble, use_container_width=True)

st.divider()

# Row 2: Machine Learning Clustering & PCA Projections
st.subheader("🧩 Player Segmentation & Clustering (K-Means)")
clustered_df = run_kmeans_clustering(filtered_df, n_clusters=4)

c1_col, c2_col = st.columns([1.3, 1])

with c1_col:
    fig_cluster = plot_kmeans_clusters(clustered_df, theme=theme)
    st.plotly_chart(fig_cluster, use_container_width=True)

with c2_col:
    st.markdown("#### 📊 Segment Counts & Statistics")
    if 'Cluster_Label' in clustered_df.columns:
        counts = clustered_df['Cluster_Label'].value_counts().reset_index()
        counts.columns = ['Segment', 'Count']
        st.dataframe(counts, use_container_width=True, hide_index=True)
        
        st.caption("""
        - **Elite**: Top tier match impact across scoring, passing & rating.
        - **Good**: Solid consistent performance across key metrics.
        - **Average**: Standard core tournament performances.
        - **Developing**: High upside or specialized lower-volume roles.
        """)

st.divider()

# Row 3: PCA 2D Projection & Random Forest Feature Importance
st.subheader("🧬 Dimensionality Reduction & Predictive Drivers")

r3_c1, r3_c2 = st.columns(2)

with r3_c1:
    pca_df = run_pca_projection(filtered_df)
    fig_pca = plot_pca_projection(pca_df, theme=theme)
    st.plotly_chart(fig_pca, use_container_width=True)

with r3_c2:
    rf_imp = run_rf_feature_importance(filtered_df)
    fig_rf = plot_rf_feature_importance(rf_imp, theme=theme)
    st.plotly_chart(fig_rf, use_container_width=True)

st.divider()

# SHAP / Feature Explanation Section
st.subheader("🔍 SHAP-Style Feature Attribution & Rating Explanainer")
st.markdown("""
Using **Random Forest feature attribution**, the system decomposes individual player ratings into key contribution drivers.
The chart below highlights how key factors (such as **Expected Goals (xG)**, **Pass Accuracy**, **Top Speed**, and **Key Passes**) contribute to overall match ratings.
""")

sample_player = st.selectbox("Select Player to Explain Rating Drivers", sorted(filtered_df['player_name'].unique()) if len(filtered_df) > 0 else [])

if sample_player:
    p_data = filtered_df[filtered_df['player_name'] == sample_player]
    if len(p_data) > 0:
        p_row = p_data.iloc[-1]
        
        # Calculate feature contributions relative to population mean
        numeric_feats = ['expected_goals_xg', 'expected_assists_xa', 'pass_accuracy', 'tackles', 'top_speed_kmh', 'distance_covered_km']
        avail_feats = [f for f in numeric_feats if f in p_data.columns]
        
        contributions = []
        for f in avail_feats:
            mean_val = filtered_df[f].mean()
            player_val = p_row[f]
            diff = player_val - mean_val
            contributions.append({'Feature': f.replace('_', ' ').title(), 'Contribution Delta': round(diff, 2)})
            
        contrib_df = pd.DataFrame(contributions)
        fig_shap = px.bar(contrib_df, x='Contribution Delta', y='Feature', orientation='h',
                          color='Contribution Delta', color_continuous_scale='RdYlGn',
                          title=f"<b>SHAP-style Feature Delta for {sample_player} vs Tournament Mean</b>")
        fig_shap.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
        st.plotly_chart(fig_shap, use_container_width=True)
