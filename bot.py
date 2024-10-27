import discord
from discord.ext import commands
import docker
import asyncio

TOKEN = "YOUR_DISCORD_BOT_TOKEN"  # Replace with your bot token

# Set up the Docker client
client = docker.from_env()

# Set up the Discord bot
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Command to create a VPS (Docker container)
@bot.command()
async def create_vps(ctx, image_name: str, name: str):
    """Create a new VPS (Docker container)."""
    try:
        container = client.containers.run(image_name, detach=True, name=name)
        await ctx.send(f"VPS created! Container ID: {container.id[:12]} (Name: {name})")
    except docker.errors.ImageNotFound:
        await ctx.send(f"Error: Image '{image_name}' not found.")
    except Exception as e:
        await ctx.send(f"Failed to create VPS: {e}")

# Command to stop a VPS
@bot.command()
async def stop_vps(ctx, name: str):
    """Stop a running VPS (Docker container)."""
    try:
        container = client.containers.get(name)
        container.stop()
        await ctx.send(f"VPS '{name}' stopped.")
    except docker.errors.NotFound:
        await ctx.send(f"Error: No running VPS found with name '{name}'.")
    except Exception as e:
        await ctx.send(f"Failed to stop VPS: {e}")

# Command to list all VPS instances
@bot.command()
async def list_vps(ctx):
    """List all running VPS instances (Docker containers)."""
    containers = client.containers.list()
    if containers:
        response = "Running VPS instances:\n" + "\n".join([f"{c.name} (ID: {c.id[:12]})" for c in containers])
    else:
        response = "No VPS instances are running."
    await ctx.send(response)

# Run the bot
bot.run(TOKEN)
                     
