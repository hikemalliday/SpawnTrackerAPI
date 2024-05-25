import discord
import bot_commands_logic as logic
from discord import app_commands
import helper
from embed import calendar_embed
from datetime import datetime

@app_commands.command(name='calendar')
async def calendar(interaction: discord.Interaction):
    results = await logic.calendar()
    if type(results) == str:
        await interaction.response.send_message(results)
    else:
         await interaction.response.send_message(embed=calendar_embed(results))

@app_commands.command(name='add_mob_death')
@app_commands.describe(mob_name='Select mob name', death_time='Enter time of death')
async def add_mob_death(interaction: discord.Interaction, mob_name: str, death_time: str = None):
    if death_time is None:
        death_time = datetime.now().strftime('%m/%d/%y/%H:%M') 
    results = await logic.add_mob_death(mob_name, death_time)
    if type(results) == str:
        await interaction.response.send_message(results)
    else:
         await interaction.response.send_message(embed=results)

@add_mob_death.autocomplete('mob_name')
async def add_mob_death_autocomplete(interaction: discord.Interaction, current: str):
    return await helper.add_mob_death_autocomplete(interaction, current)

@app_commands.command(name='delete_mob_death')
@app_commands.describe(mob_death='Select mob death')
async def delete_mob_death(interaction: discord.Interaction, mob_death: int):
    results = await logic.delete_mob_death(mob_death)
    if type(results) == str:
        await interaction.response.send_message(results)
    else:
         await interaction.response.send_message(embed=results)

@delete_mob_death.autocomplete('mob_death')
async def delete_mob_death_autocomplete(interaction: discord.Interaction, current: str):
    return await helper.delete_mob_death_autocomplete(interaction, current)



slash_commands = [ calendar, add_mob_death, delete_mob_death ]