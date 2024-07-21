from pyrogram import Client
from pyrogram.errors import UserBannedInChannel, PhoneNumberBanned
import logging
from models.funcs import ban_chat, ban_account
import uuid
from utils.status_slugs import SpammerStatusSlug

__all__ = ['Spammer']


class Spammer:
    __slots__ = [
        'client',
        'client_id_in_db'
    ]

    def __init__(
            self,
            client: Client,
            client_id_in_db: uuid
    ):
        self.client = client
        self.client_id_in_db = client_id_in_db

    async def send_message(
            self,
            chat_id: int,
            message: str
    ) -> bool:
        try:
            await self.client.send_message(
                chat_id=chat_id,
                text=message
            )
            return SpammerStatusSlug.OK
        except UserBannedInChannel:
            await ban_chat(
                chat_id=chat_id
            )
            return SpammerStatusSlug.BANNED_CHAT
        except PhoneNumberBanned:
            await ban_account(
                account_id=self.client_id_in_db
            )
            return SpammerStatusSlug.BANNED_ACCOUNT
        except Exception as e:
            logging.error(f'Error occurred while sending message to {chat_id}: {e}')
            return SpammerStatusSlug.UNKNOWN_ERROR
