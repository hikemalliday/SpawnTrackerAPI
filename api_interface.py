from fastapi import APIRouter
from message_helper import send_message_to_guild
from config import GUILD_ID, CHANNEL_ID
from pydantic import BaseModel
from db_commands import insert_mob_spawn, insert_mob_death

router = APIRouter()

class MobDeathRegexPayload(BaseModel):
    death_time: str
    mob_name: str

class MobSpawnRegexPayload(BaseModel):
    spawn_time: str
    mob_zone: str

@router.post("/mob_death_regex")
def mob_death_regex(payload: MobDeathRegexPayload):
    insert_mob_death(payload)
    print(payload)
    return payload

@router.post("/mob_spawn_regex")
def mob_spawn_regex(payload: MobSpawnRegexPayload):
    insert_mob_spawn(payload)
    print(payload)
    return payload