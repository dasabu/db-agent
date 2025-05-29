import os
from dotenv import load_dotenv

from langchain.agents import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

from db import setup_db

load_dotenv()

model = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    model='gpt-4o-mini',
)

# Setup database
db = setup_db()

# Create toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=model)

# Create SQL agent
sql_agent = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    verbose=True,
    # prefix=SQL_AGENT_PREFIX,
    # format_instructions=SQL_AGENT_FORMAR_INSTRUCTION,
)    
