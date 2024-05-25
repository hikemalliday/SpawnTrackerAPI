from bot_instance import bot
from datetime import datetime
import sqlite3
from config import DB_PATH
from datetime import datetime
from helper2 import calculate_respawn_time

def insert_mob_spawn(payload: tuple):
    try:
        spawn_time = payload[0]
        mob_zone = payload[1]
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        query = '''SELECT * FROM mob_spawn WHERE spawn_time = ? AND mob_zone = ?'''
        c.execute(query, (spawn_time, mob_zone))
        row = c.fetchone()
        if row:
            print("mob entry already exists, abort")
            return
        # mob_name, mob_spawn, mob_zone
        insert = '''INSERT INTO mob_spawn (spawn_time, mob_zone)
                VALUES (?, ?)
    '''
        c.execute(insert, (spawn_time, mob_zone))
        conn.commit()
        print("SUCCESS: Inserted mob_spawn")
        return True
    except Exception as e:
        print("ERROR: Could not insert mob_spawn")
        print(str(e))
        return False
    finally:
        conn.close()

def insert_mob_death(payload: tuple):
    try:
        death_time = payload[0]
        mob_name = payload[1]
        if death_time is None:
            death_time = datetime.now().strftime('%m/%d/%y/%H:%M')
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

def get_spawn_calendar():
    try:
        calendar = []
        current_time = datetime.now()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''SELECT * FROM mob_death ORDER BY respawn_time''')
        results = c.fetchall()
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
    finally:
        conn.close()

# Used for deleting a mob_spawn
# The discord interface selects a row to delete based on ID, therefor 
# we
def get_mob_spawn_row(mob_death: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
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
    finally:
        conn.close()
    
def delete_mob_death_by_id(mob_death: int):
     try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''DELETE FROM mob_death WHERE id = ?''', (mob_death,))
        conn.commit()
     except Exception as e:
        print(str(e))
        return str(e)
     finally:
        conn.close()





# NOTE: Used to help add_mob_death
async def fetch_mob_names_master(mob_name: str):
    try:
        like_pattern = f'{mob_name}%'
        conn = sqlite3.connect(DB_PATH)
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
    finally:
        conn.close()

        
