from os import name
import discord
import aiohttp
import requests
from discord_components import*
from discord import flags
from discord.ext import commands, tasks

client = commands.Bot(command_prefix=commands.when_mentioned_or('.'))
client.remove_command('help')

aopdkey = "AOPDKEY"

@client.command()
async def apod(ctx):
    client.ses = aiohttp.ClientSession()
    url = f'https://api.nasa.gov/planetary/apod?api_key={aopdkey}'
    async with client.ses.get(url) as r:
        if r.status in range(200, 299):
            data = await r.json()
            url = data['url']
            imgtitle = data['title']
            imgdate = data['date']
            explanation = data['explanation']
            ogimg = data['hdurl']
            credit = data['copyright']
            embed = discord.Embed(
                title='🌠 Astronomy Picture Of The Day',
                description=f'**Date -** {imgdate}', color = 000000, timestamp=ctx.message.created_at).set_image(
                url=url).add_field(name=imgtitle, 
                value=f'**Explaination - **\n{explanation}').add_field(name='Original Image -',
                value=f'[Click Here]({ogimg})',inline=False).add_field(name='Image Credit & Copyright -',
                value=credit).set_footer(text="Requested by: {}".format(ctx.author.display_name))
            await ctx.send(embed=embed, 
                        components=[
                            Button(style=ButtonStyle.URL, label='View in browser', url='https://apod.nasa.gov/apod/astropix.html')
                            ],
                            
                        )
           
@client.event
async def on_ready():
    DiscordComponents(client)
    
    print(f'{client.user} has connected to Discord!')

client.run('BOT-TOKEN')
