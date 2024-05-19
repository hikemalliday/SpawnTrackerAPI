from bot_instance import bot
from datetime import datetime
import sqlite3
from config import DB_PATH
from datetime import datetime
from helper2 import calculate_respawn_time

def insert_mob_spawn(fields: tuple):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        query = '''SELECT * FROM mob_spawn WHERE spawn_time = ? AND mob_zone = ?'''
        c.execute(query, fields)
        row = c.fetchone()
        print(f"row: {row}")
        if row:
            print("mob entry already exists, abort")
            return
        # mob_name, mob_spawn, mob_zone
        insert = '''INSERT INTO mob_spawn (spawn_time, mob_zone)
                VALUES (?, ?)
    '''
        c.execute(insert, fields)
        conn.commit()
        print("SUCCESS: Inserted mob_spawn")
        return True
    except Exception as e:
        print("ERROR: Could not insert mob_spawn")
        print(str(e))
        return False
    finally:
        conn.close()

# TODO: We will be deleteing this, we no longer will use the spawn calender table
def insert_spawn_calendar_row(mob_name: str, respawn_time: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        spawn_calendar_query = '''INSERT INTO spawn_calendar (mob_name, mob_respawn) VALUES(?, ?)'''
        c.execute(spawn_calendar_query, (mob_name, respawn_time))
        conn.commit()
    except Exception as e:
        print("ERROR: Could not insert mob_calendar")
        print(str(e))

def delete_spawn_calender():
    pass

def insert_mob_death(fields: tuple):
    try:
        death_time = fields[0]
        mob_name = fields[1]
        respawn_time = calculate_respawn_time(mob_name, death_time)
        #time_stamp = datetime.strptime(death_time, "%a %b %d %H:%M:%S %Y")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if row exists. If so, abort.
        query = '''SELECT * FROM mob_death WHERE death_time = ? AND mob_name = ?'''
        c.execute(query, (death_time, mob_name))
        row = c.fetchone()
        if row:
            print("mob entry already exists, abort")
            return
        insert = '''INSERT INTO mob_death (death_time, mob_name, respawn_time)
                VALUES (?, ?, ?)
        '''
        c.execute(insert, (death_time, mob_name, respawn_time))
        conn.commit()
        return True
    except Exception as e:
        print("ERROR: Could not insert mob_death")
        print(str(e))
        return False
    finally:
        conn.close()

# TODO: DESECRATED
def remove_spawned_rows():
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c = bot.db_connection.cursor()

        # Fetch rows where mob_respawn is in the past
        c.execute("SELECT id FROM spawn_calendar WHERE mob_respawn < ?", (current_time,))
        rows_to_delete = c.fetchall()

        # Delete rows where mob_respawn is in the past
        for row in rows_to_delete:
            c.execute("DELETE FROM spawn_calendar WHERE id = ?", row)
        
        bot.db_connection.commit()
        print("Expired entries removed successfully.")
        return True
    except Exception as e:
        print("Error removing expired entries:", e)
        return False
    
# TODO: DESEECRATED
# Re-name ot get_spawn_calender
def get_spawn_calendar():
    try:
        calendar = []
        current_time = datetime.now()
        c = bot.db_connection.cursor()
        c.execute('''SELECT * FROM mob_death ORDER BY respawn_time''')
        results = c.fetchall()
        print("get_spawn_calendar_rows.results:")
        print(results)
        if results:
            for result in results:
                id = result[0]
                mob_name = result[1]
                respawn_time = result[3]
                respawn_time_obj = datetime.strptime(result[3], '%a %b %d %H:%M:%S %Y')  # convert respawn_time to datetime
                if current_time < respawn_time_obj:
                    calendar.append((id, mob_name, respawn_time))
            print(calendar)
            return calendar
    except Exception as e:
        print("Error getting spawn_calendar rows:", e)

def get_mob_spawn_row(mob_death: int):
    try:
        c = bot.db_connection.cursor()
        c.execute('''SELECT * FROM mob_death WHERE id = ?''', (mob_death,))
        result = c.fetchall()
        row = result[0]
        if row:
            print(f"mob_death row found: {row}")
            return row
        else:
            print(f"Could not find mob_death row id: {mob_death}")
    except Exception as e:
        print(str(e))
        return str(e)
    
def delete_mob_death_by_id(mob_death: int):
     try:
        c = bot.db_connection.cursor()
        c.execute('''DELETE FROM mob_death WHERE id = ?''', (mob_death,))
        bot.db_connection.commit()
     except Exception as e:
        print(str(e))
        return str(e)
     
async def fetch_mob_names(mob_name: str):
    try:
        like_pattern = f'{mob_name}%'
        conn = bot.db_connection
        c = conn.cursor()
        c.execute(f'''
                SELECT mob_name FROM mob_master WHERE mob_name LIKE ?
                ''', 
                (like_pattern,))
        conn.commit()
        results = c.fetchall()
        if results:
            results = [result[0] for result in results]
            return results
        else:
            print(f'No mob names found for {mob_name}.')
            return None
    except Exception as e:
        print('fetch_mob_names error:', str(e))
        return str(e)
        
