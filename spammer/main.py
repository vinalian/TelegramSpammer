import json
from utils.spammer import Spammer
from utils.status_slugs import SpammerStatusSlug
from cache.get_data_from_cache import get_cache_data
from uuid import UUID
from pyrogram import Client
import logging
from typing import Optional
from pyrogram.enums import ChatType
from models.funcs import add_new_chat, update_chat, get_active_chats_data
import uuid
from datetime import datetime


async def update_chat_list(client: Client, chat_list: list[dict], account_id_in_db: uuid) -> list[dict]:
    chat_list_id = [int(x.get('chat_id')) for x in chat_list]

    chat_in_db = await get_active_chats_data(account=account_id_in_db)
    if chat_in_db:
        for chat in chat_in_db:
            chat_list.append(chat.to_dict())

    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type not in (ChatType.CHANNEL, ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE):
            continue
        if dialog.chat.id not in chat_list_id:
            if dialog.chat.title not in ('213123', 'fewswsedf', 'Тестовый чат 1'):
                continue
            new_chat = await add_new_chat(
                chat_id=dialog.chat.id,
                title=dialog.chat.title,
                account_id=account_id_in_db
            )
            if new_chat:
                chat_list.append(new_chat.to_dict())
        else:
            await update_chat(
                chat_id=dialog.chat.id,
                title=dialog.chat.title
            )
    return chat_list


async def spam_for_chat(
        chat: dict,
        spammer: Spammer,
        message: str
) -> None:
    try:
        status = await spammer.send_message(
            chat_id=chat.get('chat_id'),
            message=message,
        )
        if status == SpammerStatusSlug.OK:
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Failed to send message to chat {chat.get('chat_id')}: {str(e)}")
        return False


async def check_spammer_account(spammer, cache_data: dict) -> Optional[Spammer]:
    if spammer is None or spammer.client.name != cache_data.get('active_account').get('name'):
        async with Client(name=cache_data.get('active_account').get('name'),
                          session_string=cache_data.get('active_account').get('session_string')) as app:
            spammer = Spammer(
                client=app,
                client_id_in_db=UUID(cache_data.get('active_account').get('id')),
            )
        return spammer, True
    return spammer, False


async def main(spammer: Optional[Spammer] = None):
    cache_data = await get_cache_data()
    if not cache_data:
        await asyncio.sleep(60 * 5)
        return await main()

    if spammer is None:
        spammer, is_update = await check_spammer_account(spammer, cache_data)

    if not spammer.client.is_connected:
        await spammer.client.connect()

    actual_chat_list = await update_chat_list(
        client=spammer.client,
        chat_list=cache_data.get('chat_list'),
        account_id_in_db=UUID(cache_data.get('active_account').get('id')),
    )
    if not actual_chat_list:
        logging.warning('Нет актуальных чатов! Ждём 5 минут...')
        await asyncio.sleep(60 * 5)

    for chat in actual_chat_list:
        spammer, is_update = await check_spammer_account(spammer, cache_data)
        if is_update:
            return await main(spammer)

        chat_message_info = json.loads(cache_data.get('chat_message', '{}'))
        is_send = await spam_for_chat(chat, spammer, chat_message_info.get('message_text'))
        if is_send:
            await update_chat(
                id_in_db=uuid.UUID(chat.get('id')),
                title=chat.get('title'),
                last_message_send=datetime.now(),
            )
        await asyncio.sleep(int(cache_data.get('interval')), 10*60)
    return await main(spammer)

if __name__ == '__main__':
    import asyncio

    logging.info('Spammer started...')
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
