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