"""
    所有的 CDP 命令

    https://chromedevtools.github.io/devtools-protocol/
"""
import typing

from easypage.conn import Conn
from easypage.cdp_method.dom import Dom
from easypage.cdp_method.page import Page
from easypage.cdp_method.input import Input
from easypage.cdp_method.fetch import Fetch
from easypage.cdp_method.target import Target
from easypage.cdp_method.network import NetWork
from easypage.cdp_method.browser import Browser
from easypage.cdp_method.runtime import Runtime
from easypage.cdp_method.storage import Storage
from easypage.cdp_method.security import Security
from easypage.cdp_method.emulation import Emulation
from easypage.cdp_method.css import CSS


class CDP:
    def __init__(self, conn: Conn):
        self.__conn = conn

    def on(self, event: str, callback: typing.Callable):
        """
        新增事件

        :param event:
        :param callback:
        :return:
        """
        self.__conn.on(event=event, f=callback)

    def once(self, event: str, callback: typing.Callable):
        """
        新增事件，并且只执行一次

        :param event:
        :param callback:
        :return:
        """
        self.__conn.once(event=event, f=callback)

    def emit(self, event: str, *args, **kwargs):
        """
        触发事件

        :param event: 事件名称
        :param args:
        :param kwargs:
        :return:
        """
        if event in self.__conn._events:
            self.__conn.emit(event=event, *args, **kwargs)

    def send(self, method: str, raise_err: bool = False, params: dict = None) -> typing.Tuple[bool, dict]:
        """
        同步发送消息

        使用：status, value = send(method="", raise_err=False, params={})

        返回的结果是有两个值：
            - status 表示当前消息是否有错误发生（raise_err 为 True 时直接抛出）
            - value 是对应浏览器返回的消息，是一个 dict

        :param method:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param params:
        :return
        """
        return self.__conn.send(
            method=method,
            raise_err=raise_err,
            params=params
        )

    def closed(self) -> bool:
        """
        返回连接是否关闭

        :return:
        """
        return self.__conn.closed()

    @property
    def target(self) -> Target:
        return Target(self.__conn)

    @property
    def page(self) -> Page:
        return Page(self.__conn)

    @property
    def browser(self) -> Browser:
        return Browser(self.__conn)

    @property
    def runtime(self) -> Runtime:
        return Runtime(self.__conn)

    @property
    def dom(self) -> Dom:
        return Dom(self.__conn)

    @property
    def input(self) -> Input:
        return Input(self.__conn)

    @property
    def emulation(self) -> Emulation:
        return Emulation(self.__conn)

    @property
    def storage(self) -> Storage:
        return Storage(self.__conn)

    @property
    def fetch(self) -> Fetch:
        return Fetch(self.__conn)

    @property
    def network(self) -> NetWork:
        return NetWork(self.__conn)

    @property
    def security(self) -> Security:
        return Security(self.__conn)

    @property
    def css(self) -> CSS:
        return CSS(self.__conn)
