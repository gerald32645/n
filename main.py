import discord
import os
import asyncio
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Replace 'YOUR_GUILD_ID' with the ID of the guild you want to send the message in
guild_id = 1131985734312661115

# Replace 'YOUR_CHANNEL_ID' with the ID of the channel you want to send the message in
channel_id = 1131985734761459803

# The specific message you want to send and delete
specific_message = "lol"

is_messaging = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.content.startswith('!start'):
        global is_messaging
        if not is_messaging:
            is_messaging = True
            await send_and_delete_specific_message(message.channel)

    await bot.process_commands(message)

async def send_and_delete_specific_message(channel):
    guild = bot.get_guild(guild_id)
    if not guild:
        print(f"Guild with ID {guild_id} not found.")
        return

    target_channel = guild.get_channel(channel_id)
    if not target_channel:
        print(f"Channel with ID {channel_id} not found.")
        return

    while is_messaging:
        try:
            message = await target_channel.send(specific_message)
            await message.delete()
            await asyncio.sleep(1)  # SECONDS TO WAIT BETWEEN EACH MESSAGE
        except discord.HTTPException as e:
            if e.code == 429:
                retry_after = e.retry_after
                print(f"Hit rate limit, try again in {retry_after:.2f} seconds.")
                await asyncio.sleep(retry_after)
            else:
                print(f"HTTP Exception: {e}")
        except discord.Forbidden as e:
            print(f"Forbidden: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Start the bot
bot.run(os.environ['TOKEN'])
keep_alive()
