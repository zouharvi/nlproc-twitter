# NLProc Twitter

A bunch of small scripts to:
- Find authors on Twitter which you cite in your work.
- Find people on Twitter which tweet about things that I'm interested in.
- Unfollow inactive people

## Usage

Prerequisites:

1. Follow [@zouharvi](https://twitter.com/zouharvi) on Twitter.
2. Install `pip3 install -r requirement.txt`
3. Fill `src/keys_mock.py` with your credentials and rename it to `src/keys.py` .

### Usage (Find Authors)

Run `src/find_authors.py -b path_to_bibfile.bib` to get a list of links to cited authors which you do not yet follow.
This works also with `src/find_authors.py -a arxiv_link` and `src/find_authors.py -s semanticscholar_link` .

### Usage (Find People)

Run `src/find_people.py -q "NLProc"` to find people who have _NLProc_ in their bio. The program will automatically open the Twitter profile page<sup>1</sup> of the first 10 hits and then asks you again if you'd like to continue.<sup>2</sup>

- <sup>1</sup> I'm using Firefox in Flatpak. You may need to change the call (in `src/main.py`) to fit your setup.
- <sup>2</sup> The way I use it is to further check whether I want to follow someone in the browser and then go back to the script for another batch of 10 profiles.

## Misc.

- Why are Twitter credentials necessary? To access the API and also filter out profiles which you already follow.
- How do you get Twitter credentials? [This requires some reading](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api).