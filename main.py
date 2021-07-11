import discord
import os
import random
from keep_alive import keep_alive
from discord.ext import commands

client = commands.Bot(command_prefix = 'a?')

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('Looking for "a?"'))
  print('We have logged in as {0.user}'.format(client))
  

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  guild = ctx.guild
  await member.send(f'You were kicked from {guild.name}!')
  await member.kick(reason=reason)
  await ctx.send(f'Kicked {member.mention}!')
  


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  guild = ctx.guild
  await member.send(f'You were banned from {guild.name}')
  await member.ban(reason=reason)
  await ctx.send(f'Banned {member.mention}!')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')


  for ban_entry in banned_users:
    user = ban_entry.user


    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send('Unbanned User!')
      return


@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, *, member : discord.Member, reason=None):
  guild = ctx.guild
  mutedRole = discord.utils.get(guild.roles, name="Muted")

  if not mutedRole:
    mutedRole = await guild.create_role(name="Muted")

    for channel in guild.channels:
      await channel.set_permission(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

  await member.add_roles(mutedRole, reason=reason)  
  await ctx.send(f'Muted {member.mention}!')  
  await member.send(f'You were muted in {guild.name}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, *, member : discord.Member, reason=None):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await ctx.send(f'Unmuted {member.mention}')
   await member.send(f'You were unmuted in {ctx.guild.name}')

@client.command()
async def clear(ctx, amount=1):
  await ctx.channel.purge(limit=amount)
  await ctx.send(f'Cleared {amount} messages')

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {client.latency * 1000}ms')

@client.command(aliases=['8ball', 'eightball', '8-ball'])
async def _8ball(ctx, *, question):
  responses=["It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
  await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


keep_alive()
client.run(os.getenv('TOKEN'))