import discord
from discord.ext import commands, tasks
from mysql.connector.abstracts import MySQLCursorAbstract
import time

class Economy(commands.Cog):
    
    def __init__(self,client:commands.Bot,mydb,mycursor:MySQLCursorAbstract):
        self.client = client
        self.mydb = mydb
        self.mycursor = mycursor

    async def check_admin(self,ctx:commands.Context,name:str) -> bool:
        admins=["jumpisac321","0dinballz","someonenamedabhi"]
        if not name in admins:
            await ctx.send("Wrong!!!")
            return True
        return False

    def add_money(self,username:str,amount:int):
        self.mycursor.execute("UPDATE Members SET money = money + %s WHERE name = %s",(amount,username))
        self.mydb.commit()

    def set_money(self,username:str,amount:int):
        self.mycursor.execute("UPDATE Members SET money = %s WHERE name = %s",(amount,username))
        self.mydb.commit()

    def get_money_and_id(self,username:str):
        self.mycursor.execute("SELECT (id,money) FROM Members WHERE name = %s",(username,))
        return self.mycursor.fetchone()
    
    def add_item(self,username:str,item:str,amount:int):
        self.mycursor.execute("SELECT id FROM Members WHERE name = %s",(username,))
        other_id_raw = self.mycursor.fetchone()
        if other_id_raw == None:
            return
        other_id = str(tuple(other_id_raw)[0])
        self.mycursor.execute("SELECT id FROM Items WHERE name = %s AND user_id = %s",(item,other_id))
        if self.mycursor.fetchone() == None:
            self.mycursor.execute("INSERT INTO Items (name,amount,user_id) VALUES (%s,%s,%s)",(item,amount,other_id))
        else:
            self.mycursor.execute("UPDATE Items SET amount = amount + %s WHERE name = %s",(amount,item))
        self.mydb.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        self.mycursor.execute("SELECT name FROM Members")
        database_members = [str(member) for (member,) in self.mycursor.fetchall()]
        guild = self.client.get_guild(1269805832145600533)
        if guild == None:
            return
        real_members = [member.name for member in guild.members if not member.bot]
        members_to_add = [(member,) for member in real_members if not member in database_members]
        members_to_remove = [(str(member),) for member in database_members if not member in real_members]
        self.mycursor.executemany("INSERT INTO Members (name,money) VALUES (%s,100)",members_to_add)
        self.mycursor.executemany("DELETE FROM Members WHERE name = %s",members_to_remove)
        self.mydb.commit()

    @commands.command()
    async def give(self,ctx:commands.Context,other:discord.User,amount:int):
        if amount < 0:
            await ctx.send("You can't give negative money")
            return
        self.add_money(other.name,amount)
        self.add_money(ctx.author.name,amount)
        await ctx.send(f"You gave {other.name} {amount} {self.abhiorabhis(amount)}")

    @commands.command()
    async def balance(self,ctx:commands.Context,other:discord.User|None=None):
        if self.mycursor == None:
            return
        if other == None:
            amount_raw = self.get_money_and_id(ctx.author.name)
            if amount_raw == None:
                return
            amount = tuple(amount_raw)[1]
            await ctx.send(f"You have {amount} {self.abhiorabhis(amount)}!!!")
        else:
            amount_raw = self.get_money_and_id(other.name)
            if amount_raw == None:
                return
            amount = tuple(amount_raw)[1]
            await ctx.send(f"{other.name} has {amount} {self.abhiorabhis(amount)}!!!")

    def abhiorabhis(self,amount):
        if amount == 1:
            return "abhi"
        else:
            return "abhis"
    
    @commands.command()
    async def addmoney(self,ctx:commands.Context,other:discord.User,amount:int):
        if amount < 0:
            await ctx.send("You can't add negative money")
            return
        if self.check_admin(ctx,ctx.author.name):
            return
        self.add_money(other.name,amount)
        await ctx.send(f"{other.name} got {amount} {self.abhiorabhis(amount)}")
        
    @commands.command()
    async def removemoney(self,ctx:commands.Context,other:discord.User,amount:int):
        if amount < 0:
            await ctx.send("You can't remove negative money")
            return
        if self.check_admin(ctx,ctx.author.name):
            return
        self.add_money(other.name,-amount)
        await ctx.send(f"{other.name} lost {amount} {self.abhiorabhis(amount)}")

    @commands.command()
    async def setmoney(self,ctx:commands.Context,other:discord.User,amount:int):
        if self.check_admin(ctx,ctx.author.name):
            return
        self.set_money(other.name,amount)
        await ctx.send(f"{other.name} got {amount} {self.abhiorabhis(amount)}")

    @commands.command()
    async def giveitem(self,ctx:commands.Context,other:discord.User,item:str,amount:int):
        if self.check_admin(ctx,ctx.author.name):
            return
        self.add_item(other.name,item,amount)

    @commands.command()
    async def chop(self,ctx:commands.Context):
        self.action("chop",ctx.author.name)
        print("chop chop")

    def action(self,action:str,username:str):
        print("here")
        print(action)
        print(username)
        time_dict = {
            "chop": 30,
            "mine": 30,
            "furnace": 30,
            "shear": 30,
            "harvest": 30,
        }
        task_time = 1
        self.mycursor.execute("UPDATE Members SET task_name = %s, task_time = %s WHERE name = %s",(action,time.time()+task_time*60,username))

    @commands.Cog.listener()
    async def on_member_join(self,member):
        self.mycursor.execute("INSERT INTO Members (name,money) VALUES (%s,100)",member.name)
        self.mydb.commit()
    
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        self.mycursor.execute("DELETE FROM Members WHERE name = %s",member.name)
        self.mydb.commit()
    @tasks.loop(minutes=1)
    async def check_tasks(self):
        action_dict = {
            "chop": ("log",50),
            "mine": ("ore",10),
            "furnace": ("brick",20),
            "shear": ("wool",30),
            "harvest": ("wheat",100)
        }
        self.mycursor.execute("SELECT (name,task_name,task_time) FROM Members")
        for (name,task_name,task_time) in self.mycursor.fetchall():
            if int(str(task_time)) > int(time.time()):
                (resource,amount) = action_dict[str(task_name)]
                self.add_item(str(name),resource,amount)
                self.mycursor.execute("UPDATE Members SET task_name = NULL, task_time = NULL")
                main_channel = self.client.get_channel(1270475474820399276)
                main_channel.send(f"{name} got {amount} {resource}s")
