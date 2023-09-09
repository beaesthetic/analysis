import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe

def save_to_google_sheet(service_account_path: str, sheet_id: str, worksheet_name: str, dataframe: pd.DataFrame):
    gc = gspread.service_account(filename=service_account_path)
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    worksheet.clear()
    set_with_dataframe(worksheet=worksheet, dataframe=dataframe, include_index=False, include_column_header=True,
                       resize=True)