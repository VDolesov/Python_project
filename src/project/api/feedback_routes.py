from fastapi import APIRouter, HTTPException, status
from project.infrastructure.postgres.repository.feedback_repo import FeedbackRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.feedback import FeedbackSchema, FeedbackCreateUpdateSchema
from project.core.exceptions import FeedbackNotFound,HotelNotFound,StayNotFound,FeedbackAlreadyExists

router = APIRouter()
feedback_repo = FeedbackRepository()
database = PostgresDatabase()


@router.get(
    "/all_feedbacks",
    response_model=list[FeedbackSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_feedbacks() -> list[FeedbackSchema]:
    async with database.session() as session:
        await feedback_repo.check_connection(session=session)
        all_feedbacks = await feedback_repo.get_all_feedbacks(session=session)
    return all_feedbacks


@router.get(
    "/feedback/{feedback_id}",
    response_model=FeedbackSchema,
    status_code=status.HTTP_200_OK
)
async def get_feedback_by_id(feedback_id: int) -> FeedbackSchema:
    async with database.session() as session:
        try:
            feedback = await feedback_repo.get_feedback_by_id(session=session, feedback_id=feedback_id)
        except FeedbackNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return feedback


@router.post(
    "/add_feedback",
    response_model=FeedbackSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_feedback(feedback_dto: FeedbackCreateUpdateSchema) -> FeedbackSchema:
    async with database.session() as session:
        try:
            new_feedback = await feedback_repo.create_feedback(session=session, feedback=feedback_dto)
        except HotelNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
        except StayNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stay not found")
        except FeedbackAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Feedback already exists")
    return new_feedback


@router.put(
    "/update_feedback/{feedback_id}",
    response_model=FeedbackSchema,
    status_code=status.HTTP_200_OK
)
async def update_feedback(feedback_id: int, feedback_dto: FeedbackCreateUpdateSchema) -> FeedbackSchema:
    async with database.session() as session:
        try:
            updated_feedback = await feedback_repo.update_feedback(session=session, feedback_id=feedback_id, feedback=feedback_dto)
        except FeedbackNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_feedback


@router.delete(
    "/delete_feedback/{feedback_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_feedback(feedback_id: int) -> None:
    async with database.session() as session:
        try:
            await feedback_repo.delete_feedback(session=session, feedback_id=feedback_id)
        except FeedbackNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
