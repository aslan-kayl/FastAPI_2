from fastapi import APIRouter, status, Depends, HTTPException
from src.admin_panel.services import AdminPanelService
from typing import List
from .schemas import Info, CreateInfo
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.con.main import get_session

info_router = APIRouter()
admin_panel_service = AdminPanelService()




@info_router.get("/", response_model=List[Info])
async def get_all_infos(session: AsyncSession = Depends(get_session)):
    infos = await admin_panel_service.get_all_info(session)
    return infos


@info_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Info)
async def create_info(info_data: CreateInfo, session: AsyncSession = Depends(get_session)):
    new_info = await admin_panel_service.create_info(session, info_data)
    return new_info


@info_router.get("/{info_id}", response_model=CreateInfo)
async def get_info(info_id: int, session: AsyncSession = Depends(get_session)):
    info = await admin_panel_service.get_info(session, info_id)
    if info:
        return info
    else:
        raise HTTPException(status_code=404, detail="Info not found")

@info_router.patch("/{info_id}", response_model=Info)
async def update_info(info_id: int, info_update_data: Info, session:AsyncSession = Depends(get_session)):
    update_to_info = await admin_panel_service.update_info(info_id, session, info_update_data)
    if update_to_info is None:
        raise HTTPException(status_code=404, detail="Info not found")
    else:
        return update_info

@info_router.delete("/{info_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_info(info_id: int, session: AsyncSession = Depends(get_session)):
    info_to_delete = await admin_panel_service.delete_info(info_id, session)
    if info_to_delete is None:
        raise HTTPException(status_code=404, detail="Info not found")
    else:
        return {}