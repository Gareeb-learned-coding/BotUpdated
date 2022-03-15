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
        spotifyObject.user_playlist_create(user="s814ch55pl3cdix8t3ztevrui", name=title, public=True, description=description)
        
        embed = hikari.Embed(title="", colour=0x00ffd5, description="Playlist Created.")
        await ctx.respond(embed=embed)
        
        pp = spotifyObject.user_playlists(user="s814ch55pl3cdix8t3ztevrui")
        q = pp['items'][0]['id']
        o = pp['items'][0]['external_urls']['spotify']
        c.execute("INSERT INTO database VALUES (?, ?, ?)", (id, q, o))
        conn.commit()

def get_token():
    headers = {'Authorization': 'Basic ZjUxZTBhNTE1NjlmNGQ0NjkxZTc1ZTFiYzU2MzE0YjU6NzQ0YmUwYzc2ZWQxNGNjOTk4Y2JiYzAwNmFhYmNjMTg=', }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': "AQBB3JUEtdC2zWAUySNsgWM1BNF58EYhWOd3GDzew6ggG6qdkvanyuDOphJF_j8VPTMKnBBCMOMAY4nCr53bqbqjGdraaXiA4Ih0xrhu0AonsgaWmFLtJYRZAQ6Aa-q7dqU",
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    x = json.loads(response.text)
    get_token.variable = x['access_token']
    

@ tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
