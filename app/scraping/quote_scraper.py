import requests
import asyncio
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup
from fastapi import requests
from app.db.base import Base
from app.db.session import async_session_maker, engine
from app.models.quote import Quote
from app.models.question import Question


async def scrape_and_save_quotes():
    # quotes.toscrape.com에서 명언을 스크래핑하고 데이터베이스 저장
    print("명언 스크래핑을 시작합니다.")
    base_url = "https://quotes.toscrape.com/"
    url = base_url

    # 다음 페이지가 없을때까지 반복
    while url:
        try:
            response = requests.get(url) # 웹 페이지에 get 요청
            response.raise_for_status() # 요청 실패 시 예외 발생
            soup = BeautifulSoup(response.text, "html.parser") # HTML 콘텐츠 BeautifulSoup으로 파싱
            quotes = soup.find_all("div", class_="quote") # 'quote' 클래스를 가진 모든 div 태그를 찾아서 명언 목록 가져오기

            # 데이터베이스 세션 시작
            async with async_session_maker() as session:
                for quote_div in quotes:
                    content = quote_div.find("div", class_="text").text.strip() # 명언 내용 추출
                    author = quote_div.find("div", class_="author").text.strip() # 저자 추출

                    try:
                        new_quote = Quote(content=content, author=author) # 새로운 명언 인스턴스 생성 및 세션에 추가
                        session.add(new_quote)
                        await session.commit() # 변경 사항을 데이터베이스에 커밋
                        print(f"새로운 명언 저장: {content[:30]}...")
                    except IntegrityError:
                        await session.rollback() # 이미 존재하는 명언일 경우, 커밋 롤백하고 다음 명언으로 넘어감
                        print(f"이미 존재하는 명언입니다. 건너뜁니다: {content[:30]}...")

            # 여기까지가 내 머리의 한계

            # 다음 페이지 URL 찾기
            next_link = soup.find("li", class_="next")
            # 다음 페이지 링크 있으면 URL 업데이트, 없으면 None 할당하여 반복문 종료
            url = f"{base_url}{next_link.find('a')['href']}" if next_link else None

        except requests.exceptions.RequestException as e:
            print(f"웹 요청 중 오류가 발생했습니다: {e}")
            break
        except Exception as e:
            print(f"데이터 저장 중 오류가 발생했습니다: {e}")
            break

    print("명언 스크래핑이 완료되었습니다.")

async def create_tables(): # 임시 테이블 생성 함수
    async with engine.begin() as conn: # 데이터베이스 엔진을 사용하여 모든 테이블 생성
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__": # 스크립트가 직접 실행될 때만 아래 코드 실행
    # 테이블이 없으면 먼저 생성하고 스크래핑 시작 / asyncio.run(create_table())
    asyncio.run(scrape_and_save_quotes()) # 비동기 함수 실행