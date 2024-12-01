import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import json

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix=".", intents=intents)

# Armazenamento para termos aceitos, chats ativos e mensagens sincronizadas
user_terms_accepted = {}
active_chats = {}
message_links = {}

# Carregar dados salvos
try:
    with open("data.json", "r") as f:
        data = json.load(f)
        user_terms_accepted = data.get("terms", {})
except FileNotFoundError:
    pass

# Salvar dados persistentes
def save_data():
    with open("data.json", "w") as f:
        json.dump({"terms": user_terms_accepted}, f)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Comando .guides
@bot.command()
async def guides(ctx):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("This command can only be used in DMs.")
        return

    user_id = str(ctx.author.id)
    if user_id not in user_terms_accepted:
        terms_embed = discord.Embed(
            title="📜 **Terms of Use**",
            description=(
                "Before using this bot, you must agree to the following:\n\n"
                "**1. Respect Discord's Community Guidelines.**\n"
                "**2. Do not use the bot for harm or spam.**\n"
                "**3. Messages are forwarded; share responsibly.**\n"
                "**4. The bot owner is not responsible for misuse.**"
            ),
            color=discord.Color.green()
        )
        terms_embed.set_footer(text="🕯️ Accept the terms to proceed.")

        accept_button = Button(label="Accept", style=discord.ButtonStyle.green)
        reject_button = Button(label="Reject", style=discord.ButtonStyle.red)

        async def accept_callback(interaction):
            user_terms_accepted[user_id] = True
            save_data()
            await interaction.response.send_message("You have accepted the terms. You can now use the bot.", ephemeral=True)

        async def reject_callback(interaction):
            await interaction.response.send_message("You rejected the terms. Access to the bot is restricted.", ephemeral=True)

        accept_button.callback = accept_callback
        reject_button.callback = reject_callback

        view = View()
        view.add_item(accept_button)
        view.add_item(reject_button)

        await ctx.author.send(embed=terms_embed, view=view)
    else:
        help_embed = discord.Embed(
            title="📚 **Bot Commands**",
            description=(
                "**.guides:** Display this guide.\n"
                "**.chat [user_id]:** Synchronize chat with another user.\n"
                "**.clear:** End synchronization and delete exchanged messages."
            ),
            color=discord.Color.blue()
        )
        help_embed.set_footer(text="🕯️ Use the bot responsibly.")
        await ctx.author.send(embed=help_embed)

# Comando .chat
@bot.command()
async def chat(ctx, target_user_id: int):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("This command can only be used in DMs.")
        return

    user_id = str(ctx.author.id)
    if user_id not in user_terms_accepted:
        await ctx.send("You must accept the terms first. Use `.guides` to view them.")
        return

    target_user = await bot.fetch_user(target_user_id)
    if not target_user:
        await ctx.author.send("Invalid user ID.")
        return

    if user_id in active_chats or str(target_user_id) in active_chats:
        await ctx.author.send("Either you or the other user is already in an active chat.")
        return

    # Botões de sincronização
    sync_embed = discord.Embed(
        title="🔗 **Chat Synchronization Request**",
        description=(
            f"A user has requested to sync their chat with you. Messages will be forwarded.\n\n"
            f"**Duration:** 12 hours or until cleared."
        ),
        color=discord.Color.gold()
    )
    sync_embed.set_footer(text="🕯️ Accept to start.")

    accept_button = Button(label="Accept", style=discord.ButtonStyle.green)
    reject_button = Button(label="Reject", style=discord.ButtonStyle.red)

    async def accept_callback(interaction):
        active_chats[user_id] = target_user_id
        active_chats[str(target_user_id)] = ctx.author.id
        await interaction.response.send_message("Chat synchronized. Start messaging!", ephemeral=True)
        await ctx.author.send(f"🔗 Chat synchronized with {target_user.name}.")
        await target_user.send("🔗 Chat synchronization established.")

    async def reject_callback(interaction):
        await interaction.response.send_message("Chat synchronization rejected.", ephemeral=True)
        await ctx.author.send("The user rejected your chat request.")

    accept_button.callback = accept_callback
    reject_button.callback = reject_callback

    view = View()
    view.add_item(accept_button)
    view.add_item(reject_button)

    try:
        await target_user.send(embed=sync_embed, view=view)
    except discord.Forbidden:
        await ctx.author.send("Unable to send messages to the specified user.")

# Evento para encaminhar mensagens, edição e reações
@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        user_id = str(message.author.id)
        if user_id in active_chats:
            target_user_id = active_chats[user_id]
            target_user = await bot.fetch_user(target_user_id)

            try:
                forwarded_message = None
                if message.attachments:
                    for attachment in message.attachments:
                        forwarded_message = await target_user.send(file=await attachment.to_file())
                else:
                    forwarded_message = await target_user.send(message.content)

                # Salvar a mensagem para exclusão e edição sincronizada
                if forwarded_message:
                    message_links[message.id] = forwarded_message.id
            except discord.Forbidden:
                await message.author.send("Message forwarding failed. The user may have blocked the bot.")

        # Se o usuário der reply em uma mensagem do bot, o bot responde também
        if message.reference and message.reference.message_id in message_links.values():
            original_message = await message.channel.fetch_message(message.reference.message_id)
            if original_message.author == bot.user:
                # O bot responde com a mesma mensagem no outro chat
                target_user_id = active_chats.get(str(message.author.id))
                if target_user_id:
                    target_user = await bot.fetch_user(target_user_id)
                    await target_user.send(content=message.content, reference=original_message)

    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if isinstance(message.channel, discord.DMChannel) and message.id in message_links:
        target_user_id = active_chats.get(str(message.author.id))
        if target_user_id:
            target_user = await bot.fetch_user(target_user_id)
            try:
                target_message_id = message_links[message.id]
                target_message = await target_user.fetch_message(target_message_id)
                await target_message.delete()
            except Exception:
                pass

@bot.event
async def on_message_edit(before, after):
    if isinstance(before.channel, discord.DMChannel) and before.id in message_links:
        target_user_id = active_chats.get(str(before.author.id))
        if target_user_id:
            target_user = await bot.fetch_user(target_user_id)
            try:
                target_message_id = message_links[before.id]
                target_message = await target_user.fetch_message(target_message_id)
                await target_message.edit(content=after.content)
            except Exception:
                pass

# Comando .clear
@bot.command()
async def clear(ctx):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("This command can only be used in DMs.")
        return

    user_id = str(ctx.author.id)
    if user_id in active_chats:
        target_user_id = active_chats[user_id]
        target_user = await bot.fetch_user(target_user_id)

        await ctx.author.send("🔚 Chat synchronization ended.")
        await target_user.send("🔚 Chat synchronization ended.")

        del active_chats[user_id]
        del active_chats[str(target_user_id)]

        # Apagar mensagens enviadas pelo bot
        async for message in ctx.channel.history(limit=100):
            if message.author == bot.user:
                await message.delete()

        async for message in target_user.dm_channel.history(limit=100):
            if message.author == bot.user:
                await message.delete()

bot.run("YOUR_BOT_TOKEN")