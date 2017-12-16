We only store the oauth-token as long as the app is installed.

The token is stored in a database.
This token is used for listening to messages in a channel (where the bot is member of).
This token is also used for writing/post messages in a channel as the bot.


As soon as you uninstall the bot, your token is removed from the database as well.