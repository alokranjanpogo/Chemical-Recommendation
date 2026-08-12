import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Water Treatment Dashboard",
    page_icon="💧",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_excel("Prototype_Coagulant_Database.xlsx")

df = load_data()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("💧 Water Treatment Chemical Recommendation System")
st.markdown("### Intelligent Coagulant Recommendation Dashboard")

st.markdown("---")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Input Parameters")

turbidity = st.sidebar.slider(
    "Raw Water Turbidity (NTU)",
    min_value=1,
    max_value=800,
    value=65
)

selected_chemicals = st.sidebar.multiselect(
    "Select Chemicals for Trend Analysis",
    [
        "Powder_PAC_ppm",
        "Liquid_PAC_ppm",
        "Liquid_Alum_ppm",
        "Solid_Alum_ppm",
        "Polymer_ppm",
        "Chlorine_ppm"
    ],
    default=["Liquid_PAC_ppm", "Powder_PAC_ppm"]
)

# --------------------------------------------------
# FIND NEAREST TURBIDITY
# --------------------------------------------------

nearest_row = df.iloc[
    (df["Turbidity_NTU"] - turbidity).abs().argsort()[:1]
]

recommendation = nearest_row["Recommended_Chemical"].values[0]

powder_pac = nearest_row["Powder_PAC_ppm"].values[0]
liquid_pac = nearest_row["Liquid_PAC_ppm"].values[0]
liquid_alum = nearest_row["Liquid_Alum_ppm"].values[0]
solid_alum = nearest_row["Solid_Alum_ppm"].values[0]
polymer = nearest_row["Polymer_ppm"].values[0]
chlorine = nearest_row["Chlorine_ppm"].values[0]

# --------------------------------------------------
# RECOMMENDATION
# --------------------------------------------------

st.success(f"✅ Recommended Chemical : {recommendation}")

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Powder PAC (ppm)",
        0 if pd.isna(powder_pac) else round(powder_pac, 2)
    )

with col2:
    st.metric(
        "Liquid PAC (ppm)",
        0 if pd.isna(liquid_pac) else round(liquid_pac, 2)
    )

with col3:
    st.metric(
        "Liquid Alum (ppm)",
        0 if pd.isna(liquid_alum) else round(liquid_alum, 2)
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Solid Alum (ppm)",
        0 if pd.isna(solid_alum) else round(solid_alum, 2)
    )

with col5:
    st.metric(
        "Polymer (ppm)",
        0 if pd.isna(polymer) else round(polymer, 3)
    )

with col6:
    st.metric(
        "Chlorine (ppm)",
        round(chlorine, 2)
    )

st.markdown("---")

# --------------------------------------------------
# DOSAGE BAR CHART
# --------------------------------------------------

st.subheader("📊 Recommended Dosage at Selected Turbidity")

dose_df = pd.DataFrame({
    "Chemical": [
        "Powder PAC",
        "Liquid PAC",
        "Liquid Alum",
        "Solid Alum",
        "Polymer",
        "Chlorine"
    ],
    "Dose": [
        0 if pd.isna(powder_pac) else powder_pac,
        0 if pd.isna(liquid_pac) else liquid_pac,
        0 if pd.isna(liquid_alum) else liquid_alum,
        0 if pd.isna(solid_alum) else solid_alum,
        0 if pd.isna(polymer) else polymer,
        chlorine
    ]
})

bar_fig = px.bar(
    dose_df,
    x="Chemical",
    y="Dose",
    color="Dose",
    text="Dose",
    title=f"Chemical Dosage at {turbidity} NTU"
)

bar_fig.update_traces(textposition="outside")

st.plotly_chart(bar_fig, use_container_width=True)

# --------------------------------------------------
# TREND CHART
# --------------------------------------------------

st.subheader("📈 Chemical Trend vs Turbidity")

trend_fig = go.Figure()

for chemical in selected_chemicals:

    trend_fig.add_trace(
        go.Scatter(
            x=df["Turbidity_NTU"],
            y=df[chemical],
            mode="lines",
            name=chemical.replace("_ppm", "")
        )
    )

trend_fig.add_vline(
    x=turbidity,
    line_dash="dash",
    line_color="red"
)

trend_fig.update_layout(
    height=600,
    template="plotly_white",
    xaxis_title="Turbidity (NTU)",
    yaxis_title="Dose (ppm)"
)

st.plotly_chart(trend_fig, use_container_width=True)

# --------------------------------------------------
# RECOMMENDATION TABLE
# --------------------------------------------------

st.subheader("📋 Current Recommendation")

recommendation_df = pd.DataFrame({
    "Parameter": [
        "Turbidity",
        "Recommended Chemical",
        "Powder PAC",
        "Liquid PAC",
        "Liquid Alum",
        "Solid Alum",
        "Polymer",
        "Chlorine"
    ],
    "Value": [
        turbidity,
        recommendation,
        powder_pac,
        liquid_pac,
        liquid_alum,
        solid_alum,
        polymer,
        chlorine
    ]
})

st.dataframe(
    recommendation_df,
    use_container_width=True
)

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

st.subheader("⬇ Download Recommendation")

csv = recommendation_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="Chemical
