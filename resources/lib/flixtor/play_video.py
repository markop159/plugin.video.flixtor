import xbmcgui, xbmcplugin, json, sys

from flixtor.getter import getMovie

def play_video(video_id):
    video_json = getMovie(video_id)
    li = xbmcgui.ListItem(path=json.loads(video_json)['file'])
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
