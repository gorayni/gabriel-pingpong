import json
import multiprocessing
import os
import Queue
import select
import socket
import struct
import sys
import threading
import time
import traceback

if os.path.isdir("../../gabriel/server"):
    sys.path.insert(0, "../../gabriel/server")
import gabriel
LOG = gabriel.logging.getLogger(__name__)

sys.path.insert(0, "/home/zhuoc/pyglet-1.2.4")
import pyglet

sound_left = pyglet.media.load('audio_files/left.wav')
sound_right = pyglet.media.load('audio_files/right.wav')
player_left = pyglet.media.Player()
player_left.queue(sound_left)
player_right = pyglet.media.Player()
player_right.queue(sound_right)


class SoundHandler(gabriel.network.CommonHandler):
    def setup(self):
        super(SoundHandler, self).setup()

    def __repr__(self):
        return "Sound Server"

    def handle(self):
        LOG.info("New Pingpong app connected")
        super(SoundHandler, self).handle()

    def _handle_input_data(self):
        ## receive data
        data = self._recv_all(5)
        if data == "leftt":
            print "left"
            player_left.seek(0)
            player_left.play()
        else:
            print "right"
            player_right.seek(0)
            player_right.play()
        
    def terminate(self):
        LOG.info("Pingpong app disconnected")
        super(SoundHandler, self).terminate()

class SoundServer(gabriel.network.CommonServer):
    def __init__(self, port, handler):
        gabriel.network.CommonServer.__init__(self, port, handler) # cannot use super because it's old style class
        LOG.info("* Sound server(%s) configuration" % str(self.handler))
        LOG.info(" - Open TCP Server at %s" % (str(self.server_address)))
        LOG.info(" - Disable nagle (No TCP delay)  : %s" %
                str(self.socket.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY)))
        LOG.info("-" * 50)

    def terminate(self):
        gabriel.network.CommonServer.terminate(self)

def main():
    sound_server = SoundServer(4299, SoundHandler)
    sound_thread = threading.Thread(target = sound_server.serve_forever)
    sound_thread.daemon = True

    try:
        sound_thread.start()
        while True:
            time.sleep(100)
    except KeyboardInterrupt as e:
        sys.stdout.write("Exit by user\n")
        sound_server.terminate()
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(str(e))
        sound_server.terminate()
        sys.exit(1)
    else:
        sound_server.terminate()
        sys.exit(0)


if __name__ == '__main__':
    main()
