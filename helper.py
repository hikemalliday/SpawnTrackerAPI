
from datetime import datetime, timedelta
from bot_instance import bot
import discord
from db_commands import fetch_mob_names_master, fetch_mob_names_death
from helper2 import calculate_respawn_time
import sqlite3
from config import DB_PATH

async def add_mob_death_autocomplete(interaction: discord.Interaction, current: str):
    mob_names = await fetch_mob_names_master(current)
    if mob_names is None:
        print(f"ERROR: add_mob_death_autocomplete")
        return f"ERROR: add_mob_death_autocomplete"
    choices = []
    for mob_name in mob_names:
        print(mob_name)
        choices.append(discord.app_commands.Choice(name=mob_name, value=mob_name))
    return choices

async def delete_mob_death_autocomplete(interaction: discord.Interaction, current: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Fetch mob names and IDs matching the current input
        like_pattern = f'{current}%'
        query = '''
            SELECT id, mob_name, death_time FROM mob_death WHERE mob_name LIKE ?
            ORDER BY id DESC LIMIT 25
        '''
        c.execute(query, (like_pattern,))
        mob_deaths = c.fetchall()
        
        results = []
        for mob_death in mob_deaths:
            id, mob_name, death_time = mob_death
            will_respawn = is_mob_spawn_due(mob_name, death_time)
            if will_respawn:
                respawn_time = will_respawn
                mob_name_display = f"{mob_name}🐲"
                results.append(discord.app_commands.Choice(name=f"{mob_name_display}, died at: {death_time}. Respawns at: {respawn_time}", value=id))
            else:
                results.append(discord.app_commands.Choice(name=f"{mob_name}, died at: {death_time}", value=id))

        return results
    except Exception as e:
        print(str(e))
        return [discord.app_commands.Choice(name=f"Error: {str(e)}", value="-1")]
    finally:
        if conn:
            conn.close()    


def get_file_name() -> str:
    try:
        char_name = ''
        eq_dir = ''
        server = ''

        c = bot.db_connection.cursor()
        query = '''SELECT * FROM config
        '''
        c.execute(query)
        row = c.fetchone()

        if row:
            id, char_name, eq_dir, server = row
            if server == "RoT":
                return f"{eq_dir}logs\eqlog_{char_name}_RoT.txt"
            else:
                return f"{eq_dir}logs\eqlog_{char_name}_P1999PVP.txt"
            
        else:
            print("No rows found in the 'config' table.")
            return "" 
        
    except Exception as e:
        print(str(e))
        return str(e)



# Might be un-used -- might just force the user to enter a mob_spawn
def calculate_mob_death(mob_name, time_stamp: str):
    time_stamp_object = datetime.strptime(time_stamp, "%a %b %d %H:%M:%S %Y")
    try:
        c = bot.db_connection.cursor()
        query_mob_master = '''
        SELECT mob_name, mob_respawn_timer, variance FROM mob_master
        WHERE mob_name = ?
        '''
        c.execute(query_mob_master, (mob_name,))
        results = c.fetchone()
        if results:
            respawn_timer = results[1]
            variance = results[2]
            new_timestamp = time_stamp_object - timedelta(hours=(respawn_timer - (variance / 2)))
            new_timestamp_str = new_timestamp.strftime("%a %b %d %H:%M:%S %Y")
            return new_timestamp_str
    except Exception as e:
        print(str(e))

def convert_date_time(row: tuple) -> list:
    id = row[0]
    mob_name = row[1]
    date = row[2]
    timestamp_object = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
    timestamp_string = timestamp_object.strftime("%a %b %d %H:%M:%S")
    return (id, mob_name, timestamp_string)

# This is so that we can return dates in a more readable format to the users.
def convert_date_times(rows: list) -> list:
    # We need to create a new array, iterate over the rows and return a new list
    results = []
    for row in rows:
        id = row[0]
        mob_name = row[1]
        date = row[2]
        timestamp_object = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
        timestamp_string = timestamp_object.strftime("%a %b %d %H:%M")
        results.append((id, mob_name, timestamp_string))
    return results

# This is for converting the input /add_mob_death datetime string into what the database actually wants.
def convert_add_mob_death_datetime(death_time: str):
    parts = death_time.split('/')
    month = int(parts[0])
    day = int(parts[1])
    year = int(parts[2])
    time_parts = parts[3].split(':')
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    
    if year < 100:
        year += 2000
    
    dt = datetime(year, month, day, hour, minute)
    
    formatted_str = dt.strftime('%a %b %d %H:%M:%S %Y')
    return formatted_str

def is_mob_spawn_due(mob_name: str, death_time: str):
    respawn_time = calculate_respawn_time(mob_name, death_time)
    current_time = datetime.now()
    respawn_time_obj = datetime.strptime(respawn_time, '%a %b %d %H:%M:%S %Y')
    respawn_time_str = respawn_time_obj.strftime("%a %b %d %H:%M")
    if current_time < respawn_time_obj:
        return respawn_time_str
    else:
        return None
    


