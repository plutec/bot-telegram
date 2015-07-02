# bot-telegram
Simple telegram reusable bot

https://core.telegram.org/bots

Create a new bot https://core.telegram.org/bots#create-a-new-bot
and then copy the token to the settings file.
##Install dependencies
```
pip install -r requirements.txt
```
##Configure bot
###Create Bot
Create you bot talking with **BotFather** (https://web.telegram.org/#/im?p=@BotFather)[https://web.telegram.org/#/im?p=@BotFather] saying /newbot. Then, he will ask about the parameters to create you bot (name and username).
###Set privacy
By default, your bot only receive commands that starts with / (slash). You can change this talking with **BotFather**, saying: /setprivacy, he will ask you about the bot to perform the action and about the option. In this case you need to **disable** the privacy.
