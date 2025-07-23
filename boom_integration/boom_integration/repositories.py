from boom_integration.db import AnalyzeLog, async_session
import datetime
from sqlalchemy import select, desc


class AnalyzeLogRepository:
    @staticmethod
    async def add_log(
        question: str,
        detected_objects: list[str],
        llm_response: str,
        created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc),
    ) -> AnalyzeLog:
        log = AnalyzeLog(
            question=question,
            detected_objects=detected_objects,
            llm_response=llm_response,
            created_at=created_at or datetime.datetime.now(datetime.timezone.utc),
        )
        async with async_session() as session:
            session.add(log)
            await session.commit()
            await session.refresh(log)
            return log

    @staticmethod
    async def get_logs(limit: int = 100) -> list[AnalyzeLog]:
        async with async_session() as session:
            result = await session.execute(
                select(AnalyzeLog).order_by(desc(AnalyzeLog.created_at)).limit(limit)
            )
            return list(result.scalars().all())
