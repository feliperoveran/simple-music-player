#!/usr/bin/env python

import os
import pygame
import wget
import pwd
import grp


class Player:
    def __init__(self):
        pygame.mixer.init(channels=2)
        self.source_path = '{}/music/'.format(os.getenv('APP_PATH'))

    def play(self, file_name):
        song_path = self.source_path + file_name

        if os.path.exists(song_path):
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()

            return True
        else:
            return False

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def status(self):
        return pygame.mixer.music.get_busy()

    def download(self, url):
        file_name = url.split('/')[-1]
        file_path = self.source_path + file_name

        # check if file exists and return if it does
        if os.path.exists(file_path):
            print('File already exists. Skipping the download')
            return file_name

        print('Downloading file:', file_name)
        wget.download(url, out='{}{}'.format(self.source_path, file_name))

        # change ownership
        os.chown(
            file_path,
            pwd.getpwnam(os.getenv('APP_USER')).pw_uid,
            grp.getgrnam(os.getenv('APP_USER')).gr_gid
        )

        return file_name
