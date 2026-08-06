# ⚽ FIFA World Cup 2026 Player Performance Analytics Dashboard

An advanced, interactive 8-page Streamlit web application providing deep data analytics, tactical match intelligence, machine learning performance insights, physical performance tracking, and AI-powered player scouting for the FIFA World Cup 2026 dataset (54,600 player match records).

---

## 🌟 Key Features

1. **Overview Dashboard (`1_Overview.py`)**:
   - 8 Glassmorphic KPI Cards (Players, Matches, Teams, Goals, Rating, xG, Performance Score, Pass Accuracy).
   - Goals by Team, Match Results Pie, Tournament Stage Donut, Top 15 Scorers, Highest Rated Players, Position Rating Box Plot, Market Value Distribution, Feature Correlation Heatmap.

2. **Player Analysis (`2_Player_Analysis.py`)**:
   - Full Player Profile card (Age, Nationality, Club, Foot, Position, Height, Weight, Market Value).
   - Rating & Performance Score Timelines, Goals vs xG Scatter, Shots vs Target, 7-Axis Skill Capability Radar Chart, Match-wise performance table.

3. **Team Analysis (`3_Team_Analysis.py`)**:
   - Team level KPIs, score trends by match, tactical formation position counts, top scorers & assist providers, rating and market value distributions.

4. **Match Analysis (`4_Match_Analysis.py`)**:
   - Live custom Scoreboard widget (e.g. Spain 3 - 1 France), player rating distributions, xG scatter plots, offensive & defensive contribution breakdowns, full match stats table.

5. **Position Analysis (`5_Position_Analysis.py`)**:
   - Interactive role selector (GK, CB, RB, LB, CM, CAM, CDM, RW, LW, ST), position KPIs, rating box plots, violin spread plots, position radar benchmarks, parallel coordinates multi-metric analysis.

6. **Machine Learning Insights (`6_Performance_Insights.py`)**:
   - Market Value vs Performance scatter & age bubble charts, K-Means Clustering (Elite, Good, Average, Developing), 2D PCA Skill Projection, Random Forest Feature Importance, SHAP-style rating explainability.

7. **Physical Metrics (`7_Physical_Metrics.py`)**:
   - Distance Covered, Sprint Distance, Top Speed, Accelerations, Decelerations, Stamina KPIs; Top Fastest Players, Distance Covered, Speed Distribution, Stamina by Position.

8. **AI Player Scout (`8_AI_Player_Scout.py`)**:
   - Interactive scout filter criteria (Position, Age, Market Value, Preferred Foot, Min Rating, Min Performance).
   - Cosine Similarity & Nearest Neighbors scoring engine returning match percentages (0-100%), candidate cards, radar comparisons, and recommendation tables.

9. **Global Features (`app.py`)**:
   - 15-parameter sidebar filtering suite with quick reset & active record counter.
   - Head-to-Head Player Comparison Drawer (Player A vs Player B side-by-side radar and KPIs).
   - Player Search Autocomplete bar.
   - Theme Mode Switcher (Dark / Light Theme).
   - Export Filtered Dataset to CSV, Excel Report, or Text Executive Summary.

---

## 🛠️ Tech Stack

- **Frontend / Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly Express & Plotly Graph Objects (20+ custom dark/glassmorphism chart types)
- **Machine Learning**: Scikit-Learn (K-Means, PCA, Random Forest, Cosine Similarity)
- **Exporting**: OpenPyXL, CSV, BytesIO
- **Styling**: Custom CSS with HSL dark/light glassmorphic tokens & micro-animations

---

## 🚀 Quick Start Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Streamlit Application**:
   ```bash
   streamlit run app.py
   ```

3. Open your browser at `http://localhost:8501`.
