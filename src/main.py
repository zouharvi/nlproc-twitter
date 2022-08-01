#!/usr/bin/env python3

from twitter import *
from keys import *
import subprocess

t = Twitter(
    auth=OAuth(
        token=ACCESS_TOKEN, token_secret=ACCESS_TOKEN_SECRET,
        consumer_key=API_KEY, consumer_secret=API_KEY_SECRET
    )
)

start_page = int(input("Which page to start from? E.g. 11: "))

for page in range(start_page, 100+1):
    print("Page", page)
    result = t.users.search(q="#NLProc", count=20, page=page)
    for user in result:
        if not user["following"] and user["friends_count"] / user["followers_count"] >= 0.75 and user["followers_count"] >= 20:
            print(f"https://www.twitter.com/{user['screen_name']}  ({user['name']}):  ", f'{user["friends_count"]} / {user["followers_count"]}', user['description'])

            if input("Open? ").lower()[0] == "y":
                subprocess.Popen(["flatpak", "run", "org.mozilla.firefox", "--", f"https://www.twitter.com/{user['screen_name']}"], stderr=subprocess.DEVNULL)