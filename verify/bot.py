import discord
from discord.ext import commands
from discord import app_commands
import threading
from flask import Flask, request, send_from_directory
import asyncio
import json
import os

TOKEN = 'MTM1OTkwMTk5ODYxNDU4MTM1OA.G6r0Bb.Y5xAnoh_K5MiyzO0Xt9iwBP4Kf08H7m1vK_JNQ'  # Replace with your actual bot token
CONFIG_FILE = 'config.json'

intents = discord.Intents.default()
intents.members = True  # Ensure the bot can read member info

bot = commands.Bot(command_prefix='/', intents=intents)
app = Flask(__name__)

# ------------------ Config Helpers ------------------
def load_config():
    """Load the configuration file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("❌ config.json is empty or malformed.")
            return {}  # Return an empty dict if JSON decoding fails
    else:
        print("❌ config.json file not found.")
        return {}

def save_config(data):
    """Save the configuration file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

config_data = load_config()

# ------------------ Flask Endpoints ------------------

@app.route('/')
def index():
    """Serve the index.html at /verify."""
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/verify', methods=['GET'])
def verify_user_all_guilds():
    try:
        # Retrieve query parameters from the GET request
        user_id = request.args.get('userid')
        username = request.args.get('username')
        display_name = request.args.get('user_display_name')

        # Ensure all required parameters are present
        if not user_id or not username or not display_name:
            return "Missing parameters", 400  # Just a basic string message for the error

        print(f"🛂 Verifying {username} ({user_id}) across all guilds...")

        # Your logic to assign roles and verify across all guilds
        async def assign_roles():
            await bot.wait_until_ready()
            for guild in bot.guilds:
                config = config_data.get(str(guild.id))
                if not config:
                    continue  # Skip if no setup

                member = guild.get_member(int(user_id))
                role = guild.get_role(config['role_id'])

                if member and role:
                    try:
                        await member.add_roles(role)
                        print(f"✅ Gave '{role.name}' to {member.name} in '{guild.name}'")
                    except Exception as e:
                        print(f"❌ Failed to assign in {guild.name}: {e}")

        asyncio.run_coroutine_threadsafe(assign_roles(), bot.loop)
        
        # Return the HTML page after verification
        return send_from_directory(os.getcwd(), 'index.html')

    except Exception as e:
        print(f"❌ Verification error: {e}")
        return "Verification error", 400

def assign_role():
    try:
        user_id = request.args.get('userid')

        # Ensure the user ID is provided
        if not user_id:
            return "Missing user ID", 400  # Just a basic string message for the error

        async def assign_role_to_user():
            await bot.wait_until_ready()
            for guild in bot.guilds:
                config = config_data.get(str(guild.id))
                if not config:
                    continue  # Skip if no setup

                member = guild.get_member(int(user_id))
                role = guild.get_role(config['role_id'])

                if member and role:
                    try:
                        await member.add_roles(role)
                        print(f"✅ Assigned role '{role.name}' to {member.name} in '{guild.name}'")
                    except Exception as e:
                        print(f"❌ Failed to assign role in {guild.name}: {e}")
            # Don't return JSON, just return the HTML page
            return send_from_directory(os.getcwd(), 'index.html')

        asyncio.run_coroutine_threadsafe(assign_role_to_user(), bot.loop)
        return send_from_directory(os.getcwd(), 'index.html')

    except Exception as e:
        print(f"❌ Role assignment error: {e}")
        return "Role assignment error", 400
    
# ------------------ Slash Commands ------------------

@bot.tree.command(name="setup", description="Set up the verification role and channel")
@app_commands.describe(rolename="The role to assign", channel="Channel to allow verification")
@app_commands.checks.has_permissions(administrator=True)
async def setup(interaction: discord.Interaction, rolename: str, channel: discord.TextChannel):
    """Setup the role and channel for verification."""
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name=rolename)

    if not role:
        await interaction.response.send_message(f"❌ Role '{rolename}' not found.", ephemeral=True)
        return

    config_data[str(guild.id)] = {
        "role_id": role.id,  # Save the role by ID
        "channel_id": channel.id  # Save the channel ID
    }
    save_config(config_data)

    await interaction.response.send_message(
        f"✅ Setup complete!\nVerified users will get the role **{role.name}**.\nOnly **#{channel.name}** can use `/verify`.",
        ephemeral=True
    )

@bot.tree.command(name="verify", description="Get your verification link")
async def verify(interaction: discord.Interaction):
    """Generate a verification URL for the user."""
    guild_id = str(interaction.guild.id)

    if guild_id not in config_data:
        await interaction.response.send_message("❌ This server has not been set up for verification.", ephemeral=True)
        return

    allowed_channel_id = config_data[guild_id]['channel_id']

    if interaction.channel.id != allowed_channel_id:
        await interaction.response.send_message("❌ You can only use this command in the designated verification channel.", ephemeral=True)
        return

    user = interaction.user
    url = (
        f"http://192.168.1.222:5000/verify"
        f"?username={user.name}"
        f"&userid={user.id}"
        f"&user_display_name={user.display_name}"
    )

    await interaction.response.send_message(f"🔗 [Click here to verify]({url})", ephemeral=True)

# ------------------ Run Everything ------------------

def run_flask():
    """Start the Flask server on a separate thread."""
    print("🌐 Flask API running on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)  # Disable debug mode

if __name__ == "__main__":
    # Start Flask in a separate thread
    threading.Thread(target=run_flask).start()
    # Start the bot
    bot.run(TOKEN)