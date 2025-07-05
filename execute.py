# execute.py
import pandas as pd
import numpy as np
import re

def execute_plan(df: pd.DataFrame, plan: list) -> pd.DataFrame:
    """
    Execute a list of cleaning steps on the DataFrame.
    Supported actions: drop, impute, standardize, normalize, scale,
    convert_dtype, clip_outliers, fill_outliers, map_values,
    remove_duplicates, strip_whitespace.
    """
    for step in plan:
        col = step.get("column")
        action = step.get("action")
        method = step.get("method", "")
        params = step.get("params", {})

        if action == "drop":
            df = df.drop(columns=[col], errors="ignore")

        elif action == "impute":
            if method == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif method == "median":
                df[col] = df[col].fillna(df[col].median())
            elif method == "mode":
                df[col] = df[col].fillna(df[col].mode().iloc[0])
            elif method == "constant":
                value = params.get("value", 0)
                df[col] = df[col].fillna(value)

        elif action == "standardize":
            df[col] = df[col].astype(str).str.lower().str.strip()
            if params.get("remove_special_chars", False):
                df[col] = df[col].apply(lambda x: re.sub(r"[^\w\s]", "", x))

        elif action == "normalize":
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

        elif action == "scale":
            if method == "zscore":
                df[col] = (df[col] - df[col].mean()) / df[col].std()
            elif method == "minmax":
                df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

        elif action == "convert_dtype":
            if method in ("int", "float"):
                # 1️⃣ Filter to keep only numeric-like entries or NaN
                mask = df[col].astype(str).str.match(r'^[0-9]+(?:\.[0-9]+)?$')
                df = df[mask | df[col].isnull()]

                # 2️⃣ Convert to numeric, coercing errors to NaN
                df[col] = pd.to_numeric(df[col], errors="coerce")

                # 3️⃣ Handle NaNs: fill then cast
                if params.get("impute_missing", False):
                    im = params.get("impute_method", "median")
                    fill = df[col].mean() if im == "mean" else df[col].median()
                    df[col] = df[col].fillna(fill)

                df[col] = df[col].astype("Int64") if method == "int" else df[col].astype(float)
            elif method == "str":
                df[col] = df[col].astype(str)
            elif method == "datetime":
                date_fmt = params.get("format")
                if date_fmt:
                    df[col] = pd.to_datetime(df[col], format=date_fmt, errors='coerce')
                else:
                    df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors='coerce')

        elif action == "clip_outliers":
            lower = params.get("lower", df[col].quantile(0.01))
            upper = params.get("upper", df[col].quantile(0.99))
            df[col] = np.clip(df[col], lower, upper)

        elif action == "fill_outliers":
            method = method or "median"
            q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            iqr = q3 - q1
            lb, ub = q1 - 1.5*iqr, q3 + 1.5*iqr
            mask = (df[col] < lb) | (df[col] > ub)
            rep = df[col].median() if method == "median" else df[col].mean()
            df.loc[mask, col] = rep

        elif action == "map_values":
            mapping = params.get("mapping", {})
            df[col] = df[col].replace(mapping)

        elif action == "remove_duplicates":
            df = df.drop_duplicates()

        elif action == "strip_whitespace":
            df[col] = df[col].astype(str).str.strip()

    return df