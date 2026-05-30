# app3.py
# 파일 업로드 gui

import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV 업로드 앱", page_icon=" ")

st.title("CSV 파일 업로드 예제")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("파일 업로드 성공")
    st.write("### 데이터 미리보기")
    st.dataframe(df, use_container_width=True)
    st.write("### 기본 통계")
    st.write(df.describe())
else:
    st.info("아직 파일이 업로드되지 않았습니다.")
