import hikari
import tanjun
import spotipy
import sqlite3
import json
import requests
import asyncio

from hikari import InteractionCreateEvent, Mentions
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
@tanjun.with_member_slash_option("target", "Select whose playlist you wanna see", default=None)
@tanjun.as_slash_command("tracks", f"Look at the wonderful tracks you or your pal's have kept in their playlists.")
async def interactive_post(
    ctx: SlashContext, target: hikari.InteractionMember,
    bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot),
    client: tanjun.Client = tanjun.injected(type=tanjun.Client)
) -> None:
    get_token()
    spotifyObject = spotipy.Spotify(get_token.variable)
    if target:
        id = target.id
        c.execute("SELECT * FROM database WHERE users_id = ?", (id,))
        temp = c.fetchall()
        
        if len(temp) == 0:
            embed = hikari.Embed(title="Error", colour=0x00ffd5, description="Huh, looks like this person doesn't have own one personal playlist yet.")
            await ctx.edit_initial_response(embed=embed)
        
        else:
            m = 0
            f = temp[0]
            g = str(f[1])
            b = []
            response = spotifyObject.playlist_items(playlist_id=g)
            while m < len(response['items']):
                track = response["items"][m]["track"]["name"]
                m = m + 1
                f = str(m)
                b.append(f"" + f + '.  ' + track)

            m = 0
            n = 10
            pages = []

            x = 100
            while x > len(b):
                x -= 10

            while n < x or n == x:
                page1 = hikari.Embed(title="Tracks", url="", description=f"The tracks are: \n \n" +
                                    "\n".join(map(str, b[m:n]))+"\n", color=0xff0000)
                pages.append(page1)
                m += 10
                n += 10

            page1 = hikari.Embed(title="Tracks", url="", description=f"The tracks are: \n \n" +
                                "\n".join(map(str, b[x:len(b)+1]))+"\n", color=0xff0000)
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

            await ctx.edit_initial_response(embed=pages[0], components=[row, ])
            i = 0
            var = 0
            try:
                with bot.stream(InteractionCreateEvent, timeout=60).filter(('interaction.user.id', ctx.author.id)) as stream:
                    async for event in stream:
                        await event.interaction.create_initial_response(ResponseType.DEFERRED_MESSAGE_UPDATE,)
                        key = event.interaction.custom_id

                        if key == "➡️":
                            if i == len(pages) - 1:
                                pass
                            else:
                                i = i + 1

                        elif key == "⬅️":
                            if i == 0:
                                pass
                            else:
                                i = i - 1

                        await ctx.edit_initial_response(embed=pages[i], components=[row])

                with bot.stream(hikari.GuildMessageCreateEvent, timeout=60).filter(('author', ctx.author)) as stream:
                    async for event in stream:
                        var = event.content[:200]
                        return

            except asyncio.TimeoutError:
                await ctx.edit_initial_response("Waited for 60 seconds... Timeout.", embed=None, components=[])
    
    else:
        id = ctx.author.id
        c.execute("SELECT * FROM database WHERE users_id = ?", (id,))
        temp = c.fetchall()
        if len(temp) == 0:
            embed = hikari.Embed(title="Error", colour=0x00ffd5, description="Huh, looks like you don't have your own personal playlist yet.")
            await ctx.edit_initial_response(embed=embed)

        else:
            m = 0
            f = temp[0]
            g = str(f[1])
            b = []
            response = spotifyObject.playlist_items(playlist_id=g)
            while m < len(response['items']):
                track = response["items"][m]["track"]["name"]
                m = m + 1
                f = str(m)
                b.append(f"" + f + '.  ' + track)

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

            await ctx.edit_initial_response(embed=pages[0], components=[row, ])
            i = 0
            var = 0
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

                        elif key == "⬅️":
                            if i==0:
                                pass
                            else:
                                i = i - 1

                        await ctx.edit_initial_response(embed=pages[i], components=[row])
                    
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
