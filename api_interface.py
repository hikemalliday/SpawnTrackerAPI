from fastapi import APIRouter
from message_helper import send_message_to_guild
from config import GUILD_ID, CHANNEL_ID

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "root test"}

@router.get("/test")
async def test():
    await send_message_to_guild(GUILD_ID, CHANNEL_ID, "test")
    return "test"