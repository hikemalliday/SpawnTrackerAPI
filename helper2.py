from datetime import datetime, timedelta
from bot_instance import bot
import sqlite3
from config import DB_PATH

def calculate_respawn_time(mob_name: str, time_stamp: str):
    # Take in the time_stamp str, convert to datetime obj, add timedelta, convert to string, then return
    time_stamp_object = datetime.strptime(time_stamp, "%a %b %d %H:%M:%S %Y")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        query_mob_master = '''
        SELECT mob_name, respawn_timer, variance FROM mob_master
        WHERE mob_name = ?
        '''
        c.execute(query_mob_master, (mob_name,))
        results = c.fetchone()
        if results:
            respawn_timer = results[1]
            variance = results[2]
            new_timestamp = time_stamp_object + timedelta(hours=(respawn_timer - (variance / 2)))
            new_timestamp_str = new_timestamp.strftime("%a %b %d %H:%M:%S %Y")
            return new_timestamp_str
    except Exception as e:
        print(str(e))
    finally:
        conn.close()