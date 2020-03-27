# discord_bot

To set up a discord bot do the following steps:

1. Make sure to have python installed on your system. (`python3.8^`)

2. Make sure pipenv is installed:

run `pip install --user pipenv`

3. Clone this repository:

4. Install dependencies:

run `pipenv install`

5. Create `.env`

The `.env` file must contain `DISCORD_TOKEN=` followed by the corresponding token. 
If `DATABASE_URL` is not specified the database will be stored in memory and be lost upon a bot restart (good for testing).
Alternatively an url like `sqlite:///database.sqlite3` can be provided to make a persistent database.
Optionally `COMMAND_PREFIX` and `LOGLEVEL` can be specified.

6. Start the bot:

run `pipenv run bot`

## Contributing

To keep files tidy and consistent `black` is used for formatting. Black is included in the dev packages `pipenv install --dev`.
After working on code please run `pipenv run fmt` to format all python files.

### Writing custom commands

Commands can be added to the bot by adding a decorator to any function located in the commands folder. An example is given below:
```py
from tools.wrapper import Response
import discord

@Command(["command", "alias1", "alias2"], category="Category", hidden=False)
async def command(contents, message, client, *_args, **_kwargs):
    """ This __docstring__ will show up as help text. """
    if contents[0] = 'ping':
        return 'pong'
    else:
        r = Response()
        r.embed = discord.Embed()
        return r
```

In this example `command` is the name listed when `!help` is called, the other items in the list are added as `(alias1, alias2)`. `category` determines under which category the commands are listed in the help message and `hidden` denotes whether it is visible at all (in help, invisible commands are still usable unless whitelists are used).

Every command is passed a set of arguments. In order: 
- the `contents` of the message as a list of strings. Reconstructing is possible with `join()`. An `!echo` command would be `return ' '.join(contents)`.
- the `message` being the original message, in addition to the contents this also contains information about the author, channel etc.
- the `client` for some advanced functionality the client might be needed as such it is passed.
- the `sqlalchemy database session` information on how to use sqlalchemy can be found in the sqlalchemy documentation: (https://www.sqlalchemy.org/library.html#reference)

Sometimes not all arguments are needed and if needed more arguments can be added as such it is safer to 'collect' all remaining arguments with `*_args` and `**_kwargs` the `_` denotes that the values arent actually used.

Because discord allows for some interesting response types, such as embed or files, a wrapper called Response is provided. Simply setting the `embed` or `files` variables to the `discord.py` wrappers is sufficient in this case.

For a reference on how to create embeds or post files please refer to the `discord.py` documentation. (https://discordpy.readthedocs.io/en/latest/index.html)
