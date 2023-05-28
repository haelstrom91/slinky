import streamlit as st
import pandas as pd
import yaml

from Relay import Relay
from Persona import Persona
from Connector import Connector
from helpers import read_semantics, write_yaml

# Set up initial objects and cache them so they are persistant
@st.cache_resource
def initiate():
   sql_connector = Connector('chinook')
   semantics = read_semantics('chinook')
   interpreter = Persona("interpreter", 'gpt-3.5-turbo', st.secrets["OPENAI_API_KEY"], yaml.dump(semantics))
   relay1 = Relay(sql_connector, [interpreter])
   return interpreter, relay1

interpreter, relay1 = initiate()

if 'submissions' not in st.session_state:
   # st.session_state['submission_counter'] = 0
   st.session_state["submissions"] = []

# the Chat form
with st.form("my_form"):
   prompt = st.text_input("Ask a Question:")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
      # st.session_state['submission_counter'] += 1
      query, data = relay1.submit_prompt(prompt)
      submission_packet = {
         'prompt': prompt,
         'query': query,
         'data': data
      } 
      st.session_state["submissions"].append(submission_packet)

# Write responses 
for submission in st.session_state['submissions']:
   # st.divider()
   try:
      with st.expander(submission['prompt']):
         try:
            st.write(submission['query'])
         except:
            st.write("No query generated yet...")

         try:
            df = pd.DataFrame(submission['data'])
            st.dataframe(df)
         except:
            st.write("No data retreived yet")
   except:
      pass

