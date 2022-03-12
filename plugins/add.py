import hikari
import tanjun
import spotipy
import sqlite3
import json
import requests
import typing

from tanjun.abc import SlashContext

conn = sqlite3.connect('database.db')
c = conn.cursor()

#c.execute("""CREATE TABLE database (
#users_id integer,
#playlist_id BLOB,
#playlist_link BLOB)""")

component = tanjun.Component()


@component.with_command
@tanjun.with_str_slash_option("track", "The Spotify link to the song.")
@tanjun.as_slash_command("add", f"Add tracks to your playlist.")
async def interactive_post(
    ctx: SlashContext, track: typing.Optional[str],
    bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot),
    client: tanjun.Client = tanjun.injected(type=tanjun.Client)
) -> None:
    get_token()
    spotifyObject = spotipy.Spotify(get_token.variable)
    id = ctx.author.id
    c.execute("SELECT * FROM database WHERE users_id = ?", (id,))
    temp = c.fetchall()
    if len(temp) == 0:
        embed = hikari.Embed(title="", colour=0x00ffd5,description="You need a Personal Playlist first to use this command. \nUse the `begin` command to create one. \nUse the `add-common` command to add to the common playlist.")
        await ctx.respond(embed=embed)
    else:
        def split(track):
            return list(track)
        
        word = split({track})
        var = word[0]
        word = split(var)
        song = []
        n = 0
        while n < 22:
            song.append(word[n + 31])
            n += 1

        preUri = ''.join([str(elem) for elem in song])
        Uri = 'spotify:track:' + preUri

        c.execute("SELECT playlist_id FROM database WHERE users_id = ?", (id,))
        q = c.fetchall()
        f = q[0]
        g = str(f[0])

        spotifyObject.playlist_add_items(playlist_id=g, items=[Uri])
        embed = hikari.Embed(title="", colour=0x00ffd5,description=f"Track added!")
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
