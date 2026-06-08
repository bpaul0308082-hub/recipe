import streamlit as st
from recipe_logic import get_recipe

st.title("Keep And Cook")

# 세션 상태 초기화
if "items" not in st.session_state:
    st.session_state.items = []

# (영수증 업로드 로직 생략...)

# 요리 추천 버튼
if st.button("유통기한 임박 재료로 레시피 추천받기"):
    recipe, link = get_recipe(st.session_state.items)
    st.write(recipe)
    st.link_button("레시피 상세 확인하기", link)
