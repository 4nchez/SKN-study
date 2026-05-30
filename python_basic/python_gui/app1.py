# app1.py 
# streamlit 예제 1

import streamlit as st

st.set_page_config(page_title="파이썬 GUI 예제", page_icon="◎", layout="centered")

st.title("파이썬 Streamlit GUI 예제")
st.write("사용자 입력을 받아 화면에 출력하는 웹 GUI 입니다.")

name = st.text_input("이름을 입력하세요")
age = st.number_input("나이를 입력하세요", min_value=0, max_value=120, step=1)
major = st.selectbox("전공을 선택하세요", ["컴퓨터공학", "정보통신", "전자공학", "AI", "기타"])
memo = st.text_area("자기소개를 입력하세요")

if st.button("확인"):
    if name.strip() == "":
        st.warning("이름을 입력하세요.")
    else:
        st.success("입력이 완료되었습니다.")
        st.write("### 입력 결과")
        st.write(f"이름: {name}")
        st.write(f"나이: {age}")
        st.write(f"전공: {major}")
        st.write(f"자기소개: {memo}")
