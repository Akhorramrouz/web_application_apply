import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd

def load_db():
    gc = gspread.service_account('apply4fund-db-e189a230919b.json')
    sh = gc.open_by_key("1sX_GB2E5MazKsafxF1qLWkUMVjrlf5FljwYyghMPnic")
    worksheet = sh.sheet1
    res = worksheet.get_all_records()
    df = pd.DataFrame(res)
    return df

def update_db(df):
    gc = gspread.service_account('apply4fund-db-e189a230919b.json')
    sh = gc.open_by_key("1sX_GB2E5MazKsafxF1qLWkUMVjrlf5FljwYyghMPnic")
    worksheet = sh.sheet1
    set_with_dataframe(worksheet,df)

def save_users_extracted_data(username,final_data):
    gc = gspread.service_account('apply4fund-db-e189a230919b.json')
    sh = gc.open_by_key("1sX_GB2E5MazKsafxF1qLWkUMVjrlf5FljwYyghMPnic")
    sh.add_worksheet(username,1000,30)
    set_with_dataframe(sh.get_worksheet(-1), final_data)
    
