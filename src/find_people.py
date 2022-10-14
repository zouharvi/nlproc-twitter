#!/usr/bin/env python3

from twitter import *
from keys import *
import subprocess
import argparse

args = argparse.ArgumentParser()
args.add_argument(
    "-p", "--page", type=int,
    help="Which page to start from", default=1
)
args.add_argument("-q", "--query", default="#NLProc")
args = args.parse_args()

t = Twitter(
    auth=OAuth(
        token=ACCESS_TOKEN, token_secret=ACCESS_TOKEN_SECRET,
        consumer_key=API_KEY, consumer_secret=API_KEY_SECRET
    ),
    retry=True,
)

buffer = 0
opened = set()
for page in range(args.page, args.page + 20):
    print("\nPage", page)
    result = t.users.search(q=args.query, count=20, page=page)
    for user in result:
        if user["following"]:
            continue
        if user["friends_count"] < 0.75 * user["followers_count"]:
            continue
        if user["followers_count"] < 50:
            continue

        # fetch timeline
        # will fail if profile is private
        try:
            user_timeline = t.statuses.user_timeline(
                screen_name=user['screen_name'])
            last_active = max([
                int(tweet["created_at"].split()[-1])
                for tweet in user_timeline
            ] + [0])

            if last_active < 2022:
                continue
        except:
            continue

        if user['screen_name'] in opened:
            print("No more users found")
            exit()
        opened.add(user['screen_name'])

        print(
            f"https://www.twitter.com/{user['screen_name']}  ({user['name']})"
        )
        print(
            'Following/followers:',
            f'{user["friends_count"]} / {user["followers_count"]}'
        )
        print("Description:        ", user['description'].replace("\n", "\\n"))
        print("Last activity:      ", last_active)

        if buffer >= 10:
            buffer = 0
            response = input("Continue with the next batch? [y/n]")
            if len(response) > 0 and response.lower()[0] == "y":
                pass
            else:
                exit()

        buffer += 1
        subprocess.Popen(
            [
                "flatpak", "run", "org.mozilla.firefox", "--",
                f"https://www.twitter.com/{user['screen_name']}"
            ],
            stderr=subprocess.DEVNULL
        )
