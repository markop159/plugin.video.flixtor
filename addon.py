'''
Main class
'''
# External imports
import sys, os
import xbmcaddon

from urllib.parse import parse_qsl
#from resources.lib.flixtor.helper import play_video

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
__addon__ = xbmcaddon.Addon()
__url__ = sys.argv[0]
__handle__ = str(sys.argv[1])

# Internal imports
from flixtor.logging import log, LOGLEVEL, log_error
from flixtor.createMenu import createMenu
from flixtor.helper import play_video

# Main function
def main():
    args = dict(parse_qsl(sys.argv[2][1:]))
    cmd = args.get('cmd', None)
    url = args.get('url', None)
    video_id = args.get('video', None)
    title = args.get('title', None)
    func = args.get('func', None)
    if cmd is None:
        createMenu('main', __handle__)
    elif cmd == 'subMovies':
        createMenu('subMovies', __handle__)
    elif cmd == 'play':
        play_video(video_id)
    else:
        log("(Main) args:%s %s" % (cmd[0], __handle__), LOGLEVEL.INFO)
        createMenu(cmd, func)

if __name__ == '__main__':
	__handle__ = int(sys.argv[1])
main()
