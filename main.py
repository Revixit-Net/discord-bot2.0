import discord
from discord.ext import commands
import signal
import aiofiles.os
import sys
import multiprocessing
from dynaconf import Dynaconf

import dbmanager


config = Dynaconf(settings_files='conf/settings.yaml',apply_default_on_none=True, secrets='.secrets.yaml')
shop = Dynaconf(settings_files='conf/shop.yaml', apply_default_on_none=True, secrets='.secrets.yaml')
client = commands.Bot(command_prefix=config.bot.prefix, intents=discord.Intents.all(), help_command=None)
db = dbmanager.dbm(str(config.db.login), str(config.db.password), config.db.host, config.db.database)


@client.event
async def on_ready():
    try:
        #Загрузка папки cogs
        for dir_cogs in await aiofiles.os.listdir('./cogs'):
            for filename in await aiofiles.os.listdir(f'./cogs/{dir_cogs}'):
                if filename.endswith('.py'):
                    await client.load_extension(f'cogs.{dir_cogs}.{filename[:-3]}')
                else:
                    print(f'Не является Cogs {filename}')
        #Удаление всех команд из подсказок в Discord
        #client.tree.clear_commands(guild=None)
        for Directory in [config.web.skindir, config.web.capedir, config.web.avatardir]:
            if not await aiofiles.os.path.exists(Directory):
                await aiofiles.os.mkdir(Directory)
        print(f"Команд найдено {len(await client.tree.sync())}")
    except Exception as ex:
        print(ex)



def signal_handler(signal, frame):
    print('\nStopping!')
    scs_thread.terminate()
    client.loop.stop()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    from scstorage import API
    scs_thread = multiprocessing.Process(target=API.server)
    scs_thread.start()
    client.run(config.bot.token)