import requests
import asyncio
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup
from app.db.base import Base
from app.db.session import async_session_maker, engine
from app.models.quote import Quote
import logging

logging.basicConfig(level=logging.INFO)

# 명언을 스크래핑하고 데이터베이스에 저장하는 함수
async def scrape_and_save_quotes():
    print("명언 스크래핑을 시작합니다.")
    base_url = "https://quotes.toscrape.com/"
    url = base_url

    while url: # 다음 페이지 링크가 없을 때까지 반복
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            quotes = soup.find_all("div", class_="quote")

            print(f"찾은 명언의 수: {len(quotes)}개")

            async with async_session_maker() as session:
                for quote_div in quotes:
                    # --- 최종 수정된 부분 1: 명언 텍스트를 찾는 태그를 'div'에서 'span'으로 변경했습니다.
                    content_element = quote_div.find("span", class_="text")

                    # --- 최종 수정된 부분 2: 저자를 찾는 태그를 'div'에서 'small'로 변경했습니다.
                    author_element = quote_div.find("small", class_="author")

                    if content_element and author_element:
                        content = content_element.text.strip()
                        author = author_element.text.strip()

                        try:
                            new_quote = Quote(content=content, author=author)
                            session.add(new_quote)
                            await session.commit()
                            logging.info(f"새로운 명언 저장: {content[:30]}...")
                        except IntegrityError:
                            await session.rollback()
                            logging.warning(f"이미 존재하는 명언입니다. 건너뜁니다: {content[:30]}...")

            next_link = soup.find("li", class_="next") # 다음 페이지로 이동하기 위한 next 클래스의 li요소 찾기
            url = f"{base_url}{next_link.find('a')['href']}" if next_link else None

        except requests.exceptions.RequestException as e: # 웹 요청 중 발생할 수 있는 오류 처리
            logging.error(f"웹 요청 중 오류가 발생했습니다: {e}")
            break # 오류 발생 시 반복문 종료
        except Exception as e: # 그 외 일반적인 예외 처리
            logging.error(f"데이터 저장 중 오류가 발생했습니다: {e}")
            break # 오류 발생 시 반복문 종료

    print("명언 스크래핑이 완료되었습니다.")

# 데이터베이스 테이블을 생성하는 비동기 함수
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# 스크립트가 직접 실행될 때만 아래 코드 실행
if __name__ == "__main__":
    async def main():
        await create_tables()
        await scrape_and_save_quotes()

    asyncio.run(main())