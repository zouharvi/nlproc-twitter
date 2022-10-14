#!/usr/bin/env python3

import tqdm
from twitter import *
from keys import *
import subprocess
import argparse

args = argparse.ArgumentParser(
    description="Provide links to people you follow but which have been inactive since 2020"
)
args.add_argument("--id", default="2603766076")
args.add_argument("--cursor", default="-1")
args.add_argument("--no-wait", action="store_true")
args = args.parse_args()

t = Twitter(
    auth=OAuth(
        token=ACCESS_TOKEN, token_secret=ACCESS_TOKEN_SECRET,
        consumer_key=API_KEY, consumer_secret=API_KEY_SECRET
    ),
    retry=True,
)

cursor = args.cursor
while True:
    print("Current cursor is", cursor)
    response = t.friends.list(user_id=args.id, cursor=cursor)
    cursor = response["next_cursor"]

    for user in tqdm.tqdm(response["users"]):
        # get relationship
        relationship = t.friendships.show(
            target_id=user["id"], source_id=args.id
        )["relationship"]
        twitter_url = f"https://www.twitter.com/{relationship['target']['screen_name']}"

        # skip if I don't follow them (should not happen given friends.list filter)
        if not relationship["target"]["followed_by"]:
            continue

        # skip if they follow me
        if relationship["target"]["following"]:
            continue

        # fetch timeline
        user_timeline = t.statuses.user_timeline(
            screen_name=user['screen_name'])
        last_active = max([
            int(tweet["created_at"].split()[-1])
            for tweet in user_timeline
        ] + [0])

        if last_active >= 2021:
            continue

        twitter_url = f"https://www.twitter.com/{user['screen_name']}"
        print(f"{twitter_url:<40}  ({user['name']})")
        print("Last active:", last_active)
        subprocess.Popen(
            [
                "flatpak", "run", "org.mozilla.firefox", "--",
                f"https://www.twitter.com/{user['screen_name']}"
            ],
            stderr=subprocess.DEVNULL
        )

        # TODO: There's an access right issue here. Need to use CLIENT_{ID,SECRET}
        # response = input("Unfollow? [y/n]")
        # if len(response) > 0 and response.lower()[0] == "y":
        #     t.friendships.destroy(user_id=user["id"])

    if not args.no_wait:
        print("Next page?")
        input()
