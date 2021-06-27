import os
import asyncio
import discord
import time
import my_apis as api
from alive import keep_alive

intro_message = 'Discordwasiyo! Mai pappu hu\nseedhi baat kahu to mai bakwaas karne ke liye bana hu\nkuch commands se mai trigger hota hu\n\nMere se Hello sunke khudko meri tarah V.I.P samajhna chahte ho... \nto pehle mujhe "hello pappu" bolna padega\n\nMai dad jokes maar leta hu... roj mummy se seekhta hu\nJoke sunna hai to bolo --> "pappu joke suna"\n(waise mujhe pasand nahi agar tum mere jokes pe feedback na do to)\n\nKoi aapko attention dena pasand karta hai ya nahi(basically kaun kaun online hai) \njaanne ke liye dabaayein --> "koi hai?"\n\nLogo ki beizzati karna to pasand hai hi aapko, wo seva me bhi mai uplabdh hu...\nkisi chutiye ko insult karne ke liye --> "pappu insult" kehke mention kare\n\nmai apni mom ki bahut izzat karta hu, agar unpe "yo momma" waale joke maare to bahut pele jaoge\nhimmat hai to aajao!'

intro_to_be_updated = '\n...\n...\n...\n...\n...\nAccha accha theek hai...\nWaise to mai bahut charming hu, but mujhe kabhi alvida kehna ho to "bye pappu" kardena\nafterall mujhe bhi to aaraam chahiye hota hai!\naur modi ki bakwaas se pak jao to mujhe --> "aaja pappu" kehke bula lena!'

feedback = ['ghatiya --> 1', 'badiya --> 2']

goodbyes_italian = ['Arrivederci!', 'Ciao! Ciao!', 'Accha chalta hu... voting me yaad rakhna']

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    mention = f'<@!{client.user.id}>'
    mentions = message.mentions
    print(mentions)

    msg = message.content.lower()
    channel = message.channel

    if msg == 'pappu?':
        await channel.send(intro_message)

    # greet our bot
    elif msg.startswith('hello pappu'):
        await channel.send('Hello! ' + message.author.name)

    elif msg.startswith('koi hai?'):
        time.sleep(3)
        online_members = []
        for member in channel.members:
            if member.status == discord.Status.online and (not member.bot) and member != message.author:
                online_members.append(member.display_name)
        
        if len(online_members) == 0:
            await channel.send('sannata chha gaya hai...\npar mai hu na!')
        else:
            await channel.send(', '.join(online_members) + "\tye sab hai...\naur mai to hamesha hu hi is desh ki janta ke liye")

    # get dad_joke from api file and reply based on the feedback given
    elif msg.startswith('pappu joke suna'):
        joke_body = api.get_dad_joke()
        await channel.send(joke_body['setup'])
        time.sleep(3)
        await channel.send(joke_body['punchline'])
        time.sleep(2)
        await channel.send("Joke kaisa laga!?\n" + '\n'.join(feedback))
        
        def check(m):
            return m.author != client.user and m.channel == channel
        try:
            reply = await client.wait_for('message', timeout=10.0, check=check)
            if reply.content == '1':
                await channel.send("because you deserve stupid jokes my friend.\n{.author.name} Gaand mara!".format(reply))
            elif reply.content == '2':
                await channel.send("mummy ko batata hu khush ho jayengi!")
            else:
                await channel.send("itni jaldi kya hai\nek reply hi to maang raha tha, baad me chat karlete :unamused: ")
        except asyncio.TimeoutError:
            await channel.send("nikal liye kya?? kuch pucha tha maine!! :unamused:\nsaala koi seriously hi nahi leta mujhe!") 

    # get yo_momma_joke
    elif msg.startswith(f'{mention} yo momma') or msg.startswith('pappu yo momma') or msg.startswith(f'{mention}yo momma') or (msg.startswith('yo momma') and (client.user in mentions)):
        await channel.send(message.author.mention + ' ' + api.get_yo_momma_joke()) 
    
    # get insults
    elif msg.startswith('pappu insult'):
        if len(mentions) == 1:
            await channel.send(mentions[0].mention + ' ' + api.get_evil_insult())
        elif len(mentions) > 1:
            await channel.send("I don't like to roast multiple people at once, give me only one mention!")
        else:
            await channel.send(api.get_evil_insult())

    # # get rid of the bot
    # elif msg.startswith('bye pappu'):
    #     await channel.send(random.choice(goodbyes_italian))
    #     def check(m):
    #       return m.author != client.user and m.channel == channel and m.content.startswith('aaja pappu')
    #     await client.wait_for('message', check=check)
    #     await channel.send('bachna ae haseeno, lo mai aa gaya...!')

keep_alive()
client.run(os.getenv('TOKEN'))