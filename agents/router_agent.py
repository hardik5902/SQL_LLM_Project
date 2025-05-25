from retrievers.sql import generate_sql_query, run_sql_query
import re

def router_agent(question: str) -> dict:
    """
    Processes a natural language question into SQL, executes it, and returns full context.

    Returns:
        dict: { "question": str, "sql": str, "output": str or list }
    """
    print("=" * 50)
    print(f"Processing question: {question}")
    
    try:
        print("Tool Used: SQLTool")
        output = generate_sql_query(question)
        
        # Extract SQL from markdown block if exists
        sql_match = re.search(r"```sql\s*(.*?)\s*```", output.content, re.S)
        sql = sql_match.group(1).strip() if sql_match else output.content.strip()
        
        print(f"Generated SQL: {sql}")
        
        # Execute SQL
        result = run_sql_query(sql)
        print(f"Result: {result}")
        print("=" * 50)
        
        return {
            "question": question,
            "sql": sql,
            "output": result
        }

    except Exception as e:
        error_msg = f"Error in router agent: {str(e)}"
        print(error_msg)
        print("=" * 50)
        return {
            "question": question,
            "sql": None,
            "output": error_msg
        }