import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ----------------------------------
# COFFEE THEME
# ----------------------------------

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
# PAGE STYLING
# ----------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #F8F4F0;
}

section[data-testid="stSidebar"] {
    background-color: #3E2723;
}

section[data-testid="stSidebar"] * {
    color: white;
}

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

</style>
""", unsafe_allow_html=True)

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
🤖 ML Product Success Predictor
</h1>

<h3 style="color:white;">
Predict Product Performance Using Machine Learning
</h3>

<p style="color:white;">
Random Forest Classification Model
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ----------------------------------
# LOAD DATA
# ----------------------------------

df = pd.read_csv(
    "Afficionado Coffee Roasters.xlsx - Transactions.csv"
)

df["Revenue"] = (
    df["transaction_qty"] *
    df["unit_price"]
)

# ----------------------------------
# CREATE PERFORMANCE CLASSES
# ----------------------------------

product_perf = (
    df.groupby("product_detail")
    .agg({
        "Revenue":"sum",
        "transaction_qty":"mean",
        "unit_price":"mean",
        "product_category":"first",
        "store_location":"first"
    })
    .reset_index()
)

high = product_perf["Revenue"].quantile(0.70)
low = product_perf["Revenue"].quantile(0.30)

def classify(revenue):

    if revenue >= high:
        return "High Performer"

    elif revenue <= low:
        return "Low Performer"

    else:
        return "Medium Performer"

product_perf["Performance"] = (
    product_perf["Revenue"]
    .apply(classify)
)

# ----------------------------------
# ENCODING
# ----------------------------------

cat_encoder = LabelEncoder()
store_encoder = LabelEncoder()
target_encoder = LabelEncoder()

product_perf["Category"] = (
    cat_encoder.fit_transform(
        product_perf["product_category"]
    )
)

product_perf["Store"] = (
    store_encoder.fit_transform(
        product_perf["store_location"]
    )
)

product_perf["Target"] = (
    target_encoder.fit_transform(
        product_perf["Performance"]
    )
)

# ----------------------------------
# FEATURES
# ----------------------------------

X = product_perf[
    [
        "transaction_qty",
        "unit_price",
        "Category",
        "Store"
    ]
]

y = product_perf["Target"]

# ----------------------------------
# TRAIN TEST SPLIT
# ----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ----------------------------------
# MODEL
# ----------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    preds
)

# ----------------------------------
# KPI CARDS
# ----------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🎯 Accuracy</div>
        <div class="kpi-value">{accuracy:.2%}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📦 Products</div>
        <div class="kpi-value">{len(product_perf)}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🤖 Model</div>
        <div class="kpi-value">RF</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------------------------
# PREDICTOR
# ----------------------------------

st.markdown("""
<h2 style="color:#4E342E;">
🔮 Predict Product Success
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<h3 style="color:#4E342E;">
📦 Transaction Quantity
</h3>
""", unsafe_allow_html=True)
qty = st.number_input(
    "",
    min_value=1,
    value=10
)

st.markdown("""
<h3 style="color:#4E342E;">
💰 Unit Price
</h3>
""", unsafe_allow_html=True)
price = st.number_input(
    " ",
    min_value=0.1,
    value=5.0
)

st.markdown("""
<h3 style="color:#4E342E;">
☕ Product Category
</h3>
""", unsafe_allow_html=True)
category = st.selectbox(
    "  ",
    df["product_category"].unique()
)

st.markdown("""
<h3 style="color:#4E342E;">
🏪 Store Location
</h3>
""", unsafe_allow_html=True)
store = st.selectbox(
    "   ",
    df["store_location"].unique()
)

if st.button("🔮 Predict Product Success"):

    category_encoded = (
        cat_encoder.transform(
            [category]
        )[0]
    )

    store_encoded = (
        store_encoder.transform(
            [store]
        )[0]
    )

    prediction = model.predict(
        [[
            qty,
            price,
            category_encoded,
            store_encoded
        ]]
    )

    result = (
        target_encoder.inverse_transform(
            prediction
        )[0]
    )

    probability = (
        model.predict_proba(
            [[
                qty,
                price,
                category_encoded,
                store_encoded
            ]]
        ).max()
    )

    # ----------------------------------
# PREDICTION RESULT CARD
# ----------------------------------

    if result == "High Performer":

        st.markdown(f"""
        <div style="
        background-color:#D7CCC8;
        padding:18px;
        border-radius:12px;
        border-left:8px solid #2E7D32;
        margin-top:10px;
        ">

        <h3 style="
        color:#4E342E;
        margin:0;
        ">
        🟢 Prediction: {result} | Confidence: {probability:.0%}
        </h3>

        </div>
        """, unsafe_allow_html=True)

    elif result == "Medium Performer":

        st.markdown(f"""
        <div style="
        background-color:#D7CCC8;
        padding:18px;
        border-radius:12px;
        border-left:8px solid #F9A825;
        margin-top:10px;
        ">

        <h3 style="
        color:#4E342E;
        margin:0;
        ">
        🟡 Prediction: {result} | Confidence: {probability:.0%}
        </h3>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div style="
        background-color:#D7CCC8;
        padding:18px;
        border-radius:12px;
        border-left:8px solid #C62828;
        margin-top:10px;
        ">

        <h3 style="
        color:#4E342E;
        margin:0;
        ">
        🔴 Prediction: {result} | Confidence: {probability:.0%}
        </h3>

        </div>
        """, unsafe_allow_html=True)

# ----------------------------------
# FEATURE IMPORTANCE
# ----------------------------------

st.markdown("""
<h2 style="color:#4E342E;">
📊 Feature Importance
</h2>
""", unsafe_allow_html=True)

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

fig = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="What Drives Product Success?",
    color="Importance"
)

fig.update_layout(
    paper_bgcolor="#000814",
    plot_bgcolor="#000814",
    font=dict(color="white"),
    title_font=dict(color="white")
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# ML INSIGHTS
# ----------------------------------

st.markdown("""
<div style="
background-color:#EFEBE9;
padding:20px;
border-radius:12px;
border-left:8px solid #6D4C41;
">

<h3 style="color:#4E342E;">
🤖 Machine Learning Insights
</h3>

<ul style="color:#5D4037;font-size:16px;">
<li>Transaction Quantity is the strongest predictor of success.</li>
<li>Unit Price significantly impacts product performance.</li>
<li>Product Category influences revenue contribution.</li>
<li>Store Location has a smaller but measurable impact.</li>
<li>High-performing products should be prioritized in marketing campaigns.</li>
</ul>

</div>
""", unsafe_allow_html=True)
