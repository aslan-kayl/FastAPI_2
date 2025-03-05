from fastapi import APIRouter, status, Depends, HTTPException
from src.admin_panel.services import AdminPanelService
from typing import List
from .schemas import Answer, CreateAnswer
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.con.main import get_session

answer_router = APIRouter()
admin_panel_service = AdminPanelService()



@answer_router.get("/", response_model=List[Answer])
async def get_all_answers(session: AsyncSession = Depends(get_session)):
    answers = await admin_panel_service.get_all_answers(session)
    return answers

@answer_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Answer)
async def create_answer(answer_data: CreateAnswer, session: AsyncSession = Depends(get_session)):
    new_answer = await admin_panel_service.create_answer(session, answer_data)
    return new_answer


@answer_router.get("/{answer_id}", response_model=Answer)
async def get_answer(answer_id: int, session: AsyncSession = Depends(get_session)):
    answer = await admin_panel_service.get_answer(session, answer_id)
    if answer:
        return answer
    else:
        raise HTTPException(status_code=404, detail="Answer not found")

@answer_router.patch("/{answer_id}", response_model=Answer)
async def update_answer(answer_id:int, answer_update_data: Answer, session: AsyncSession = Depends(get_session)):
    update_to_answer = await admin_panel_service.update_answer(answer_id, session, answer_update_data)
    if update_to_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    else:
        return update_to_answer

@answer_router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(answer_id: int, session: AsyncSession = Depends(get_session)):
    answer_to_delete = await admin_panel_service.delete_answer(answer_id, session)
    if answer_to_delete is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    else:
        return {}
