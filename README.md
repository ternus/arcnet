ARCNET: a comprehensive webapp for an Assassins' Guild ten-day
==============================================================

ARCNET is a complex, multifaceted webapp written in January 2010 for
the [MIT Assassins' Guild][] ten-day game "Arcadia Rising."  I
([Christian Ternus][]) wrote it over the course of ~a month under
heavy time pressure; please forgive the resulting roughness.


Though written to Arcadia's specs, many pieces of this webapp may be
useful to you if you're running a similar game.  It's written in
Django (albeit an earlier version, see below); if you know Django,
you'll probably be OK.  

A breakdown of key directories and files follows.  The code is broken
out into several Django apps, possibly allowing you to grab only what
you need and leave the rest behind.

* `core/`: the central character model on which everything else
          depends.  If you're reusing this code, you want this.
          Includes code for character profiles.
* `cyber/`: the hacking mechanic, including ICE, the hacking
          obstacles: sudoku, word search, "Social Engineering," etc.
          There are a number of clever tricks here.
* `elog/`: a unified event logging system, used to notify
          characters, the public, and the GMs when stuff happens.
* `mail/`: a complete player-to-player mail system.  Supports
          anonymous mail at the cost of computrons (a game currency).
* `media/`: blog-style posting, uploading of video and audio,
	   and the Public Opinion mechanic.
* `pedia/`: the Arkipedia, a compilation of information about
          the Arcadia station.  Might be useful for an in-game
	  reference.
* `research/`: the research mechanic, including ultra-spiffy
          auto-generated research tree images, colorized for your
          pleasure.
* `templates/`: templates are not split out by app, so you'll
          need to pull the ones you want from here.  All the static
          images and so forth live in here.
* `settings.py`: the Django settings file
* `test.py`: the game database initialization code.  Check
          this to see what sorts of data we populated Arcadia with.

This code was written using Django 0.96.  It probably needs some
serious updating to work with any newer version.  It also may have odd
dependencies; good luck.

This code is released under the GNU General Public License version 2.
If you use it for your game, I'd appreciate a mention, and I'd
definitely appreciate you forking this code on GitHub and making your
improvements public (once your game has run, of course.)

THIS CODE COMES WITH NO WARRANTY OR PROMISE OF FUNCTIONALITY
WHATSOEVER. IT IS ALMOST CERTAINLY INSECURE. IT MAY BREAK ON DAY
EIGHT, REVEAL SECRETS TO YOUR PLAYERS, COMPROMISE YOUR SERVER, AND
KICK YOUR PUPPY. NEITHER THE AUTHORS NOR THE MIT ASSASSINS' GUILD
ASSUME ANY LIABILITY WHATSOEVER FOR ANYTHING YOU DO WITH THIS CODE.
DON'T COME CRYING TO ME IF IT DOESN'T WORK.

Enjoy!

-ternus 

December 2012

[MIT Assassins' Guild]: http://www.mit.edu/~assassin/
[Christian Ternus]: http://cternus.net
