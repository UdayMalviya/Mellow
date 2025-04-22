import streamlit as st
import pandas as pd
import numpy as np
import os
from utils.api import upload_file, get_datasets, get_versions, clean_with_ai
import plotly.express as px

st.set_page_config(page_title="Mellow ", layout="wide")
st.title("📊 Mellow BI - Structured Dataset Upload & EDA")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filters' not in st.session_state:
    st.session_state.filters = {}

# Upload section
with st.form("upload_form"):
    st.header("📁 Upload Dataset")
    dataset_name = st.text_input("Dataset Name")
    dataset_desc = st.text_area("Description")
    created_by = st.text_input("Created By")
    version_name = st.text_input("Version Name")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    submit = st.form_submit_button("Upload")

if submit:
    if not all([dataset_name, dataset_desc, created_by, version_name, uploaded_file]):
        st.warning("Please fill out all fields and upload a file.")
    else:
        with st.spinner("Uploading dataset..."):
            success, df = upload_file(dataset_name, version_name, uploaded_file)
            if success:
                st.session_state.df = df  # Store the DataFrame in session state
                st.session_state.filters = {}  # Clear filters on new upload
                st.success("✅ Dataset and Version Uploaded")
                st.write(st.session_state.df.head())  # Display the first few rows of the uploaded dataset
            else:
                st.error("❌ Failed to upload dataset.")

# Display visualizations if a dataset is successfully uploaded
df = st.session_state.df
if df is not None:
    st.header("📊 Exploratory Data Analysis (EDA)")

    # Filter and Sort Section
    st.sidebar.header("FilterWhere and Sort Data")
    
    # Filters
    filtered_df = df.copy()
    for col in df.columns:
        if df[col].nunique() <= 50:  # Only show filter for columns with fewer than 50 unique values
            unique_vals = df[col].dropna().unique()  # Drop NaN values
            default_vals = st.session_state.filters.get(col, list(unique_vals))  # Get saved filters or defaults
            selected_val = st.sidebar.multiselect(f"Filter by {col}", unique_vals, default=default_vals)
            if selected_val:
                filtered_df = filtered_df[filtered_df[col].isin(selected_val)]
                st.session_state.filters[col] = selected_val  # Save the selected filters

    # Sorting
    sort_column = st.sidebar.selectbox("Sort by Column", df.columns, index=0)
    sort_order = st.sidebar.radio("Sort Order", ["Ascending", "Descending"], index=0)
    ascending = sort_order == "Ascending"
    filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

    # Display filtered and sorted data
    st.subheader("Filtered and Sorted Data")
    st.dataframe(filtered_df)

    # Basic statistics
    st.subheader("Basic Statistics")
    st.write(filtered_df.describe())

    # Advanced statistics
    st.subheader("Advanced Statistics")
    numeric_cols = filtered_df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        skewness = filtered_df[numeric_cols].skew()
        kurtosis = filtered_df[numeric_cols].kurtosis()
        quantiles = filtered_df[numeric_cols].quantile(q=[0.25, 0.5, 0.75])

        # Reshape quantiles for DataFrame
        quantiles_df = quantiles.unstack().reset_index()
        quantiles_df.columns = ['Feature', 'Quantile Level', 'Value']

        stats = {
            "Skewness": skewness,
            "Kurtosis": kurtosis,
            "Quantiles": quantiles_df
        }

        # Display Skewness and Kurtosis
        st.table(pd.concat([
            skewness.rename('Skewness').to_frame(),
            kurtosis.rename('Kurtosis').to_frame()
        ], axis=1).T)

        # Display Quantiles
        st.subheader("Quantiles")
        st.dataframe(quantiles_df.pivot_table(index='Feature', columns='Quantile Level', values='Value'))
    else:
        st.warning("No numeric columns to compute advanced statistics.")

    # Correlation matrix heatmap
    st.subheader("Correlation Matrix Heatmap")
    corr_matrix = filtered_df.corr(numeric_only=True)
    fig_corr = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='Viridis')
    st.plotly_chart(fig_corr, use_container_width=True)

    # Distribution plots
    st.subheader("Distribution Plots")
    numeric_cols = filtered_df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        bins_slider = st.slider(f"Bins for {col}", min_value=5, max_value=100, value=30, key=f"bins_{col}")
        fig_dist = px.histogram(filtered_df, x=col, nbins=bins_slider, marginal="box", title=f"Distribution of {col}")
        st.plotly_chart(fig_dist, use_container_width=True)

    # Scatter plots
    st.subheader("Scatter Plots")
    numeric_cols = filtered_df.select_dtypes(include=['number']).columns
    if len(numeric_cols) >= 2:
        scatter_x = st.selectbox("Select X-axis variable:", numeric_cols, key="scatter_x")
        scatter_y = st.selectbox("Select Y-axis variable:", numeric_cols, index=1, key="scatter_y")
        
        if scatter_x != scatter_y:
            opacity_slider = st.slider("Opacity", min_value=0.1, max_value=1.0, value=0.7, step=0.1, key="opacity")
            fig_scatter = px.scatter(filtered_df, x=scatter_x, y=scatter_y, opacity=opacity_slider, title=f"Scatter Plot of {scatter_x} vs {scatter_y}")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("X and Y axis variables must be different.")
    else:
        st.warning("Not enough numeric columns to generate scatter plots.")

    # Line plots for time series data
    st.subheader("Time Series Line Plots")
    datetime_cols = filtered_df.select_dtypes(include=['datetime', 'timedelta']).columns
    if len(datetime_cols) > 0:
        datetime_col = st.selectbox("Select Date/Time Column:", datetime_cols, key="datetime_col")
        numeric_cols = filtered_df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            value_col = st.selectbox("Select Value Column:", numeric_cols, key="value_col")
            fig_line = px.line(filtered_df.sort_values(by=datetime_col), x=datetime_col, y=value_col, title=f"Line Plot of {value_col} Over Time")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("No numeric columns to plot against the date/time column.")
    else:
        st.warning("No date/time columns found in the dataset.")

    # Download options
    st.subheader("Download Options")
    csv_data = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered and Sorted Dataset as CSV",
        data=csv_data,
        file_name="filtered_sorted_dataset.csv",
        mime="text/csv",
    )

    # Download individual visualizations
    if st.button("Download All Visualizations as HTML"):
        html_content = ""
        figures = [
            fig_corr,
            *(px.histogram(filtered_df, x=col, nbins=bins_slider, marginal="box", title=f"Distribution of {col}") for col in numeric_cols),
            fig_scatter,
            fig_line
        ]
        for chart in figures:
            if chart:
                html_content += chart.to_html(full_html=False, include_plotlyjs='cdn')

        with open("visualizations.html", "w") as f:
            f.write(html_content)
        with open("visualizations.html", "rb") as f:
            st.download_button(
                label="Download Visualizations",
                data=f,
                file_name="visualizations.html",
                mime="text/html",
            )
        os.remove("visualizations.html")

# View existing datasets
st.subheader("Existing Datasets")
existing_datasets = get_datasets()
if existing_datasets:
    for dataset in existing_datasets:
        st.write(f"- **{dataset['name']}** ({dataset['id']})")
else:
    st.info("No datasets found.")