import discord
from discord.ext import commands
class Loger(commands.Cog):

    def __init__(self,client):
        self.client = client

    def log_sent_message(self,message:discord.Message):
        with open("logs/logfile.txt","a") as logfile:
            logfile.write("Message Sent!\n")
            logfile.write(f"author:{message.author.name}\n")
            logfile.write(f"content:{message.content}\n")
            logfile.write(f"attatchments:{[x.url for x in message.attachments]}\n")
    
    def log_edit_message(self,before:discord.Message,after:discord.Message):
        with open("logs/logfile.txt","a") as logfile:
            logfile.write("Message Edited!\n")
            logfile.write(f"author:{before.author.name}\n")
            logfile.write(f"content before:{before.content}\n")
            logfile.write(f"content after:{after.content}\n")
            logfile.write(f"attatchments before:{[x.url for x in before.attachments]}\n")
            logfile.write(f"attatchments after:{[x.url for x in after.attachments]}\n")
    
    def log_delete_message(self,message:discord.Message):
        with open("logs/logfile.txt","a") as logfile:
            logfile.write("Message Deleted!\n")
            logfile.write(f"author:{message.author.name}\n")
            logfile.write(f"content:{message.content}\n")
            logfile.write(f"attatchments:{[x.url for x in message.attachments]}\n")
    
    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        self.log_sent_message(message)

    @commands.Cog.listener()
    async def on_message_edit(self,before:discord.Message,after:discord.Message):
        self.log_edit_message(before,after)
    
    @commands.Cog.listener()
    async def on_message_delete(self,message:discord.Message):
        self.log_delete_message(message)
