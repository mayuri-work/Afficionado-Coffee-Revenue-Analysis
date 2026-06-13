import streamlit as st
import pandas as pd
import plotly.express as px


coffee_layout = dict(
    template="plotly_white",
    paper_bgcolor="#F8F4F0",
    plot_bgcolor="#FFF8F3",
    font=dict(
        color="#4E342E",
        size=14
    )
)

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="Coffee Analytics Dashboard",
    page_icon="☕",
    layout="wide"
)

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
☕ Afficionado Coffee Roasters
</h1>

<h3 style="color:white;">
Product Optimization & Revenue Analysis Dashboard
</h3>

<p style="color:white;">
Brewing Insights • Driving Revenue • Optimizing Products
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ----------------------------------
# SIDEBAR
# ----------------------------------

# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.markdown("### 🎯 Filters")

category = st.sidebar.multiselect(
    "☕ Category",
    df["product_category"].unique(),
    default=list(df["product_category"].unique())
)

store = st.sidebar.multiselect(
    "🏪 Store Location",
    df["store_location"].unique(),
    default=list(df["store_location"].unique())
)

top_n = st.sidebar.slider(
    "Top N Products",
    min_value=5,
    max_value=20,
    value=10
)

# ----------------------------------
# FILTER DATA
# ----------------------------------

filtered_df = df[
    (df["product_category"].isin(category)) &
    (df["store_location"].isin(store))
]

# ----------------------------------
# KPI VALUES
# ----------------------------------

revenue = filtered_df["Revenue"].sum()

qty = filtered_df["transaction_qty"].sum()

transactions = filtered_df["transaction_id"].nunique()

products = filtered_df["product_detail"].nunique()

# ----------------------------------
# SIDEBAR INSIGHTS
# ----------------------------------

hero_product = "☕ I Need My Bean! T-shirt"

st.sidebar.markdown(f"""
<div style="
background-color:#3E2723;
padding:18px;
border-radius:15px;
border-left:5px solid #D7CCC8;
">

<div style="
color:#D7CCC8;
font-size:14px;
font-weight:bold;
">
🏆 HERO PRODUCT
</div>

<div style="
color:white;
font-size:20px;
font-weight:bold;
margin-top:8px;
">
{hero_product}
</div>

</div>
""", unsafe_allow_html=True)

# ----------------------------------
# KPI CARDS
# ----------------------------------

# ----------------------------------
# COFFEE KPI CARDS
# ----------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 Revenue</div>
        <div class="kpi-value">${revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🛒 Quantity Sold</div>
        <div class="kpi-value">{qty:,}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📄 Transactions</div>
        <div class="kpi-value">{transactions:,}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">☕ Products</div>
        <div class="kpi-value">{products}</div>
    </div>
    """, unsafe_allow_html=True)
# ----------------------------------
# TOP ROW
# ----------------------------------

left, right = st.columns(2)

with left:

    top_revenue = (
        filtered_df.groupby("product_detail")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        top_revenue,
        x="Revenue",
        y="product_detail",
        orientation="h",
        title="Top Revenue Products"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    top_sales = (
        filtered_df.groupby("product_detail")["transaction_qty"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        top_sales,
        x="transaction_qty",
        y="product_detail",
        orientation="h",
        title="Top Selling Products"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------
# SECOND ROW
# ----------------------------------

left, right = st.columns(2)

with left:

    category_revenue = (
        filtered_df.groupby("product_category")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_revenue,
        values="Revenue",
        names="product_category",
        title="Category Revenue Share"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    store_revenue = (
        filtered_df.groupby("store_location")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        store_revenue,
        x="store_location",
        y="Revenue",
        title="Revenue by Store"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------
# POPULARITY VS REVENUE
# ----------------------------------

st.markdown("""
<h2 style="
color:#4E342E;
font-weight:bold;
">
📊 Popularity vs Revenue
</h2>
""", unsafe_allow_html=True)

product_summary = (
    filtered_df.groupby("product_detail")
    .agg({
        "transaction_qty":"sum",
        "Revenue":"sum"
    })
    .reset_index()
)

fig = px.scatter(
    product_summary,
    x="transaction_qty",
    y="Revenue",
    hover_name="product_detail",
    title="Popularity vs Revenue"
)

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
    filtered_df.groupby("product_detail")
    .agg({
        "transaction_qty":"sum",
        "Revenue":"sum"
    })
    .reset_index()
)

st.dataframe(
    table,
    use_container_width=True
)

# ----------------------------------
# DOWNLOAD BUTTON
# ----------------------------------

st.download_button(
    "⬇ Download Filtered Data",
    filtered_df.to_csv(index=False),
    "coffee_data.csv"
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
💡 Business Recommendations
</h3>

<ul style="color:#5D4037;font-size:16px;">
<li>Focus marketing efforts on Coffee and Tea categories.</li>
<li>Promote top revenue-generating products.</li>
<li>Review low-performing menu items.</li>
<li>Maintain product diversity.</li>
<li>Leverage hero products in campaigns.</li>
</ul>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:linear-gradient(90deg,#3E2723,#6D4C41);
padding:15px;
border-radius:10px;
text-align:center;
margin-top:20px;
">

<span style="
color:white;
font-size:16px;
font-weight:bold;
">
☕ Built with Streamlit | Data Analytics Project | 2026
</span>

</div>
""", unsafe_allow_html=True)