from src.admin_panel.models import Banner
from src.admin_panel.banner.schemas import CreateBanner


def convert_create_banner_to_orm(banner_create: CreateBanner) -> Banner:
    data = banner_create.dict()
    return Banner(**data)