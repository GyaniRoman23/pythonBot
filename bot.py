import discord
import os
import pyfiglet
from discord.ext import commands
from discord.commands import Option
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

bot = discord.Bot(intents=discord.Intents.all())


MY_GUILDS = [939094080661635142, 939438947594039316]

print(pyfiglet.figlet_format("Mass DM Bot"))


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=MY_GUILDS)
async def latency(ctx, *, message: str):
    await ctx.send(f"{message}")


@bot.slash_command(guild_ids=MY_GUILDS)
async def message_all(
    ctx,
    message: Option(str, required=True),
    server: Option(str, options=["all", "my"], required=True),
):
    await ctx.respond("Sending message to all members")
    for guild in bot.guilds:
        if (
            guild.id == ctx.guild.id
        ):  # TODO: remove this condition on production to make it send to all members of all guilds bot is in
            for member in guild.members:
                if member.id == bot.user.id:
                    continue
                try:
                    await member.send(message)
                except discord.Forbidden as e:
                    print(e)


@bot.slash_command(guild_ids=MY_GUILDS)
async def purge(
    ctx, amount: Option(int, "Amount of messages to delete", required=True)
):
    await ctx.channel.purge(limit=int(amount))
    await ctx.respond("Messages deleted")
    await ctx.channel.purge(limit=1)


@bot.slash_command(guild_ids=MY_GUILDS)
async def send_invites(ctx):
    invite = await ctx.channel.create_invite()
    await ctx.respond("Sending invites...")
    for guild in bot.guilds:
        if (
            guild.id == ctx.guild.id
        ):  # TODO: Change == to != when sending to user so it invites people in all other guilds`` bot is in
            for member in guild.members:
                if member.id == bot.user.id:
                    continue
                try:
                    await member.send(invite.url)
                except discord.Forbidden as e:
                    print(e)


bot.run(token)
