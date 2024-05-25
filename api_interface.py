from fastapi import APIRouter
from message_helper import send_message_to_guild
from config import GUILD_ID, CHANNEL_ID
from pydantic import BaseModel
from db_commands import insert_mob_spawn, insert_mob_death
from embed import mob_death_embed, mob_spawn_embed
from helper import calculate_respawn_time


router = APIRouter()

class MobDeathRegexPayload(BaseModel):
    death_time: str
    mob_name: str

class MobSpawnRegexPayload(BaseModel):
    spawn_time: str
    mob_zone: str

# NOTE: Have to convert the payload to tuples (conflicts with other logic if we dont)
@router.post("/mob_death_regex")
async def mob_death_regex(payload: MobDeathRegexPayload):
    death_payload = (payload.death_time, payload.mob_name)
    insert_mob_death(death_payload)
    respawn_time = calculate_respawn_time(payload.mob_name, payload.death_time)
    embed = mob_death_embed(payload.death_time, payload.mob_name, respawn_time)
    await send_message_to_guild(GUILD_ID, CHANNEL_ID, embed)
    return payload

@router.post("/mob_spawn_regex")
async def mob_spawn_regex(payload: MobSpawnRegexPayload):
    spawn_payload = (payload.spawn_time, payload.mob_zone)
    insert_mob_spawn(spawn_payload)
    embed = mob_spawn_embed(payload.mob_zone, payload.spawn_time)
    await send_message_to_guild(GUILD_ID, CHANNEL_ID, embed)
    return payload