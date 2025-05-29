import streamlit as st
from csv_agent import agent, df, CSV_PROMPT_PREFIX, CSV_PROMPT_SUFFIX

st.title('Database CSV Agent')

st.write('### Dataset Preview')
st.write(df.head())

st.write('### Ask a question')
question = st.text_input(
    'Enter your question', 
    'Which department makes the most on average and show the actual amount.'
)
submit = st.button('Submit')

if submit and question:
    query = CSV_PROMPT_PREFIX + question + CSV_PROMPT_SUFFIX
    with st.spinner('Thinking...'):
        result = agent.invoke(query)        
    if result:
        st.write('### Final Answer')
        st.write(result['output'])
    