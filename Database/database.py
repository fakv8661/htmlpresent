from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy import select

from Database import db_setting as dbs
from Database import models

engine = create_async_engine(dbs.get_dburl(), pool_size=20, max_overflow=40)
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
            )
            if not where_hidden:
                stmt = stmt.where(models.Presentation.hidden == False)

            cur = await session.execute(stmt)
            obj = cur.scalars().all()

            return obj

    @staticmethod
    async def GetPresentationByID(id: int, where_hidden:bool=False) -> models.Presentation | None:
        async with session_factory() as session:
            stmt = (
                select(models.Presentation)
                .where(models.Presentation.id == id)
            )
            if not where_hidden:
                stmt = stmt.where(models.Presentation.hidden == False)

            cur = await session.execute(stmt)
            
            return cur.scalar()

    @staticmethod
    async def CreatePresentation(name: str, author: str, description: str,
                                 file: str, image: str | None, owner_id: int) -> None:
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

    @staticmethod
    async def HidePresentation(id: int, hidden: bool) -> None:
        async with session_factory() as session:
            stmt = (
                select(models.Presentation)
                .where(models.Presentation.id == id)
            )

            cur = await session.execute(stmt)
            row = cur.scalar()

            if row is not None:
                row.hidden = hidden

            await session.commit()

    @staticmethod
    async def DeletePresentation(id: int) -> None:
        async with session_factory() as session:
            stmt = (
                select(models.Presentation)
                .where(models.Presentation.id == id)
            )

            cur = await session.execute(stmt)
            row = cur.scalar()

            if row is not None:
                await session.delete(row)

            await session.commit()



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
                .where(models.Admin.id == admin_id, 
                       models.Admin.high_admin == True)
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

    @staticmethod
    async def GetAllAdmins() -> list[tuple[int, int, str]]:
        async with session_factory() as session:
            stmt = (
                select(models.Admin.id,
                       models.Admin.telegram_id,
                       models.Admin.login)
            )

            cur = await session.execute(stmt)

            rows = cur.all()

            return rows

    @staticmethod
    async def GetAdminIDByLogin(login: str) -> int | None:
        async with session_factory() as session:
            stmt = (
                select(models.Admin.id)
                .where(models.Admin.login == login)
            )

            cur = await session.execute(stmt)

            return cur.scalar()

    @staticmethod
    async def DeleteAdmin(id: int) -> None:
        async with session_factory() as session:
            stmt = (
                select(models.Admin)
                .where(models.Admin.id == id)
            )

            cur = await session.execute(stmt)
            row = cur.scalar()

            if row is not None:
                await session.delete(row)
                await session.commit()

    @staticmethod
    async def CreateAdmin(login: str, password_hash: str, telegram_id: int = None):
        async with session_factory() as session:
            admin = models.Admin(login=login,
                                 password=password_hash,
                                 telegram_id=telegram_id)

            session.add(admin)
            await session.commit()

    @staticmethod
    async def GetHashPassword(admin_id: int) -> str | None:
        async with session_factory() as session:
            stmt = (
                select(models.Admin.password)
                .where(models.Admin.id == admin_id)
            )

            cur = await session.execute(stmt)
            row = cur.scalar()

            return row

    @staticmethod
    async def LinkTelegram(admin_id: int, telegram_id: int):
        async with session_factory() as session:
            stmt = (
                select(models.Admin)
                .where(models.Admin.id == admin_id)
            )

            cur = await session.execute(stmt)
            row = cur.scalar()

            if row:
                row.telegram_id = telegram_id
                await session.commit()
                
            