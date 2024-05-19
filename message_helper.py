from bot_instance import bot

async def send_message_to_guild(guild_id, channel_id, message):
    guild = bot.get_guild(guild_id)
    print(f"guild: {guild}")
    if guild:
        # Replace CHANNEL_ID with the actual ID of the channel you want to send the message to
        channel = guild.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            print("Channel not found for guild:", guild_id)
    else:
        print("Guild not found:", guild_id)