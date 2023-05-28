import streamlit as st
import openai

from helpers import read_semantics

semantics = read_semantics('chinook')
tab1, tab2, tab3 = st.tabs(['tables', 'joins', 'metrics'])

tab1.json(semantics['tables'])
tab2.json(semantics['joins'])
tab3.json(semantics['metrics'])
