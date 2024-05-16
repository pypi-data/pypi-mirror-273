from typing import Optional
from aipkgs_core.utils.singleton import Singleton
from flask_socketio import SocketIO


@Singleton
class SocketIOCore:
    def __init__(self):
        self.__socketio: Optional[SocketIO] = None
        self.__app = None

    @property
    def socketio(self) -> Optional[SocketIO]:
        return self.__socketio

    def __initialize_socketio(self, app, async_mode: str = None):
        self.__app = app
        self.__socketio = SocketIO(app, async_mode=async_mode)

    def initialize_socketio(self, app, async_mode: str = None):
        self.__initialize_socketio(app=app, async_mode=async_mode)

    def run(self, host: str = None, port: int = None):
        self.__socketio.run(self.__app, host=host, port=port)


def initialize_socketio(app, async_mode: str = None) -> SocketIO:
    SocketIOCore.shared.initialize_socketio(app=app, async_mode=async_mode)
    return SocketIOCore.shared.socketio


def socketio() -> SocketIO:
    return SocketIOCore.shared.socketio


def run(host: str = None, port: int = None):
    SocketIOCore.shared.run(host=host, port=port)
