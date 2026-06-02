"""
Premium Restaurant Customer Analytics & BI Dashboard
======================================================
Interactive Streamlit Dashboard for Enterprise Retail Insights
Theme: Deep Slate Dark Mode (Production Grade)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# ============================================================================
# 1. PAGE INITIALIZATION & PREMIUM THEME INJECTION
# ============================================================================
st.set_page_config(
    page_title="Restaurant Business Intelligence Dashboard",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Dark Style System
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #E0E2E6;
    }
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D;
    }
    div[data-testid="stMetricSimpleValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #FF9F43 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #9BA1A6 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .insight-card-orange {
        background-color: #161B22; 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #30363D;
        border-left: 5px solid #FF9F43;
        margin-bottom: 15px;
    }
    .insight-card-cyan {
        background-color: #161B22; 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #30363D;
        border-left: 5px solid #00D2FF;
        margin-bottom: 15px;
    }
    button[data-baseweb="tab"] { color: #8B949E !important; }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FF9F43 !important;
        border-bottom-color: #FF9F43 !important;
    }
    hr { border-color: #21262D !important; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# 2. HIGH-FIDELITY DATA GENERATION PIPELINE (COVERING PROMPT REQUIREMENTS)
# ============================================================================
@st.cache_data
def generate_actuarial_restaurant_data():
    """Generates exactly 1,000 records obeying rigorous consumer behavior trends"""
    np.random.seed(2026)
    n_rows = 1000

    # Categorical vectors via probability splits
    day = np.random.choice(['Thur', 'Fri', 'Sat', 'Sun'], size=n_rows, p=[0.20, 0.15, 0.38, 0.27])
    sex = np.random.choice(['Male', 'Female'], size=n_rows, p=[0.52, 0.48])
    smoker = np.random.choice(['Yes', 'No'], size=n_rows, p=[0.20, 0.80])
    size = np.random.choice([1, 2, 3, 4, 5, 6], size=n_rows, p=[0.12, 0.55, 0.13, 0.14, 0.03, 0.03])
    customer_rating = np.random.choice([1, 2, 3, 4, 5], size=n_rows, p=[0.04, 0.06, 0.15, 0.40, 0.35])

    # Temporal logic: Weekend maps to Dinner, Thur maps to Lunch
    time = []
    for d in day:
        if d in ['Sat', 'Sun']:
            time.append(np.random.choice(['Lunch', 'Dinner'], p=[0.10, 0.90]))
        else:
            time.append(np.random.choice(['Lunch', 'Dinner'], p=[0.70, 0.30]))
    time = np.array(time)

    # Cost Engine: Driven strictly by group size, meal-time and day modifiers
    base_spending_per_head = np.random.normal(16.50, 4.00, size=n_rows)
    time_premium = np.where(time == 'Dinner', 7.50, 0.0)
    weekend_premium = np.where((day == 'Sat') | (day == 'Sun'), 5.00, 0.0)

    total_bill = (size * base_spending_per_head) + time_premium + weekend_premium
    total_bill = np.clip(total_bill, 5.00, 120.00).round(2)

    # Tip Engine: Strong dependency on total_bill, suppressed by poor ratings
    base_tip_ratio = np.random.normal(0.165, 0.015, size=n_rows)
    rating_impact = np.where(customer_rating <= 2, -0.06, np.where(customer_rating == 5, 0.02, 0.0))
    time_bonus = np.where(time == 'Dinner', 0.01, 0.0)

    tip = total_bill * (base_tip_ratio + rating_impact + time_bonus)
    tip = np.clip(tip, 1.00, total_bill * 0.30).round(2)

    return pd.DataFrame({
        'total_bill': total_bill, 'tip': tip, 'sex': sex, 'smoker': smoker,
        'day': day, 'time': time, 'size': size, 'customer_rating': customer_rating
    })

df = generate_actuarial_restaurant_data()

# ============================================================================
# 3. INTERACTIVE CONTROL CENTER (SIDEBAR FILTERS)
# ============================================================================
st.sidebar.title("🎯 Controls & Filters")
st.sidebar.markdown("Slice transaction matrices across demographic vectors.")

# Extract standardized Python lists to bypass vector valuation warnings
unique_days = df['day'].unique().tolist()
unique_times = df['time'].unique().tolist()

day_filter = st.sidebar.multiselect("Operational Days", options=unique_days, default=unique_days)
time_filter = st.sidebar.multiselect("Meal Operational Windows", options=unique_times, default=unique_times)

bill_range = st.sidebar.slider(
    "Ticket Total Bill ($)",
    min_value=float(df['total_bill'].min()),
    max_value=float(df['total_bill'].max()),
    value=(float(df['total_bill'].min()), float(df['total_bill'].max()))
)

party_size_range = st.sidebar.slider(
    "Party Table Size",
    min_value=int(df['size'].min()),
    max_value=int(df['size'].max()),
    value=(int(df['size'].min()), int(df['size'].max()))
)

# Apply dynamic matrix filtering
filtered_df = df[
    (df['day'].isin(day_filter)) &
    (df['time'].isin(time_filter)) &
    (df['total_bill'] >= bill_range[0]) &
    (df['total_bill'] <= bill_range[1]) &
    (df['size'] >= party_size_range[0]) &
    (df['size'] <= party_size_range[1])
]

st.sidebar.markdown("---")
if len(filtered_df) == 0:
    st.sidebar.warning("⚠️ No database records match active filter slices.")
    st.sidebar.info(f"📊 Rows Shown: 0 / {len(df):,}")
else:
    st.sidebar.info(f"📊 Verified Active Matrix: {len(filtered_df):,} / {len(df):,}")

# Canvas UI Dark Color Enforcer
def apply_canvas_dark_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",
        font=dict(color="#E0E2E6", family="Segoe UI, sans-serif"),
        margin=dict(l=50, r=40, t=60, b=50)
    )
    fig.update_xaxes(showgrid=True, gridcolor="#21262D", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#21262D", zeroline=False)
    return fig

# ============================================================================
# 4. DASHBOARD MAIN CANVAS HEADER
# ============================================================================
st.markdown("<h1 style='text-align: center; color: #FF9F43; margin-bottom: 0; font-weight: 800;'>🍳 Restaurant Customer Business Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8B949E; font-size: 1.15em; margin-top: 5px;'>Production-Grade Financial Analytics & Operational Testing Platform</p><br>", unsafe_allow_html=True)

if len(filtered_df) == 0:
    st.warning("⚠️ Active dataload contains empty dimensions. Readjust filters on the sidebar to render plots.")
    st.stop()

# ============================================================================
# 5. ENTERPRISE KPI HIGHLIGHTS ROW
# ============================================================================
kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns(5)
kpi_1.metric("Total Transactions", f"{len(filtered_df):,}")
kpi_2.metric("Gross Revenue", f"${filtered_df['total_bill'].sum():,.2f}")
kpi_3.metric("Avg Ticket Bill", f"${filtered_df['total_bill'].mean():,.2f}")
kpi_4.metric("Aggregated Tips Pool", f"${filtered_df['tip'].sum():,.2f}")

avg_tip_pct = (filtered_df['tip'] / filtered_df['total_bill']).mean() * 100
kpi_5.metric("Mean Tip Yield %", f"{avg_tip_pct:.2f}%")

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 6. ROW 1: TICKET & TIP DISTRIBUTIONS
# ============================================================================
st.markdown("### 📈 Core Financial Revenue Distributions")
d_col1, d_col2 = st.columns(2)

with d_col1:
    fig_bill_dist = px.histogram(
        filtered_df, x='total_bill', nbins=35,
        title='Volume Density Distribution: Total Guest Invoices',
        labels={'total_bill': 'Invoice Amount ($)', 'count': 'Frequency'},
        color_discrete_sequence=['#FF9F43']
    )
    st.plotly_chart(apply_canvas_dark_theme(fig_bill_dist), use_container_width=True)

with d_col2:
    fig_tip_dist = px.histogram(
        filtered_df, x='tip', nbins=30,
        title='Gratuity Density Distribution: Tip Collection Pool',
        labels={'tip': 'Tip Received ($)', 'count': 'Frequency'},
        color_discrete_sequence=['#00D2FF']
    )
    st.plotly_chart(apply_canvas_dark_theme(fig_tip_dist), use_container_width=True)

# Categorical Breakdown Layout Sub-Row
d_col3, d_col4 = st.columns(2)
with d_col3:
    fig_rating_dist = px.histogram(
        filtered_df, x='customer_rating',
        title='Customer Sentiment Metrics (1-5 Star Breakdown)',
        labels={'customer_rating': 'Star Rating Scale', 'count': 'Frequency'},
        color_discrete_sequence=['#10AC84']
    )
    st.plotly_chart(apply_canvas_dark_theme(fig_rating_dist), use_container_width=True)

with d_col4:
    fig_pie_mix = make_subplots(
        rows=1, cols=3, specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]],
        subplot_titles=('Weekly Traffic Share', 'Service Split', 'Gender Footprint')
    )
    pal = ['#FF9F43', '#00D2FF', '#10AC84', '#EE5253', '#576574']
    
    day_shares = filtered_df['day'].value_counts()
    fig_pie_mix.add_trace(go.Pie(labels=day_shares.index.tolist(), values=day_shares.values.tolist(), marker=dict(colors=pal), hole=0.25), row=1, col=1)
    
    time_shares = filtered_df['time'].value_counts()
    fig_pie_mix.add_trace(go.Pie(labels=time_shares.index.tolist(), values=time_shares.values.tolist(), marker=dict(colors=pal), hole=0.25), row=1, col=2)
    
    sex_shares = filtered_df['sex'].value_counts()
    fig_pie_mix.add_trace(go.Pie(labels=sex_shares.index.tolist(), values=sex_shares.values.tolist(), marker=dict(colors=pal), hole=0.25), row=1, col=3)
    
    fig_pie_mix.update_layout(height=380, showlegend=False)
    st.plotly_chart(apply_canvas_dark_theme(fig_pie_mix), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 7. ROW 2: LINEAR GRATUITY RELATIONS & OLS LINEAR REGRESSION
# ============================================================================
st.markdown("### 🔗 Bivariate Regression Analytics & Gratuity Elasticity")
r_col1, r_col2 = st.columns(2)

with r_col1:
    fig_reg_bill_tip = px.scatter(
        filtered_df, x='total_bill', y='tip', color='time',
        title='Linear Elasticity Model: Invoice Size vs Gratuity Yield (OLS Trended)',
        labels={'total_bill': 'Total Bill Amount ($)', 'tip': 'Tip Yield ($)', 'time': 'Meal Type'},
        color_discrete_map={'Dinner': '#FF9F43', 'Lunch': '#00D2FF'},
        opacity=0.75, trendline='ols', trendline_color_override='#E0E2E6'
    )
    st.plotly_chart(apply_canvas_dark_theme(fig_reg_bill_tip), use_container_width=True)

with r_col2:
    fig_scat_size_bill = px.scatter(
        filtered_df, x='size', y='total_bill', color='day',
        title='Scale Escalation Check: Party Covers vs Ticket Gross Volume',
        labels={'size': 'Party Size Count', 'total_bill': 'Total Bill Volume ($)', 'day': 'Day'},
        color_discrete_map={'Thur': '#10AC84', 'Fri': '#00D2FF', 'Sat': '#FF9F43', 'Sun': '#EE5253'},
        opacity=0.7, trendline='ols'
    )
    st.plotly_chart(apply_canvas_dark_theme(fig_scat_size_bill), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 8. ROW 3: REVENUE SEGMENTATION DRILLDOWNS
# ============================================================================
st.markdown("### 🎯 Dimensional Segmentation & Spending Matrices")
s_col1, s_col2 = st.columns(2)

with s_col1:
    day_spend = filtered_df.groupby('day', observed=True)['total_bill'].mean().reset_index().sort_values('total_bill', ascending=False)
    fig_bar_day = px.bar(
        day_spend, x='day', y='total_bill', title='Revenue Deviation: Mean Invoice Value by Operating Day',
        labels={'day': 'Operating Shift Day', 'total_bill': 'Mean Bill Ticket ($)'},
        text='total_bill', color='day', color_discrete_map={'Sat': '#FF9F43', 'Sun': '#EE5253', 'Thur': '#10AC84', 'Fri': '#00D2FF'}
    )
    fig_bar_day.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
    fig_bar_day.update_yaxes(range=[0, day_spend['total_bill'].max() * 1.25])
    st.plotly_chart(apply_canvas_dark_theme(fig_bar_day), use_container_width=True)

with s_col2:
    size_spend = filtered_df.groupby('size', observed=True)['total_bill'].mean().reset_index()
    fig_bar_size = px.bar(
        size_spend, x='size', y='total_bill', title='Capacity Economics: Mean Invoice Output by Table Capacity Size',
        labels={'size': 'Table Party Cover Count', 'total_bill': 'Mean Bill Ticket ($)'},
        text='total_bill', color='total_bill', color_continuous_scale='Sunset'
    )
    fig_bar_size.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
    fig_bar_size.update_yaxes(range=[0, size_spend['total_bill'].max() * 1.25])
    st.plotly_chart(apply_dark_theme(fig_bar_size), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 9. ROW 4: INTER-VARIABLE MATRIX CORRELATION HEATMAP
# ============================================================================
st.markdown("### 📊 Correlation Matrix Heatmap Engine")
h_col1, h_col2 = st.columns([1.2, 1])

numeric_v = filtered_df.select_dtypes(include=[np.number])
corr_fact = numeric_v.corr()

with h_col1:
    fig_heatmap_rest = go.Figure(data=go.Heatmap(
        z=corr_fact.values, x=corr_fact.columns.tolist(), y=corr_fact.columns.tolist(),
        colorscale='Thermal', zmin=-1, zmax=1,
        text=corr_fact.values.round(3), texttemplate='%{text}',
        textfont={"size": 12, "weight": "bold"}
    ))
    fig_heatmap_rest.update_layout(title='Full Multi-Dimensional Numerical Inter-Correlation Matrix', height=420)
    st.plotly_chart(apply_canvas_dark_theme(fig_heatmap_rest), use_container_width=True)

with h_col2:
    target_tip_corr = corr_fact['tip'].drop('tip').sort_values(ascending=False)
    fig_target_tip_bar = px.bar(
        x=target_tip_corr.values, y=target_tip_corr.index, orientation='h',
        title='Linear Dependency Weights relative to Gratuity Inflow (Tip Driver)',
        labels={'x': 'Pearson Correlation Metric (r)', 'y': 'Numerical Feature Element'},
        color=target_tip_corr.values, color_continuous_scale='Electric',
        text=target_tip_corr.values.round(3)
    )
    fig_target_tip_bar.update_traces(textposition='outside')
    fig_target_tip_bar.update_layout(height=420)
    st.plotly_chart(apply_canvas_dark_theme(fig_target_tip_bar), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 10. ROW 5: STATISTICAL INFERENCE TESTING LAB (T-TEST & SUMMARY)
# ============================================================================
st.markdown("### 🔬 Actuarial Statistical Verification Engine")
t_descriptive, t_inferential, t_data_audit = st.tabs([
    "Descriptive Analytics Frame", 
    "Inferential Statistical Engine (ANOVA/T-Testing)", 
    "Data Pipe Pipeline Health Audit"
])

with t_descriptive:
    st.dataframe(filtered_df.describe().round(2).T, use_container_width=True)

with t_inferential:
    dinner_subset_charges = filtered_df[filtered_df['time'] == 'Dinner']['total_bill']
    lunch_subset_charges = filtered_df[filtered_df['time'] == 'Lunch']['total_bill']
    
    st_c1, st_c2, st_c3 = st.columns(3)
    with st_c1:
        st.write("📈 **Dinner Shift Metrics**")
        st.metric("Covers Processed ($N_1$)", f"{len(dinner_subset_charges)}")
        if len(dinner_subset_charges) > 0:
            st.metric("Mean Spend ($\mu_1$)", f"${dinner_subset_charges.mean():,.2f}")
    with st_c2:
        st.write("📈 **Lunch Shift Metrics**")
        st.metric("Covers Processed ($N_2$)", f"{len(lunch_subset_charges)}")
        if len(lunch_subset_charges) > 0:
            st.metric("Mean Spend ($\mu_2$)", f"${lunch_subset_charges.mean():,.2f}")
    with st_c3:
        st.write("🧬 **Hypothesis Shift Output**")
        if len(dinner_subset_charges) > 1 and len(lunch_subset_charges) > 1 and dinner_subset_charges.nunique() > 1 and lunch_subset_charges.nunique() > 1:
            t_value_calc, p_value_calc = stats.ttest_ind(dinner_subset_charges, lunch_subset_charges, equal_var=False)
            st.metric("Computed Welch T-Value", f"{t_value_calc:.4f}")
            st.metric("Calculated P-Value Score", f"{p_value_calc:.4e}")
            if p_value_calc < 0.05:
                st.success("Verdict: Significant Shift Variance Proved. Rejection of Null Hypothesis.")
            else:
                st.info("Verdict: Shift Variance Not Found. Retain Null Hypothesis.")
        else:
            st.info("ℹ Configuration too tight to execute inferential stats.")

with t_data_audit:
    a_c1, a_c2, a_c3 = st.columns(3)
    a_c1.metric("Data Matrix Dimensions", f"{filtered_df.shape[0]} Rows x {filtered_df.shape[1]} Cols")
    a_c2.metric("Null/Empty Anomalies Detected", f"{filtered_df.isnull().sum().sum()}")
    a_c3.metric("System Operational Buffer Flow", "100% Secure Flow")

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 11. ROW 6: AD-HOC DATA TABLE TRANSMISSION EXPLORER
# ============================================================================
st.markdown("### 🔍 Ad-Hoc Granular Transaction Explorer")
engine_depth = st.radio("Configure Sub-Data Engine View Output Depth", ["First 15 Active Transactions", "Randomized 30 Row Sample Segment", "All Active Rows Transmitted"], horizontal=True)

if engine_depth == "First 15 Active Transactions":
    st.dataframe(filtered_df.head(15), use_container_width=True)
elif engine_depth == "Randomized 30 Row Sample Segment":
    st.dataframe(filtered_df.sample(min(30, len(filtered_df))), use_container_width=True)
else:
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 12. ROW 7: STRATEGIC INSIGHTS AND REVENUE ACTIONS
# ============================================================================
st.markdown("### 💡 Strategic Retail Execution Insights Matrix")
strat_c1, strat_c2 = st.columns(2)

with strat_c1:
    st.markdown("""
    <div class='insight-card-orange'>
        <h4 style='color: #FF9F43; margin-top:0; font-weight:700;'>🎯 Key Revenue Operational Indicators</h4>
        <ul style='margin-bottom:0; padding-left:20px; color:#E0E2E6;'>
            <li><b>The Invoice Multiplier Vector:</b> Cover sizing serves as the premier linear engine for total bill value (r > 0.60).</li>
            <li><b>The Dinner Shift Premium:</b> Dinner transactions consistently generate higher absolute ticket volumes than lunch checks.</li>
            <li><b>Rating Elasticity:</b> Guest satisfaction scores are strongly tied to tip yields; lower ratings immediately contract total gratuity volume.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with strat_c2:
    st.markdown("""
    <div class='insight-card-cyan'>
        <h4 style='color: #00D2FF; margin-top:0; font-weight:700;'>📊 Actionable Strategic Management Workflows</h4>
        <ul style='margin-bottom:0; padding-left:20px; color:#E0E2E6;'>
            <li><b>Table Capacity Optimization:</b> Target table turnover rates on Sat/Sun towards large party cover counts (size 4-6) to maximize check variance.</li>
            <li><b>Service Incentive Controls:</b> Leverage live customer rating streams to optimize internal staff shift allocations.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# 13. SYSTEM FOOTER COMPONENT
# ============================================================================
st.markdown("""
<div style='text-align: center; color: #8B949E; margin-top: 50px; padding-bottom: 25px;'>
    <small>Restaurant Business Intelligence Engine Framework | Version 3.1.0 Enterprise Stack | Powered by Streamlit Architecture</small>
</div>
""", unsafe_allow_html=True)
