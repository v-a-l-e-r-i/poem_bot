import os
from aiogram.filters import BaseFilter
from aiogram.types import Message

ADMIN_IDS = set(map(int, os.getenv("ADMIN_IDS", "").split(",")))

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMIN_IDS
