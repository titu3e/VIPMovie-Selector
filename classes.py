#!/usr/bin/env python3

import os, json, msg, re


class Chat:

    def __init__(self, chatId):
        self.Id = str(chatId)
        self.path = 'data/' + self.Id + '/'


class Movie:

    def __init__(self, titleId, chatId):
        self.chat = Chat(chatId)
        self.titleId = titleId
        self.URL = 'https://www.imdb.com/title/' + self.titleId
        self.recs = self.getRecs()
        self.json = self.getJson()
        self.name = self.json['name']
        self.genre = self.getGenre()
        self.keywords = self.getKeywords()
        self.director = self.getDirector()
        self.actor = self.getActor()
        self.info = self.getInfo()

    def getRecs(self):
        recs = []
        pattern = re.compile(r"title/tt\d+/")
        cmd = 'curl -Ls ' + self.URL
        with os.popen(cmd) as p:
            output = ''
            line = p.readline()

            while line:
                if '<div class="article" id="titleRecs">' in line:
                    line = p.readline()
                    while '<div class="rec_overviews">' not in line:
                        line = p.readline()
                        match = pattern.search(line)
                        if match:
                            titleId = match[0].split('/')[1]
                            recs.append(titleId)
                    break
                line = p.readline()

        recs = list(set(recs))

        return recs


    def getJson(self):
        cmd = 'curl -Ls ' + self.URL
        with os.popen(cmd) as p:
            output = ''
            line = p.readline()

            while line:
                if '<script type="application/ld+json">{' in line:
                    output += '{\n'
                    line = p.readline()
                    while '</script>' not in line:
                        output += line
                        line = p.readline()
                    break
                line = p.readline()

        output += '}'
        output = json.loads(output)

        return output

    def getGenre(self):
        json = self.json

        if 'genre' in json.keys():
            genre = json['genre']
            if type(genre) == str:
                return genre
            elif type(genre) == list:
                return ', '.join(genre)
            else:
                return
        else:
            return

    def getKeywords(self):
        json = self.json

        if 'keywords' in json.keys():
            keywords = json['keywords']
            if type(keywords) == str:
                return keywords.replace(',',', ')
            elif type(keywords) == list:
                return ', '.join(keywords)
            else:
                return
        else:
            return

    def getDirector(self):
        json = self.json

        if 'director' in json.keys():
            director = json['director']
            if type(director) == dict:
                return director['name']
            elif type(director) == list:
                directors = []
                for i in json['director']:
                    directors.append(i['name'])
                return ', '.join(directors)
            else:
                return

    def getActor(self):
        json = self.json

        if 'actor' in json.keys():
            actor = json['actor']
            if type(actor) == dict:
                return actor['name']
            elif type(actor) == list:
                actors = []
                for i in json['actor']:
                    actors.append(i['name'])
                return ', '.join(actors)
            else:
                return

    def getInfo(self):
        name = self.name
        director = self.director
        actor = self.actor
        genre = self.genre
        keywords = self.keywords

        output = msg.filminfo.format(name, director, actor, genre, keywords)
        output += self.URL

        global most_recent
        most_recent[self.chat.Id] = self

        return output


most_recent = {}
