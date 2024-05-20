import discord
from config import froak_icon

def mob_spawn_embed(zone_name: str, time_stamp: str) -> object:
    embed = discord.Embed(title='Mob has spawned', color=discord.Color.random())
    embed.set_thumbnail(url=f'{froak_icon}')
    embed.add_field(name='Zone', value=zone_name)
    embed.set_footer(text=time_stamp)
    return embed

def mob_death_embed(death_time: str, mob_name: str, respawn_time: str) -> object:
    embed = discord.Embed(title='Mob has died', color=discord.Color.random())
    embed.set_thumbnail(url=f'{froak_icon}')
    embed.add_field(name='Mob Name', value=mob_name)
    embed.add_field(name='Respawn Time', value=respawn_time)
    embed.set_footer(text=f"Died at: {death_time}")
    return embed

def calendar_embed(results: list) -> object:
    embed = discord.Embed(title='Spawn Calendar', color=discord.Color.random())
    for result in results:
         mob_name = result[1]
         mob_respawn = result[2]
         embed.add_field(name=mob_name, value=mob_respawn, inline=False)
    embed.set_footer(text=f"All times in CST")
    return embed

def delete_mob_death_embed(mob_death_row: list) -> object:
    embed = discord.Embed(title=f'Mob Death Deleted: {mob_death_row[1]}', color=discord.Color.random())
    embed.set_thumbnail(url=f'{froak_icon}')
    death_time = mob_death_row[2]
    respawn_time = mob_death_row[3]
    embed.add_field(name="Died at:", value=death_time, inline=False)
    embed.add_field(name="Spawned at:", value=respawn_time, inline=False)
    embed.set_footer(text="All times in CST")
    return embed

def add_mob_death_embed(add_mob_death: list) -> object:
    embed = discord.Embed(title=f'Mob Death Added: {add_mob_death[0]}', color=discord.Color.random())
    embed.set_thumbnail(url=f'{froak_icon}')
    death_time = add_mob_death[1]
    respawn_time = add_mob_death[2]
    embed.add_field(name="Died at:", value=death_time, inline=False)
    embed.add_field(name="Will spawn at:", value=respawn_time, inline=False)
    embed.set_footer(text="All times in CST")
    return embed