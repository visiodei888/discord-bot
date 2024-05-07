import discord
import os
from decouple import config
from discord.ext import commands
import pymysql
import asyncio

intents = discord.Intents.default()
intents.guild_messages = True 
intents.guild_reactions = True
intents.guilds = True 
intents.messages = True  
intents.reactions = True  


mubot = commands.Bot(command_prefix="/",intents=discord.Intents.all())

def fetch_data(query):
    connection = pymysql.connect(
        host=config("DB_HOST"),
        user=config("DB_USER"),
        password=config("DB_PASSWORD"),
        db=config("DB_NAME")
    )
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()



def execute_query(query):
    connection = pymysql.connect(
        host=config("DB_HOST"),
        user=config("DB_USER"),
        password=config("DB_PASSWORD"),
        db=config("DB_NAME")
    )
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

@mubot.event
async def on_member_join(member):
    welcome_channel = mubot.get_channel(1236694797956288554)
    message = f"Welcome to the server {member.name}"
    await welcome_channel.send(message)
    await member.send(message)
    

@mubot.event
async def on_message(message):
    if message.author.bot:
        return
    words = message.content.split()
    for word in words:
        execute_query(f"INSERT INTO user_words (discord_id, word) VALUES ('{message.author.id}', '{word}')")

    await mubot.process_commands(message)


@mubot.command()
async def word_status(ctx):
    result = fetch_data("SELECT word, COUNT(*) as count FROM user_words GROUP BY word ORDER BY count DESC LIMIT 10")
    if result:
        await ctx.send("Top 10 most used words:")
        for row in result:
            await ctx.send(f"{row[0]}: {row[1]}")
    else:
        await ctx.send("No words found.")


@mubot.command()
async def user_status(ctx, user: discord.User):
    result = fetch_data(f"SELECT word, COUNT(*) as count FROM user_words WHERE discord_id = '{user.id}' GROUP BY word ORDER BY count DESC LIMIT 10")
    if result:
        await ctx.send(f"Top 10 most used words by {user.name}:")
        for row in result:
            await ctx.send(f"{row[0]}: {row[1]}")
    else:
        await ctx.send("No words found for this user.")


def create_role_select():
    select = discord.ui.Select(
        placeholder="Select your role",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="amin", value="role1"),
            discord.SelectOption(label="Beginner", value="role2"),
            discord.SelectOption(label="Tester", value="role3")
        ]
    )
    return select

@mubot.command(name="select-role")
async def select_role(ctx):
    select = create_role_select()
    view = discord.ui.View()
    view.add_item(select)
    message = await ctx.send("Select your role:", view=view)

    try:
        interaction = await mubot.wait_for("select_option", timeout=60)  # Timeout after 60 seconds
        role_name = interaction.values[0]
        user_id = interaction.user.id
        execute_query(f"INSERT INTO user_role (discord_id, role) VALUES ('{user_id}', '{role_name}') ON DUPLICATE KEY UPDATE role='{role_name}'")
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await interaction.user.add_roles(role)
            await ctx.send(f"Role '{role.name}' has been assigned to you.")
        else:
            await ctx.send("Role not found.")
    except asyncio.TimeoutError:
        await ctx.send("Role selection timed out.")

   
mubot.run(config("TOKEN"))