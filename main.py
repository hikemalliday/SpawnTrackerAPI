from fastapi import FastAPI
from bot_instance import bot
from db_connection import DatabaseConnection
import bot_commands_interface as bot_commands
from config import BOT_TOKEN, DB_PATH
import uvicorn
import asyncio
from api_interface import router as api_router
import ssl
from tables import create_tables
from calendar_alerts import calendar_alerts

# # SSL
# ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# ssl_context.load_cert_chain('./cert.pem', './key.pem')

app = FastAPI()

async def run_discord_bot():
    try:
        create_tables()
        @bot.event
        async def on_ready():
            print("on_ready")
            try:
                for command in bot_commands.slash_commands:
                    bot.tree.add_command(command)
                    print(f'Adding command: {command.name}')
                synced = await bot.tree.sync()
                print(f'Synced {len(synced)} command(s)')
            except Exception as e:
                print(e)
        await bot.start(BOT_TOKEN)
    finally:
        print("bot launch finally block")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_discord_bot())
    asyncio.create_task(calendar_alerts())

app.include_router(api_router)

if __name__ == "__main__":
    print("main block")
    uvicorn.run(
        app,
        host="127.0.0.1",  
        port=8000
    )