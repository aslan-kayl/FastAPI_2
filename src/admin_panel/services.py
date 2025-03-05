from .answer.schemas import CreateAnswer
from .info.schemas import CreateInfo
from .models import Banner, Question, Answer, Info
from src.admin_panel.banner.schemas import CreateBanner
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.con.base64 import save_image_from_base64
from .question.schemas import CreateQuestion
from .utils.converts import convert_create_banner_to_orm


class AdminPanelService:
    async def get_all_banners(self, session: AsyncSession):
        statement = select(Banner).order_by(Banner.id)

        result = await session.exec(statement)

        return result.all()

    async def get_banner(self, session: AsyncSession, banner_id: int):
        statement = select(Banner).where(Banner.id == banner_id)

        result = await session.exec(statement)

        banner = result.first()

        return banner if banner is not None else None

    async def create_banner(self, session: AsyncSession, banner_data: CreateBanner):
        banner_data_dict = banner_data.model_dump()

        image_base64 = banner_data_dict.get('image')
        if image_base64:
            file_path = save_image_from_base64(image_base64, output_dir='static/image/banner')
            banner_data_dict['image'] = file_path

        validated_data = CreateBanner.model_validate(banner_data_dict)
        new_banner = convert_create_banner_to_orm(validated_data)

        session.add(new_banner)

        await session.commit()

        return new_banner

    async def update_banner(self, banner_id: int, update_banner: CreateBanner, session: AsyncSession):
        banner_to_update = await self.get_banner(session, banner_id)
        if banner_to_update is not None:

            update_data_dict = update_banner.model_dump()

            for k, v in update_data_dict.items():
                setattr(banner_to_update, k, v)

            await session.commit()

            return banner_to_update
        else:
            return None

    async def delete_banner(self, banner_id: int, session: AsyncSession):
        banner_to_delete = await self.get_banner(session, banner_id)

        if banner_to_delete is not None:
            await session.delete(banner_to_delete)

            await session.commit()

            return {}
        else:
            return None

    async def get_all_info(self, session: AsyncSession):
        statement = select(Info).order_by(Info.id)
        result = await session.exec(statement)
        return result.all()

    async def get_info(self, session: AsyncSession, info_id: int):
        statement = select(Info).where(Info.id == info_id)
        result = await session.exec(statement)
        info = result.first()
        return info if info is not None else None

    async def create_info(self, session: AsyncSession, info_data: CreateInfo):
        info_data_dict = info_data.model_dump()
        new_info = Info(**info_data_dict)
        session.add(new_info)
        await session.commit()
        return new_info

    async def update_info(self, info_id: int, update_info: CreateInfo, session: AsyncSession):
        info_to_update = await self.get_info(session, info_id)
        if info_to_update is not None:

            update_data_dict = update_info.model_dump()

            for k, v in update_data_dict.items():
                setattr(info_to_update, k, v)

            await session.commit()

            return info_to_update
        else:
            return None

    async def delete_info(self, info_id: int, session: AsyncSession):
        info_to_delete = await self.get_info(session, info_id)
        if info_to_delete is not None:
            await session.delete(info_to_delete)

            await session.commit()

            return {}
        else:
            return None

    async def get_all_question(self, session: AsyncSession):
        statement = select(Question).order_by(Question.id)
        result = await session.exec(statement)

        return result.all()

    async def get_question(self, session: AsyncSession, question_id: int):
        statement = select(Question).where(Question.id == question_id)
        result = await session.exec(statement)
        question = result.first()
        return question if question is not None else None

    async def create_question(self, session: AsyncSession, question_data: CreateQuestion):
        question_data_dict = question_data.model_dump()
        new_question = Question(**question_data_dict)
        session.add(new_question)
        await session.commit()
        return new_question

    async def update_question(self, question_id: int, update_question: CreateQuestion, session: AsyncSession):
        question_to_update = await self.get_question(session, question_id)
        if question_to_update is not None:
            update_data_dict = update_question.model_dump()
            for k, v in update_data_dict.items():
                setattr(question_to_update, k, v)
            await session.commit()
            return question_to_update
        else:
            return None

    async def delete_question(self, question_id: int, session: AsyncSession):
        question_to_delete = await self.get_question(session, question_id)
        if question_to_delete is not None:
            await session.delete(question_to_delete)

            await session.commit()

            return {}
        else:
            return None

    async def get_all_answer(self, session: AsyncSession):
        statement = select(Answer).order_by(Answer.id)
        result = await session.exec(statement)
        return result.all()

    async def get_answer(self, session: AsyncSession, answer_id: int):
        statement = select(Answer).where(Answer.id == answer_id)
        result = await session.exec(statement)
        answer = result.first()
        return answer if answer is not None else None

    async def create_answer(self, session: AsyncSession, answer_data: CreateAnswer):
        answer_data_dict = answer_data.model_dump()
        new_answer = Answer(**answer_data_dict)
        session.add(new_answer)
        await session.commit()
        return new_answer

    async def update_answer(self, answer_id: int, update_answer: CreateAnswer, session: AsyncSession):
        answer_to_update = await self.get_answer(session, answer_id)
        if answer_to_update is not None:
            update_data_dict = update_answer.model_dump()
            for k, v in update_data_dict.items():
                setattr(answer_to_update, k, v)
            await session.commit()
            return answer_to_update
        else:
            return None

    async def delete_answer(self, answer_id: int, session: AsyncSession):
        answer_to_delete = await self.get_answer(session, answer_id)
        if answer_to_delete is not None:
            await session.delete(answer_to_delete)

            await session.commit()

            return {}
        else:
            return None
