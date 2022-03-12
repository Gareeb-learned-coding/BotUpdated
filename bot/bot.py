import hikari
import tanjun
import os

def build_bot() -> hikari.GatewayBot:
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot = hikari.GatewayBot(TOKEN)
    make_client(bot)

    return bot


def make_client(bot: hikari.GatewayBot) -> tanjun.Client:
    client = (
        tanjun.Client.from_gateway_bot(
            bot,
            mention_prefix=True,
            declare_global_commands=True
        )
    ).add_prefix("!")

    client.load_modules("plugins.begin")
    client.load_modules("plugins.add")
    client.load_modules("plugins.remove")
    client.load_modules("plugins.tracks")
    client.load_modules("plugins.link")
    client.load_modules("plugins.help")
    
    return client
