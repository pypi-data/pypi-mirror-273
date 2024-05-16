"""
    response 是设计的获取到 body 之后才会触发事件
    为了最大化提高效率，只在需要的时候获取
"""
import re
from typing import Callable, Dict

from easypage.cdp import CDP
from easypage.request import Request
from easypage.response import Response


class Listener:

    def __init__(self, context_id: str):
        """

        :param context_id: 上下文 id
        """
        self._http_listen_on = False
        self.__context_id = context_id
        self.__request_listeners: Dict[Callable, dict] = {}
        self.__response_listeners: Dict[Callable, dict] = {}

    @property
    def context_id(self):
        return self.__context_id

    """
        添加
    """

    def request(self, callback: Callable):
        """
        请求监听（匹配所有请求）

        :param callback:
        :return:
        """
        self.__request_listeners[callback] = {
            "func": callback
        }
        self._http_listen_on = True

    def request_on_url(self, url: str, callback: Callable, is_regex: bool = True):
        """
        请求监听

        :param url: 待匹配的 url
        :param is_regex: 是否正则匹配，不是那就用包含关系（in 匹配）
        :param callback:
        :return:
        """
        self.__request_listeners[callback] = {
            "url": url,
            "func": callback,
            "is_regex": is_regex
        }
        self._http_listen_on = True

    def response(self, callback: Callable):
        """
        响应监听（匹配所有响应）

        :param callback:
        :return:
        """
        self.__response_listeners[callback] = {
            "func": callback
        }
        self._http_listen_on = True

    def response_on_url(self, url: str, callback: Callable, is_regex: bool = True):
        """
        响应监听

        :param url: 待匹配的 url
        :param is_regex: 是否正则匹配，不是那就用包含关系（in 匹配）
        :param callback:
        :return:
        """
        self.__response_listeners[callback] = {
            "url": url,
            "func": callback,
            "is_regex": is_regex
        }
        self._http_listen_on = True

    def response_on_mime_type(self, mime_type: str, callback: Callable, is_regex: bool = True):
        """
        响应监听（根据响应的 mime_type，如：text/html、image/png、application/json）

        :param mime_type: 待匹配的 mime_type
        :param is_regex: 是否正则匹配，不是那就用包含关系（in 匹配）
        :param callback:
        :return:
        """
        self.__response_listeners[callback] = {
            "mime_type": mime_type,
            "func": callback,
            "is_regex": is_regex
        }
        self._http_listen_on = True

    """
        触发
    """

    def _on_request(self, request: Request):
        """
        请求触发

        :param request:
        :return:
        """
        for func, config in self.__request_listeners.items():
            if "url" in config:
                is_regex = config["is_regex"]
                if is_regex:
                    if re.search(config["url"], request.url):
                        func(request)
                elif config["url"] in request.url:
                    func(request)
            elif "is_regex" not in config:
                func(request)

    def _on_response(self, response: Response, cdp: CDP):
        """
        响应触发

        :param response: 响应
        :param cdp: cdp
        :return:
        """
        run_functions = []

        for func, config in self.__response_listeners.items():
            if "url" in config:
                is_regex = config["is_regex"]
                if is_regex:
                    if re.search(config["url"], response.url):
                        run_functions.append(func)
                elif config["url"] in response.url:
                    run_functions.append(func)
            if "mime_type" in config:
                is_regex = config["is_regex"]
                if is_regex:
                    if re.search(config["mime_type"], response.mime_type):
                        run_functions.append(func)
                elif config["mime_type"] in response.mime_type:
                    run_functions.append(func)
            elif "is_regex" not in config:
                run_functions.append(func)

        # 判断要不要处理
        if len(run_functions) == 0:
            return

        # 先去触发获取响应体
        response._get_body()

        # 构造事件去触发响应
        def handle_response():
            """
            触发响应

            :return:
            """
            for rf in run_functions:
                rf(response)

        # 创建事件
        cdp.once(event=f"handle_response_{response.request_id}", callback=handle_response)

    """
        移除
    """

    def remove_request(self, callback: Callable):
        """
        移除请求监听

        :param callback:
        :return:
        """
        if callback in self.__request_listeners:
            del self.__request_listeners[callback]

    def remove_response(self, callback: Callable):
        """
        移除响应监听

        :param callback:
        :return:
        """
        if callback in self.__response_listeners:
            del self.__response_listeners[callback]

    """
        其它方法
    """

    def _event_trigger(self, event: str, enable: bool = False):
        """
        事件触发器

        :param event: 事件
        :param enable: 启用状态
        :return:
        """
