# NLProc Twitter

A small script to find people on Twitter which (1) tweet about things that I'm interested in, (2) have non-protected profiles and (3) are active.

## Usage

1. Follow [@zouharvi](https://twitter.com/zouharvi) on Twitter.
2. Fill `src/keys_mock.py` with your credentials and rename it to `src/keys.py` .
3. Run `src/main.py -q "NLProc"` to find people who have _NLProc_ in their bio. The program will automatically open the Twitter profile page<sup>1</sup> of the first 10 hits and then asks you again if you'd like to continue.<sup>2</sup>

- <sup>1</sup> I'm using Firefox in Flatpak. You may need to change the call (in `src/main.py`) to fit your setup.
- <sup>2</sup> The way I use it is to further check whether I want to follow someone in the browser and then go back to the script for another batch of 10 profiles.


## TODO

- Have a script that turns `.bib` file of a publication to a list of links to author Twitter profiles.