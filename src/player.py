#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import pygame
import urllib


class Player:
    def __init__(self):
        pygame.mixer.init(channels=2)

    def play(self, file_name):
        # TODO: check if file exists
        pygame.mixer.music.load("samples/{}".format(file_name))
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def status(self):
        return pygame.mixer.music.get_busy()


class routesHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self.player = Player()
        BaseHTTPRequestHandler.__init__(self, *args)

    def _write_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _return_response(self, text):
        self.wfile.write(json.dumps({'response': text}).encode('utf8'))

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        self._write_headers()

        if parsed_path.path == '/play':
            self.player.play(parsed_path.query)
            self._return_response('playing {}'.format(parsed_path.query))
        elif parsed_path.path == '/stop':
            self.player.stop()
            self._return_response('stopped playing')
        elif parsed_path.path == '/pause':
            self.player.pause()
            self._return_response('paused playing')
        elif parsed_path.path == '/unpause':
            self.player.unpause()
            self._return_response('unpaused playing')
        elif parsed_path.path == '/status':
            if self.player.status():
                self._return_response('playing')
            else:
                self._return_response('idle')


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', int(os.getenv('SERVER_PORT'))), routesHandler)

    try:
        print('Started httpserver on port ', os.getenv('SERVER_PORT'))
        # Wait forever for incoming http requests
        server.serve_forever()
    except KeyboardInterrupt:
            pass

    server.server_close()
