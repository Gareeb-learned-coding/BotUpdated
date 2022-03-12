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
@tanjun.with_str_slash_option("description", "Describe your playlist a bit.")
@tanjun.with_str_slash_option("title", "What would you like your playlist to be called?")
@tanjun.as_slash_command("begin", f"Create your own Personal Playlist!")
async def interactive_post(
    ctx: SlashContext, title: typing.Optional[str], description: typing.Optional[str],
    bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot),
    client: tanjun.Client = tanjun.injected(type=tanjun.Client)
) -> None:
    get_token()
    spotifyObject = spotipy.Spotify(get_token.variable)
    id = ctx.author.id
    c.execute("SELECT * FROM database WHERE users_id = ?", (id,))
    temp = c.fetchall()
    if len(temp) != 0:
        embed = hikari.Embed(title="", colour=0x00ffd5, description="You already have your own personal playlist.")
        await ctx.respond(embed=embed)
    else:
        
        spotifyObject.user_playlist_create(user="31wts2xbpngwxvhblc5j3s2jsauq", name={title}, public=True, description={description})
        
        await ctx.respond("Playlist Created!")
        
        pp = spotifyObject.user_playlists(user="31wts2xbpngwxvhblc5j3s2jsauq")
        q = pp['items'][0]['id']
        o = pp['items'][0]['external_urls']['spotify']
        c.execute("INSERT INTO database VALUES (?, ?, ?)", (id, q, o))
        conn.commit()

def get_token():
    headers = {'Authorization': 'Basic NWJjODIzMDI2M2EyNGI3NzhhYjQxMTRmN2EyMTVkMDY6YTM0ODU4YWUxZWNlNDE2MDg1MGQzOGE0NDEyYjNkOTg=',}


    data = {
        'grant_type': 'refresh_token',
        'refresh_token': "AQAIxWRAXRLsOuZ81K_MAMnR8qonzsouwG8hKzP1PnkYb4X0F3VfXIo_bzySMG7S2k4PMnxic15nyPOFMFj4V3Co3t6EAry_Rl6c6O_scw9-YEpJbiuUqSevZqMbCu63W1M",
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    x = json.loads(response.text)
    get_token.variable = x['access_token']
    

@ tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
