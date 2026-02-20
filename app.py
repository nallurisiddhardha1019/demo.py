import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data Explorer", layout="wide")

st.title("📊 Streamlit Data Explorer")

st.markdown("Upload a CSV file to explore your data interactively.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df)

    st.subheader("Summary Statistics")
    st.write(df.describe())

    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    if numeric_columns:
        st.subheader("Data Visualization")

        col1, col2 = st.columns(2)

        with col1:
            x_axis = st.selectbox("Select X-axis", numeric_columns)

        with col2:
            y_axis = st.selectbox("Select Y-axis", numeric_columns)

        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
        st.pyplot(fig)

        st.subheader("Filter Data")

        selected_column = st.selectbox("Select column to filter", numeric_columns)
        min_value = float(df[selected_column].min())
        max_value = float(df[selected_column].max())

        selected_range = st.slider(
            "Select range",
            min_value,
            max_value,
            (min_value, max_value)
        )

        filtered_df = df[
            (df[selected_column] >= selected_range[0]) &
            (df[selected_column] <= selected_range[1])
        ]

        st.write(filtered_df)

    else:
        st.warning("No numeric columns found in dataset.")
else:
    st.info("Please upload a CSV file to begin.")