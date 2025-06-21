import sqlite3
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class DatabaseQueryToolInput(BaseModel):
    """Input for the database query tool."""
    query: str = Field(description="The SQL query to execute")
    parameters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional parameters for parameterized queries"
    )

def database_query_tool(query: str, parameters: Optional[Dict[str, Any]] = None) -> str:
    """
    Executes SQL queries against the SQLite database (tables.db) and returns the results.
    Handles SELECT queries (returning data) and other queries (returning status).
    Provides error handling and safe query execution.
    
    Args:
        query: The SQL query to execute
        parameters: Optional dictionary of parameters for parameterized queries
        
    Returns:
        str: Query results as a string or error message
    """
    try:
        # Connect to the database
        conn = sqlite3.connect('tables.db')
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        cursor = conn.cursor()
        
        # Execute the query with parameters if provided
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        
        # Handle SELECT queries (return data)
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            if not results:
                return "No results found."
            
            # Convert results to a readable format
            columns = [description[0] for description in cursor.description]
            output = []
            for row in results:
                row_dict = dict(row)
                output.append(row_dict)
            
            return str(output)
        # Handle other queries (return status)
        else:
            conn.commit()
            return f"Query executed successfully. Rows affected: {cursor.rowcount}"
            
    except sqlite3.Error as e:
        return f"Database error occurred: {str(e)}"
    except Exception as e:
        return f"Unexpected error occurred: {str(e)}"
    finally:
        if conn:
            conn.close()
