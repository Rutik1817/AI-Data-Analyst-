from sqlalchemy import create_engine, inspect
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import sqlite3
import json
import os
import re

# ==============================
# Configuration
# ==============================

GROQ_API_KEY = "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"

db_url = "sqlite:///amazon.db"

# ==============================
# Step 1: Extract Schema
# ==============================

def extract_schema(db_url):
    engine = create_engine(db_url)
    inspector = inspect(engine)

    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)

        schema[table_name] = [
            col["name"] for col in columns
        ]

    return json.dumps(schema, indent=2)

# ==============================
# Step 2: Text To SQL
# ==============================

def text_to_sql(schema, user_prompt):

    SYSTEM_PROMPT = """
    You are an expert SQL generator.

    Rules:
    1. Generate only SQL.
    2. Use only tables and columns present in schema.
    3. Do not explain anything.
    4. Do not generate markdown.
    5. Do not use ```sql blocks.
    6. Output only executable SQL.
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user",
         """Schema:
{schema}

Question:
{question}

SQL Query:
""")
    ])

    llm = ChatGroq(
        groq_api_key="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",
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

    chain = prompt_template | llm

    response = chain.invoke({
        "schema": schema,
        "question": user_prompt
    })

    sql_query = response.content.strip()

    sql_query = re.sub(r"```sql", "", sql_query)
    sql_query = re.sub(r"```", "", sql_query)

    return sql_query.strip()

# ==============================
# Step 3: Execute Query
# ==============================

def execute_sql(sql_query):

    if not sql_query.upper().startswith("SELECT"):
        raise Exception(
            "Only SELECT statements are allowed."
        )

    conn = sqlite3.connect("amazon.db")

    cursor = conn.cursor()

    result = cursor.execute(sql_query)

    rows = result.fetchall()

    conn.close()

    return rows

# ==============================
# Main Function
# ==============================

def get_data_from_database(user_prompt):

    schema = extract_schema(db_url)

    sql_query = text_to_sql(
        schema,
        user_prompt
    )

    print("\nGenerated SQL:")
    print(sql_query)

    results = execute_sql(sql_query)

    return sql_query, results

# ==============================
# Testing
# ==============================

if __name__ == "__main__":

    prompt = "Show top 5 products with highest ratings"

    sql, result = get_data_from_database(prompt)

    print("\nResults:")
    print(result)