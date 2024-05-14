import socketio
from pymitter import EventEmitter
from .sign import sign_im, create_session_id, get_machine_code
import time

NAMESPACE = '/socket-io'


# 监听内置的 'message' 事件


class AutoWxIm:
    def __init__(self, client_type, url, appid, secret, namespaces):
        self.sio = socketio.Client()
        self.event = EventEmitter()
        self.__client_type = client_type
        self.__url = url
        self.__appid = appid
        self.__secret = secret
        self.__namespace = namespaces
        self.__machine_code = get_machine_code()
        self._listen()

    def connect(self):
        session_id = create_session_id()
        timestamp = int(time.time() * 1000)
        sign = sign_im(self.__client_type, self.__secret, self.__appid, session_id, timestamp)

        headers = {
            "appid": self.__appid,
            "timestamp": str(timestamp),
            "sign": sign,
            "machine_code": self.__machine_code,
            "session_id": session_id,
            "client_type": self.__client_type,
        }

        self.sio.connect(self.__url,
                         transports=['websocket'],
                         namespaces=[self.__namespace],
                         headers=headers)

    # 监听事件
    def _listen(self):
        self.sio.on('task', namespace=NAMESPACE)(self._on_task)
        self.sio.on('test-im', namespace=NAMESPACE)(self._on_test_im)
        self.sio.on('connect', namespace=NAMESPACE)(self._on_connect)
        self.sio.on('disconnect', namespace=NAMESPACE)(self._on_disconnect)

    def _on_test_im(self, data):
        self.event.emit('test-im', data)

    def _on_task(self, data):
        self.event.emit('task', data)

    def _on_connect(self):
        print('Connected to the server')
        self.event.emit('connect')

    def _on_disconnect(self):
        print('Disconnected from the server')
        self.event.emit('disconnect')

    def on_task(self, callback):
        self.event.on('task', callback)

    def on_task_result(self, callback):
        self.event.on('task-result', callback)

    def on(self, event, callback):
        self.event.on(event, callback)
