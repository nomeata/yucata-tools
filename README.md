yucata-tools
============

This repository contains some inofficial tools that might be convenient for the
heavy user of the great and free online boardgame platform [yucata.de].

Use at your own risk!

These tools do not use official APIs, so they are likely to break regularly
when the server changes. Also, use them at a reasonable frequency, in order to
not have the server admins lock us out.

Features
--------

Currently, yucata-tools has only one feature: Opening the game you have to play
next in the browser. To use it, simply start the provided python script:

    $ ./yucata.py
    Cannot fetch games. Trying to log in first.
    Login: nomeata
    Password: 
    7 games are running, you can move at 1 games
    You now have to move at a game of Russian Railroads.
    Opening http://www.yucata.de/de/Game/4619291...
    
At this point, the browser will open this game. If there is no game where you
have to do a move, nothing happens.

The script will store the cookie, so the next time you will not have to log in
again. It does not store the password, though, so when the cookie expires, you
will be asked again for the password.

TODO
----

The code is not the cleanest. But for this simple task, that does not matter.

It has `/de/` hardcoded. If that bothers you, let me know.

I’d like to turn this into a small app for the SailfishOS, so that I can use it
on my [Jolla Phone].

[yucata.de]: http://yucata.de/
[Jolla Phone]: http://jolla.com/
 
