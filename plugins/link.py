import hikari
import tanjun
import spotipy
import sqlite3
import json
import requests

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
@tanjun.with_member_slash_option("target", "Select whose playlist's link you want", default=None)
@tanjun.as_slash_command("link", f"Get a link to your or your pal's personal playlist.")
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
            embed = hikari.Embed(title="Error", colour=0x00ffd5,
                                 description="Huh, looks like this person doesn't have own one personal playlist yet.")
            await ctx.respond(embed=embed)

        else:
            c.execute("SELECT playlist_link FROM database WHERE users_id = ?", (id,))
            d = c.fetchall()
            s = ' '.join(map(str, d))
            embed = hikari.Embed(title="", description=f"The playlist's link is :\n"+s[2:58]+"", color=0x00ffcc)
            await ctx.respond(embed=embed)
    
    else:
        id = ctx.author.id
        c.execute("SELECT playlist_link FROM database WHERE users_id = ?", (id,))
        d = c.fetchall()
        s = ' '.join(map(str, d))
        embed = hikari.Embed(
            title="", description=f"The playlist's link is :\n"+s[2:58]+"", color=0x00ffcc)
        await ctx.respond(embed=embed)

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


@ tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
