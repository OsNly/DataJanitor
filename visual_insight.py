# visual_insight.py
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
import json
from openai_client import call_llm

visual_prompt = PromptTemplate.from_template("""
You are a data visualization expert. You will be given a summary of a cleaned dataset.

Your tasks:
1. Suggest 3–5 very interesting visualizations that makes sense and would help uncover patterns or relationships (Avoid correlation matrix).
2. For each, describe what insight it may reveal.
3. For each, write Python code using pandas/seaborn/matplotlib to generate an appealing plot. Use 'df' as the dataframe and be precise with column names.
4. Always be careful and precise with column names 
Output JSON in this exact format:
{{
  "visualizations": [
    {{
      "title": "Histogram of Age",
      "description": "Shows the distribution of age",
      "code": "sns.histplot(df['age'], kde=True); plt.title('Age Distribution'); plt.savefig('charts/age.png'); plt.clf()"
    }},
    ...
  ]
}}

Dataset Summary:
{column_data}
""")

def generate_visual_plan(column_data):
    prompt = visual_prompt.format(column_data=json.dumps(column_data, indent=2))
    response = call_llm(prompt, temperature=0)

    import re
    match = re.search(r"\{.*\}", response, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            return parsed.get("visualizations", [])
        except json.JSONDecodeError:
            print("Failed to parse visualization JSON. Raw output:\n", response)
    else:
        print("No valid JSON object found for visuals. Raw output:\n", response)
    return []