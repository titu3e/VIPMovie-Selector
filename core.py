#!/usr/bin/env python3

import os, classes, msg


def checkDb(target=''):
    if target == '':
        pass

    prefix, suffix = 'data/', '.tsv.gz'
    basics = 'movie.basics'
    ratings1k = 'title.ratings1k'
    ratings10k = 'title.ratings10k'
    ratings100k = 'title.ratings100k'
    N, N_ok = 0, 0

    for i in [basics, ratings1k, ratings10k, ratings100k]:
        i = prefix + i + suffix
        if os.path.isfile(i):
            N_ok += 1
        N += 1

    if N == N_ok and N == 4:
        return msg.datacheckpassed.format(N_ok, N)

    else:
        return msg.datacheckfailed.format(N_ok, N)


def prepDb(target=''):
    if target == '':
        pass

    check = checkDb('')
    if check[-15:] == msg.datacheckpassed[-15:]:
        return msg.nothingtodo

    prefix, suffix = 'data/', '.tsv.gz'
    basics = 'movie.basics'
    ratings1k = 'title.ratings1k'
    ratings10k = 'title.ratings10k'
    ratings100k = 'title.ratings100k'
    baseurl = 'https://datasets.imdbws.com/'

    b_test = os.path.isfile(str(prefix + basics + suffix))
    r1k_test = os.path.isfile(str(prefix + ratings1k + suffix))
    r10k_test = os.path.isfile(str(prefix + ratings10k + suffix))
    r100k_test = os.path.isfile(str(prefix + ratings100k + suffix))
    r_test = r1k_test and r10k_test and r100k_test

    if not b_test:
        filename = 'title.basics' + suffix
        source = baseurl + filename
        cmd = 'curl -Ls ' + source + ' -o data/' + filename + ' --create-dirs'
        os.system(cmd)
        cmd = 'zcat data/' + filename
        cmd += '| awk \'{if($2 == "movie" && $5 == 0) print $0}\' | gzip - >'
        cmd += prefix + basics + suffix
        cmd += '&& rm data/' + filename
        os.system(cmd)
    if not r_test:
        filename = 'title.ratings' + suffix
        source = baseurl + filename
        cmd = 'curl -Ls ' + source + ' -o data/' + filename + ' --create-dirs'
        os.system(cmd)
        for t in ['1', '10', '100']:
            cmd = 'zcat data/' + filename + '| sed 1d'
            cmd += '| awk \'{if($3 >= ' + t + '000) print $0}\' | gzip - >'
            cmd += prefix + 'title.ratings' + t + 'k' + suffix
            os.system(cmd)
        cmd = 'rm data/' + filename
        os.system(cmd)

    return msg.dbrestored


def upgradeDb(target=''):
    if target == '':
        pass

    check = checkDb('')
    if check[-15:] == msg.datacheckpassed[-15:]:
        prefix, suffix = 'data/', '.tsv.gz'
        basics = 'movie.basics'
        ratings1k = 'title.ratings1k'
        ratings10k = 'title.ratings10k'
        ratings100k = 'title.ratings100k'
        mtimelist = []
        from time import time
        epoch = time()
        for i in [basics, ratings1k, ratings10k, ratings100k]:
            i = prefix + i + suffix
            if os.path.isfile(i):
                mtimelist.append(os.path.getmtime(i))
        oldest = min(mtimelist)
        timediff = int(epoch - oldest)
        if timediff < 604800:
            return msg.nothingtodo
        else:
            cmd = 'rm -f data/*.tsv.gz'
            os.system(cmd)

    return prepDb('')


def recommend(target=''):
    if target == '':
        pass

    from classes import most_recent

    if chat.Id not in most_recent or not most_recent[chat.Id]:
        return msg.forgetful

    prev = most_recent[chat.Id]
    recs = most_recent[chat.Id].recs

    if recs == []:
        return msg.gotnothing

    from random import shuffle

    shuffle(recs)

    filename = chat.path + 'liked.movies.txt'
    if os.path.isfile(filename):
        with open(filename) as f:
            f = f.read().splitlines()
            N = len(f)
            for i in range(len(f)):
                f[i] = f[i].split()[0]
            liked = f
    else:
        liked = []

    filename = chat.path + 'watch.list.txt'
    if os.path.isfile(filename):
        with open(filename) as f:
            f = f.read().splitlines()
            for i in range(len(f)):
                f[i] = f[i].split()[0]
            watch = f
    else:
        watch = []

    filename = chat.path + 'recs.list.txt'
    if os.path.isfile(filename):
        with open(filename) as f:
            f = f.read().splitlines()
            for i in range(len(f)):
                f[i] = f[i].split()[0]
            recent = f
    else:
        recent = []

    N = int(N ** 1.6)
    N = min([N + 4, 100])
    N = str(N)

    for r in recs:
        if r in liked or r in watch or r in recent:
            continue
        r = classes.Movie(r, chat.Id)

        if r.json['@type'] == 'Movie':
            classes.most_recent[chat.Id] = r
            movie = r

            filename = chat.path + 'recs.list.txt'
            with open(filename, 'a') as o:
                o.write(movie.titleId + '\t' + movie.name + '\n')

            cmd = 'temp=`mktemp`;'
            cmd += 'tail -' + N + ' ' + filename + ' >$temp;'
            cmd += 'mv $temp ' + filename
            os.system(cmd)

            if target == 'direct':
                output = msg.similarto.format(prev.name, prev.director)
                output += movie.info
                return output
            else:
                return movie

    return msg.gotnothing


def getRand(dataset, basename='title', opener = 'zcat ', allowEmptyAttr=False):
    check = checkDb('')
    if check[-15:] == msg.datacheckpassed[-15:]:
        pass
    else:
        return checkDb('')

    if dataset[:5] == 'local':
        opener, filename = 'cat ', chat.path + 'liked.movies.txt'
        if not os.path.isfile(filename):
            return msg.gotnothing
    elif dataset == 'watchlist':
        opener, filename = 'cat ', chat.path + 'watch.list.txt'
        if not os.path.isfile(filename):
            return msg.gotnothing
    else:
        if dataset[:7] != 'ratings':
            if dataset == 'anymovie':
                allowEmptyAttr = True
            basename, dataset = 'movie', 'basics'

        filename = 'data/' + basename + '.' + dataset + '.tsv.gz'

    cmd = opener + filename + '| wc -l'
    with os.popen(cmd) as p:
        number_of_lines = p.read().rstrip()

    json = {}

    while not set(['genre', 'keywords', 'actor', 'director']) <= set(json.keys()):
        cmd = opener + filename + '| sed -n "`shuf -i1-' + number_of_lines + ' -n1`p"'
        with os.popen(cmd) as p:
            random_entry = p.read().rstrip()

        if random_entry[0:2] == 'tt':
            titleId = random_entry.split()[0]
            random_movie = classes.Movie(titleId, chat.Id)
            json = random_movie.json
            if json['@type'] != 'Movie':
                json = {}
                continue
            if allowEmptyAttr:
                break
        else:
            return

    if dataset == 'localrr':
        movie = recommend()
        if type(movie) == classes.Movie:
            output = msg.similarto.format(random_movie.name, random_movie.director)
            output += movie.info
            return output
        else:
            return msg.gotnothing

    return random_movie.info


def dbFind(query, category='tt'):
    if query == '':
        return msg.missingarg
    else:
        q = 0
        if '+' in query:
            query = query.split('+')
            q += int(query[1])
            query = query[0].rstrip()

    URL = 'https://www.imdb.com/find?s=' + category + '&q=' + query.replace(" ", "+")

    if category == 'tt':
        cmd = 'curl -Ls "' + URL + '" | grep -Eo \'/title/tt[0-9]+/\' | uniq'
    if category == 'nm':
        cmd = 'curl -Ls "' + URL + '" | grep -Eo \'/name/nm[0-9]+/\' | uniq'

    with os.popen(cmd) as p:
        output = p.read().splitlines()

    if len(output) == 0 or len(output) <= q:
        return msg.notfound

    from classes import most_recent
    if chat.Id in most_recent:
        title = most_recent[chat.Id]
        if title != None and title.titleId in output:
            output.remove('/title/' + title.titleId + '/')

    for i in output[q:]:
        if category == 'tt':
            titleId = i.split('/')[-2]
            movie = classes.Movie(titleId, chat.Id)
            if movie.json['@type'] != 'Movie': continue

            return movie.info

        elif category == 'nm':

            return str('https://www.imdb.com' + i)


def dbFindPerson(query):
    return dbFind(query, category='nm')


def save(target=''):
    if target == '':
        pass

    from classes import most_recent

    if chat.Id not in most_recent or not most_recent[chat.Id]:
        return msg.forgetful
    else:
        movie = most_recent[chat.Id]

    if os.path.isfile(str(chat.path + 'watch.list.txt')):
        with open(str(chat.path + 'watch.list.txt')) as f:
            f = f.read().splitlines()
            for l in f:
                if movie.titleId in l:
                    return msg.alreadysaved.format(movie.name)

    filename = chat.path + 'liked.movies.txt'
    if os.path.isfile(filename):
        cmd = 'sed -i /' + movie.titleId + '/d ' + filename
        os.system(cmd)

    key = '\n' + movie.titleId + '\t'

    with open(str(chat.path + 'watch.list.txt'), 'a',) as o:
        o.write(key[1:] + movie.name + '\n')

    return str('"' + movie.name + '" added to the watch list.')


def like(target=''):
    if target == '':
        pass

    from classes import most_recent

    if chat.Id not in most_recent or not most_recent[chat.Id]:
        return msg.forgetful
    else:
        movie = most_recent[chat.Id]

    if os.path.isfile(str(chat.path + 'liked.movies.txt')):
        with open(str(chat.path + 'liked.movies.txt')) as f:
            f = f.read().splitlines()
            for l in f:
                if movie.titleId in l:
                    return msg.alreadyliked.format(movie.name)

    key = '\n' + movie.titleId + '\t'

    with open(str(chat.path + 'liked.directors.txt'), 'a') as o:
        director = movie.director
        if director:
            director = key[1:] + director.replace(', ', key) + '\n'
            o.write(director)

    with open(str(chat.path + 'liked.actors.txt'), 'a') as o:
        actor = movie.actor
        if actor:
            actor = key[1:] + actor.replace(', ', key) + '\n'
            o.write(actor)

    with open(str(chat.path + 'liked.genres.txt'), 'a') as o:
        genre = movie.genre
        if genre:
            genre = key[1:] + genre.replace(', ', key) + '\n'
            o.write(genre)

    with open(str(chat.path + 'liked.keywords.txt'), 'a') as o:
        keywords = movie.keywords
        if keywords:
            keywords = key[1:] + keywords.replace(', ', key) + '\n'
            o.write(keywords)

    with open(str(chat.path + 'liked.movies.txt'), 'a',) as o:
        o.write(key[1:] + movie.name + '\n')

    filename = chat.path + 'watch.list.txt'
    if os.path.isfile(filename):
        cmd = 'sed -i /' + movie.titleId + '/d ' + filename
        os.system(cmd)

    return str('Ok! You liked "' + movie.name + '".')


def erase(target=''):
    cmd = 'ls -1 ' + chat.path + '*.txt 2>/dev/null'
    with os.popen(cmd) as p:
        filelist = p.read().splitlines()
    if len(filelist) == 0:
        return msg.gotnothing

    if target == '':
        pass
    elif target[:2] == '--' or target[0] == '—':
        target = target.replace('—', '--')
        target = target[2:].split()
        n, s = len(target), 's have'
        for i in target:
            for f in filelist:
                if i[:2] != 'tt':
                    n -= 1
                    continue
                cmd = 'sed -i /' + i + '/d ' + f
                os.system(cmd)

                if n == 1: s = ' has'

        return msg.erase1.format(max([n, 0]), s)

    from classes import most_recent

    if chat.Id not in most_recent or not most_recent[chat.Id]:
        return msg.forgetful

    for f in filelist:
        cmd = 'sed -i /' + most_recent[chat.Id].titleId + '/d ' + f
        os.system(cmd)

    movie_title = most_recent[chat.Id].name
    most_recent[chat.Id] = None

    return msg.erase2.format(movie_title)


def massLike(target=''):
    if target == '':
        return msg.emptylist
    elif target == 'latest':
        filename = chat.path + 'liked.movies.txt.lst'
        if not os.path.isfile(filename):
            return msg.gotnothing
        cmd = 'cut -f1 ' + filename
        with os.popen(cmd) as p:
            target = p.read()
    elif target == 'backup':
        filename = 'movies.bak'
        if not os.path.isfile(filename):
            return msg.gotnothing
        cmd = 'cut -f1 ' + filename
        with os.popen(cmd) as p:
            target = p.read()

    Nm, Nd, Na, Ng, Nk = 0, 0, 0, 0, 0

    for i in target.split():
        i = classes.Movie(i, chat.Id)

        if i.json['@type'] == 'Movie':
            like('')
            Nm += 1
            director = i.director
            if director:
                Nd += len(i.director.split(','))
            actor = i.actor
            if actor:
                Na += len(i.actor.split(','))
            genre = i.genre
            if genre:
                Ng += len(i.genre.split(','))
            keywords = i.keywords
            if keywords:
                Nk += len(i.keywords.split(','))

    output = msg.donefetching.format(Nm, Nd, Na, Ng, Nk)

    return output


def exportData(target=''):
    if target == '':
        pass

    filelist = ['actors', 'directors', 'genres', 'keywords', 'movies']
    for i in range(len(filelist)):
        filelist[i] = chat.path + 'liked.' + filelist[i] + '.txt'

    for f in filelist:
        if not os.path.isfile(f):
            return False, None

    archive = '/tmp/tmoviebot.' + str(chat.Id) + '.zip'
    cmd = 'cd ' + chat.path + ';'
    cmd += 'zip -r ' + archive + ' *.txt >/dev/null'
    os.system(cmd)

    return True, archive


def readCharts(target=''):
    if target == '':
        return msg.readcharts
    target = target[0].lower()

    filename = chat.path + 'liked.'
    if target == 'a': filename += 'actors'
    elif target == 'd': filename += 'directors'
    elif target == 'g': filename += 'genres'
    elif target == 'k': filename += 'keywords'
    else:
        return msg.readcharts
    filename += '.txt'

    if not os.path.isfile(filename):
        return msg.gotnothing

    cmd = 'cut -f2- ' + filename + '| sort | uniq -c | sort -nrk1 | head -10 | sed -E \'s/ +//\''
    with os.popen(cmd) as p:
        output = p.read()

    if output == '':
        return msg.gotnothing

    return output


def forget(target=''):
    if target == '':
        pass

    filename = chat.path + 'liked.movies.txt'
    if os.path.isfile(filename):
        cmd = 'mv ' + filename + '{,.lst}'
        os.system(cmd)

    cmd = 'rm -f ' + chat.path + '*.txt'
    os.system(cmd)

    return msg.cleanslate


def watchList(target=''):
    if target == '':
        pass

    filename = chat.path + 'watch.list.txt'

    if not os.path.isfile(filename):
        return msg.gotnothing

    cmd = 'cut -f2 ' + filename
    with os.popen(cmd) as p:
        output = p.read()

    if output == '':
        return msg.gotnothing

    return str(msg.watchlist + output)


def showLast(target=''):
    if target == '':
        pass

    filename = chat.path + 'liked.movies.txt'

    if not os.path.isfile(filename):
        return msg.gotnothing

    cmd = 'tail -10 ' + filename + '| cut -f2'
    with os.popen(cmd) as p:
        output = p.read()

    if output == '':
        return msg.gotnothing

    return str(msg.showlast + output)
