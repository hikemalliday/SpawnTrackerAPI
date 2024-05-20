from bot_instance import bot
from discord import Embed

async def send_message_to_guild(guild_id: int, channel_id: int, message: str | Embed = None):
    guild = bot.get_guild(guild_id)
    print(f"guild: {guild}")
    if guild:
        channel = guild.get_channel(channel_id)
        if channel:
            if message != str:
                await channel.send(embed=message)
            else:
                await channel.send(message)
        else:
            print(f"Channel not found for guild: {guild_id}")
    else:
        print(f"Guild not found: {guild_id}")