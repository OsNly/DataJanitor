# analyze.py
import pandas as pd
from ydata_profiling import ProfileReport


def analyze_csv(file_path):
    """
    Reads a CSV file with low_memory=False to handle mixed types,
    generates a profiling report (optional), and returns summary info.

    Returns:
        dict: {
            "summary": descriptive stats dict,
            "columns": per-column info (dtype, missing_pct, unique_vals, example_vals),
            "shape": (rows, columns)
        }
    """
    # Read full file to avoid DtypeWarning on mixed types
    df = pd.read_csv(file_path, low_memory=False)

    # Optional profiling report (uncomment to save HTML)
    # profile = ProfileReport(df, title="Profiling Report", minimal=True, explorative=True)
    # profile.to_file("profiling_report.html")

    # Descriptive summary
    summary = df.describe(include='all').to_dict()

    # Column-level details
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