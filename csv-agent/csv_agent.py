import os
from dotenv import load_dotenv
import pandas as pd

# from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
    # create_csv_agent
)

load_dotenv()

model = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_name='gpt-3.5-turbo',
    temperature=0,
)

df = pd.read_csv('salaries_2023.csv').fillna(value=0)

agent = create_pandas_dataframe_agent(
    llm=model,
    df=df,
    verbose=True, # print the agent's chain of thought
)

CSV_PROMPT_PREFIX = '''First set the pandas display options to show all the columns,
get the column names, then answer the question.
'''

CSV_PROMPT_SUFFIX = '''
- **ALWAYS** before giving the Final Answer, try another method.
Then reflect on the answers of the two methods you did and ask yourself if it answers correctly the original question.
If you are not sure, try another method.
FORMAT 4 FIGURES OR MORE WITH COMMAS.
- If the methods tried do not give the same result,reflect and try again until you have two methods that have the same result.
- If you still cannot arrive to a consistent result, say that you are not sure of the answer.
- If you are sure of the correct answer, create a beautiful and thorough response using Markdown.
- **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE, ONLY USE THE RESULTS OF THE CALCULATIONS YOU HAVE DONE**.
- **ALWAYS**, as part of your "Final Answer", explain how you got to the answer on a section that starts with: "\n\nExplanation:\n".
In the explanation, mention the column names that you used to get to the final answer.
'''