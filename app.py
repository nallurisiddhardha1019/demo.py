import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(
    page_title="Professional Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------
# Caching Data Load
# -----------------------
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# -----------------------
# Main App
# -----------------------
st.title("📊 Professional Analytics Dashboard")

if uploaded_file is not None:

    df = load_data(uploaded_file)

    st.success("File uploaded successfully!")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Show raw data
    with st.expander("🔍 Preview Data"):
        st.dataframe(df, use_container_width=True)

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_columns) == 0:
        st.warning("No numeric columns found for analysis.")
        st.stop()

    # -----------------------
    # KPI Section
    # -----------------------
    st.subheader("📌 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Numeric Columns", len(numeric_columns))

    # -----------------------
    # Filtering Section
    # -----------------------
    st.sidebar.subheader("🔎 Filter Data")

    selected_column = st.sidebar.selectbox(
        "Select Column to Filter",
        numeric_columns
    )

    min_value = float(df[selected_column].min())
    max_value = float(df[selected_column].max())

    selected_range = st.sidebar.slider(
        "Select Range",
        min_value,
        max_value,
        (min_value, max_value)
    )

    filtered_df = df[
        (df[selected_column] >= selected_range[0]) &
        (df[selected_column] <= selected_range[1])
    ]

    # -----------------------
    # Chart Section
    # -----------------------
    st.subheader("📈 Data Visualization")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Scatter", "Histogram", "Box", "Line"]
    )

    x_axis = st.selectbox("Select X-axis", numeric_columns)
    y_axis = st.selectbox("Select Y-axis", numeric_columns)

    if chart_type == "Scatter":
        fig = px.scatter(filtered_df, x=x_axis, y=y_axis)

    elif chart_type == "Histogram":
        fig = px.histogram(filtered_df, x=x_axis)

    elif chart_type == "Box":
        fig = px.box(filtered_df, x=x_axis, y=y_axis)

    elif chart_type == "Line":
        fig = px.line(filtered_df, x=x_axis, y=y_axis)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------
    # Download Section
    # -----------------------
    st.subheader("⬇️ Download Filtered Data")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file from the sidebar to begin.")
