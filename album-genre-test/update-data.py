#Get data ready for analysis 

import json
import requests , re , random , os ,time

"""

Ways to compare songs : 

genre

duration

word count

word/duration ratio

year

rhyme detection 
    https://github.com/michaelfromyeg/RapViz
    https://www.readcube.com/articles/10.18061%2F1811%2F48548
    



////////////////////////////////////////////////////////////////////

wiki page format : 
https://en.wikipedia.org/wiki/So_Cold_(Breaking_Benjamin_song)
https://en.wikipedia.org/wiki/Starships_(song)



https://en.wikipedia.org/w/rest.php/v1/search/page?q=frank sinatra One for My Baby (And One More for the Road)



https://en.wikipedia.org/w/rest.php/v1/search/page?q=frank%20sinatra%20One%20for%20My%20Baby%20(And%20One%20More%20for%20the%20Road)


26171131

26171131

1979060



https://en.wikipedia.org/w/index.php?curid=1979060





https://en.wikipedia.org/wiki/starships_nicki_minaj



https://en.wikipedia.org/wiki/So_Cold_(Breaking_Benjamin_song)


///////////////////////////////////////////////////////////////////
- i can get duration from deezer

- i can make a function to get word count in lyrics 

- do i want to include word to song length ratio

- need to get year


https://api.deezer.com/search?q=track:"socold"artist:"breakingbenjamin"


13711277

https://api.deezer.com/track/13711277

"""