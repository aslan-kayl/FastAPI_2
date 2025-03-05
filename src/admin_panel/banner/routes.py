from fastapi import APIRouter, status, Depends, HTTPException
from src.admin_panel.services import AdminPanelService
from typing import List
from .schemas import Banner, CreateBanner
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.con.main import get_session

banner_router = APIRouter()
admin_panel_service = AdminPanelService()


@banner_router.get("/", response_model=List[Banner])
async def get_all_banners(session: AsyncSession = Depends(get_session)):
    banners = await admin_panel_service.get_all_banners(session)
    return banners


@banner_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Banner)
async def create_banner(banner_data: CreateBanner, session: AsyncSession = Depends(get_session)):
    new_banner = await admin_panel_service.create_banner(session, banner_data)
    return new_banner


@banner_router.get("/{banner_id}", response_model=CreateBanner)
async def get_banner(banner_id: int, session: AsyncSession = Depends(get_session)):
    banner = await admin_panel_service.get_banner(session, banner_id)
    if banner:
        return banner
    else:
        raise HTTPException(status_code=404, detail="Banner not found")


@banner_router.patch("/{banner_id}", response_model=CreateBanner)
async def update_banner(banner_id: int, banner_update_data: CreateBanner, session: AsyncSession = Depends(get_session)):
    update_to_banner = await admin_panel_service.update_banner(banner_id, banner_update_data, session)
    if update_to_banner is None:
        raise HTTPException(status_code=404, detail="Banner not found")
    else:
        return update_banner


@banner_router.delete("/{banner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_banner(banner_id: int, session: AsyncSession = Depends(get_session)):
    banner_to_delete = await admin_panel_service.delete_banner(banner_id, session)
    if banner_to_delete is None:
        raise HTTPException(status_code=404, detail="Banner not found")
    else:
        return {}
