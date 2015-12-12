# bergerbot

![Bergerbot](http://i.imgur.com/ICIOoty.png?2)

Discord chatbot using [discord.py](https://github.com/rapptz/discord.py). Powered partly by [chatterbot](https://github.com/gunthercox/ChatterBot). Created for Michael Berger

##Usage
I typically run via `pm2 start discord_main.py`. I find that (at least on my network) I occasionally run into Broken Pipe errors when running for extended periods of time. `pm2` will automatically restart bergerbot if it goes down.

