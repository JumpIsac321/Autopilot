from discord.ext import commands
from mysql.connector.abstracts import MySQLCursorAbstract
import sentence_generator

class Sentence(commands.Cog):
    def __init__(self,client,mydb,mycursor:MySQLCursorAbstract):
        self.client = client
        self.mydb = mydb
        self.mycursor = mycursor
    
    @commands.command()
    async def add(self,ctx, word:str, *word_type_list:str):
        if (not word.isalpha):
            await ctx.send("Must contain only letters")
            return
        parse_result = self.parse_word_type(word_type_list)
        if parse_result != None:
            (query_type,query_hasobject) = parse_result
        else:
            await ctx.send("Wrong!!!")
            return
        if (self.mycursor == None or self.mydb == None):
            return
        self.mycursor.execute("SELECT * FROM Words WHERE content = %s AND type = %s AND hasobject = %s",(word,query_type,query_hasobject))
        if len(self.mycursor.fetchall()):
            await ctx.send("Word already exists")
            return
        self.mycursor.execute("INSERT INTO Words (content,type,hasobject) VALUES (%s,%s,%s)",(word,query_type,query_hasobject))
        self.mydb.commit();
    
    @commands.command()
    async def addproper(self,ctx,*words):
        proper_noun = ""
        for word in words:
            proper_noun += word
            proper_noun += " "
        proper_noun = proper_noun.rstrip()
        if (self.mycursor != None and self.mydb != None):
            self.mycursor.execute("SELECT * FROM Words WHERE content = %s AND type = \"proper_noun\" AND hasobject = %s",(proper_noun,False))
            if len(self.mycursor.fetchall()):
                await ctx.send("Word already exists")
                return
            self.mycursor.execute("INSERT INTO Words (content,type,hasobject) VALUES (%s,\"proper_noun\",%s)",(proper_noun,False))
            self.mydb.commit();
        else:
            print("What have you done?")
    
    
    
    def parse_word_type(self,word_type_list):
        if (len(word_type_list) < 1 or len(word_type_list) > 3):
            return None
        parts_of_speech = ["noun","verb","adjective","adverb","interjection"]
        single_parts_of_speech = ["adjective","adverb","interjection"]
        tenses = ["plural","past","present"]
        correct_query_types = ["plain_noun","plural_noun","plain_verb","plural_verb","past_verb","present_verb"]
        part_of_speech = None
        tense = "plain"
        hasobject = False
        for modifier in word_type_list:
            if modifier in parts_of_speech:
                parts_of_speech = modifier
            elif modifier in tenses and tense == "plain":
                tense = modifier
            elif modifier == "object" and hasobject == False:
                hasobject = True
            else:
                return None
        if part_of_speech in single_parts_of_speech:
            return part_of_speech
        query_type = f"{tense}_{part_of_speech}"
        if not query_type in correct_query_types:
            return None
        return (query_type,hasobject)
        
    @commands.command()
    async def talk(self,ctx):
        sentence_generator.fetch_words()
        await ctx.send(sentence_generator.create_sentence())
    
    @commands.command()
    async def words(self,ctx):
        if self.mycursor == None:
            return
        self.mycursor.execute("SELECT (content) FROM Words")
        all_words = ""
        for word in self.mycursor.fetchall():
            all_words += str(tuple(word)[0])
            all_words += "\n"
        await ctx.send(all_words.lstrip())
