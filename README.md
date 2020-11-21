# Tar's RSS Feed Telegram Bot

Posts RSS feeds to Telegram channels or private chats.

## Setup Telegram Bot
* Create Telegram bot (@BotFather) to get API Key ("token")
* Write one message to your bot and get your "chat_id" from `https://api.telegram.org/bot<TOKEN>/getUpdates`

## Setup Python Bot
```bash
git clone https://github.com/TarEnethil/rss-telegram-bot.git
cd rss-telegram-bot
python3 -m venv venv
venv/bin/activate
pip install -r requirements.txt
cp config.json.template config.json
```

* Add "token" (Telegram Bot Token) to `config.json`
* configure feeds accoring to the template

## Setup cronjob
`crontab -e`

Examples:
```
# check for new feeds every hour
0 * * * * cd <path>/rss-telegram-bot && venv/bin/python bot.py
```


## Usage

```
usage: bot.py [-h] [--debug]

Tar's Simple RSS Telegram Bot

optional arguments:
  -h, --help  show this help message and exit
  --debug     don't send via telegram, print to stdout instead
```
