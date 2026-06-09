import streamlit as st
import pandas as pd # pandas 추가
from recipe_logic import get_recipe

st.title("🍳 Keep And Cook")

# 세션 상태 초기화
if "items" not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = []

# 임시 데이터 추가 버튼
if st.button("임시 재료 데이터 추가하기"):
    st.session_state.items = [
        {"name": "우유", "dDay": 1, "purchase_date": "2026-06-07"},
        {"name": "계란", "dDay": 3, "purchase_date": "2026-06-05"},
        {"name": "양파", "dDay": 7, "purchase_date": "2026-06-01"}
    ]
    st.rerun()

st.write("---")
st.write("### 🧊 현재 냉장고 목록")

# 표 출력 방식 변경 (에러 방지)
if st.session_state.items:
    # 딕셔너리 리스트를 Pandas DataFrame으로 변환하여 안전하게 출력
    df = pd.DataFrame(st.session_state.items)
    st.dataframe(df, use_container_width=True)
else:
    st.info("데이터가 없습니다. 위 버튼을 눌러 샘플을 추가하세요.")

# 레시피 추천 버튼
if st.button("유통기한 임박 재료로 레시피 추천받기"):
    if not st.session_state.items:
        st.error("먼저 재료를 추가해주세요!")
    else:
        with st.spinner("레시피를 생성하는 중..."):
            recipe_text, used_ingredients = get_recipe(st.session_state.items)
            st.markdown("### 🍳 추천 요리")
            st.write(recipe_text)
