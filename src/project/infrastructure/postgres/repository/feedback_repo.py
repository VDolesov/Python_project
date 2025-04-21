from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from project.infrastructure.postgres.models import Feedback
from project.schemas.feedback import FeedbackCreateUpdateSchema, FeedbackSchema
from project.core.exceptions import FeedbackNotFound, FeedbackAlreadyExists


class FeedbackRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False

    async def get_all_feedbacks(self, session: AsyncSession) -> list[FeedbackSchema]:
        result = await session.execute(select(Feedback))
        return [FeedbackSchema.model_validate(obj=feedback) for feedback in result.scalars().all()]

    async def get_feedback_by_id(self, session: AsyncSession, feedback_id: int) -> FeedbackSchema:
        result = await session.execute(select(Feedback).where(Feedback.feedback_id == feedback_id))
        feedback = result.scalars().first()
        if not feedback:
            raise FeedbackNotFound()
        return FeedbackSchema.model_validate(obj=feedback)

    async def create_feedback(self, session: AsyncSession, feedback: FeedbackCreateUpdateSchema) -> Feedback:
        existing_feedback = await session.execute(
            select(Feedback).where(
                Feedback.hotel_id == feedback.hotel_id,
                Feedback.stay_id == feedback.stay_id,
            )
        )
        if existing_feedback.scalars().first():
            raise FeedbackAlreadyExists()

        new_feedback = Feedback(
            hotel_id=feedback.hotel_id,
            stay_id=feedback.stay_id,
            name=feedback.name,
            address=feedback.address,
        )
        session.add(new_feedback)
        await session.commit()
        await session.refresh(new_feedback)
        return new_feedback

    async def update_feedback(
        self, session: AsyncSession, feedback_id: int, feedback: FeedbackCreateUpdateSchema
    ) -> Feedback:
        result = await session.execute(select(Feedback).where(Feedback.feedback_id == feedback_id))
        existing_feedback = result.scalars().first()
        if not existing_feedback:
            raise FeedbackNotFound()

        existing_feedback.hotel_id = feedback.hotel_id
        existing_feedback.stay_id = feedback.stay_id
        existing_feedback.name = feedback.name
        existing_feedback.address = feedback.address
        await session.commit()
        await session.refresh(existing_feedback)
        return existing_feedback

    async def delete_feedback(self, session: AsyncSession, feedback_id: int) -> None:
        result = await session.execute(select(Feedback).where(Feedback.feedback_id == feedback_id))
        feedback = result.scalars().first()
        if not feedback:
            raise FeedbackNotFound()

        await session.delete(feedback)
        await session.commit()
