'''
here we create menus (channel and epg)
'''
# External imports
import sys, os
import urllib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import time
import json
from datetime import datetime as dt
from datetime import timedelta

# Addon variables
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
__addon__ = xbmcaddon.Addon()
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])

# Internal imports
from flixtor.helper import getMovies, getTVShows, getSeasons, getEpisodes
from flixtor.logging import log, LOGLEVEL, log_error


# TODO: Treba nardit vse od začetka :D

# Domain


def createMenu(command, handle):
    # Creates menu depending on command
    xbmc.log(msg="Test Message", level=xbmc.LOGINFO)
    xbmc.log(msg="%s" %command, level=xbmc.LOGINFO)
    if command == 'M':
        xbmc.log('Handle: %s' %handle)
        createMovieMenu(handle)
    elif command == 'tvshow':
        createTVShowMenu(handle)
    elif command == 'seasons':
        createSeasonsMenu(handle)
    elif command == 'episodes':
        createEpisodesMenu(handle)
    else:
        createMainMenus(command, handle)

def createMainMenus(command, handle):
    mainMenuItems = {'Movies':
                        {'Home': 'home',
                        'Genres': ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science-Fiction', 'TV-Movie', 'Thriller', 'War', 'Western'],
                        'Search':'search'
                        },
                     'TVShows WIP': ['kategorija1', 'kategorija2']
                     }

    if command == 'main':
        listings = []
        for item in mainMenuItems.keys():
            li = xbmcgui.ListItem(label=item)
            li.setInfo('folder', {'title': item})
            url = '{0}?cmd={1}'.format(__url__, 'sub'+item)
            isFolder = True
            listings.append((url,li,isFolder))
        xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
        xbmcplugin.endOfDirectory(__handle__)

    elif command == 'subMovies':
        listings = []
        for item in mainMenuItems['Movies'].keys():
            li = xbmcgui.ListItem(label=item)
            li.setInfo('folder', {'title': item})
            url = '{0}?cmd={1}&func={2}'.format(__url__, 'M', item)
            isFolder = True
            listings.append((url,li,isFolder))
        xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
        xbmcplugin.endOfDirectory(__handle__)

def createMovieMenu(command):

    movies = getMovies(command)

    listings = []
    for movie in movies:
        xbmc.log("Movie: %s" %movie,2)
        li = xbmcgui.ListItem(label=movie['title'])
        li.setProperty('fanart_image', movie['image'])
        li.setInfo('video', {'title': movie['title'], 'genre': movie['genres']})
        url = '{0}?cmd=play&video={1}'.format(__url__, movie['movie_id'])
        isFolder = False
        listings.append((url,li,isFolder))
    xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
    xbmcplugin.endOfDirectory(__handle__)


def createTVShowMenu(handle):

    tvShows = getTVShows()

    listings = []
    for tvShow in tvShows:
        li = xbmcgui.ListItem(label=tvShow['name'], thumbnailImage=tvShow['thumb'])
        li.setProperty('fanart_image', tvShow['fanart'])
        li.setInfo('video', {'title': tvShow['name'], 'genre': tvShow['genre']})
        url = url = '{0}?cmd=seasons&show_id={1}'.format(__url__, tvshow['show_id'])
        isFolder = True
        listings.append((url,li,isFolder))
    xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
    xbmcplugin.endOfDirectory(__handle__)


def createSeasonsMenu(handle):

    seasons = getSeasons(show_id)

    listings = []
    for season in seasons:
        li = xbmcgui.ListItem(label=season['name'], thumbnailImage=season['thumb'])
        li.setProperty('fanart_image', season['fanart'])
        li.setInfo('video', {'title': season['name'], 'genre': season['genre']})
        url = url = '{0}?cmd=episodes&show_id={1}'.format(__url__, season['show_id'])
        isFolder = True
        listings.append((url,li,isFolder))
    xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
    xbmcplugin.endOfDirectory(__handle__)


def createEpisodesMenu(handle):

    episodes = getEpisodes(show_id)

    listings = []
    for episode in episodes:
        li = xbmcgui.ListItem(label=episode['name'], thumbnailImage=episode['thumb'])
        li.setProperty('fanart_image', episode['fanart'])
        li.setInfo('video', {'title': episode['name'], 'genre': episode['genre']})
        url = episode['url']
        isFolder = False
        listings.append((url,li,isFolder))
    xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
    xbmcplugin.endOfDirectory(__handle__)
