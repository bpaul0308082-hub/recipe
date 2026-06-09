import streamlit as st
import pandas as pd
from recipe_logic import get_recipe

st.title("🍳 Keep And Cook")

# --- ⚙️ 사이드바: API 키 2개 입력받기 ---
with st.sidebar:
    st.header("⚙️ 설정")
    user_api_key = st.text_input("OpenAI API Key", type="password")
    tavily_api_key = st.text_input("Tavily API Key (검색용)", type="password")
    st.markdown("[Tavily API 키 발급받기](https://tavily.com/)")

# 세션 상태 초기화
if "ingredient_list" not in st.session_state:
    st.session_state.ingredient_list = []

if st.button("임시 재료 데이터 추가하기"):
    st.session_state.ingredient_list = [
        {"name": "우유", "dDay": 1, "purchase_date": "2026-06-07"},
        {"name": "계란", "dDay": 3, "purchase_date": "2026-06-05"},
        {"name": "양파", "dDay": 7, "purchase_date": "2026-06-01"}
    ]
    st.rerun()

st.write("---")
st.write("### 🧊 현재 냉장고 목록")

if len(st.session_state.ingredient_list) > 0:
    df = pd.DataFrame(st.session_state.ingredient_list)
    st.dataframe(df, use_container_width=True)
else:
    st.info("데이터가 없습니다. 위 버튼을 눌러 샘플을 추가하세요.")

# --- 레시피 추천 및 화면 출력 ---
if st.button("유통기한 임박 재료로 레시피 추천받기"):
    if not user_api_key or not tavily_api_key:
        st.error("👈 왼쪽 사이드바에 OpenAI와 Tavily API Key를 모두 입력해주세요!")
    elif not st.session_state.ingredient_list:
        st.error("먼저 재료를 추가해주세요!")
    else:
        with st.spinner("웹에서 가장 맛있는 레시피를 찾아 요약하는 중..."):
            
            # 4개의 결과값을 받아옴 (텍스트, 사용된재료리스트, 유튜브링크, 블로그링크)
            recipe_text, used_ingredients, yt_link, blog_link = get_recipe(
                st.session_state.ingredient_list, 
                user_api_key, 
                tavily_api_key
            )
            
            if used_ingredients:
                st.markdown("### 🍳 추천 요리")
                st.write(recipe_text)
                
                # 출처 영역 UI
                st.markdown("---")
                st.markdown("### 🔗 레시피 출처 및 참고 영상")
                
                # 화면을 반으로 나누어 한쪽엔 영상, 한쪽엔 블로그 버튼 배치
                col1, col2 = st.columns(2)
                
                with col1:
                    if yt_link:
                        st.video(yt_link) # 유튜브 영상 화면에 바로 임베드
                    else:
                        st.info("관련 유튜브 영상을 찾지 못했습니다.")
                        
                with col2:
                    if blog_link:
                        st.link_button("📝 원본 참고 블로그 보러가기", blog_link)
                    else:
                        st.info("관련 블로그를 찾지 못했습니다.")
            else:
                st.error(recipe_text)
