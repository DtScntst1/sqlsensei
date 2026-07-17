from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SQLSensei API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite Database Setup for Demo
DB_PATH = "sqlite:///./sqlsensei.db"
engine = create_engine(DB_PATH)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                city TEXT
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                product_name TEXT,
                amount REAL,
                date TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """))
        # Insert sample data if empty
        result = conn.execute(text("SELECT COUNT(*) FROM customers")).fetchone()
        if result[0] == 0:
            conn.execute(text("INSERT INTO customers (name, age, city) VALUES ('Ali', 28, 'Istanbul'), ('Ayse', 34, 'Ankara'), ('Mehmet', 45, 'Izmir')"))
            conn.execute(text("INSERT INTO sales (customer_id, product_name, amount, date) VALUES (1, 'Laptop', 15000, '2023-01-15'), (2, 'Phone', 8000, '2023-02-20'), (3, 'Monitor', 3000, '2023-03-05'), (1, 'Keyboard', 500, '2023-04-10')"))
            conn.commit()

@app.on_event("startup")
def startup():
    init_db()

class QueryRequest(BaseModel):
    question: str
    api_key: str

@app.post("/api/v1/query")
async def generate_sql_and_chart(req: QueryRequest):
    if not req.api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    
    os.environ["GROQ_API_KEY"] = req.api_key
    
    try:
        db = SQLDatabase.from_uri(DB_PATH)
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        
        # 1. Generate SQL via custom LCEL
        schema = db.get_table_info()
        sql_prompt = PromptTemplate.from_template(
            "You are a SQLite expert. Given the database schema below, write a syntactically correct SQLite query that answers the question.\n"
            "Return ONLY the SQL query, without any markdown or code blocks.\n\n"
            "Schema:\n{schema}\n\n"
            "Question: {question}\nSQL Query:"
        )
        sql_chain = sql_prompt | llm | StrOutputParser()
        sql_query = sql_chain.invoke({"schema": schema, "question": req.question})
        
        # Clean markdown formatting from sql_query if any
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
        # 2. Execute SQL
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            
        # 3. Generate Chart Config (ECharts)
        chart_prompt = PromptTemplate.from_template(
            "You are an expert data visualization assistant. Given the following SQL query and its execution result, generate a valid JSON object representing an Apache ECharts configuration option to visualize this data.\n\n"
            "Query: {query}\n"
            "Result: {result}\n\n"
            "Return ONLY a valid JSON object. No markdown formatting, no explanation."
        )
        
        chart_chain = chart_prompt | llm
        chart_json_str = chart_chain.invoke({
            "query": sql_query,
            "result": str(data[:10]) # Send at most 10 rows to avoid token limit
        }).content
        
        if chart_json_str.startswith("```json"):
            chart_json_str = chart_json_str.replace("```json", "").replace("```", "").strip()
            
        try:
            chart_config = json.loads(chart_json_str)
        except json.JSONDecodeError:
            chart_config = None

        return {
            "sql": sql_query,
            "data": data,
            "chart_config": chart_config
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
