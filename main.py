import sys  #Импорт sys
import discord     #Импорт библиотеки дискорда
import os   #Импорт os

from config import settings     #Импорт конфига
from discord.ext import commands     #Импорт комманд из discord.ext
from datetime import datetime     #Импорт библиотеки времени из datetime


bot = commands.Bot(command_prefix = settings['bot_prefix'])


@bot.event
async def on_ready():
    print('Бот запущен!')
    await bot.change_presence(activity = discord.Game(name = 'Версия бота: '+settings['bot_version']))
    if settings['logs'] == True:
        embed = discord.Embed(title = 'Бот запущен!')
        embed.set_footer(text = datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        await bot.get_channel(settings['logs_channel_id']).send(embed = embed)


#Логи
@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.author.nick == None:
            nickname = message.author.name
        else:
            nickname = message.author.nick
        if not message.content.startswith(settings['bot_prefix']):
            print(f'[MESSAGE] <<{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}>> {nickname} in [#{message.channel}] :\n {message.content} ')
            if settings['logs'] == True:
                embed = discord.Embed(title = f'{nickname} в [#{message.channel}] :', description = f'"{message.content}"')
                embed.set_footer(text = datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                await bot.get_channel(settings['logs_channel_id']).send(embed = embed)
        else:
            print(f'[COMMAND] <<{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}>> {nickname} in [#{message.channel}] :\n {message.content} ')
            if settings['logs'] == True:
                embed = discord.Embed(title = f'{nickname} в [#{message.channel}] :', description = f'"{message.content}"')
                embed.set_footer(text = datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                await bot.get_channel(settings['logs_channel_id']).send(embed = embed)
    await bot.process_commands(message)


#Команда time
@bot.command()
async def bot_time(ctx):
    if settings['delete_commands'] == True:
        await ctx.channel.purge(limit = 1)
    await ctx.send(datetime.now().strftime("%Y/%m/%D %H:%M:%S"))


#Команда clear
@bot.command()
async def clear(ctx, number):
    number = int(number)
    if number > 0 and number < 100:
        await ctx.channel.purge(limit = 1+number)
        await ctx.send(f'**Удалено {number} сообщений**')
    else:
        await ctx.send('**Неверная команда.**')


#Ошибка
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.author.mention('**Неверная команда.**')


#Выключение
@bot.command()
@commands.is_owner()
async def stop(ctx):
    print('Shutting down...')
    if settings['logs'] == True:
        embed = discord.Embed(title = 'Отключение бота...')
        embed.set_footer(text = datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        await bot.get_channel(settings['logs_channel_id']).send(embed = embed)
    if settings['delete_commands'] == True:
        await ctx.channel.purge(limit = 1)
    exit()


#Обновление (перезапуск)
@bot.command()
@commands.is_owner()
async def update(ctx):
    print('Рестарт бота...')
    if settings['logs'] == True:
        embed = discord.Embed(title = 'Рестарт бота...')
        embed.set_footer(text = datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        await bot.get_channel(settings['logs_channel_id']).send(embed = embed)
    if settings['delete_commands'] == True:
        await ctx.channel.purge(limit = 1)
    os.execv(sys.executable, ['python'] + sys.argv)


bot.run(settings['bot_token'])
