import gspread
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
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
