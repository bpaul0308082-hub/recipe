import streamlit as st
import pandas as pd
from recipe_logic import get_recipe

st.title("🍳 Keep And Cook")

# --- ⚙️ 사이드바: API 키 입력란 추가 ---
with st.sidebar:
    st.header("⚙️ 설정")
    # type="password"로 설정하여 입력한 키가 화면에 노출되지 않게 합니다.
    user_api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
    st.markdown("[OpenAI API 키 발급받기](https://platform.openai.com/api-keys)")

# 세션 상태 초기화 
if "ingredient_list" not in st.session_state:
    st.session_state.ingredient_list = []

# 임시 데이터 추가 버튼
if st.button("임시 재료 데이터 추가하기"):
    st.session_state.ingredient_list = [
        {"name": "우유", "dDay": 1, "purchase_date": "2026-06-07"},
        {"name": "계란", "dDay": 3, "purchase_date": "2026-06-05"},
        {"name": "양파", "dDay": 7, "purchase_date": "2026-06-01"}
    ]
    st.rerun()

st.write("---")
st.write("### 🧊 현재 냉장고 목록")

# 데이터가 있을 때만 DataFrame 생성
if len(st.session_state.ingredient_list) > 0:
    df = pd.DataFrame(st.session_state.ingredient_list)
    st.dataframe(df, use_container_width=True)
else:
    st.info("데이터가 없습니다. 위 버튼을 눌러 샘플을 추가하세요.")

# 레시피 추천 버튼
if st.button("유통기한 임박 재료로 레시피 추천받기"):
    # 1. API 키가 입력되었는지 먼저 확인
    if not user_api_key:
        st.error("👈 왼쪽 사이드바에 OpenAI API Key를 먼저 입력해주세요!")
    # 2. 재료가 있는지 확인
    elif not st.session_state.ingredient_list:
        st.error("먼저 재료를 추가해주세요!")
    else:
        with st.spinner("레시피를 생성하는 중..."):
            # 입력받은 user_api_key를 함수로 전달!
            recipe_text, used_ingredients = get_recipe(st.session_state.ingredient_list, user_api_key)
            
            if used_ingredients:
                st.markdown("### 🍳 추천 요리")
                st.write(recipe_text)
            else:
                st.error(recipe_text)
