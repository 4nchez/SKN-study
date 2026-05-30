# app2.py
# 표와 그래프가 포함된 gui 예제 2

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="데이터 시각화 앱", page_icon="★", layout="wide")

st.title("Streamlit 데이터 시각화 예제")
data = {
 "과목": ["Python", "SQL", "Spring Boot", "React", "AI"],
 "점수": [85, 78, 92, 88, 95]
}

df = pd.DataFrame(data)  # data 사전을 데이터프레임(표형태)을 만들기함
# print(df)

st.subheader("1. 데이터 표")
st.dataframe(df, use_container_width=True)

st.subheader("2. 데이터 요약")
st.write(df.describe(include="all"))

st.subheader("3. 막대그래프")
fig, ax = plt.subplots()
ax.bar(df["과목"], df["점수"])
ax.set_xlabel("과목")
ax.set_ylabel("점수")
ax.set_title("과목별 점수")
st.pyplot(fig)
