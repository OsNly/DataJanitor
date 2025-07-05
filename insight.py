# insight.py
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
import json
from openai_client import call_llm

insight_prompt = PromptTemplate.from_template("""
You are a senior data analyst. You are given a dataset summary and column statistics after cleaning.

Please perform the following:
1. Describe the structure of the data in natural language (Aabic).
2. Mention any interesting patterns or distributions in Arabic (e.g. most common values, ranges, anomalies).
3. Derive any basic insights you can in Arabic (e.g. relationships between columns, high-cardinality features, outliers).
4. Point out anything surprising or worth further investigation in Arabic.
                                            

Be specific. Don't explain generic EDA steps — interpret the data as if you're preparing a short report.

Column Summary:
{column_data}
""")

def generate_insights(column_data):
    prompt = insight_prompt.format(column_data=json.dumps(column_data, indent=2))
    return call_llm(prompt, temperature=0)