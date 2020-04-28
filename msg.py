#!/usr/bin/env python3


start = """
🤖 Usage:
/start show this message (alt. /help or /h)
/random pick movies from various lists (alt. /r)
/manage view or edit bot local data (alt. /m)
/info about this bot (alt. /i)

🔍 Search:
/film <film title> (alt. /find or just /f)
/who <person name>
both can cycle through results by adding +N after the query,
e.g. <bela lugosi +1>
"""

info = """
📜 What it does:

Besides randomly picking popular (or less popular) movies from IMDb listings, this bot basically does three things:

- it searches for movies with /f
- it remembers what you liked with /l
- it saves what you'd like to watch next with /s

Then, you can:

- randomly pick movies from your watch list with the /rw command
- based on what you liked, randomly pick a recommended movie with /rr

Everything else deals with managing lists with /m.

🛠 Other commands:
/check test the integrity of bot local data
/upgrade sync data with the latest IMDb version
/git to get a link to the public repository. 
"""

github = """
If you like this bot, say hi to its creator @rpolve 👨‍💻

https://github.com/rpolve/telegram-movie-bot
"""

random = """
👉 Based on your data:
/rr pick a random recommentation
/rw pick a movie from the watch list
/rt pick a movie you already liked
/re pick from last mentioned movie's IMDb recommendations

🎲 Random pick:
/r100 any movie with at least 100,000 votes
/r10 same but 10,000 votes
/r1 at least 1,000 votes
/ra any movie with non empty attributes
/tr true random
"""

manage = """
🍿 Edit:
/like store last mentioned movie (alt. /l)
/save add movie to the watch list (alt. /s)
/erase remove all traces of last mentioned movie

📽 View:
/last show most recently liked movies
/watch show watch list (alt. /w)
/top show most liked Actors, Directors, Genres or Keywords

💪 Mass actions:
/import <list> lets you import a list of movies, see /how2i
/export sends you a zipped archive with your data 
/forget empties all lists ⚠
"""

filminfo = """
Title: {}
Director: {}
Cast: {}
Genre: {}
Keywords: {}

👍 /like this movie or /save it for later

"""

how2i = """
💡 How to /import:

The import function allows for liking movies en masse. It takes as argument a whitespace separated list of title Ids, such as <tt0033467 tt0056801 tt0054215 ...> and so on.

Depending on lenght, it could take a while, but you'll be notified when it's done importing.

With <latest> as an argument, you can also try to restore the latest data set if you emptied all data by mistake.

With <backup> as an argument, it will attempt to import a fixed list of movies. This is mainly for testing purposes.
"""

gotnothing = """
Sorry, I've got nothing. 🤦
"""

forgetful = """
Sorry, I don't remember any /film. 😰\nTry searching for it!
"""

missingarg = """
Missing argument. 🙄 See /help.
"""

notfound = """
Not found. 🙁
"""

emptylist = """
Empty list. 🤷

See /how2i for more information.
"""

readcharts = """
Do you want to see top (A)ctors, (D)irectors, (G)enres or (K)eywords?
"""

cleanslate = """
Sometimes it's better to begin with a clean slate... 💣

See /how2i in order to undo.
"""

erase1 = """
Done. {} movie{} been erased from my memory. 🧠
"""

erase2 = """
\"{}\" has been erased from my memory. 🧠
"""

donefetching = """
Fetching complete. 

Imported {} movies, {} directors, {} actors, {} genres and {} keywords.
"""

datacheckpassed = """
{}/{} checked: everything ok. ✅
"""

datacheckfailed = """
{}/{} checked: something went wrong... 🤯

/upgrade the data base version to restore.
"""

nothingtodo = """
Nothing to do here. 😎
"""

dbrestored = """
Data base version upgraded. /check integrity?
"""

alreadyliked = """
You already liked \"{}\".
"""

alreadysaved = """
You already saved \"{}\".
"""

watchlist = """
🍿 Your watch list:

"""

showlast = """
👍 Your last liked movies:

"""

similarto = """
Similar to \"{}\" by {}:
"""
