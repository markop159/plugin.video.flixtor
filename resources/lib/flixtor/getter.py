'''
all file downloading and channels extracting is done here
'''
# external imports
import sys, os
import requests
import xbmc, xbmcplugin, xbmcaddon, xbmcgui
from bs4 import BeautifulSoup
from flixtor.javascript import translate, getKey

# addon variables
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__handle__ = int(sys.argv[1])

# domain
_domain_ = 'https://flixtor.se'

s = requests.Session()

def getMovies(command, page=1, search=None):
    xbmc.log(msg="Test Message", level=xbmc.LOGINFO)

    if command == 'Home':
        moviesURL = '%s/home' %_domain_
    elif command == 'Movies':
        moviesURL = '%s/ajax/show/movies/all/from/1900/to/2099/rating/0/votes/0/language/all/type/all/genre/all/latest/page/%s' %(_domain_, page)
    elif search == None:
        moviesURL ='%s/ajax/show/movies/all/from/1900/to/2099/rating/0/votes/0/language/all/type/all/genre/%s/latest/page/%s' %(_domain_, command, page)
    else:
        moviesURL ='%s/ajax/show/search/%s/from/1900/to/2099/rating/0/votes/0/language/all/type/all/genre/all/latest/page/%s' %(_domain_, search, page)
    movies = s.get(moviesURL)
    xbmc.log("Movies: %s" %movies.text,2)
    soup = BeautifulSoup(movies.text, 'html.parser')

    div_movies = soup.find_all('div', attrs={'class': 'py-2'}) #all movies

    items = []

    for movie in div_movies:
        # parse each movie to json
        #xbmc.log("Movie: %s" %movie,2)
        try:
            title = movie.find('div', {'class': 'p-0 card-text title sh1'}).text
            year = movie.find('div', {'class': 'p-0 card-text t12 sh1'}).text
            genres = movie.find('div', {'class': 'p-0 card-text mt-auto mx-2 t10 genres sh1'}).text
            image = movie.find('img', {'class': 'card-img-top'})['src']
            movie_id = movie.find('span', {'class': 'favorite fa-fw t14 text-info pointer'})['data-pid']
            try:
                ytlink = movie.find('span', {'class': 'ytt fa fa-youtube-play fa-2x fa-fw text-danger pointer'})['data-ytlink']
            except:
                ytlink = None

            xbmc.log("Movie: %s; %s; %s; %s; %s" %(title,year,genres,image,movie_id),2)

            items.append({
                'title': title,
                'year': year,
                'genres': genres,
                'image': image,
                'movie_id': movie_id,
                'ytLink': ytlink
                })
        except:
            continue

    xbmc.log("Items: %s" %items,2)
    return items

def getTVShows(command, page=1, search=None):
    xbmc.log(msg="Test Message", level=xbmc.LOGINFO)

    if command == 'Home':
        showsURL = '%s/home' %_domain_
    elif command == 'Movies':
        showsURL = '%s/ajax/show/tvshows/all/from/1900/to/2099/rating/0/votes/0/language/all/type/all/genre/all/latest/page/%s' %(_domain_, page)
    elif search == None:
        showsURL ='%s/ajax/show/tvshows/all/from/1900/to/2099/rating/0/votes/0/language/all/type/all/genre/%s/latest/page/%s' %(_domain_, command, page)
    else:
        showsURL ='%s/ajax/show/search/%s/from/1900/to/2099/rating/0/votes/0/language/all/type/all/genre/all/latest/page/%s' %(_domain_, search, page)
    shows = s.get(showsURL)
    xbmc.log("Movies: %s" %shows.text,2)
    soup = BeautifulSoup(shows.text, 'html.parser')

    div_shows = soup.find_all('div', attrs={'class': 'py-2'}) #all movies

    items = []

    for show in div_shows:
        # parse each movie to json
        #xbmc.log("Movie: %s" %movie,2)
        try:
            title = show.find('div', {'class': 'p-0 card-text title sh1'}).text
            year = show.find('div', {'class': 'p-0 card-text t12 sh1'}).text
            genres = show.find('div', {'class': 'p-0 card-text mt-auto mx-2 t10 genres sh1'}).text
            image = show.find('img', {'class': 'card-img-top'})['src']
            show_url = show.find('div', {'class': 'cflip m-0 link2'})['data-href']
            try:
                ytlink = show.find('span', {'class': 'ytt fa fa-youtube-play fa-2x fa-fw text-danger pointer'})['data-ytlink']
            except:
                ytlink = None

            xbmc.log("TV Show: %s; %s; %s; %s; %s" %(title,year,genres,image,show_url),2)

            items.append({
                'title': title,
                'year': year,
                'genres': genres,
                'image': image,
                'show_url': show_url,
                'ytLink': ytlink
                })
        except:
            continue


    #xbmc.log("Movies headers: %s" %movies.headers,2)
    #xbmc.log("Movies Cookies: %s" %movies.cookies,2)
    #xbmc.log("Movies Text: %s" %movies.text,2)
    #xbmc.log("Movies Text: %s" %div_movies,2)

    xbmc.log("Items: %s" %items,2)
    return items

def getSeasons(show_id):
    seasons = ''

def getEpisodes(show_id):
    episode = ''

def getMovie(movie_id):
    key = getKey()
    clrnc2 = 'mr3jnfsgluajmqndtc0tlgoh8m'
    s.get('%s/watch/movie/%s' %(_domain_, movie_id))
    clrnc = s.cookies.get_dict()['_clrnc']
    url = '%s/ajax/v4/m/%s?_=%s' %(_domain_, movie_id, key)
    path = "/ajax/v4/m/%s?_=%s" %(movie_id, key)
    cookie = "_clrnc=%s; _pk_id.1.6ee3=e8c493139aa2c07a.1628233034.; _pk_ses.1.6ee3=1" %clrnc

    headers = {
    "method":"GET",
    "authority":"flixtor.se",
    "scheme":"https",
    "path":path,
    "pragma":"no-cache",
    "cache-control":"no-cache",
    "accept":"text/plain, */*; q=0.01",
    "x-requested-with":"XMLHttpRequest",
    "sec-ch-ua-mobile":"?0",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62",
    "sec-fetch-site":"same-origin",
    "sec-fetch-mode":"cors",
    "sec-fetch-dest":"empty",
    "referer":"https://flixtor.se/home",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"en-US,en;q=0.9,sl;q=0.8",
    "cookie": cookie
    }
    xbmc.log("Headers: %s" %headers,2)
    ajaxCall = s.get(url, headers=headers)
    xbmc.log("Ajax v4: %s" %ajaxCall.text,2)

    movieJson = translate(ajaxCall.text)
    xbmc.log("Movie: %s" %movieJson,2)

    return movieJson

def getUserInput():
    keyboard = xbmc.Keyboard()
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        input = keyboard.getText()
    return input
