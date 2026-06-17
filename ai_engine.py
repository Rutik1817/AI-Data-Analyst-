import pandas as pd
from langchain_groq import ChatGroq

GROQ_API_KEY = "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"

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

def generate_insights(df):

    summary = f"""
    Dataset Shape: {df.shape}

    Columns:
    {list(df.columns)}

    Statistics:
    {df.describe(include='all').to_string()}
    """

    prompt = f"""
    Analyze this dataset and provide:

    1. Key Insights
    2. Trends
    3. Anomalies
    4. Business Recommendations

    Dataset:
    {summary}
    """

    response = llm.invoke(prompt)

    return response.content