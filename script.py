import pyautogui
import discord
from discord.ext import commands
from dotenv import load_dotenv 
import cv2
import numpy as np

import os
import asyncio
import time

load_dotenv("./GuiAutomation/secrets.env") #if inside the root dir
load_dotenv("./secrets.env") #if inside the project dir

PHONE_NUMBER = os.getenv("BARRIER_PHONE_NUMBER")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

PHONE_LINK_ICON = (1174, 1040) #change with your 
CALL_BUTTON = (1664, 882)
MINIMIZE_WINDOW = (1803, 19)

#debug videos
MEDIA_FOLDER = "media"
os.makedirs(MEDIA_FOLDER, exist_ok=True)
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
FOURCC = cv2.VideoWriter_fourcc(*"XVID") #type format
FPS = 24.0
LAST_DEBUG_VIDEO="debug.avi"
FILENAME = os.path.join(MEDIA_FOLDER, LAST_DEBUG_VIDEO)
recording_event = asyncio.Event()

# Intents to access member and message events
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)


class FeedbackView(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.user = user

    @discord.ui.button(label="✅ Success", style=discord.ButtonStyle.green)
    async def success_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            await interaction.response.send_message("Thanks for confirming success!", ephemeral=True)
            self.stop()
        else:
            await interaction.response.send_message("Only the requestor can submit feedback!", ephemeral=True)

    @discord.ui.button(label="❌ Failure", style=discord.ButtonStyle.red)
    async def failure_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            await interaction.response.send_message("Please describe the issue in the debug channel!", ephemeral=True)
            
            debug_channel = discord.utils.get(interaction.guild.text_channels, name="debug")
            video_path = os.path.join(MEDIA_FOLDER, LAST_DEBUG_VIDEO)
            
            if debug_channel:
                if os.path.exists(video_path):
                    with open(video_path, "rb") as file:
                        await debug_channel.send(
                            content=f"{self.user.mention} reported a failure. Please check the video for details!",
                            file=discord.File(file, filename=LAST_DEBUG_VIDEO)
                        )
                else:
                    await debug_channel.send(f"{self.user.mention} reported a failure, but no debug video was found.")
            self.stop()
        else:
            await interaction.response.send_message("Only the requestor can submit feedback!", ephemeral=True)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name="general")  
    if welcome_channel:
        await welcome_channel.send(f"Welcome to the server, {member.mention}! 🎉 \nAny message sent in the general channel will trigger a barrier opening. If you encounter any troubles along with the application please write a descriptional message inside the debug channel!")
    print(f"{member.name} has joined the server!")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.name != "general":
        return
    
    #add a check for a list with untrusted/blacklisted users

    recording_event.clear()    
    asyncio.create_task(startRecording()) # background
    await asyncio.sleep(2)
    await asyncio.to_thread(callBarrier) # block the code to make photos

    print(f"{message.author.name}: {message.content}")

    view = FeedbackView(message.author)
    await message.channel.send(
        f"User {message.author.mention} triggered a barrier opening.\n"
        "If you encountered any issues, please report using the buttons below:",
        view=view
    )
    await bot.process_commands(message)
async def startRecording():
    print(f"Start Screen recording...")
    out = cv2.VideoWriter(FILENAME, FOURCC, FPS, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while not recording_event.is_set():  
        img = pyautogui.screenshot()  
        frame = np.array(img)  
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
        out.write(frame) 
        await asyncio.sleep(1 / FPS) #while command doesn t let the cpu be idle so we need a manual sleep

    out.release()  #media directory permission shouldn't be read-only
    print(f"Recording saved: {FILENAME}")

# PHONE LINK INTERACTION
# sleep pauses the execution for recording function to capture the actions
def callBarrier():
    print(f"Start gui automation")
    pyautogui.click(PHONE_LINK_ICON)
    time.sleep(2)
    pyautogui.write(PHONE_NUMBER, interval=0.1)
    time.sleep(2)
    pyautogui.click(CALL_BUTTON)
    time.sleep(5)
    pyautogui.click(MINIMIZE_WINDOW)
    print(f"Stop gui automation")
    # Stop recording after GUI automation finishes
    recording_event.set()
        
bot.run(TOKEN)
