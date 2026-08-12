import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Water Treatment Recommendation System",
    page_icon="💧",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_excel("Prototype_Coagulant_Database.xlsx")

df = load_data()

# =====================================================
# HEADER
# =====================================================

st.title("💧 Water Treatment Chemical Recommendation Dashboard")

st.markdown("""
### Intelligent Coagulant Recommendation System

Enter Raw Water Turbidity and get:

✅ Recommended Chemical  
✅ PAC Dose  
✅ Alum Dose  
✅ Polymer Dose  
✅ Chlorine Dose  
✅ Interactive Dosage Trend Analysis
""")

st.divider()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Input Parameters")

turbidity = st.sidebar.number_input(
    "Enter Turbidity (NTU)",
    min_value=1,
    max_value=800,
    value=65
)

selected_chemicals = st.sidebar.multiselect(
    "Select Chemicals for Trend Graph",
    [
        "Powder_PAC_ppm",
        "Liquid_PAC_ppm",
        "Liquid_Alum_ppm",
        "Solid_Alum_ppm",
        "Polymer_ppm",
        "Chlorine_ppm"
    ],
    default=[
        "Liquid_PAC_ppm",
        "Powder_PAC_ppm"
    ]
)

# =====================================================
# FIND CLOSEST TURBIDITY VALUE
# =====================================================

closest_row = df.iloc[
    (df["Turbidity_NTU"] - turbidity).abs().argsort()[:1]
]

recommendation = closest_row["Recommended_Chemical"].values[0]

powder_pac = closest_row["Powder_PAC_ppm"].values[0]
liquid_pac = closest_row["Liquid_PAC_ppm"].values[0]
liquid_alum = closest_row["Liquid_Alum_ppm"].values[0]
solid_alum = closest_row["Solid_Alum_ppm"].values[0]
polymer = closest_row["Polymer_ppm"].values[0]
chlorine = closest_row["Chlorine_ppm"].values[0]

# =====================================================
# RECOMMENDATION BOX
# =====================================================

st.success(f"✅ Recommended Chemical : {recommendation}")

# =====================================================
# KPI CARDS
# =====================================================

st.subheader("Recommended Dosages")

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
        0 if pd.isna(chlorine) else round(chlorine, 2)
    )

st.divider()

# =====================================================
# DOSAGE BAR CHART
# =====================================================

st.subheader("📊 Dosage at Selected Turbidity")

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
        0 if pd.isna(chlorine) else chlorine
    ]
})

bar_fig = px.bar(
    dose_df,
    x="Chemical",
    y="Dose",
    color="Dose",
    text="Dose",
    title=f"Recommended Dosage at {turbidity} NTU"
)

bar_fig.update_traces(textposition="outside")

st.plotly_chart(bar_fig, use_container_width=True)

# =====================================================
# TREND ANALYSIS
# =====================================================

st.subheader("📈 Chemical Dosage Trend")

trend_fig = go.Figure()

for chem in selected_chemicals:

    trend_fig.add_trace(
        go.Scatter(
            x=df["Turbidity_NTU"],
            y=df[chem],
            mode="lines",
            name=chem.replace("_ppm", "")
        )
    )

trend_fig.add_vline(
    x=turbidity,
    line_color="red",
    line_dash="dash"
)

trend_fig.update_layout(
    height=600,
    template="plotly_white",
    xaxis_title="Turbidity (NTU)",
    yaxis_title="Dosage (ppm)"
)

st.plotly_chart(trend_fig, use_container_width=True)

# =====================================================
# RECOMMENDATION TABLE
# =====================================================

st.subheader("📋 Current Recommendation")

result_df = pd.DataFrame({
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
    result_df,
    use_container_width=True
)

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

csv = result_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Recommendation",
    data=csv,
    file_name="Chemical_Recommendation.csv",
    mime="text/csv"
)

# =====================================================
# VIEW DATABASE
# =====================================================

with st.expander("📂 View Complete Database"):
    st.dataframe(df, use_container_width=True)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Prototype Water Treatment Coagulant Recommendation System"
)
