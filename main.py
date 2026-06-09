import streamlit as st
from recipe_logic import get_recipe # 앞서 만든 recipe_logic.py를 import

st.set_page_config(page_title="Keep And Cook", page_icon="🍳")
st.title("🍳 Keep And Cook")
st.subheader("냉장고 재료 맞춤 레시피 추천")

# 1. 세션 상태 초기화 (데이터 저장소)
if "items" not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = []

# 2. 임시 데이터 추가 (파일 업로드 전 테스트용)
if st.button("임시 재료 데이터 추가하기"):
    st.session_state.items = [
        {"name": "우유", "dDay": 1, "purchase_date": "2026-06-07"},
        {"name": "계란", "dDay": 3, "purchase_date": "2026-06-05"},
        {"name": "양파", "dDay": 7, "purchase_date": "2026-06-01"},
        {"name": "상한 우유", "dDay": -2, "purchase_date": "2026-05-20"} # 유통기한 지난 재료
    ]
    st.success("데이터가 추가되었습니다! 유통기한이 지난 '상한 우유'는 제외될 거예요.")
    st.rerun()

# 3. 현재 재료 목록 출력
st.write("---")
st.write("### 🧊 현재 냉장고 목록")
if st.session_state.items:
    st.table(st.session_state.items)
else:
    st.info("재료를 추가하거나 영수증을 업로드해주세요.")

# 4. 레시피 추천 버튼
if st.button("유통기한 임박 재료로 레시피 추천받기"):
    if not st.session_state.items:
        st.error("먼저 재료를 추가해주세요!")
    else:
        with st.spinner("레시피를 생성하는 중..."):
            # 로직 함수 호출
            recipe_text, used_ingredients = get_recipe(st.session_state.items)
            
            if used_ingredients:
                st.success(f"활용 재료: {', '.join(used_ingredients)}")
                st.markdown("### 🍳 단계별 요리 레시피")
                st.write(recipe_text)
            else:
                st.warning(recipe_text)

# 5. 초기화 버튼
if st.button("목록 초기화"):
    st.session_state.items = []
    st.rerun()
