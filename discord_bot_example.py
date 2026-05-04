import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'logged as {self.user}')
    async def on_message(self,message):
        print(f'{message.author} said {message.content}')
intents=discord.Intents.default()
intents.message_content=True    
client=Client(intents=intents)
client.run("")
