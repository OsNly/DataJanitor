#plan.py
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
import json
import re
from openai_client import call_llm

prompt_template = PromptTemplate.from_template("""
You are a highly skilled data cleaning agent. Your job is to deeply understand the structure and meaning of each column in a dataset based on its summary statistics and example values, and generate a detailed, justified cleaning plan.

The dataset may contain:
- numeric columns (age, price, income, etc)
- categorical columns (gender, country, status, etc)
- identifiers (id, uuid, etc)
- text fields (comments, descriptions, etc)
- dates or timestamps
- unexpected or noisy values
- missing data
- inconsistent formatting

Your goal is to:
1. Identify what each column most likely represents.
2. Decide if it should be cleaned, imputed, dropped, mapped, scaled, or standardized.
3. Choose appropriate cleaning methods (e.g., impute with median, map inconsistent values, detect and fill outliers).
4. Add reasoning for each step to explain **why** you made that decision.
5. At the end, summarize what you did overall in plain language for a human to understand.

Output JSON with this exact format:
Note: The key must be spelled "column" exactly. Do not use "colum" or any other variant.
{{
  "plan": [
    {{
      "column": "col_name",
      "action": "impute" | "drop" | "standardize" | "normalize" | "scale" | "clip_outliers" | "fill_outliers" | "convert_dtype" | "map_values" | "strip_whitespace" | "remove_duplicates",
      "method": "mean" | "median" | "mode" | "minmax" | "zscore" | "constant" | "int" | "float" | "datetime" | null,
      "params": {{ optional dictionary of extra parameters }},
      "reason": "Detailed and logical explanation of why this cleaning step is needed."
    }},
    ...
  ],
  "explanation": "A clear, human-friendly summary of the full cleaning plan."
}}

Think carefully. Only propose changes that are statistically or logically justified. Be rigorous but practical.

Column Analysis:
{column_data}
""")

def generate_cleaning_plan(analysis_dict):
    column_data = json.dumps(analysis_dict["columns"], indent=2)
    prompt = prompt_template.format(column_data=column_data)
    result = call_llm(prompt, temperature=0)

    match = re.search(r"\{.*\}", result, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            return parsed.get("plan", []), parsed.get("explanation", "")
        except json.JSONDecodeError:
            print("Failed to parse JSON. Raw output:\n", result)
            return [], ""
    else:
        print("No valid JSON object found. Raw output:\n", result)
        return [], ""