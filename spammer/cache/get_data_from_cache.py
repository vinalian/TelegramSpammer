from pickle import loads, dumps
from .redis_cache import redis
from typing import Union, Literal, Optional
from pydantic import BaseModel
from models.funcs import get_active_account_data, get_active_chats_data, get_messages_data
import json

__all__ = ['get_cache_data']


class RedisCacheData(BaseModel):
    active_account: dict
    interval: int
    chat_list: Optional[list[dict]] = None
    chat_message: str
    personal_message: str


async def get_full_account_data() -> Union[RedisCacheData, bool]:
    account_data = await get_active_account_data()
    if not account_data:
        return False

    active_chats = await get_active_chats_data(account=account_data)
    message_data = await get_messages_data()
    return RedisCacheData(**{
        'active_account': account_data.to_dict(),
        'interval': account_data.interval.interval,
        'chat_list': [chat.to_dict() for chat in active_chats],
        'chat_message': message_data.get('chat_message', None),
        'personal_message': message_data.get('personal_message', None),
    })


async def write_data_to_redis(
        data: RedisCacheData,
        *,
        redis,
        ex: int = 60 * 60 * 24  # Cache data for 1 day.,
) -> None:
    redis.set('active_account', dumps(data.active_account), ex=ex)
    redis.set('interval', data.interval, ex=ex)
    redis.set('chat_list', dumps(data.chat_list), ex=ex)
    redis.set('messages:personal', dumps(data.personal_message), ex=ex)
    redis.set('messages:chat', dumps(data.chat_message), ex=ex)


async def get_cache_data(
        key: Literal[
            'active_account',
            'interval',
            'chat_list',
            'chat_message',
            'personal_message',
            None
        ] = None
) -> dict:
    if key:
        key = f':1:{key}'

        cache = redis.get(key)
        if cache:
            return loads(cache)
        return None

    else:
        data = {}
        for key in ['active_account', 'interval', 'chat_list', 'messages:personal', 'messages:chat']:
            cache = redis.get(f':1:{key}')
            if cache:
                if key == 'messages:personal':
                    key = 'personal_message'
                    data[key] = loads(cache)

                if key == 'messages:chat':
                    key = 'chat_message'
                    data[key] = loads(cache)
                if key in ('active_account', 'chat_list'):
                    cache = json.loads(loads(cache))
                    data[key] = cache
                    if key == 'active_account':
                        data['interval'] = cache.get('interval', 60 * 10)

        if data:
            return RedisCacheData(**data).model_dump(mode='python')

        data = await get_full_account_data()
        if data is False:
            return None

        await write_data_to_redis(data, redis=redis)

        return data.model_dump(
            mode='python'
        )
