from pyrogram import Client
from typing import Optional

from pyrogram.errors import PhoneCodeExpired

from .status_slugs import AuthStatusSlug

__all__ = ["auth"]


class Auth:
    def __init__(self):
        self.client: Optional[Client] = None

    async def _auth_with_name(self, name: str, session_string: str, account_id: str) -> dict:
        try:
            client = Client(name=name, session_string=session_string)
            self.client = client
            await self.client.connect()
        except Exception as e:
            return {
                "status": AuthStatusSlug.ERROR,
                "data": str(e)
            }

        return {
            "status": AuthStatusSlug.AUTH_SUCCESS,
            "data": {
                "account_id": account_id
            }
        }

    async def _auth_with_code(self, name: str, phone_number: str, api_id: str, api_hash: str, account_id: str,
                              phone_code: Optional[str] = None, phone_code_hash: Optional[str] = None) -> dict:
        try:
            if not self.client:
                client = Client(name=name, api_id=api_id, api_hash=api_hash, workers=2)
                self.client = client
                await self.client.connect()

            if phone_code is None and phone_code_hash is None:
                send_code = await self.client.send_code(phone_number)
                return {
                    "status": AuthStatusSlug.CODE_SEND,
                    "data": {
                        "phone_code_hash": send_code.phone_code_hash,
                        "timeout": send_code.timeout,
                        "account_id": account_id
                    }
                }
            elif self.client:
                try:
                    await self.client.sign_in(
                        phone_number=phone_number,
                        phone_code_hash=phone_code_hash,
                        phone_code=phone_code
                    )
                except PhoneCodeExpired:
                    return {
                        "status": AuthStatusSlug.ERROR,
                        "data": "Код подтверждения не верный или устарел. Запросите новый код."
                    }
            else:
                return {
                    "status": AuthStatusSlug.ERROR,
                    "data": "Ошибка! Возможно сессия устарела!"
                }

            session_string = await self.client.export_session_string()

            return {
                "status": AuthStatusSlug.AUTH_SUCCESS,
                "data": {
                    "session_string": session_string,
                    "account_id": account_id
                }
            }
        except Exception as e:
            return {
                "status": AuthStatusSlug.ERROR,
                "data": str(e)
            }

    async def sign_in_client(self, name: str, api_id: str, api_hash: str, phone_number: str, account_id: str,
                             phone_code: Optional[str] = None, phone_code_hash: Optional[str] = None,
                             session_string: Optional[str] = None) -> dict:
        if session_string:
            return await self._auth_with_name(name, session_string, account_id)
        else:
            return await self._auth_with_code(name, phone_number, api_id, api_hash, account_id, phone_code,
                                              phone_code_hash)


auth = Auth()
