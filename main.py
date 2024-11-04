import nextcord
from nextcord.ext import commands
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup with default intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is connected to {len(bot.guilds)} servers')

# Command: Hello
@bot.command(name='hello')
async def hello(ctx):
    """Greets the user with their name"""
    try:
        await ctx.send(f'Hello, {ctx.author.mention}! 👋')
    except Exception as e:
        await ctx.send("Sorry, I couldn't process that request. Please try again later.")
        print(f"Error in hello command: {e}")

# Command: Roll
@bot.command(name='roll')
async def roll(ctx):
    """Generates a random number between 1 and 100"""
    try:
        number = random.randint(1, 100)
        await ctx.send(f'🎲 {ctx.author.mention} rolled: **{number}**')
    except Exception as e:
        await ctx.send("Sorry, I couldn't generate a random number. Please try again.")
        print(f"Error in roll command: {e}")

# Command: Server Info
@bot.command(name='info')
async def info(ctx):
    """Displays basic information about the server"""
    try:
        guild = ctx.guild
        embed = nextcord.Embed(
            title=f"📊 Server Information: {guild.name}",
            color=nextcord.Color.blue()
        )
        
        # Add server information fields
        embed.add_field(name="Server Owner", value=guild.owner.name, inline=False)
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Server Created", value=guild.created_at.strftime("%B %d, %Y"), inline=False)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("Sorry, I couldn't fetch the server information. Please try again.")
        print(f"Error in info command: {e}")

# Error Handling: Command not found
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Type `!help` to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    else:
        await ctx.send("❌ An error occurred while processing your command.")
        print(f"Unexpected error: {error}")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)