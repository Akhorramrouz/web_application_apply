import pandas as pd

df = pd.read_excel('db_streamlit.xlsx').iloc[2,:]
print(df.to_json())