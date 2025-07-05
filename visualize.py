# visualize.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_column_distributions(df: pd.DataFrame, output_dir="charts"):
    os.makedirs(output_dir, exist_ok=True)

    for col in df.columns:
        plt.figure(figsize=(6, 4))

        if pd.api.types.is_numeric_dtype(df[col]):
            sns.histplot(df[col].dropna(), kde=True)
            plt.title(f"Distribution of {col}")
        elif pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == object:
            top_vals = df[col].value_counts().nlargest(10)
            sns.barplot(x=top_vals.values, y=top_vals.index)
            plt.title(f"Top categories in {col}")
        else:
            continue

        plt.tight_layout()
        plt.savefig(f"{output_dir}/{col}.png")
        plt.close()

def plot_relationships(df, target_col='income', output_dir="charts"):
    os.makedirs(output_dir, exist_ok=True)

    for col in df.columns:
        if col == target_col:
            continue

        if pd.api.types.is_numeric_dtype(df[col]) and target_col in df.columns:
            plt.figure(figsize=(6, 4))
            sns.boxplot(x=target_col, y=col, data=df)
            plt.title(f"{col} by {target_col}")
            plt.tight_layout()
            plt.savefig(f"{output_dir}/{col}_by_{target_col}.png")
            plt.close()
