from models.tables import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, insert
from typing import Optional, Union
from models.session_wrapper import database_connector
import uuid
import datetime

__all__ = [
    'get_active_account_data',
    'get_messages_data',
    'get_active_chats_data',
    'ban_chat',
    'ban_account',
    'add_new_chat',
    'update_chat'
]


@database_connector
async def get_active_account_data(session: AsyncSession) -> Optional[Account]:
    active_account_stmt = select(Account).where(Account.is_active == True).join(Interval.account)
    orm = await session.execute(active_account_stmt)
    active_account: Account = orm.scalar_one_or_none()
    if active_account is None:
        return
    return active_account


@database_connector
async def get_active_chats_data(session: AsyncSession, *, account: Union[Account, uuid]) -> list[Chat]:
    if isinstance(account, Account):
        account_id = account.id
    else:
        account_id = account

    chat_stmt = select(Chat).where(
        and_(
            Chat.account_id == account_id,
            Chat.is_active == True,
            Chat.is_banned == False
        )
    )
    orm = await session.execute(chat_stmt)
    active_chats = orm.scalars().all()
    return active_chats


@database_connector
async def get_messages_data(session: AsyncSession) -> dict:
    message_stmt = select(Message)
    orm = await session.execute(message_stmt)
    messages_data = orm.scalars().all()

    messages_dict = {}
    for message in messages_data:
        messages_dict[message.message_type] = message.message_text
    return messages_dict


@database_connector
async def ban_chat(session: AsyncSession, *, chat_id: int) -> bool:
    stmt = update(Chat).where(Chat.id == chat_id).values(is_banned=True)
    await session.execute(stmt)
    return True


@database_connector
async def ban_account(session: AsyncSession, *, account_id: int) -> bool:
    stmt = update(Account).where(Account.id == account_id).values(is_bannded=True)
    await session.execute(stmt)
    return True


@database_connector
async def add_new_chat(
        session: AsyncSession,
        *,
        title: str,
        chat_id: int,
        account_id: uuid,
        last_message_send: Optional[datetime] = None
) -> Optional[Chat]:
    stmt = insert(
        Chat
    ).values(
        title=title,
        chat_id=chat_id,
        account_id=account_id,
        last_message_send=last_message_send
    ).returning(Chat)
    orm = await session.execute(stmt)
    return orm.scalar_one()


@database_connector
async def update_chat(
        session: AsyncSession,
        *,
        id_in_db: uuid,
        last_message_send: Optional[datetime] = None,
        title: str,
):
    stmt = update(
        Chat
    ).where(
        Chat.id == id_in_db
    ).values(
        title=title,
    )
    if last_message_send is not None:
        stmt = stmt.values(last_message_send=last_message_send)
    await session.execute(stmt)
    return True
