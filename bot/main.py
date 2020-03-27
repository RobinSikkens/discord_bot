"""
Provides the main entry point for the discord bot.
"""

import logging
import os
import discord

# Import from local modules.
import commands
from tools.logger import get_logger
from tools.wrapper import Response
from registry import COMMAND_DICT, safe_call, CommandNotFoundError

CLIENT = discord.Client()
LOGGER = get_logger("bot")
PREFIX = os.environ.get("COMMAND_PREFIX", "!")

DB_ENGINE = None
DB_SESSION = None


@CLIENT.event
async def on_ready():
    """ Log login information. """

    print(f"Logged in as bot: {CLIENT.user.name} ({CLIENT.user.id}).")
    LOGGER.info("Logged in as bot: %s (%s).", CLIENT.user.name, CLIENT.user.id)

    print("Connected to the following servers:")
    server_list = await CLIENT.fetch_guilds().flatten()
    for s in server_list:
        print(s.name)


@CLIENT.event
async def on_message(message):
    """ Send message to handler when recieved. """
    await handle_message(message)


@CLIENT.event
async def on_message_edit(_, post):
    """ After message is edited send to handler. """
    await handle_message(post)


async def handle_message(m):
    """ Handle an incoming message. """

    # If not the correct prefix, return.
    if not m.content.startswith(PREFIX):
        return

    # Disable self-activation.
    if m.author == CLIENT.user:
        return

    # Split message on command.
    m_command, *m_contents = m.content.split()
    LOGGER.debug(f"Message: {m_command}, {m_contents}")

    response = None
    try:
        response = await safe_call(
            COMMAND_DICT, m_command[len(PREFIX) :], m_contents, m, CLIENT, DB_SESSION,
        )
    except CommandNotFoundError:
        LOGGER.debug(f"Command unknown: {m_command[1:]}")
        return

    # If no response was given return.
    if not response:
        return

    if isinstance(response, Response):
        if not response.message and not response.embed:
            return
        if response.files:
            if isinstance(response.files, list):
                await m.channel.send(
                    content=response.message,
                    embed=response.embed,
                    files=response.files,
                    delete_after=response.delete_after,
                )
            else:
                await m.channel.send(
                    content=response.message,
                    embed=response.embed,
                    file=response.files,
                    delete_after=response.delete_after,
                )
        else:
            await m.channel.send(
                content=response.message,
                embed=response.embed,
                delete_after=response.delete_after,
            )

    else:
        await m.channel.send(response)


def main():
    """ Initialize and start bot processes. """
    # Set up logging.
    log_level = os.environ.get("LOGLEVEL", "INFO")
    logging.basicConfig(
        filename="bot.log",
        level=log_level,
        format="[%(asctime)s]%(name)s: %(levelname)s: %(message)s",
    )

    # Load commands.
    commands.load_plugins()

    # Connect to discord.
    CLIENT.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
