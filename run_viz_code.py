# run_viz_code.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re

def run_visualizations(df, visual_plan):
    globals_dict = {
        "df": df,
        "sns": sns,
        "plt": plt,
        "pd": pd
    }

    chart_paths = []

    for viz in visual_plan:
        print(f"{viz['title']}: {viz['description']}")
        try:
            exec(viz["code"], globals_dict)
            matches = re.findall(r"plt\.savefig\(['\"](.*?)['\"]\)", viz["code"])
            if matches:
                chart_paths.append(matches[0])
        except Exception as e:
            print(f"Failed to run code: {e}")

    return chart_paths