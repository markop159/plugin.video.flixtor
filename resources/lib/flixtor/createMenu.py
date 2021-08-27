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
from datetime import timedelta, date

# Addon variables
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
__addon__ = xbmcaddon.Addon()
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])

# Internal imports
from flixtor.helper import getMovies, getTVShows, getSeasons, getEpisodes, getUserInput

def createMenu(command, func, page=1):
    # Creates menu depending on command
    xbmc.log(msg="Test Message", level=xbmc.LOGINFO)
    xbmc.log(msg="%s" %command, level=xbmc.LOGINFO)
    if command == 'M':
        xbmc.log('Func: %s' %func)
        if func == 'Genres':
            createMainMenus('genreMovies')
        elif func == 'Search':
            query=getUserInput()
            createMovieMenu(func, query)
        else:
            createMovieMenu(func, None, page)
    if command == 'T':
        xbmc.log('Func: %s' %func)
        if func == 'Genres':
            createMainMenus('genreTVShows')
        elif func == 'Search':
            query=getUserInput()
            createTVShowMenu(command, query)
        else:
            createTVShowMenu(func)
    elif command == 'tvshow':
        createTVShowMenu(func)
    elif command == 'seasons':
        createSeasonsMenu(func)
    elif command == 'episodes':
        createEpisodesMenu(func)
    else:
        createMainMenus(command)

def createMainMenus(command):
    mainMenuItems = {'Movies':
                        {'Home': 'home',
                        'Movies': 'movies',
                        'Genres': ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science-Fiction', 'TV-Movie', 'Thriller', 'War', 'Western'],
                        'Search':'search'
                        },
                     'TVShows':
                        {'Home': 'home',
                        'TVShows': 'TVShows',
                        'Genres': ['Action-Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'History', 'Kids', 'Music', 'Musical', 'Mystery', 'News', 'Reality', 'Romance', 'Sci-Fi-Fantasy', 'Soap', 'Talk', 'War-Politics', 'Western'],
                        'Search':'search'
                        }
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

    elif command == 'subTVShows':
        listings = []
        for item in mainMenuItems['TVShows'].keys():
            li = xbmcgui.ListItem(label=item)
            li.setInfo('folder', {'title': item})
            url = '{0}?cmd={1}&func={2}'.format(__url__, 'T', item)
            isFolder = True
            listings.append((url,li,isFolder))
        xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
        xbmcplugin.endOfDirectory(__handle__)

    elif command == 'genreMovies':
        listings = []
        for item in mainMenuItems['Movies']['Genres']:
            li = xbmcgui.ListItem(label=item)
            li.setInfo('folder', {'title': item})
            url = '{0}?cmd={1}&func={2}'.format(__url__, 'M', item)
            isFolder = True
            listings.append((url,li,isFolder))
        xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
        xbmcplugin.endOfDirectory(__handle__)

    elif command == 'genreTVShows':
        listings = []
        for item in mainMenuItems['TVShows']['Genres']:
            li = xbmcgui.ListItem(label=item)
            li.setInfo('folder', {'title': item})
            url = '{0}?cmd={1}&func={2}'.format(__url__, 'T', item)
            isFolder = True
            listings.append((url,li,isFolder))
        xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
        xbmcplugin.endOfDirectory(__handle__)

def createMovieMenu(func, search=None, page=1):

    if search == None:
        movies = getMovies(func, page)
    else:
        movies = getMovies(func, page, search)

    listings = []
    for movie in movies:
        if (movie['year'] == str(date.today().year)):
            xbmc.log("Movie: %s" %movie,2)
            li = xbmcgui.ListItem(label=movie['title'])
            li.setArt({'fanart': 'https:'+movie['image'], 'icon': 'https:'+movie['image']})
            li.setInfo('video', {'title': movie['title'], 'genre': movie['genres'], 'year': movie['year']})
            if not movie['ytLink'] == None:
                li.addContextMenuItems([('Trailer', 'PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=%s)' %movie['ytLink'])])
            li.setProperty('IsPlayable', 'true')
            url = '{0}?cmd=play&video={1}&title={2}&genre={3}&year={4}'.format(__url__, movie['movie_id'], movie['title'], movie['genres'], movie['year'])
            isFolder = False
            listings.append((url,li,isFolder))
    if not func == 'Home':
        page = int(page)+1
        url = '{0}?cmd=M&func={1}&page={2}'.format(__url__, func, page)
        li = xbmcgui.ListItem(label='go to page %s' %page)
        isFolder = True
        listings.append((url,li,isFolder))
    xbmcplugin.addDirectoryItems(__handle__,listings,len(listings))
    xbmcplugin.endOfDirectory(__handle__)


def createTVShowMenu(command):

    tvShows = getTVShows(command)

    listings = []
    for tvShow in tvShows:
        if (tvShow['show_url'].startswith('/watch/tv/')):
            li = xbmcgui.ListItem(label=tvShow['title'])
            li.setArt({'fanart': 'https:'+tvShow['image'], 'icon': 'https:'+tvShow['image']})
            li.setInfo('video', {'title': tvShow['title'], 'genre': tvShow['genres'], 'year': tvShow['year']})
            if not tvShow['ytLink'] == None:
                li.addContextMenuItems([('Trailer', 'PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=%s)' %tvShow['ytLink'])])
            url = url = '{0}?cmd=seasons&show_url={1}'.format(__url__, tvShow['show_url'])
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
