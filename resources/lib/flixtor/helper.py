'''
all file downloading and channels extracting is done here
'''
# external imports
import sys, os
import requests, json
import xbmc, xbmcplugin, xbmcaddon, xbmcgui
#import xmltodict
import time
import base64
import xml.etree.ElementTree as ET
from datetime import datetime as dt
from datetime import timedelta
from collections import defaultdict
from resources.lib import js2py
from urllib.request import unquote
from bs4 import BeautifulSoup


# addon variables
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__handle__ = int(sys.argv[1])

#_stream_file = os.path.join(__addondir__, 'video.strm')

s = requests.Session()
# internal imports
from flixtor.logging import log, LOGLEVEL, log_error

def getMovies(command):
    xbmc.log(msg="Test Message", level=xbmc.LOGINFO)

    #url = 'https://flixtor.se/home'
    if command == 'Home':
        moviesURL = 'https://flixtor.se/home'
    else:
        moviesURL ='https://flixtor.se/ajax/show/movies/all/from/1900/to/2099/rating/0/votes/0/language/all/type/all/genre/%s/latest/page/1' %command
    #moviesURL ='https://flixtor.se/home'
    movies = s.get(moviesURL)
    #xbmc.log("Movies: %s" %movies.cookies,2)
    #cookie = s.cookies
    soup = BeautifulSoup(movies.text, 'html.parser')

    div_movies = soup.find_all('div', attrs={'class': 'py-2'}) #all movies

    items = []
    #items.append(cookie.get_dict()['_clrnc'])

    for movie in div_movies:
        # parse each movie to json
        #xbmc.log("Movie: %s" %movie,2)
        try:
            title = movie.find('div', {'class': 'p-0 card-text title sh1'}).text
            year = movie.find('div', {'class': 'p-0 card-text t12 sh1'}).text
            genres = movie.find('div', {'class': 'p-0 card-text mt-auto mx-2 t10 genres sh1'}).text
            image = movie.find('img', {'class': 'card-img-top'})['src']
            movie_id = movie.find('span', {'class': 'favorite fa-fw t14 text-info pointer'})['data-pid']
            ytlink = movie.find('span', {'class': 'ytt fa fa-youtube-play fa-2x fa-fw text-danger pointer'})['data-ytlink']

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


    #xbmc.log("Movies headers: %s" %movies.headers,2)
    #xbmc.log("Movies Cookies: %s" %movies.cookies,2)
    #xbmc.log("Movies Text: %s" %movies.text,2)
    #xbmc.log("Movies Text: %s" %div_movies,2)

    #js = js2py.eval_js()
    #items.append({
    #'cookie':cookie
    #})
    xbmc.log("Items: %s" %items,2)
    return items

def getTVShows(handle):
    shows = ''

def getSeasons(show_id):
    seasons = ''

def getEpisodes(show_id):
    episode = ''

def getMovie(movie_id):
    key = getKey()
    #key = '1628660729095'
    #movie_id2 = '24475371'
    clrnc2 = 'mr3jnfsgluajmqndtc0tlgoh8m'
    s.get('https://flixtor.se/watch/movie/%s' %movie_id)
    clrnc = s.cookies.get_dict()['_clrnc']
    url = 'https://flixtor.se/ajax/v4/m/%s?_=%s' %(movie_id, key)
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

def translate(encoded_ajax):
    js_code = '''
    function trans(f){
	var g = f.replace(/[a-zA-Z]/g, function(a) {
		    return String.fromCharCode(("Z" >= a ? 90 : 122) >= (a = a.charCodeAt(0) + 13) ? a : a - 26)
	    })
	   return g;
    }
    '''
    js_code2 = '''
    function translate(f){
    for (var g = decodeURIComponent(f), k = [], l = 0; l < g.length; l++) {
            var m = g.charCodeAt(l);
            k[l] = 33 <= m && 126 >= m ? String.fromCharCode(33 + (m + 14) % 94) : String.fromCharCode(m)
        }
    g = k.join("");

    return g;
    }
    '''
    trans = js2py.eval_js(js_code)
    halfDecodedAjax = trans(encoded_ajax)
    translate = js2py.eval_js(js_code2)
    decodedAjax = translate(base64.b64decode(halfDecodedAjax).decode())

    return decodedAjax
    #xbmc.log("JS2PY : %s" %test3,2)
    #xbmc.log("Translate : %s" %base64.b64decode(test3).decode(),2)
    #xbmc.log("Translate2 : %s" %test4,2)

def getKey():
    js = 'Math.round(new Date / 1E3)'
    key = js2py.eval_js(js)
    xbmc.log("Key: %s" %key,2)
    return key

def play_video(video_id):
    #if not os.path.exists(__addondir__):
    #    os.makedirs(__addondir__)
    #xbmc.log('Play: %s; %s' %(movie_id,cookie))
    video_json = getMovie(video_id)
    # Pass the item to the Kodi player.
    #strm_file=open(_stream_file, 'w+')
    #strm_file.write(json.loads(video_json)['file'])
    #strm_file.close()
    #xbmc.log('Movie: %s' %movie,2)
    #movie = json.loads(movie)
    #xbmc.log('Movie2: %s' %movie,2)
    #file = os.path.join(__addondir__, 'video.strm')
    li = xbmcgui.ListItem(path=json.loads(video_json)['file'])
    #li.setInfo('video', {'Title': title})
    #xbmc.log('File: %s' %file,2)
    #playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    #playlist.add(url=file, listitem=li)

    #xbmc.Player().play(file)
    #while not Player().isPlaying():
    #    xbmc.sleep(10)
    #xbmc.Player().updateInfoTag(li)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)


    '''
    listitem = xbmcgui.ListItem('Ironman')
    listitem.setInfo('video', {'Title': 'Ironman', 'Genre': 'Science Fiction'})
    xbmc.Player().play(url, listitem, windowed)
    xbmc.Player().play(playlist, listitem, windowed, startpos)
    '''

    #xbmcplugin.setResolvedUrl(__handle__, succeeded=True, listitem=li)
