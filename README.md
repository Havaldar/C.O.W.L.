# C.O.W.L.

## What is this?
- Creates a large network of marvel comic book characters based on co-occurences 
- finds communitities of closely related characters based on input preferences
- finds the importance of each character in the partition to the story
- shows a graph of characters you should follow to get the best flavour for the character you want
- As well as their importance

## Why do this?
- I really like comics and whenever I try to get into a specific character I always feel I am missing out on her/his tangential stories.
- This way I can follow the group of characters that would give me the most information

## How did I do this?
- By repeated bisections of the social graph using the fiedler vector
- Followed only the half in which the node exists like binary search

## To Run:
- clone this repo
- make sure you have pip and virtualenv
- setup a virtualenv and activate it
- pip install -r requirements.txt
- python main.py <character-id-num> <num-of-characters-you-want-in-partition>
