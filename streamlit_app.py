# streamlit_app.py
import streamlit as st
import pandas as pd
import re
from analyze import analyze_csv
from plan import generate_cleaning_plan
from execute import execute_plan
from insight import generate_insights
from visual_insight import generate_visual_plan
from run_viz_code import run_visualizations
from report import ReportBuilder
import tempfile
import sys

st.set_page_config(page_title="Data Cleaning & EDA Agent 🤙🏼", layout="wide")

st.title("Smart Data Cleaning & EDA Agent 🤙🏼")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    try:
        # Read into pandas DataFrame
        df = pd.read_csv(uploaded_file, low_memory=False)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            df.to_csv(tmp.name, index=False)
            tmp_path = tmp.name

        with st.spinner("Analyzing input file..."):
            analysis = analyze_csv(tmp_path)
        st.success("Analysis complete.")

        # Cleaning Plan
        st.header("Cleaning Plan")
        cleaning_plan, explanation = generate_cleaning_plan(analysis)
        st.json(cleaning_plan)
        st.write(explanation)

        # Execute Cleaning
        st.header("Executing Cleaning Plan")
        cleaned_df = execute_plan(df, cleaning_plan)
        st.dataframe(cleaned_df)

        # Download Cleaned CSV
        st.download_button(
            label="Download Cleaned CSV 🤙🏼",
            data=cleaned_df.to_csv(index=False).encode("utf-8"),
            file_name="cleaned_data.csv",
            mime="text/csv")
        
        # Insights
        st.header("Data Insights")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_clean:
            cleaned_df.to_csv(tmp_clean.name, index=False)
            tmp_clean_path = tmp_clean.name
        cleaned_analysis = analyze_csv(tmp_clean_path)
        insights = generate_insights(dict(cleaned_analysis["columns"]))
        st.write(insights)


        # Visualization Plan & Execution
        st.header("Visualizations")
        visual_plan = generate_visual_plan(cleaned_analysis["columns"])
        if visual_plan:
            chart_paths = run_visualizations(cleaned_df, visual_plan)
            if chart_paths:
                cols = st.columns(len(chart_paths))
                for col, path in zip(cols, chart_paths):
                    col.image(path, use_container_width=True)
                    desc = next((v.get("description", "") for v in visual_plan if path in v.get("code", "")), "")
                    col.caption(desc)
            else:
                st.warning("No charts were generated.")
        else:
            st.warning("No visualization plan was generated.")

        # Generate Report PDF
        st.header("Download Report")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            report = ReportBuilder(pdf_file.name)
            report.add_title("Smart Data Cleaning & EDA Report")
            report.add_section("Cleaning Summary", explanation)
            report.add_section("EDA Summary", insights)
            if visual_plan:
                for viz in visual_plan:
                    img = re.findall(r"plt\.savefig\(['\"](.*?)['\"]\)", viz.get("code", ""))
                    if img:
                        report.add_plot(img[0], viz.get("description", ""))
            report.save()

            with open(pdf_file.name, "rb") as f:
                st.download_button(
                    "Download PDF Report 🤙🏼",
                    data=f.read(),
                    file_name="report.pdf",
                    mime="application/pdf"
                )

    except Exception as e:
        st.error(f"An error occurred: {e}")