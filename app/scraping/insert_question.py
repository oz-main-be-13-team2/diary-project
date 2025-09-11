import asyncio
from app.db.base import Base
from app.db.session import async_session_maker, engine
from app.models.question import Question

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def insert_manual_questions():
    questions_to_insert = [
        "나의 강점과 약점은 각각 무엇인가요?",
        "오늘 하루 중 가장 감사했던 순간은 언제인가요?",
        "1년 전의 나와 지금의 나는 어떻게 다른가요?",
        "가장 후회하는 결정은 무엇이고, 그로부터 무엇을 배웠나요?",
        "나에게 행복이란 무엇인가요?",
        "가장 기억에 남는 칭찬은 무엇이고, 그 이유는 무엇인가요?",
        "가장 큰 두려움은 무엇이고, 그 두려움을 어떻게 극복할 수 있을까요?",
        "만약 돈과 시간이 무제한이라면 가장 먼저 하고 싶은 일은 무엇인가요?",
        "내가 가장 중요하게 생각하는 가치는 무엇인가요?",
        "내 삶에서 가장 큰 영감을 주는 사람은 누구인가요?",
        "최근에 새롭게 배운 것은 무엇이고, 그것을 어떻게 활용할 수 있을까요?",
        "나를 가장 잘 설명할 수 있는 단어 세 가지는 무엇인가요?",
        "나의 삶에서 가장 큰 성공은 무엇이고, 가장 큰 실패는 무엇인가요?",
        "나는 보통 스트레스를 어떻게 해소하나요?",
        "어떤 사람이 되고 싶나요?",
        "최근에 가장 크게 웃었던 순간은 언제였나요?",
        "가장 자랑스러운 순간은 무엇인가요?",
        "나에게 진정한 친구란 어떤 의미인가요?",
        "나를 가장 편안하게 해주는 장소나 활동은 무엇인가요?",
        "앞으로 5년 뒤 나의 모습은 어떨까요?"
    ]

    async with async_session_maker() as session:
        for question_text in questions_to_insert:
            new_question = Question(question_text=question_text)
            session.add(new_question)

        await session.commit()
    print("질문이 성공적으로 데이터베이스에 추가되었습니다.")

if __name__ == "__main__":
    async def main():
        await create_tables()
        await insert_manual_questions()

    asyncio.run(main())