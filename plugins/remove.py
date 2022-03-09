import hikari
import tanjun
import spotipy
import sqlite3
import json
import requests
import asyncio
from hikari import InteractionCreateEvent
from hikari.interactions.base_interactions import ResponseType
from hikari.messages import ButtonStyle
from tanjun.abc import SlashContext

conn = sqlite3.connect('database.db')
c = conn.cursor()

#c.execute("""CREATE TABLE database (
#users_id integer,
#playlist_id BLOB,
#playlist_link BLOB)""")

component = tanjun.Component()


@component.with_command
@tanjun.as_slash_command("remove", f"Remove tracks from your playlist.")
async def interactive_post(
    ctx: SlashContext,
    bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot),
    client: tanjun.Client = tanjun.injected(type=tanjun.Client)
) -> None:
    get_token()
    spotifyObject = spotipy.Spotify(get_token.variable)
    id = ctx.author.id
    c.execute("SELECT * FROM database WHERE users_id = ?", (id,))
    temp = c.fetchall()
    if len(temp) == 0:
        embed = hikari.Embed(title="", colour=0x00ffd5,description="You need a Personal Playlist first to use this command. \nUse the `begin` command to create one.")
        await ctx.edit_initial_response(embed=embed)
    else:
        m = 0
        f = temp[0]
        g = str(f[1])
        b = []
        response = spotifyObject.playlist_items(playlist_id=g)
        while m < len(response['items']):
            track = response["items"][m]["track"]["name"]
            f = str(m)
            b.append(f"" + f + '.  ' + track)
            m = m + 1

        m = 0
        n = 10
        pages = []

        x = 100
        while x > len(b):
            x -= 10

        while n < x or n == x:
            page1 = hikari.Embed(title="Tracks", url="", description=f"The tracks are: \n \n" +"\n".join(map(str, b[m:n]))+"\n", color=0xff0000)
            pages.append(page1)
            m += 10
            n += 10

        page1 = hikari.Embed(title="Tracks", url="", description=f"The tracks are: \n \n" +"\n".join(map(str, b[x:len(b)+1]))+"\n", color=0xff0000)
        pages.append(page1)
        row = ctx.rest.build_action_row()
    (
        row.add_button(ButtonStyle.PRIMARY, "⬅️")
        .set_label("Back")
        .set_emoji("⬅️")
        .add_to_container()
    )
    (
        row.add_button(ButtonStyle.PRIMARY, "➡️")
        .set_label("Next")
        .set_emoji("➡️")
        .add_to_container()
    )

    row1 = ctx.rest.build_action_row()
    (
        row1.add_button(ButtonStyle.PRIMARY, "0️⃣")
        .set_label("")
        .set_emoji("0️⃣")
        .add_to_container()
    )
    (
        row1.add_button(ButtonStyle.PRIMARY, "1️⃣")
        .set_label("")
        .set_emoji("1️⃣")
        .add_to_container()
    )
    (
        row1.add_button(ButtonStyle.PRIMARY, "2️⃣")
        .set_label("")
        .set_emoji("2️⃣")
        .add_to_container()
    )
    (
        row1.add_button(ButtonStyle.PRIMARY, "3️⃣")
        .set_label("")
        .set_emoji("3️⃣")
        .add_to_container()
    )
    (
        row1.add_button(ButtonStyle.PRIMARY, "4️⃣")
        .set_label("")
        .set_emoji("4️⃣")
        .add_to_container()
    )
    
    row2 = ctx.rest.build_action_row()
    (
        row2.add_button(ButtonStyle.PRIMARY, "5️⃣")
        .set_label("")
        .set_emoji("5️⃣")
        .add_to_container()
    )
    (
        row2.add_button(ButtonStyle.PRIMARY, "6️⃣")
        .set_label("")
        .set_emoji("6️⃣")
        .add_to_container()
    )
    (
        row2.add_button(ButtonStyle.PRIMARY, "7️⃣")
        .set_label("")
        .set_emoji("7️⃣")
        .add_to_container()
    )
    (
        row2.add_button(ButtonStyle.PRIMARY, "8️⃣")
        .set_label("")
        .set_emoji("8️⃣")
        .add_to_container()
    )
    (
        row2.add_button(ButtonStyle.PRIMARY, "9️⃣")
        .set_label("")
        .set_emoji("9️⃣")
        .add_to_container()
    )

    await ctx.edit_initial_response(content="Type the track number to be removed", embed=pages[0], components=[row, row1, row2, ])
    i = 0
    r = 0

    try:
        with bot.stream(InteractionCreateEvent, timeout=60).filter(('interaction.user.id', ctx.author.id)) as stream:
            async for event in stream:
                await event.interaction.create_initial_response(ResponseType.DEFERRED_MESSAGE_UPDATE,)
                key = event.interaction.custom_id
                
                if key == "➡️":
                    if i==len(pages) - 1:
                        pass
                    else:
                        i = i + 1
                        await ctx.edit_initial_response(content="Type the track number to be removed.", embed=pages[i], components=[row, row1, row2])

                elif key == "⬅️":
                    if i==0:
                        pass
                    else:
                        i = i - 1
                        await ctx.edit_initial_response(content="Type the track number to be removed.", embed=pages[i], components=[row, row1, row2])

                elif key == "0️⃣":
                    r = 0
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(playlist_id=g, items=f)

                    embed = hikari.Embed(title="", colour=0x00ffd5,description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")
                
                elif key == "1️⃣":
                    r = 1
                    i = 10 * i
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(
                        playlist_id=g, items=f)

                    embed = hikari.Embed(
                        title="", colour=0x00ffd5, description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")
                
                elif key == "2️⃣":
                    r = 2
                    i = 10 * i
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(
                        playlist_id=g, items=f)

                    embed = hikari.Embed(
                        title="", colour=0x00ffd5, description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")
                
                elif key == "3️⃣":
                    r = 3
                    i = 10 * i
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(
                        playlist_id=g, items=f)

                    embed = hikari.Embed(
                        title="", colour=0x00ffd5, description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")

                elif key == "4️⃣":
                    r = 4
                    i = 10 * i
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(
                        playlist_id=g, items=f)

                    embed = hikari.Embed(
                        title="", colour=0x00ffd5, description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")

                elif key == "5️⃣":
                    r = 5
                    i = 10 * i
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(
                        playlist_id=g, items=f)

                    embed = hikari.Embed(
                        title="", colour=0x00ffd5, description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")

                elif key == "6️⃣":
                    r = 6
                    i = 10 * i
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(
                        playlist_id=g, items=f)

                    embed = hikari.Embed(
                        title="", colour=0x00ffd5, description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")

                elif key == "7️⃣":
                    r = 7
                    i = 10 * i
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(
                        playlist_id=g, items=f)

                    embed = hikari.Embed(
                        title="", colour=0x00ffd5, description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")

                elif key == "8️⃣":
                    r = 8
                    i = 10 * i
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(
                        playlist_id=g, items=f)

                    embed = hikari.Embed(
                        title="", colour=0x00ffd5, description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")

                elif key == "9️⃣":
                    r = 9
                    i = 10 * i
                    f = [response["items"][r+i]["track"]['uri']]
                    spotifyObject.playlist_remove_all_occurrences_of_items(
                        playlist_id=g, items=f)

                    embed = hikari.Embed(
                        title="", colour=0x00ffd5, description="Track Removed.")
                    await ctx.edit_initial_response(embed=embed, components=[], content="")

        with bot.stream(hikari.GuildMessageCreateEvent, timeout=60).filter(('author', ctx.author)) as stream:
            async for event in stream:
                var = event.content[:200]
                return

    except asyncio.TimeoutError:
        await ctx.edit_initial_response("Waited for 60 seconds... Timeout.", embed=None, components=[])

def get_token():
    headers = {'Authorization': 'Basic NWJjODIzMDI2M2EyNGI3NzhhYjQxMTRmN2EyMTVkMDY6YTM0ODU4YWUxZWNlNDE2MDg1MGQzOGE0NDEyYjNkOTg=', }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': "AQAIxWRAXRLsOuZ81K_MAMnR8qonzsouwG8hKzP1PnkYb4X0F3VfXIo_bzySMG7S2k4PMnxic15nyPOFMFj4V3Co3t6EAry_Rl6c6O_scw9-YEpJbiuUqSevZqMbCu63W1M",
    }

    response = requests.post(
        'https://accounts.spotify.com/api/token', headers=headers, data=data)

    x = json.loads(response.text)
    get_token.variable = x['access_token']


async def track(ctx: SlashContext, bot: hikari.GatewayBot, client: tanjun.Client):    
    try:
        with bot.stream(hikari.GuildMessageCreateEvent, timeout=60).filter(('author', ctx.author)) as stream:
            async for event in stream:
                track.variable = event.content[:200]
                return
    
    except asyncio.TimeoutError:
        await ctx.edit_initial_response("Waited for 60 seconds... Timeout.", embed=None, components=[])

@ tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
