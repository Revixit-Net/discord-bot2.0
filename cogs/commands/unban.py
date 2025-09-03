import discord
from discord.ext import commands
from discord import app_commands

from main import config, db

class Unban(commands.Cog):
    def __init__(self, client):
        self.client = client


    def check_role(self, interaction):
        guild = discord.utils.get(self.client.guilds, id = config.bot.guild)
        member = guild.get_member(interaction.user.id)
        for list_role in member.roles:
            if list_role.id == config.bot.adminRole:
                return True

    @app_commands.command(name="unban", description="Разбанить игрока по железу")
    @app_commands.describe(ban_user = "Ник Discord пользователя которого нужно разбанить")
    @app_commands.default_permissions(permissions=0)
    async def ban(self, interaction: discord.Integration, ban_user: app_commands.Range[str, 1, None]):
        try:
            if Unban.check_role(self, interaction):
                if db.connect():
                    guild = discord.utils.get(self.client.guilds, id = config.bot.guild)
                    member = guild.get_member_named(ban_user)
                    if member != None:
                        db.unbane(member.id)
                        await interaction.response.send_message(f'{ban_user} **успешно разбанин по железу.**')
                    else:
                        await interaction.response.send_message(f'{ban_user} **данный человек не находится на Discord сервере.**')
            else:
                embedVar = discord.Embed(title="Недостаточно прав!", description="*У вас не достаточно прав на выполнение данной команды.*", color=0xf44336)
                await interaction.response.send_message(embed=embedVar)
        except Exception as ex:
            print(ex)
            await interaction.response.send_message('**Ошибка:** Обратитесь для решения проблемы администратору.')
        finally:
            db.close()
                


async def setup(client):
    await client.add_cog(Unban(client))