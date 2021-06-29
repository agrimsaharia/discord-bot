import os
import asyncio
import discord
import time
import my_apis as api

intro_message = 'Hey guys! I am your friend Ami and i am designed to make your day better. Here are somethings I can ' \
                'do ... '

feedback = ['Good --> 1', 'Bad --> 2']

goodbyes = ['See ya later, alligator!', 'Ciao! Ciao!', 'Bye Guys!']

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


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

    if msg == 'ami?':
        await channel.send(intro_message)

    # greet our bot
    elif msg.startswith('hello ami'):
        await channel.send('Hello! ' + message.author.name)

    elif msg.startswith('anyone there?'):
        time.sleep(3)
        online_members = []
        for member in channel.members:
            if member.status == discord.Status.online and (
                    not member.bot) and member != message.author:
                online_members.append(member.display_name)

        if len(online_members) == 0:
            await channel.send('No one\'s here i suppose')
        else:
            await channel.send(
                'These folks are online: ' + ', '.join(online_members) +
                "\nAnd of course there is me for you, forever!")

    # get dad_joke from api file and reply based on the feedback given
    elif msg.startswith('ami dad joke'):
        joke_body = api.get_dad_joke()
        await channel.send(joke_body['setup'])
        time.sleep(3)
        await channel.send(joke_body['punchline'])
        time.sleep(2)
        await channel.send("How was the joke!?\n" + '\n'.join(feedback))

        def check(m):
            return m.author != client.user and m.channel == channel

        try:
            reply = await client.wait_for('message', timeout=10.0, check=check)
            if reply.content == '1':
                await channel.send("Thanks dude!")
            elif reply.content == '2':
                await channel.send(
                    f"I'll get better, thanks for responding {reply.author.name}"
                )
        except asyncio.TimeoutError:
            await channel.send("No one is responding? I feel so lonely now")

    # get yo_momma_joke
    elif msg.startswith(f'{mention} yo momma') or msg.startswith('ami yo momma'):
        await channel.send(message.author.mention + ' ' +
                           api.get_yo_momma_joke())

    # get insults
    elif msg.startswith('ami insult'):
        if len(mentions) == 1:
            await channel.send(mentions[0].mention + ' ' +
                               api.get_evil_insult())
        elif len(mentions) > 1:
            await channel.send(
                "I don't like to roast multiple people at once, give me only one mention!"
            )
        else:
            await channel.send(api.get_evil_insult())

client.run(os.getenv('TOKEN'))
