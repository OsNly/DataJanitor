# analyze.py
import pandas as pd



def analyze_csv(file_path):

    df = pd.read_csv(file_path, low_memory=False)


    summary = df.describe(include='all').to_dict()

    column_info = {}
    for col in df.columns:
        series = df[col]
        column_info[col] = {
            "dtype": str(series.dtype),
            "missing_pct": series.isnull().mean() * 100,
            "unique_vals": series.nunique(dropna=True),
            "example_vals": series.dropna().unique()[:5].tolist()
        }

    return {
        "summary": summary,
        "columns": column_info,
        "shape": df.shape
    }
