import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.markdown("""
<style>
            /* Coffee Slider */

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #6D4C41 !important;
}

.stSlider [data-baseweb="slider"] > div > div {
    background-color: #A1887F !important;
}

/* Main background */
.stApp {
    background-color: #F8F4F0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #3E2723;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* KPI Cards */
.kpi-card {
    background-color: #D7CCC8;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
}

.kpi-value {
    font-size: 30px;
    font-weight: bold;
    color: #4E342E;
}

.kpi-title {
    font-size: 16px;
    color: #5D4037;
}

/* Headers */
h1, h2, h3 {
    color: #4E342E;
}

/* Tables */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* Recommendation box */
.recommend-box {
    background-color: #EFEBE9;
    padding: 15px;
    border-left: 6px solid #6D4C41;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Selected filter pills */
span[data-baseweb="tag"] {
    background-color: #6D4C41 !important;
    color: white !important;
}

/* Cross icon inside pills */
span[data-baseweb="tag"] svg {
    fill: white !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# COFFEE THEME
# ----------------------------------

coffee_layout = dict(
    template="plotly_dark",
    paper_bgcolor="#020817",
    plot_bgcolor="#020817",
    font=dict(
        color="white",
        size=14
    )
)

# ----------------------------------
# LOAD DATA
# ----------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "Afficionado Coffee Roasters.xlsx - Transactions.csv"
    )

    df["Revenue"] = (
        df["transaction_qty"]
        * df["unit_price"]
    )

    return df


df = load_data()

# ----------------------------------
# HEADER
# ----------------------------------

st.markdown("""
<div style="
background: linear-gradient(90deg,#3E2723,#6D4C41);
padding:25px;
border-radius:15px;
text-align:center;
">

<h1 style="color:white;">
📈 Revenue Optimization
</h1>

<h3 style="color:white;">
Analyze Revenue Contribution & Business Impact
</h3>

<p style="color:white;">
Discover revenue drivers and optimization opportunities
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ----------------------------------
# KPI VALUES
# ----------------------------------

total_revenue = df["Revenue"].sum()

top_product = (
    df.groupby("product_detail")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

# Pareto data

pareto = (
    df.groupby("product_detail")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

pareto["Contribution_%"] = (
    pareto["Revenue"]
    / pareto["Revenue"].sum()
) * 100

pareto["Cumulative_%"] = (
    pareto["Contribution_%"]
    .cumsum()
)

top10_ratio = (
    pareto.head(10)["Revenue"].sum()
    / pareto["Revenue"].sum()
) * 100

products_80 = len(
    pareto[
        pareto["Cumulative_%"] <= 80
    ]
)

# ----------------------------------
# KPI CARDS
# ----------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 Revenue</div>
        <div class="kpi-value">${total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🏆 Top Product</div>
        <div class="kpi-value-small">{top_product}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📊 Top 10 Revenue Share</div>
        <div class="kpi-value">{top10_ratio:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">☕ Products for 80%</div>
        <div class="kpi-value">{products_80}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------------------------
# CATEGORY REVENUE
# ----------------------------------

left, right = st.columns(2)

with left:

    category_revenue = (
        df.groupby("product_category")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_revenue,
        values="Revenue",
        names="product_category",
        title="📊 Revenue by Category"
    )

    fig.update_layout(**coffee_layout)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    store_revenue = (
        df.groupby("store_location")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        store_revenue,
        x="store_location",
        y="Revenue",
        title="🏪 Revenue by Store",
        color_discrete_sequence=["#8EC5F4"]
    )

    fig.update_layout(**coffee_layout)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------
# REVENUE CHAMPIONS
# ----------------------------------

top_revenue = (
    df.groupby("product_detail")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_revenue,
    x="Revenue",
    y="product_detail",
    orientation="h",
    title="💰 Revenue Champions",
    color_discrete_sequence=["#8EC5F4"]
)

fig.update_layout(**coffee_layout)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# PRODUCT TYPE REVENUE
# ----------------------------------

product_type_revenue = (
    df.groupby("product_type")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    product_type_revenue,
    x="Revenue",
    y="product_type",
    orientation="h",
    title="☕ Product Types Driving Revenue",
    color_discrete_sequence=["#8EC5F4"]
)

fig.update_layout(**coffee_layout)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# PARETO ANALYSIS
# ----------------------------------

st.markdown("""
<h2 style="color:#4E342E;">
📊 Pareto Analysis (80/20 Rule)
</h2>
""", unsafe_allow_html=True)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=pareto.head(20)["product_detail"],
        y=pareto.head(20)["Contribution_%"],
        name="Contribution %"
    )
)

fig.add_trace(
    go.Scatter(
        x=pareto.head(20)["product_detail"],
        y=pareto.head(20)["Cumulative_%"],
        mode="lines+markers",
        name="Cumulative %"
    )
)

fig.update_layout(**coffee_layout)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# REVENUE TABLE
# ----------------------------------

st.markdown("""
<h2 style="color:#4E342E;">
📋 Revenue Contribution Table
</h2>
""", unsafe_allow_html=True)

st.dataframe(
    pareto,
    use_container_width=True
)

# ----------------------------------
# DOWNLOAD
# ----------------------------------

st.download_button(
    "⬇ Download Revenue Analysis",
    pareto.to_csv(index=False),
    "revenue_analysis.csv"
)

# ----------------------------------
# RECOMMENDATIONS
# ----------------------------------

st.markdown("""
<div style="
background-color:#EFEBE9;
padding:20px;
border-radius:12px;
border-left:8px solid #6D4C41;
">

<h3 style="color:#4E342E;">
💡 Revenue Optimization Recommendations
</h3>

<ul style="color:#5D4037;font-size:16px;">
<li>Focus marketing on Coffee and Tea categories.</li>
<li>Promote high-revenue products aggressively.</li>
<li>Review low-impact menu items.</li>
<li>Monitor revenue concentration risk.</li>
<li>Expand successful product lines.</li>
<li>Use hero products for cross-selling.</li>
</ul>

</div>
""", unsafe_allow_html=True)