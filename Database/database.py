from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy import select

from Database import db_setting as dbs
from Database import models

engine = create_async_engine(dbs.get_dburl(), echo=True, pool_size=20, max_overflow=40)
session_factory = async_sessionmaker(engine)


async def InitDatabase():
    async with engine.connect() as conn:
        await conn.run_sync(models.Base.metadata.create_all, checkfirst=True)
        await conn.commit()

class PresentationDatabase():
    @staticmethod
    async def GetAllPresentations(where_hidden:bool=False) -> list[models.Presentation] | None:
        async with session_factory() as session:
            stmt = (
                select(models.Presentation)
                .where(models.Presentation.hidden == where_hidden)
            )

            cur = await session.execute(stmt)
            obj = cur.scalars().all()

            return obj

    @staticmethod
    async def GetPresentationByID(id: int, where_hidden:bool=False) -> models.Presentation | None:
        async with session_factory() as session:
            stmt = (
                select(models.Presentation)
                .where(models.Presentation.hidden == where_hidden,
                       models.Presentation.id == id)
            )

            cur = await session.execute(stmt)
            
            return cur.scalar()

    @staticmethod
    async def CreatePresentation(name: str, author: str, description: str,
                                 file: str, image: str | None, owner_id: int):
        async with session_factory() as session:
            presentation = models.Presentation(
                name=name,
                owner_id=owner_id,
                author=author,
                description=description,
                file=file,
                preview_image=image
            )

            session.add(presentation)
            await session.commit()

    @staticmethod
    async def GetPresentationsByOwner(owner_id: int) -> list[models.Presentation]:
        async with session_factory() as session:
            stmt = (
                select(models.Presentation)
                .where(models.Presentation.owner_id == owner_id)
            )

            cur = await session.execute(stmt)
            rows = cur.scalars().all()

            return rows


class AdminPanel():
    @staticmethod
    async def AdminCheck(tg_id: int, high_level:bool=False) -> bool:
        """Return true if record is exists"""
        async with session_factory() as session:
            stmt = (
                    select(models.Admin)
                    .where(models.Admin.telegram_id == tg_id)
                )
            if high_level:
                stmt = stmt.where(models.Admin.high_admin == high_level)
            cur = await session.execute(stmt)

            row = cur.scalar()

            return row is not None

    @staticmethod
    async def isHighAdmin(admin_id: int) -> bool:
        async with session_factory() as session:
            stmt = (
                select(models.Admin)
                .where(models.Admin.id == admin_id, models.Admin.high_admin == True)
            )

            cur = await session.execute(stmt)

            row = cur.scalar()

            return row is not None

    @staticmethod
    async def PresentationLimitCheck(admin_id: int, limit:int=3) -> bool:
        async with session_factory() as session:
            stmt = (
                select(models.Presentation.id)
                .where(models.Presentation.owner_id == admin_id)
            )

            cur = await session.execute(stmt)

            presentations = cur.scalars().all()

            return not (len(presentations) >= limit)

    @staticmethod
    async def GetAdminIDByTg(tg_id: int) -> int | None:
        async with session_factory() as session:
            stmt = (
                select(models.Admin.id)
                .where(models.Admin.telegram_id == tg_id)
            )

            cur = await session.execute(stmt)

            return cur.scalar()