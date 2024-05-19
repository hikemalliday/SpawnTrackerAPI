from db_commands import get_spawn_calendar, get_mob_spawn_row, delete_mob_death_by_id, insert_mob_death
import helper
import helper2
from embed import delete_mob_death_embed, add_mob_death_embed

async def calendar():
    try:
        results = get_spawn_calendar()
        results = helper.convert_date_times(results)
        if results:
            return results
        else:
            return "No upcoming spawn windows."
    except Exception as e:
        print(str(e))
        return str(e)
    
async def add_mob_death(mob_name: str, death_time: str):
    try:
        formatted_str = helper.convert_add_mob_death_datetime(death_time)
        success = insert_mob_death((formatted_str, mob_name))
        respawn_time = helper2.calculate_respawn_time(mob_name, formatted_str)
        if success == True:
            return add_mob_death_embed([mob_name, formatted_str, respawn_time])
        else:
            return f"❌Error: Could not add mob death."
    except Exception as e:
        print(str(e))
        return str(e)
    
async def delete_mob_death(mob_death: int):
    try:
        # We take in the pk, now we need to delete the row from 'mob_death', then find the respawn row
        # by calculating mob_respawn, and then removing that row
        mob_death_row = get_mob_spawn_row(mob_death)
        delete_mob_death_by_id(mob_death)
        if mob_death_row:
            return delete_mob_death_embed(mob_death_row)
        else:
            return "❌Error: could not delete mob_death."
    except Exception as e:
        print(str(e))
        return str(e)
    

    
        

