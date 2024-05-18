from kabaret import flow
from kabaret.flow.object import _Manager
from libreflow.baseflow import ProjectSettings
from libreflow.baseflow.shot import Sequence, Shot
from libreflow.baseflow.file import TrackedFile

from . import _version
__version__ = _version.get_versions()['version']

class PlaySequence(flow.Action):
    _MANAGER_TYPE = _Manager

    def needs_dialog(self):
        return False

    def run(self, button):
        mov_filters = self.root().project().settings().movie_filters.get()
        print('filters from PlaySequence:', mov_filters)

class PlayShot(flow.Action):
    _MANAGER_TYPE = _Manager

    def needs_dialog(self):
        return False

    def run(self, button):
        mov_filters = self.root().project().settings().movie_filters.get()
        print('filters from PlayShot:', mov_filters)

class PlayMovie(flow.Action):
    _MANAGER_TYPE = _Manager

    def needs_dialog(self):
        return False

    def run(self, button):
        mov_filters = self.root().project().settings().movie_filters.get()
        print('filters from PlayMovie:', mov_filters)


def movie_filters_param(parent):
    if isinstance(parent, ProjectSettings):
        r = flow.Param(list)
        r.name = 'movie_filters'
        r.index = None
        return r

def play_shot_action(parent):
    if isinstance(parent, Shot):
        r = flow.Child(PlayShot)
        r.name = 'quick_play_shot'
        r.index = None
        return r

def play_sequence_action(parent):
    if isinstance(parent, Sequence):
        r = flow.Child(PlaySequence)
        r.name = 'quick_play_sequence'
        r.index = None
        return r

def play_movie_action(parent):
    if isinstance(parent, TrackedFile) and parent.format.get() == 'mov':
        r = flow.Child(PlayMovie)
        r.name = 'quick_play_movie'
        r.index = None
        return r

def install_extensions(session):
    return {
        "play_movies": [
            movie_filters_param,
            play_sequence_action,
            play_shot_action,
            play_movie_action,
        ]
    }
