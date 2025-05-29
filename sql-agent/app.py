import streamlit as st

from sql_agent import sql_agent, SQL_AGENT_PREFIX, SQL_AGENT_FORMAR_INSTRUCTION

st.title('SQL Query Database Agent')

question = st.text_input('Enter your question...')

submit = st.button('Submit')

if question and submit:
    query = SQL_AGENT_PREFIX + question + SQL_AGENT_FORMAR_INSTRUCTION
    with st.spinner('Thinking...'):
        result = sql_agent.invoke(query)
    if result:
        print(result)
        st.markdown(result['output'])
    

