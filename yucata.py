#!/usr/bin/python
# -*- encoding: utf8 -*-

# © 2014 Joachim Breitner
# License: MIT (see LICENSE)

import urllib
import urllib2
import cookielib
import xdg.BaseDirectory
import os.path
import ConfigParser
import getpass
import json
import webbrowser
import re

# setup
cookiefile = os.path.join(xdg.BaseDirectory.save_data_path("yucata-tools"), "cookies")
cookiejar =cookielib.LWPCookieJar(cookiefile)
try:
    cookiejar.load()
except IOError:
    pass

br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
br.addheaders = [('User-agent', 'yucata-tools (https://github.com/nomeata/yucata-tools)')]


configfile = os.path.join(xdg.BaseDirectory.save_config_path("yucata-tools"), "config.ini")
config = ConfigParser.RawConfigParser()
config.read(configfile)

if not config.has_section('Login'):
    config.add_section('Login')

login = None
if config.has_option('Login', 'username'):
    login = config.get('Login', 'username')


def get_cookie():
    global login
    prompt = "Login [%s]: " % login if login else "Login: "
    thelogin = raw_input(prompt)
    if thelogin:
        login = thelogin
    password = getpass.getpass()

    config.set('Login', 'username', login)
    config.write(file(configfile, 'wb'))

    page = br.open("http://www.yucata.de/de").read()

    data ={
        "ctl00$ctl07$edtLogin": login,
        "ctl00$ctl07$edtPassword": password,
        "ctl00$ctl07$cbxCookie": 'on',
        "ctl00$ctl07$btnLogin": "Anmelden",
        }

    for name in ('__VIEWSTATE', '__VIEWSTATEGENERATOR'):
        field_re = re.compile(r'id="%s" value="([^"]+)"' % name)
        m = field_re.search(page)
        if not m:
            raise Exception("No %s found" % name)
        data[name] = m.group(1)

    query = urllib.urlencode(data)
    page = br.open("http://www.yucata.de/de",query).read()
    cookiejar.save()

def try_get_games():
    try:
        resp = br.open("http://www.yucata.de/Services/YucataService.svc/GetCurrentGames", data="")
        return resp.read()
    except urllib2.HTTPError as e:
        if int(e.code) == 500:
            return None
        else:
            raise
        
def get_games():
    games = try_get_games()
    if games is None:
        print ("Cannot fetch games. Trying to log in first.")
        get_cookie()
        games = try_get_games()
    if games is None:
        print ("Sorry, cannot fetch games")
        return

    data = json.loads(games)
    #print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    games = data["d"]["Games"]
    games_on_turn = []
    next_game = None

    next_game_id = data["d"]["NextGameOnTurn"]

    for g in games:
        on_turn = g["PlayerOnTurn"]
        for p in g["Players"]:
            if p["PlayerID"] == on_turn and p["Login"] == login:
                games_on_turn.append(g)
        if g["ID"] == next_game_id:
            next_game = g

    print("%d games are running, you can move at %d games" % (len(games), len(games_on_turn)))
    if next_game:
        print(u"You now have to move at a game of %s." % next_game["GameName"])
        url = "http://www.yucata.de/de/Game/%d" % next_game_id
        print("Opening %s..." % url)
        webbrowser.open(url)

get_games()
