import gspread
import streamlit as st
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    creds = Credentials.from_service_account_file(
        ".streamlit/google_credentials.json", scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open(st.secrets["SHEET_NAME"]).sheet1
    return sheet

def load_comments():
    sheet = get_sheet()
    records = sheet.get_all_records()
    return records

def save_comment(name, email, comment):
    sheet = get_sheet()
    all_values = sheet.get_all_values()
    next_id = len(all_values)
    sheet.append_row([
        next_id,
        name,
        email,
        comment,
        "",
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ])

def delete_comment(row_index):
    sheet = get_sheet()
    sheet.delete_rows(row_index + 2)

def save_reply(row_index, reply):
    sheet = get_sheet()
    sheet.update_cell(row_index + 2, 5, reply)