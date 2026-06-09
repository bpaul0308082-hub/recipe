import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

def get_recipe(items, openai_key, tavily_key):
    # 1. 유통기한 남은 재료 필터링 및 정렬
    valid_items = [item for item in items if isinstance(item.get('dDay'), int) and item['dDay'] >= 0]
    
    if not valid_items:
        return "유통기한이 남은 재료가 없습니다.", None, None, None
    
    sorted_items = sorted(valid_items, key=lambda x: x['dDay'])
    urgent_items = sorted_items[:3]
    ingredient_names = [item['name'] for item in urgent_items]
    search_keywords = " ".join(ingredient_names)

    youtube_url = None
    blog_url = None
    source_context = ""

    # 2. Tavily를 이용해 유튜브 및 블로그 링크 검색
    try:
        tavily = TavilyClient(api_key=tavily_key)
        
        # 유튜브 레시피 검색 (site:youtube.com 활용)
        yt_search = tavily.search(query=f"{search_keywords} 자취생 요리 레시피 site:youtube.com", search_depth="basic", max_results=1)
        if yt_search['results']:
            youtube_url = yt_search['results'][0]['url']
            
        # 블로그/웹 레시피 검색 및 내용 추출
        web_search = tavily.search(query=f"{search_keywords} 간단 요리 레시피", search_depth="basic", max_results=1)
        if web_search['results']:
            blog_url = web_search['results'][0]['url']
            source_context = web_search['results'][0]['content'] # 검색된 웹페이지의 본문 일부
            
    except Exception as e:
        return f"검색 중 오류가 발생했습니다 (Tavily API 키 확인 필요): {str(e)}", None, None, None

    # 3. 검색된 정보(source_context)를 바탕으로 OpenAI 레시피 생성
    try:
        client = OpenAI(api_key=openai_key)
        prompt = f"""
        냉장고 재료: {', '.join(ingredient_names)}
        검색된 웹 출처 내용: {source_context}

        위 재료와 검색된 출처 내용을 바탕으로 자취생 맞춤형 요리 레시피를 작성해줘.

        요청 사항:
        1. 요리 이름
        2. 단계별 조리법 (1. ~, 2. ~ 형식)
        3. 마지막에 이 레시피가 실제 웹 출처를 참고하여 만들어졌음을 안내해줘.
        
        정중하고 친절한 어조로 작성해줘.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        recipe_text = response.choices[0].message.content
        return recipe_text, ingredient_names, youtube_url, blog_url
        
    except Exception as e:
        return f"레시피 생성 중 오류 발생: {str(e)}", None, None, None
