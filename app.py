# app.py
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import date

# Google Sheets 認証（Secretsから読み込む）
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds_dict = st.secrets["gcp_service_account"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(credentials)

# Google Sheetsを開く
spreadsheet = client.open("smz-diary")  # シート名と一致させる
worksheet = spreadsheet.sheet1

# Streamlit UI
st.title("📔 日記アプリ smz-diary")

# 入力フォーム
entry_date = st.date_input("日付", value=date.today())
title = st.text_input("タイトル")
content = st.text_area("内容")
tag = st.text_input("タグ (例: 家族, 仕事, 健康)")
weather = st.selectbox("天気", ["☀️ 晴れ", "⛅ 曇り", "🌧️ 雨", "⛄ 雪", "その他"])

if st.button("保存"):
    # IDは既存データの行数＋1
    records = worksheet.get_all_records()
    next_id = len(records) + 1
    
    worksheet.append_row([next_id, str(entry_date), title, content, tag, weather])
    st.success("保存しました！")

# 過去データを表示
st.subheader("📊 過去のエントリー")
data = worksheet.get_all_records()
df = pd.DataFrame(data)
st.dataframe(df)


