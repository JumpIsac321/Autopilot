import discord
from discord.ext import commands

class Reactor(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if self.is_image(message) or self.is_tenor(message):
            if not "jonkler" in message.content:
                print("safe")
                await message.add_reaction("\U00002b06")
            await message.add_reaction("\U00002B07")
        #await self.client.process_commands(message)
    
    def is_tenor(self,message):
        return message.content.startswith("https://tenor.com")
    
    def is_image(self,message):
        extensions = [".jpg", ".jpeg", ".png", ".gif",".webp",".svg",".mp4",".mov"]
        for file in message.attachments:
            for extension in extensions:
                if file.filename.endswith(extension):
                    return True
