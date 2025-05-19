import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
import re

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

db = SQLDatabase.from_uri("duckdb:///data/enterprise.duckdb")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
)

def get_schema() -> str:
    return db.get_table_info()

def generate_sql_query(question: str) -> str:
    schema = get_schema()

    system_prompt = (
        "You are an expert SQL assistant. "
        "Write a syntactically correct DuckDB SQL query that answers the user’s question. "
        "Use only the tables and columns listed below and fully qualify table names if needed.\n\n"
        f"### Schema ###\n{schema}\n\n"
        "Return *only* the SQL, nothing else—no markdown, no explanation."
    )

    sql = llm.invoke(system_prompt + f"\n\n### Question ###\n{question}")

    return sql

def run_sql_query(query: str):
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return execute_query_tool.invoke(query)

question = "Return the top 5 customers in the database based on total order amount."
output = generate_sql_query(question)
sql = re.search(r"```sql\s*(.*?)\s*```", output.content, re.S).group(1)
print(sql.strip())
print("\n")
results = run_sql_query(sql)
print(results)