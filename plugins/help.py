import hikari
import tanjun

from tanjun.abc import SlashContext

component = tanjun.Component()


@component.with_command
@tanjun.as_slash_command("help", f"Get Help!!")
async def interactive_post(
    ctx: SlashContext,
    bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot),
    client: tanjun.Client = tanjun.injected(type=tanjun.Client)
) -> None:
    embed = hikari.Embed(title="Help", description=f"", color=0x00ffcc
    ).add_field(name= f"Add [track]", value= f"Adds the given track to your personal playlist."
    ).add_field(name= f"Begin", value= f"Creates your own personal playlist."
    ).add_field(name= f"Link (target)", value= f"Provides you link of yours or others playlist."
    ).add_field(name= f"Remove", value= f"Removes the track from your playlist."
    ).add_field(name= f"Tracks (target)", value= f"Look at yours or others tracks in their playlist.")

    await ctx.edit_inital_response(embed=embed)
