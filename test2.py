import streamlit as st
import pandas as pd


df = pd.DataFrame({"A":[1,2],"B":[3,4],"C":[,]})
st.dataframe(df)

if st.button("dd"):
    df.iloc[0]['A'] = 8

st.dataframe(df)