from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils import auth, AuthStatusSlug

app = FastAPI()


class AccountData(BaseModel):
    account_id: str
    phone_number: str
    api_id: str
    api_hash: str
    name: str
    phone_code_hash: Optional[str] = None
    phone_code: Optional[str] = None
    session_string: Optional[str] = None


@app.post('/authorize_account')
async def auth_account(
    account_data: AccountData,
):
    try:
        res = await auth.sign_in_client(
            **account_data.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    match res.get('status'):
        case AuthStatusSlug.AUTH_SUCCESS:
            return {
                'status': 'authorized',
                'session_string': res.get('data').get('session_string'),
            }
        case AuthStatusSlug.CODE_SEND:
            return {
                'status': 'code_send',
                'phone_code_hash': res.get('data').get('phone_code_hash'),
                'timeout': res.get('data').get('timeout', None),
            }
        case AuthStatusSlug.ERROR:
            return {
                'status': 'error',
                'data': res.get('data')
            }
