#!/usr/bin/env python3

from twitter import *
from keys import *
import subprocess
import argparse

args = argparse.ArgumentParser()
args.add_argument("--handle", default="zouharvi")
args = args.parse_args()

t = Twitter(
    auth=OAuth(
        token=ACCESS_TOKEN, token_secret=ACCESS_TOKEN_SECRET,
        consumer_key=API_KEY, consumer_secret=API_KEY_SECRET
    )
)

response = t.users.lookup(screen_name=args.handle)[0]
print(response["screen_name"], response["id"])