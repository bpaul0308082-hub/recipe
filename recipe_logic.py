import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

def get_recipe(items):
    if not items:
        return "냉장고에 재료가 없습니다.", None
    
    try:
        sorted_items = sorted([item for item in items if 'dDay' in item], key=lambda x: x['dDay'])
    except Exception as e:
        return f"데이터 형식 오류: {str(e)}", None

    if not sorted_items:
        return "유효한 재료 데이터가 없습니다.", None
        
    urgent_items = [item['name'] for item in sorted_items[:3]]
    main_ingredient = urgent_items[0]
    
    # 1. Tavily 검색 강화 (인기 있는 블로그/유튜브 탐색)
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
    # 쿼리에 '블로그'와 '유튜브'를 명시하여 검색 품질 향상
    query = f"{main_ingredient} 맛있게 만드는 법 블로그 유튜브 레시피"
    search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
    
    # 검색된 결과 중 가장 적합한 것 선택
    best_result = search_result['results'][0] if search_result['results'] else None
    source_title = best_result.get('title', '관련 레시피') if best_result else "알 수 없음"
    source_url = best_result.get('url', 'https://www.youtube.com') if best_result else "https://www.youtube.com"

    # 2. OpenAI에게 검색된 출처 정보를 전달하여 레시피 작성 요청
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = f"""
    냉장고 재료: {', '.join(urgent_items)}
    추천 출처: {source_title} ({source_url})
    
    위의 출처를 참고하여, 냉장고 재료를 활용한 자취생 맞춤형 레시피를 작성해줘.
    1. 요리 이름
    2. 간단한 조리 순서 (단계별)
    3. 이 레시피를 선택한 이유 (출처 기반)
    정중하고 친절한 어조로 작성해줘.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        recipe_text = response.choices[0].message.content
        
        # 텍스트 내에 URL을 포함하여 반환
        final_output = f"{recipe_text}\n\n🔗 **참고 출처:** [{source_title}]({source_url})"
        
        return final_output, source_url
    except Exception as e:
        return f"서비스 호출 오류: {str(e)}", None
