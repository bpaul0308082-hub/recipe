import streamlit as st
from recipe_logic import get_recipe

st.title("Keep And Cook - 레시피 추천")

# 세션 데이터 확인
if "items" not in st.session_state:
    st.session_state.items = []

if st.button("유통기한 임박 재료로 레시피 받기"):
    if not st.session_state.items:
        st.warning("냉장고에 재료가 없습니다.")
    else:
        with st.spinner("임박한 재료를 분석하여 레시피를 만드는 중..."):
            recipe_text, used_ingredients = get_recipe(st.session_state.items)
            
            if used_ingredients:
                st.success(f"활용 재료: {', '.join(used_ingredients)}")
                st.markdown("### 🍳 단계별 요리 레시피")
                st.write(recipe_text)
            else:
                st.error(recipe_text)
