from bot_instance import bot
import fixtures
from helper2 import calculate_respawn_time
import sqlite3
from config import DB_PATH


def create_config_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # drop_query = '''
        # DROP TABLE config
        # '''
        # c.execute(drop_query)
        # bot.db_connection.commit()
        create = '''
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            char_name TEXT NOT NULL,
            eq_dir TEXT NOT NULL,
            server TEXT NOT NULL
        )
        '''

        c.execute(create)
        conn.commit()
        print("config table created.")

        c.execute("SELECT COUNT(*) FROM config")
        count = c.fetchone()[0]

        # If the table is empty, insert a default row
        if count == 0:
            default_values = ('Fullstack', 'C:/RoT/', 'RoT')
            c.execute("INSERT INTO config (char_name, eq_dir, server) VALUES (?, ?, ?)", default_values)
            print("Default row inserted.")
    except Exception as e:
        print(str(e))
        return str(e)
    finally:
        conn.close()

def create_mob_death_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # drop_query = '''
        # DROP TABLE mob_death
        # '''
        # c.execute(drop_query)
        # bot.db_connection.commit()
        create = '''
        CREATE TABLE IF NOT EXISTS mob_death (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mob_name TEXT NOT NULL,
            death_time TEXT NOT NULL,
            respawn_time TEXT NOT NULL
        )
        '''
        c.execute(create)
        conn.commit()

        c.execute('''SELECT * FROM mob_death''')
        rows = c.fetchall()
        if len(rows) == 0:
            insert_query = '''INSERT INTO mob_death (mob_name, death_time, respawn_time) VALUES (?, ?, ?)'''
            data_to_insert = []
            for mob_death in fixtures.mob_deaths:
                mob_name = mob_death[0]
                death_time = mob_death[1]
                respawn_time = calculate_respawn_time(mob_name, death_time)
                row = (mob_name, death_time, respawn_time)
                data_to_insert.append(row)
            c.executemany(insert_query, data_to_insert)
            conn.commit()
            print("Fixture data inserted into mob_death table.")
    except Exception as e:
        print(str(e))
        return str(e)
    finally:
        conn.close()

def create_mob_spawn_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        drop_query = '''
        DROP TABLE mob_spawn
        '''
        c.execute(drop_query)
        conn.commit()
        query = '''
        CREATE TABLE IF NOT EXISTS mob_spawn (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spawn_time TEXT NOT NULL,
            mob_zone TEXT NOT NULL
        )
        '''

        c.execute(query)
        conn.commit()
        print("mob_spawn table created.")
    except Exception as e:
        print(str(e))
        return str(e)
    finally:
        conn.close()
    
def create_mob_master():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        drop_query = '''
        DROP TABLE mob_master
        '''
        c.execute(drop_query)
        conn.commit()
        create = '''
        CREATE TABLE IF NOT EXISTS mob_master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mob_name TEXT NOT NULL,
            respawn_timer NUMBER,
            variance NUMBER
        )
        '''
        c.execute(create)
        conn.commit()
        print("mob_master table created.")
        # If table is newly created, insert
        select = '''SELECT * FROM mob_master'''
        c.execute(select)
        rows = c.fetchall()
        if len(rows) == 0:

            insert = '''
                INSERT INTO mob_master (mob_name, respawn_timer, variance)
                VALUES (?, ?, ?)
            '''
            c.executemany(insert, fixtures.mob_master)  
            conn.commit()
            print("mob_master inserts performed.")
    except Exception as e:
        print(str(e))
        return str(e)
    finally:
        conn.close()

def create_tables():
    create_config_table()
    create_mob_death_table()
    create_mob_spawn_table()
    create_mob_master()
