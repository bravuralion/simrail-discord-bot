# Simrail Discord Bot

This Discord bot is intended for Simrail Discord community servers. It shows in the current version the status of the signal boxes where they are currently not occupied. The bot uses the official status page of Simrail and updates itself if new signal boxes are added. It is planned to extend this bot even further and add more features. The community is invited to participate in the development.


# Current commands of the bot

 - **!set_channel** ID
	- This command tells the bot which channel it should use to post the updates.
 - **!stations** en/en/pl
	 - This command sets which server groups it should check for availability.

## Serverliste editieren

You can edit the server list with **!stations**. To do this, you need to adjust the server names at line 12 in the code at **server_sets**:

![enter image description here](https://github.com/mrpowershell/simrail-discord-bot/raw/main/img/server_lists.jpg)
## Installing the bot on a Discord server

First of all, you need to make sure that the server or hosting provider you want to run the bot on has Python available, since the bot is written in Python. If you don't have your own server, you can use https://bot-hosting.net/. You have to make sure that the packages **discord aiohttp asyncio** are installed. If not you can install them via **pip install PACKAGENAME**. In the example bot-hosting you can enter them under startup:

![enter image description here](https://github.com/mrpowershell/simrail-discord-bot/raw/main/img/packages.png)

In order to use the bot on a Discord server, you need to create a new application on [Discord Developer Portal](https://discord.com/developers). As soon as you have created your bot with your desired name, you have to copy the token via: 

![enter image description here](https://github.com/mrpowershell/simrail-discord-bot/raw/main/img/token.jpg)
Then insert the token here: `client.run('bot_secret_in_here')` at the very end of the script.

Next, you need to invite the bot to your server. To do this, go to OAuth2 -> Url Generator and select bot under Scopes. At Bot Permissions select either Administrator or at least Send Messages and Manage Messages. Then copy the url and open it in a new tab to invite the bot to your server:

![enter image description here](https://github.com/mrpowershell/simrail-discord-bot/raw/main/img/invite.jpg)

As soon as you start the bot, the following should be displayed in the console:

![enter image description here](https://github.com/mrpowershell/simrail-discord-bot/raw/main/img/botlog.jpg)
If an error appears here, either the token is not correct or you have forgotten to install a package. From now on the bot is ready for use.

Now go to the channel where the bot should post the updates. First write **!set_channel** and mark the channel. Then select the server group with **!stations de/en/pl** and the bot should start displaying the status message.

## Copyright

It would be nice if you don't remove the credit from the code. 



