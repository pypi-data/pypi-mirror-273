import requests
import time
from .sign import sign_request, create_session_id, sign_im
from .crypto import get_machine_code
from .im import AutoWxIm
from .request import Request
import asyncio


class AutoWxSdk:
    def __init__(self, client_type, appid: str, secret: str, base_url: str):
        self._client_type = client_type
        self._appid = appid
        self._secret = secret
        self._base_url = base_url
        self._machine_code = get_machine_code()

        self.im = AutoWxIm(self._client_type, base_url, appid, secret, '/socket-io')
        self.request = Request(base_url, appid, secret)

    def test_task(self):
        print('--> start-test-task')
        # asyncio.run(self._mocker_test_task())
        result = [None, '']
        if self._client_type == 'mocker':
            result = asyncio.run(self._mocker_test_task())

        if self._client_type == 'sdk':
            result = asyncio.run(self._sdk_test_task())

        if result[0] is None:
            print('Error: client_type is invalid!')
            return
        if not result[0]:
            print(result[1])
            return

        print('<-- end-test-task')

    async def wait_im(self, type: str, check: callable, timeout: int = 10):
        event = asyncio.Event()

        def on_task(data):
            if not check(data):
                return

            event.set()
            self.im.event.off(type, on_task)

        self.im.event.on(type, on_task)
        await asyncio.wait_for(event.wait(), timeout)

    async def wait_im_task(self, task_key: str, timeout: int = 10):
        await self.wait_im('task', lambda data: data['taskKey'] == task_key, timeout)

    async def wait_im_task_result(self, task_key: str, timeout: int = 10):
        await self.wait_im('task_result', lambda data: data['taskKey'] == task_key, timeout)

    async def _mocker_test_task(self):
        url = "/api/wb-mocker/test-task"
        task_key = create_session_id()
        # im是否已经收到了task
        is_im_received_task = False

        res_request = self.request.post(url, {'taskKey': task_key})

        if res_request['code']:
            return [False, res_request['message']]

        # request请求完成之前im就已经收到了
        if is_im_received_task:
            return [True, "Success!"]

        await self.wait_im_task(task_key, 10)
        return [True, "Success!"]

    async def _sdk_test_task(self):
        url = "/api/wb-sdk/test-task"
        task_key = create_session_id()
        # im是否已经收到了task
        is_im_received_task = False

        res_request = self.request.post(url, {'taskKey': task_key})

        if res_request['code']:
            return [False, res_request['message']]

        # request请求完成之前im就已经收到了
        if is_im_received_task:
            return [True, "Success!"]

        await self.wait_im_task_result(task_key, 10)
        return [True, "Success!"]

    def ping(self):
        url = "/api/wb-mocker/ping"
        return self.request.post(url)

    def mocker_test_im(self):
        url = "/api/wb-mocker/test-im"
        return self.request.post(url)

    def connect_im(self):
        self.im.connect()

    def on_task(self, callback):
        self.im.on_task(callback)

    def on_task_result(self, callback):
        self.im.on_task_result(callback)
