from imageai.Detection import ObjectDetection
import discord
from discord.ext import commands
from bot_logic import gen_pass
import random
import os
import requests
intents = discord.Intents.default()
intents.message_content = True
ciekawostki=["♻️ Recykling jednej puszki oszczędza energię potrzebną do zasilania TV przez 3 godziny.",
    "♻️ Szkło można przetwarzać nieskończoną ilość razy.",
    "♻️ Papier powinien być czysty – tłusty papier nie nadaje się do recyklingu.",
    "♻️ Plastikowe butelki rozkładają się nawet 500 lat.",
    "♻️ Recykling aluminium oszczędza 95% energii."]
bot = commands.Bot(command_prefix='!', intents=intents)
#kaczki
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
#psy
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.event
async def on_ready():
    print(f'Zalogowaliśmy się jako {bot.user}')
@bot.command()
async def img(ctx):
    if len(ctx.message.attachments) == 1:
        await ctx.message.attachments[0].save('C:\\Users\\xtrol\\Desktop\\python\\bot\\obrazek.jpg')
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath("C:\\Users\\xtrol\\Desktop\\python\\bot\\yolov3.pt")
        detector.loadModel()

        detections = detector.detectObjectsFromImage(
            input_image="C:\\Users\\xtrol\\Desktop\\python\\bot\\obrazek.jpg", 
            output_image_path="C:\\Users\\xtrol\\Desktop\\python\\bot\\obrazek2.jpg", 
            minimum_percentage_probability=30)
        with open("C:\\Users\\xtrol\\Desktop\\python\\bot\\obrazek.jpg","rb") as f:
            picture = discord.file(f)
        await ctx.send(file=picture)
@bot.command()
async def hello(ctx): 
    await ctx.send(f'Cześć')

@bot.command()
async def mis(ctx):
    await ctx.send(f":bear:")
@bot.command()
async def slon(ctx):
    await ctx.send(f":elephant:")
@bot.command()
async def haslo(ctx):
    await ctx.send(gen_pass(10))
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
#
@bot.command()
async def joined(ctx, member: discord.Member):
    # Joined at can be None in very bizarre cases so just handle that as well
    if member.joined_at is None:
        await ctx.send(f'{member} has no join date.')
    else:
        await ctx.send(f'{member} joined {discord.utils.format_dt(member.joined_at)}')
#losowanie 
@bot.command()
async def losuj(ctx):
    x = random.randint(1,100000)
    await ctx.send(f"🎲 Wylosowana liczba: **{x}**")
#ruletka
@bot.command()
async def ruletka(ctx):
    r = random.randint(1, 3)
    if r==1:
        wynik = ':red_square:'
    elif r==2:
        wynik = ':black_large_square:'
    else:
        wynik = ':green_square:'
    await ctx.send(f"Wylosowałeś: {wynik}")
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)} ms")
#mem1
@bot.command()
async def mem(ctx):
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}', 'rb') as f:
            picture = discord.File(f)
    await ctx.send(file=picture)
#kaczuszki
@bot.command('duck')
async def duck(ctx):
    '''Po wywołaniu polecenia duck program wywołuje funkcję get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)
@bot.command('dog')
#pieski
async def dog(ctx):
    image_url = get_dog_image_url()
    await ctx.send(image_url)
#papier
@bot.command()
async def papier(ctx):
    await ctx.send("niebieski pojemnik")
#plastik
@bot.command()
async def plastik(ctx):
    await ctx.send("żółty pojemnik")
#szklo
@bot.command()
async def szklo(ctx):
    await ctx.send("zielonym pojemnik")
#biodegradalne
@bot.command()
async def zepsutejedzenie(ctx):
    await ctx.send("brązowy pojemnik")
#czyszczenie chatu
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount:int):
    msg = await ctx.send(f'🗑️ deleated {amount} messages')
    await ctx.channel.purge(limit=amount+1)
    await msg.delate(delay=3)
#ciekawostki
@bot.command()
async def eco(ctx):
    await ctx.send(random.choice(ciekawostki))
@bot.command()
async def segregacja(ctx,*,item:str):
    item = item.lower()
    if item in ["butelka plastikowa",'plastik','reklamówka']:
        await ctx.send('Plastik -> pojemnik  ŻÓŁTY')
    elif item in['papier', 'karton', "gazeta"]:
        await ctx.send('papier -> pojemnik niebieski')
    elif item in ["szkło","butelka szklana"]:
        await ctx.send("Szkło -> pojemnik ZIELONY") 

