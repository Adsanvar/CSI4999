import os, threading, sys

ip = sys.argv[1]
threading.Timer(1.25, os.system('chromium-browser --start-fullscreen --kiosk http://'+ip+':5000')).start()