from asyncio import iscoroutinefunction
from models.engine import database


def database_connector(func):
    # Get session before function
    # commit + close session after function.
    async def wrapper(*args, **kwargs):
        if not iscoroutinefunction(func):
            # if function not async.
            raise ValueError("Decorator must be used for async functions!")

        session = None
        try:
            session = await database.create_session()
            func_ = await func(session=session, *args, **kwargs)
            await session.commit()
            await session.close()
            return func_
        except Exception as e:
            if session:
                await session.rollback()
                await session.commit()
                await session.close()
            return False

    return wrapper
