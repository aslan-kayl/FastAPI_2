from fastapi import APIRouter, status, Depends, HTTPException
from src.admin_panel.services import AdminPanelService
from typing import List
from .schemas import Question, CreateQuestion
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.con.main import get_session

question_router = APIRouter()
admin_panel_service = AdminPanelService()


@question_router.get("/", response_model=List[Question])
async def get_all_questions(session: AsyncSession = Depends(get_session)):
    questions = await admin_panel_service.get_all_question(session)
    return questions

@question_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Question)
async def create_question(question_data: CreateQuestion, session: AsyncSession = Depends(get_session)):
    new_question = await admin_panel_service.create_question(session, question_data)
    return new_question

@question_router.get("/{question_id}", response_model=Question)
async def get_question(question_id: int, session: AsyncSession = Depends(get_session)):
    question = await admin_panel_service.get_question(session, question_id)
    if question:
        return question
    else:
        raise HTTPException(status_code=404, detail="Question not found")

@question_router.patch("/{question_id}", response_model=Question)
async def update_question(question_id: int, question_update_data: Question, session:AsyncSession = Depends(get_session)):
    update_to_question = await admin_panel_service.update_question(question_id, session, question_update_data)
    if update_to_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    else:
        return update_to_question

@question_router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, session: AsyncSession = Depends(get_session)):
    question_to_delete = await admin_panel_service.delete_question(question_id, session)
    if question_to_delete is None:
        raise HTTPException(status_code=404, detail="Question not found")
    else:
        return {}