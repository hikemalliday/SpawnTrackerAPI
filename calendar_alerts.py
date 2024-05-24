import asyncio
import sqlite3
from config import DB_PATH, GUILD_ID_DEV, CHANNEL_ID_DEV
from datetime import datetime
from message_helper import send_message_to_guild
from embed import calendar_alert_embed

async def calendar_alerts():
    while True:
        print("calendar alert loop")
        await asyncio.sleep(60)  # Wait for 1 minute
        # Perform your SQLite select and logic here
        curr_time = datetime.now()
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mob_death")
            results = cursor.fetchall()
            for result in results:
                mob_name = result[1]
                respawn_time = datetime.strptime(result[3], '%a %b %d %H:%M:%S %Y')
                time_difference = abs((respawn_time - curr_time).total_seconds())
                if time_difference <= 30:
                    embed = calendar_alert_embed(mob_name)
                    await send_message_to_guild(GUILD_ID_DEV, CHANNEL_ID_DEV, embed)
            conn.close()
        except Exception as e:
            print(f"Error during calendar_alerts(): {e}")