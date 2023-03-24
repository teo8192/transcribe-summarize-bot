import os

import discord
from discord.ext import commands
import discord.sinks

from datetime import datetime

import config
import speech_recognition as sr
import text_analytics as ta

file_directory = "recordings"
os.makedirs(file_directory, exist_ok=True)

description = 'A bot that transcribes voice channels.'
bot_prefix = "!"

intents = discord.Intents.default()

# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=bot_prefix)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command(pass_context=True, name="start", help="Starts audio recording.")
async def start_record(ctx):
    await ctx.author.voice.channel.connect() # Connect to the voice channel of the author
    ctx.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, ctx) # Start the recording
    await ctx.channel.send("Recording...")

async def finished_callback(sink, ctx):
    # Here you can access the recorded files:
    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]

    time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    for user_id, audio in sink.audio_data.items():
        filename = f"{user_id}-{time}.{sink.encoding}"
        with open(os.path.join(file_directory, filename), "wb") as f:
            f.write(audio.file.read())
        text = sr.recognize_from_file(os.path.join(file_directory, filename))
        joined_text = "\n".join(text)
        await ctx.channel.send(f"Transcribed text for {user_id}: {joined_text}")
        summary = ta.summarize_text(text)
        joined_summary = "\n".join(summary)
        await ctx.channel.send(f"Summary for {user_id}: {joined_summary}")

    await ctx.channel.send(f"Finished! Recorded audio for {', '.join(recorded_users)}.", files=files)
    await ctx.voice_client.disconnect() # Disconnect from the voice channel

@bot.command(pass_context=True, name="stop", help="Stops the recording.")
async def stop_recording(ctx):
    ctx.voice_client.stop_recording() # Stop the recording, finished_callback will shortly after be called
    await ctx.channel.send("Stopped!")
# client.run(TOKEN)
bot.run(config.TOKEN)
