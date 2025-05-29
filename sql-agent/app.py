import streamlit as st

from sql_agent import sql_agent
from prompts import create_query

st.title('SQL Query Database Agent')

question = st.text_input('Enter your question...')

submit = st.button('Submit')

if question and submit:
    query = create_query(question)
    with st.spinner('Thinking...'):
        result = sql_agent.invoke(query)
    if result:
        st.markdown(result['output'])
    

