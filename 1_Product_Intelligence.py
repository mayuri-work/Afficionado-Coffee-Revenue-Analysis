import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# COFFEE THEME
# ----------------------------------
st.markdown("""
<style>

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

coffee_layout = dict(
    template="plotly_dark",
    paper_bgcolor="#020817",
    plot_bgcolor="#020817",
    font=dict(
        color="white",
        size=14
    ),
    title_font=dict(
        color="white",
        size=18
    )
)

# ----------------------------------
# CSS
# ----------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F8F4F0;
}

/* KPI Cards */
.kpi-card {
    background-color: #D7CCC8;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    margin-bottom:10px;
}

.kpi-value {
    font-size: 28px;
    font-weight: bold;
    color: #4E342E;
}

.kpi-title {
    font-size: 16px;
    color: #5D4037;
}

/* Headers */
h1,h2,h3 {
    color:#4E342E;
}

/* Insight Box */
.insight-box {
    background-color:#EFEBE9;
    padding:20px;
    border-radius:12px;
    border-left:8px solid #6D4C41;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# LOAD DATA
# ----------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "Afficionado Coffee Roasters.xlsx - Transactions.csv"
    )

    df["Revenue"] = (
        df["transaction_qty"] *
        df["unit_price"]
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
📦 Product Intelligence
</h1>

<h3 style="color:white;">
Analyze Product Popularity & Performance
</h3>

<p style="color:white;">
Discover best-selling and most efficient products
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ----------------------------------
# PRODUCT SUMMARY
# ----------------------------------

product_summary = (
    df.groupby("product_detail")
    .agg({
        "transaction_qty":"sum",
        "Revenue":"sum"
    })
    .reset_index()
)

# ----------------------------------
# KPI VALUES
# ----------------------------------

total_products = (
    product_summary["product_detail"]
    .nunique()
)

best_product = (
    product_summary
    .sort_values(
        "Revenue",
        ascending=False
    )
    .iloc[0]["product_detail"]
)

avg_revenue = (
    product_summary["Revenue"]
    .mean()
)

# ----------------------------------
# KPI CARDS
# ----------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📦 Total Products</div>
        <div class="kpi-value">{total_products}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🏆 Best Product</div>
        <div class="kpi-value-small">{best_product}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 Average Revenue</div>
        <div class="kpi-value">${avg_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------
# POPULARITY VS REVENUE
# ----------------------------------

st.markdown("""
<h2 style="
color:#4E342E;
font-weight:bold;
">
📊 Popularity vs Revenue Analysis
</h2>
""", unsafe_allow_html=True)

fig = px.scatter(
    product_summary,
    x="transaction_qty",
    y="Revenue",
    hover_name="product_detail",
    color_discrete_sequence=["#8EC5F4"],
    orientation="h",
    title="Top 10 Products by Sales",
)

fig.update_traces(
    marker=dict(
        size=10,
        opacity=0.8,
    )
)

fig.update_layout(**coffee_layout)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# TOP PRODUCTS
# ----------------------------------

st.markdown("""
<h2 style="
color:#4E342E;
font-weight:bold;
">
Top Products
</h2>
""", unsafe_allow_html=True)
left, right = st.columns(2)

with left:

    top_sales = (
        product_summary
        .sort_values(
            "transaction_qty",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
    top_sales,
    x="transaction_qty",
    y="product_detail",
    orientation="h",
    title="Top 10 Products by Sales",
    color_discrete_sequence=["#8EC5F4"]
)

fig.update_layout(**coffee_layout)

st.plotly_chart(
    fig,
    use_container_width=True
)

with right:

    top_revenue = (
        product_summary
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
    top_revenue,
    x="Revenue",
    y="product_detail",
    orientation="h",
    title="Top 10 Products by Revenue",
    color_discrete_sequence=["#8EC5F4"]
)

fig.update_layout(**coffee_layout)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# PRODUCT TABLE
# ----------------------------------

st.markdown("""
<h2 style="
color:#4E342E;
font-weight:bold;
">
📋 Product Performance Table
</h2>
""", unsafe_allow_html=True)

table = (
    product_summary
    .sort_values(
        "Revenue",
        ascending=False
    )
)

st.dataframe(
    table,
    use_container_width=True
)

# ----------------------------------
# DOWNLOAD BUTTON
# ----------------------------------

st.download_button(
    "⬇ Download Product Data",
    table.to_csv(index=False),
    "product_intelligence.csv"
)

# ----------------------------------
# INSIGHTS
# ----------------------------------

st.markdown("""
<div class="insight-box">

<h3 style="color:#4E342E;">
💡 Product Intelligence Insights
</h3>

<ul style="color:#5D4037;font-size:16px;">
<li>Identify products with high sales volume.</li>
<li>Focus promotions on high-revenue products.</li>
<li>Review products with low popularity and revenue.</li>
<li>Improve visibility of top-performing products.</li>
<li>Use best-selling products in marketing campaigns.</li>
</ul>

</div>
""", unsafe_allow_html=True)