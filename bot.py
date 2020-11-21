#!venv/bin/python3

import json
import telebot
import feedparser
import argparse
import os
import time
import re

config_file = "config.json"
cache_file = ".mycache"

def escape_markdown(text: str,  entity_type: str = None) -> str:
    if entity_type in ['pre', 'code']:
        escape_chars = r'\`'
    elif entity_type == 'text_link':
        escape_chars = r'\)'
    else:
        escape_chars = r'_*[]()~`>#+-=|{}.!'

    return re.sub('([{}])'.format(re.escape(escape_chars)), r'\\\1', text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tar's Simple RSS Telegram Bot")
    parser.add_argument("--debug", action="store_true", help="don't send via telegram, print to stdout instead", dest="debug")

    args = parser.parse_args()

    # load config with feeds and telegram token
    with open("config.json", "r") as f:
        config = json.load(f)

    # create cache file if it not exists
    if not os.path.exists(cache_file):
        with open(cache_file, "w+") as f:
            f.write("{}")

    # read cache file
    with open(cache_file, "r") as f:
        cache = json.load(f)

    for feed in config["feeds"]:
        url = feed["feed_url"]
        f = feedparser.parse(url)
        posts = []

        # add to cache if not already in there
        if not url in cache.keys():
            cache[url] = { "last_update" : 0 }

        newest_time = cache[url]["last_update"]

        # iterate all posts until an old one is found
        for i in range(len(f.entries)):
            post = f.entries[i]

            old_time = cache[url]["last_update"]
            new_time = time.mktime(post.published_parsed)

            if new_time > old_time:
                title = escape_markdown(feed["title"])
                author = escape_markdown(feed["author"])
                post_published = escape_markdown(post.published)
                post_title = escape_markdown(post.title)
                post_link = escape_markdown(post.link, "text_link")

                message = "Update for *{}* by *{}*, posted {}\n".format(title, author, post_published)
                message += "[{}]({})".format(post_title, post_link)

                posts.append(message)

                # keep newest published date for cache
                newest_time = max(new_time, newest_time)
            else:
                break

        cache[url]["last_update"] = newest_time
        bot = telebot.TeleBot(config["token"])

        # start with oldest new post
        posts.reverse()
        for post in posts:
            try:
                if args.debug:
                    print(post)
                else:
                    bot.send_message(feed["chat_id"], post, parse_mode="MarkdownV2")
            except Exception as e:
                print(e)

    # write newest post's timestamp to cache
    with open(cache_file, "w+") as f:
        json.dump(cache, f)

    exit(0)