from nonebot import get_plugin_config, on_command
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from .config import Config

__plugin_meta__ = PluginMetadata(
    name='nonebot-plugin-are-you-ok',
    description='A simple plugin for confirming the status of bot.',
    usage='@bot ping',
    type='application',
    config=Config,
    supported_adapters=None,
)

config = get_plugin_config(Config)


ping = on_command('ping', rule=to_me())


@ping.handle()
async def _(matcher: Matcher):
    await matcher.finish('pong')
