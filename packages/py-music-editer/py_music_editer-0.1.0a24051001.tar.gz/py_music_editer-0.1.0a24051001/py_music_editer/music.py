"""
py_music_editer/music.py
Version: 0.1.0.alpha24051001
Copyright @CooooldWind_
Protected by Apache License Version 2.0.
https://www.apache.org/licenses/LICENSE-2.0
"""
from mutagen.id3 import ID3


class Music:

    def __init__(self, filename=""):
        self.title = ""
        self.artist: list[str] = []
        self.album = ""
        
        pass
