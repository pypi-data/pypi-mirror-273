"""
    页面 driver
"""
import json
import re
import threading
import time
import base64
import websocket
from pathlib import Path
from parsel import Selector
from bs4 import BeautifulSoup
from easypage.listener import Listener
from easypage.logger import logger
from easypage.driver.driver import Driver
from easypage.options import BrowserOptions
from typing import Tuple, Union, List, Callable
from easypage import definition, errors, operate
from easypage.conn import TYPE_PAGE, DRIVER_TYPE
from easypage.request import Request
from easypage.response import Response
from easypage.utils import other_utils, browser_utils


class PageDriver(Driver):
    def __init__(
            self,
            opts: BrowserOptions,
            page_id: str,
            context_id: str,
            context_driver,
            proxy: definition.Proxy = None
    ):
        """

        :param opts: 配置
        :param page_id: driver_id
        :param context_id: 所属上下文 id
        :param context_driver: 所属上下文 driver
        :param proxy: 代理
        """
        super().__init__(opts, TYPE_PAGE, page_id)
        self.page_id = page_id
        self.context_id = context_id
        self._proxy = proxy
        self._opts = opts
        self._context_driver = context_driver

        # TODO 查找一下是否有可能出现未捕获到请求，但是出现响应的情况
        # 预设参数
        self.__loading: bool = True
        self.__requests_cache = {}  # 可能会有相同请求，request_id 也一样，所以不能移除
        self.__response_cache = {}

        # TODO 考虑根据不同的条件去设置是否启动监听避免额外的资源消耗，可以根据事件在 Listener 进行驱动
        # 启用事件
        self.cdp.dom.enable()
        self.cdp.page.enable()
        self.cdp.security.set_ignore_certificate_errors()
        self.cdp.fetch.enable(handle_auth_requests=True)
        self.cdp.network.enable()
        self.cdp.css.enable()

        # 事件监听
        self.cdp.on(event='Page.lifecycleEvent', callback=self.__on_page_life_cycle_event)
        self.cdp.on(event='Page.loadEventFired', callback=self.__on_page_load_event_fired)
        self.cdp.on(event='Page.frameStartedLoading', callback=self.__on_page_frame_started_loading)
        self.cdp.on(event='Page.frameStoppedLoading', callback=self.__on_page_frame_stopped_loading)
        self.cdp.on(event='Fetch.requestPaused', callback=self.__on_fetch_request_paused)
        self.cdp.on(event='Fetch.authRequired', callback=self.__on_fetch_auth_required)
        self.cdp.on(event='Network.requestWillBeSent', callback=self.__on_network_request_will_be_sent)
        self.cdp.on(event='Network.requestWillBeSentExtraInfo',
                    callback=self.__on_network_request_will_be_sent_extra_info)
        self.cdp.on(event='Network.responseReceived', callback=self.__on_network_response_received)
        self.cdp.on(event='Network.loadingFinished', callback=self.__on_network_loading_finished)

    def get(self, url, **kwargs) -> Tuple[bool, Union[None, str]]:
        """
        访问某个页面

        返回的第一个值是请求命令是否成功
        返回的第二个值是当请求失败的时候发送原因，比如设置的代理访问不通

        :param url:
        :param kwargs:
        :return:
        """
        if "frameId" not in kwargs:
            kwargs["frameId"] = self.page_id
        status, result = self.cdp.page.navigate(url=url, **kwargs)
        if not status:
            return False, None

        elif "errorText" in result:
            logger.warning("url：{} errorText：{}", url, result["errorText"])
            return False, result["errorText"]

        return True, None

    def query_selector(
            self,
            selector: str,
            node_id: int = None,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementNotFound]:
        """
        选择元素

        :param selector: 选择器
        :param node_id: 节点 id（基于某个节点查找时需要）
        :param raise_err: 是否报错
        :return:
        """
        status, new_node = self.cdp.dom.query_selector(
            selector=selector,
            node_id=node_id,
            raise_err=raise_err,
        )
        if (status and new_node['nodeId'] == 0) or not new_node or not status:
            if raise_err:
                raise errors.ElementNotFound(selector)
            return None

        return Element(node_id=new_node['nodeId'], page=self)

    def query_selector_all(
            self,
            selector: str,
            node_id: int = None,
            raise_err: bool = False
    ) -> Union[List['Element'], None, errors.ElementNotFound]:
        """
        选择元素

        :param selector: 选择器（支持 css、xpath）
        :param node_id: 节点 id（基于某个节点查找时需要）
        :param raise_err: 是否报错
        :return:
        """
        status, new_nodes = self.cdp.dom.query_selector_all(
            selector=selector,
            node_id=node_id,
            raise_err=raise_err,
        )
        if not status or not new_nodes:
            if raise_err:
                raise errors.ElementNotFound(selector)
            return None

        elements = []
        for nn in new_nodes['nodeIds']:
            elements.append(Element(node_id=nn, page=self))
        return elements

    def eval_js(self, js: str, raise_err: bool = False, **kwargs) -> Tuple[bool, any]:
        """
        执行 js 脚本

        :param js: 路径或者 js 字符串
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :return: 可能是字符串、数字等
        """
        status, result = self.cdp.runtime.evaluate(js=js, raise_err=raise_err, **kwargs)
        if not status:
            return status, result

        if 'value' in result['result']:
            return True, result['result']['value']
        else:
            return False, result['result']['description']

    def iframes(self) -> List["Element"]:
        """
        获取所有的 iframe

        :return:
        """
        # operate.pages(self._opts.address)

        elements = []

        status, new_node_ids = self.cdp.dom.query_selector_all(
            selector="iframe",
        )
        if not new_node_ids or not status:
            return elements

        for node_id in new_node_ids['nodeIds']:
            # 获取 frameId
            status, frame_detail = self.cdp.dom.describe_node(nodeId=node_id)
            if not frame_detail or not status:
                continue
            frame_id = frame_detail['node']['frameId']

            # 判断是否同域
            status, frame_tree = self.cdp.page.get_frame_tree()
            if not status:
                continue
            frame_tree = frame_tree["frameTree"]

            """
                小知识点
                同域名的情况下，再次查询实际上是基于 iframe 的 document
                所以这里在新建 iframe 的时候是要基于 iframe document 的 nodeId，这点和普通元素不一样
                
                不同域名的情况下，实际上就是另一个 page 去对待即可
            """
            if frame_id in json.dumps(frame_tree, ensure_ascii=False):  # 同域的话会获取到比如在 'childFrames' 内
                elements.append(Element(
                    node_id=frame_detail["node"]["contentDocument"]['nodeId'],
                    page=self,
                    is_iframe=True,
                    iframe_node_id=node_id,
                    iframe_owner_page=self
                ))
            else:
                try:
                    page_driver = PageDriver(
                        opts=self._opts,
                        page_id=frame_id,  # 页面的 targetId
                        context_id=self.context_id,  # 页面的上下文 id
                        context_driver=self._context_driver,
                        proxy=self._proxy,
                    )
                    status, iframe_dom = page_driver.cdp.dom.get_document()
                    if not status:
                        continue
                    elements.append(Element(
                        node_id=iframe_dom['root']['nodeId'],  # 这里的原理和上面一样，直接放 dom 的 id
                        page=page_driver,
                        is_iframe=True,
                        iframe_node_id=node_id,
                        iframe_owner_page=self
                    ))
                except websocket.WebSocketBadStatusException:
                    logger.warning("当前 iframe 可能已不在页面上：{}", frame_id)

        return elements

    def iframe_search(self, attr_name: str, attr_value: str, is_regex: bool = False) -> "Element":
        """
        这里是提供了一组可以通过指定属性，通过【正则、in】去匹配属性值的方法

        :param attr_name: 需要去判断的属性名
        :param attr_value: 对应属性名
        :param is_regex: 为 False 时通过 in 判断，为 True 时通过 re 正则判断
        :return:
        """
        iframes = self.iframes()

        for iframe in iframes:
            if not iframe.attrs.get(attr_name):
                continue

            attr = iframe.attrs[attr_name]

            if is_regex:
                if re.search(attr_value, attr):
                    return iframe
            elif attr_value in attr:
                return iframe

    def cookies(self, only_key_val: bool = True, domain: str = None) -> Union[List[dict], dict]:
        """
        获取 cookie

        :param only_key_val: 是否仅返回 {name:'',value:''} 形式
        :param domain: 指定域名
        :return: [{'name': '', 'value': '', 'domain': '', 'path': '', 'expires': -1, 'size': 161, 'httpOnly': True, 'secure': True, 'session': True, 'sameSite': 'Strict', 'priority': 'Medium', 'sameParty': False, 'sourceScheme': 'Secure', 'sourcePort': 443}]
        """
        status, cookies = self.cdp.storage.get_cookies(context_id=self.context_id)
        if not status:
            return []

        cookies = cookies['cookies']

        if only_key_val:
            cookie_dict = {}
            for c in cookies:
                if domain:
                    if c['domain'] == domain:
                        cookie_dict[c['name']] = c['value']
                else:
                    cookie_dict[c['name']] = c['value']

            return cookie_dict
        else:
            if domain:
                return list(filter(lambda x: x['domain'] == domain, cookies))
            return cookies

    def screenshot(
            self,
            save_path: str = None,
            format_type: str = "png",
            quality: int = None,
            clip: dict = None,
            from_surface: bool = True,
            capture_beyond_viewport: bool = False,
            optimize_for_speed: bool = False,
    ) -> bytes:
        """
        截图

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-captureScreenshot

        clip 参考：https://chromedevtools.github.io/devtools-protocol/tot/Page/#type-Viewport

        :param save_path: 保存本地的路径
        :param format_type: jpeg, png, webp，默认值为 png
        :param quality: 压缩质量范围为 [0..100]（仅限 jpeg）
        :param clip: 仅捕获给定区域的屏幕截图（{x:1,y:1,width:1,height:1,scale:1}）
        :param from_surface: 从表面捕获屏幕截图，而不是从视图捕获屏幕截图，默认值为 true
        :param capture_beyond_viewport: 捕获视口之外的屏幕截图，默认值为 false
        :param optimize_for_speed: 优化图像编码以提高速度，而不是优化结果大小（默认为 false）
        :return: {"data":""}
        """
        # 等待页面加载
        self.wait_loaded()

        # 截图
        status, data = self.cdp.page.capture_screenshot(
            format_type=format_type,
            quality=quality,
            clip=clip,
            from_surface=from_surface,
            capture_beyond_viewport=capture_beyond_viewport,
            optimize_for_speed=optimize_for_speed
        )

        if not status or not data:
            return b""

        data_bytes = base64.b64decode(data["data"])

        # 保存本地
        if save_path:
            save_path = Path(save_path).absolute().resolve()
            save_path.parent.mkdir(parents=True, exist_ok=True)
            if not save_path.suffix:
                save_path = save_path.with_suffix(".png")

            with open(save_path, "wb") as f:
                f.write(data_bytes)

        return data_bytes

    def reload(
            self,
            ignore_cache: bool = False,
            scrip_to_evaluate_onload: str = None,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        刷新页面

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-reload

        :param ignore_cache: 是否忽略浏览器缓存(所有资源都会重新加载)
        :param scrip_to_evaluate_onload：注入的脚本（origin 变了就不会注入了）
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.cdp.page.reload(
            ignore_cache=ignore_cache,
            scrip_to_evaluate_onload=scrip_to_evaluate_onload,
            raise_err=raise_err,
            need_callback=need_callback
        )

    def stop_loading(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        停止页面加载（强制页面停止所有导航和挂起的资源提取）

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-stopLoading

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.cdp.page.stop_loading(
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def close(self):
        """
        关闭当前页面

        :return:
        """
        self.cdp.page.close()

    """
        等待 TODO 等待是否需要单独写一个类，公用等待方法
    """

    def wait_loaded(self, status: str = "complete", timeout: int = None):
        """
        等待页面加载完成

        :param status: 可选 interactive、complete
        :param timeout: 没有提供会使用全局的
        :return:
        """
        timeout = timeout or self._opts.timeout

        # 输入检查
        dom_read_states = ["interactive", "complete"]
        if status not in dom_read_states:
            status = "complete"

        # 加载等待
        start_time = time.time()
        while time.time() - start_time < timeout:
            dom_status = self.ready_state

            if dom_status == status or dom_status == "complete":
                self.__loading = False
                return

            if self.cdp.closed():
                break

            time.sleep(0.1)

    def wait_for_selector(
            self,
            selector: str,
            node_id: int = None,
            timeout: int = None,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementWaitTimeout]:
        """
        等待某个元素

        :param timeout:
        :param node_id:
        :param selector:
        :param raise_err:
        :return:
        """
        timeout = timeout or self._opts.timeout

        start_time = time.time()
        while time.time() - start_time < timeout:
            ele = self.query_selector(selector=selector, node_id=node_id)

            if ele:
                return ele

            if self.cdp.closed():
                break

            time.sleep(0.1)

        if raise_err:
            raise errors.ElementWaitTimeout(selector)

    def wait_for_selectors(
            self,
            selectors: List[str],
            node_id: int = None,
            timeout: int = None,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementWaitTimeout]:
        """
        等待多个元素，谁先拿到就返回谁（所以要自己注意放入的顺序）

        :param timeout:
        :param node_id:
        :param selectors: 元素列表
        :param raise_err:
        :return:
        """
        timeout = timeout or self._opts.timeout

        start_time = time.time()

        while time.time() - start_time < timeout:
            for s in selectors:
                ele = self.query_selector(selector=s, node_id=node_id)

                if ele:
                    return ele

                if self.cdp.closed():
                    break

            time.sleep(0.1)

        if raise_err:
            raise errors.ElementWaitTimeout(selectors)

    def wait_for_url(
            self,
            url: str,
            is_regex: bool = True,
            back_resp: bool = False,
            timeout: int = None,
            raise_err: bool = False
    ) -> Union[Request, Response, None]:
        """
        等待直到某个 url 出现

        应用场景：点击后等待某个响应出现，也可以获取其响应结果

        :param url: 待匹配的 url
        :param is_regex: 是否正则匹配，不是那就用包含关系（in 匹配）
        :param timeout: 等待超时时间
        :param back_resp: 是否返回响应，否的话返回 Request 是的话返回 Response（有属性 request 访问到 Request）
        :param raise_err: 是否报错
        :return:
        """
        is_show = False
        result_req: Request = None  # type:ignore
        result_resp: Response = None  # type:ignore

        # 请求回调
        def req_callback(req: Request):
            nonlocal is_show, result_req
            is_show = True
            result_req = req

        def resp_callback(resp: Response):
            nonlocal is_show, result_resp
            is_show = True
            result_resp = resp

        # 请求监听
        if back_resp:
            self.listen.response_on_url(url=url, callback=resp_callback, is_regex=is_regex)
        else:
            self.listen.request_on_url(url=url, callback=req_callback, is_regex=is_regex)

        timeout = timeout or self._opts.timeout
        start_time = time.time()
        while time.time() - start_time < timeout:
            if is_show:
                if back_resp:
                    return result_resp
                return result_req
            elif self.cdp.closed():
                break

            time.sleep(0.1)

        if raise_err:
            raise errors.UrlWaitTimeout(url)

        return None

    """
        访问属性
    """

    @property
    def user_agent(self) -> str:
        """
        返回 ua

        :return:
        """
        status, data = self.cdp.browser.version()
        if not status:
            return ""
        return data["userAgent"]

    @property
    def ready_state(self) -> str:
        """
        页面加载状态

        :return:
        """
        return self.eval_js(js="document.readyState")[-1]

    @property
    def url(self) -> str:
        """
        当前页面的 url

        :return:
        """
        status, root = self.cdp.dom.get_document()

        if not status:
            return ""

        return root['root']['documentURL']

    @property
    def content(self) -> str:
        """
        当前页面的内容

        :return:
        """
        status, root = self.cdp.dom.get_document()
        if not status:
            return ""

        back_end_node_id = root['root']['backendNodeId']

        status, html = self.cdp.dom.get_outer_html(backendNodeId=back_end_node_id)
        if not status:
            return ""

        return html["outerHTML"]

    @property
    def listen(self) -> Listener:
        """
        事件监听

        :return:
        """
        return self._context_driver.listen

    """
       事件监听
    """

    @other_utils.catch_error
    def __on_page_life_cycle_event(self, *args, **kwargs):
        """
        针对顶级页面生命周期事件（如导航、加载、绘制等）触发

        :return:
        """
        self.__loading = True
        logger.debug("页面开始加载：{}", kwargs)

    @other_utils.catch_error
    def __on_page_load_event_fired(self, *args, **kwargs):
        """
        页面加载完成将会被触发

        :return:
        """
        self.__loading = False
        logger.debug("页面加载耗时：{}", kwargs['timestamp'])

    @other_utils.catch_error
    def __on_page_frame_started_loading(self, *args, **kwargs):
        """
        加载开始

        :return:
        """
        self.__loading = True

    @other_utils.catch_error
    def __on_page_frame_stopped_loading(self, *args, **kwargs):
        """
        加载结束

        :return:
        """
        self.__loading = False

    @other_utils.catch_error
    def __on_fetch_request_paused(self, *args, **kwargs):
        """
        请求监听

        请求将暂停，直到客户端响应 替换为 continueRequest、failRequest 或 fulfillRequest

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#event-requestPaused

        :param args:
        :param kwargs: {"method":"Fetch.requestPaused","params":{"requestId":"interception-job-1.0","request":{"url":"https://www.baidu.com/","method":"GET","headers":{"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36","sec-ch-ua":"\"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"","sec-ch-ua-mobile":"?0","sec-ch-ua-platform":"\"Windows\""},"initialPriority":"VeryHigh","referrerPolicy":"strict-origin-when-cross-origin"},"frameId":"E361A685E14EAEC054BEF17592DF25DF","resourceType":"Document"}}
        :return:
        """
        request_id = kwargs["requestId"]
        network_id = kwargs.get("networkId")  # fetch 的 networkId 就是 network 的 requestId

        self.cdp.fetch.continue_request(
            request_id=request_id,
        )

        if not network_id:
            return

        # 请求输出
        request = Request(kwargs)
        # logger.warning("requests 存入：{}", network_id)
        self.__requests_cache[network_id] = request

        # 请求触发
        self.listen._on_request(request=request)

    @other_utils.catch_error
    def __on_network_request_will_be_sent(self, *args, **kwargs):
        """
        请求监听

        有时候 fetch 监听不到，需要通过这里监听

        https://chromedevtools.github.io/devtools-protocol/tot/Network/#event-requestWillBeSent

        :param args:
        :param kwargs:
        :return:
        """
        request_id = kwargs['requestId']

        if request_id not in self.__requests_cache:
            # logger.warning("request_will_be_sent 存入：{}", request_id)

            request = Request(kwargs)

            self.__requests_cache[request_id] = request

            # 请求触发
            self.listen._on_request(request=request)

    @other_utils.catch_error
    def __on_network_request_will_be_sent_extra_info(self, *args, **kwargs):
        """
        请求监听

        https://chromedevtools.github.io/devtools-protocol/tot/Network/#event-requestWillBeSentExtraInfo

        :param args:
        :param kwargs:
        :return:
        """
        request_id = kwargs['requestId']

    @other_utils.catch_error
    def __on_fetch_auth_required(self, *args, **kwargs):
        """
        监听 authRequired

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#event-authRequired

        :param args:
        :param kwargs:
        :return:
        """
        request_id = kwargs['requestId']

        user = None
        pwd = None
        if self._proxy:
            user = self._proxy.get("user")
            pwd = self._proxy.get("pwd")
        elif self._opts.proxy and "user" in self._opts.proxy and "pwd" in self._opts.proxy:
            user = self._opts.proxy.get("user")
            pwd = self._opts.proxy.get("pwd")

        if not user or not pwd:
            logger.error("未获取到代理的账号密码！")
            return

        self.cdp.fetch.continue_with_auth(
            request_id=request_id,
            user=user,
            pwd=pwd,
        )

    @other_utils.catch_error
    def __on_network_response_received(self, *args, **kwargs):
        """
        响应监听

        https://chromedevtools.github.io/devtools-protocol/tot/Network/#event-responseReceived

        :param args:
        :param kwargs:
        :return:
        """
        request_id = kwargs["requestId"]

        # 存储响应
        self.__response_cache[request_id] = kwargs

    @other_utils.catch_error
    def __on_network_loading_finished(self, *args, **kwargs):
        """
        响应结束

        https://chromedevtools.github.io/devtools-protocol/tot/Network/#event-loadingFinished

        :param args:
        :param kwargs:
        :return:
        """
        request_id = kwargs["requestId"]

        # 获取请求
        if request_id not in self.__requests_cache:
            logger.warning("请求缓存无该 id：{}", request_id)
            return
        if request_id not in self.__response_cache:
            del self.__requests_cache[request_id]
            logger.warning("响应缓存无该 id：{}", request_id)
            return
        request_cache = self.__requests_cache[request_id]
        response_cache = self.__response_cache[request_id]

        # 存储输出
        response = Response(response_cache, request_cache, self.cdp)

        # 触发响应
        self.listen._on_response(response, self.cdp)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


"""
    动作链
"""


# modifiers
class Key:
    Alt = 1
    Ctrl = 2
    Backspace = 8
    Shift = 4
    Meta = 8


# windowsVirtualKeyCode
class KeyCode:
    Backspace = 8
    Tab = 9
    Enter = 13
    Shift = 16
    Ctrl = 17
    Alt = 18
    PauseOrBreak = 19
    CapsLock = 20
    Esc = 27
    Space = 32
    PageUp = 33
    PageDown = 34
    End = 35
    Home = 36
    LeftArrow = 37
    UpArrow = 38
    RightArrow = 39
    DownArrow = 40
    Insert = 45
    Delete = 46
    A = 65
    B = 66
    C = 67
    D = 68
    E = 69
    F = 70
    G = 71
    H = 72
    I = 73
    J = 74
    K = 75
    L = 76
    M = 77
    N = 78
    O = 79
    P = 80
    Q = 81
    R = 82
    S = 83
    T = 84
    U = 85
    V = 86
    W = 87
    X = 88
    Y = 89
    Z = 90
    Windows = 91  # Windows 键
    RightClick = 93
    Numpad_0 = 96
    Numpad_1 = 97
    Numpad_2 = 98
    Numpad_3 = 99
    Numpad_4 = 100
    Numpad_5 = 101
    Numpad_6 = 102
    Numpad_7 = 103
    Numpad_8 = 104
    Numpad_9 = 105
    Multiply = 106
    Add = 107
    Subtract = 109
    DecimalPoint = 110
    Divide = 111
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    NumLock = 144
    ScrollLock = 145
    SemiColon = 186
    EqualSign = 187
    Comma = 188
    Dash = 189
    Period = 190
    ForwardSlash = 191
    GraveAccent = 192
    OpenBracket = 219
    BackSlash = 220
    CloseBracket = 221
    SingleQuote = 222


class ActionChain:
    def __init__(self, node_id: int, page: PageDriver, ele: "Element"):
        self.page = page
        self.node_id = node_id
        self.ele = ele

    def focus(self):
        """
        聚焦

        :return:
        """
        self.page.cdp.dom.focus(nodeId=self.node_id)

    def clear(self, simulation: bool = True):
        """
        清空输入框的值

        :param simulation: 模拟真实操作
        :return:
        """
        if not simulation:
            # 非模拟的话，实际的修改可能并不会生效（元素修改了，但是页面没更改）
            self.page.cdp.dom.set_attribute_value(
                name="value",
                value="",
                node_id=self.node_id,
            )
        else:
            # 全选
            self.ctrl(key=KeyCode.A)

            # 删除
            self.page.cdp.input.dispatch_key_event(
                event_type="rawKeyDown",
                windowsVirtualKeyCode=KeyCode.Backspace,
                modifiers=Key.Backspace,
            )

        return self

    def input_text(self, val: str, delay: float = 0, simulation: bool = True):
        """
        输入文本（模拟输入）

        :param val:
        :param simulation: 模拟真实操作
        :param delay: 延时输入（s）
        :return:
        """
        if not simulation:
            # 非模拟的话，实际的修改可能并不会生效（元素修改了，但是页面没更改）
            self.page.cdp.dom.set_attribute_value(
                name="value",
                value=val,
                node_id=self.node_id,
            )
        else:
            # 对焦
            self.focus()

            # 输入
            for v in val:
                self.page.cdp.input.dispatch_key_event(
                    event_type="keyDown",
                    is_key_pad=True,
                    key=v,
                    text=v,
                    code="Key " + v.upper(),
                )

                self.page.cdp.input.dispatch_key_event(
                    event_type="keyUp",
                    is_key_pad=True,
                    key=v,
                    text=v,
                    code="Key " + v.upper(),
                )

                time.sleep(delay)

        return self

    def ctrl(self, key: int):
        """
        ctrl 事件

        :param key: 如 ctrl+A 只要输入 a 或 A 就行了
        :return:
        """
        # 对焦
        self.focus()

        # 输入
        self.page.cdp.input.dispatch_key_event(
            event_type="rawKeyDown",
            windowsVirtualKeyCode=key,
            modifiers=Key.Ctrl,
        )

        return self

    # TODO 增加组合输入
    # def combination_input(self, modifiers: int, value: Union[str, int] = None):
    #     """
    #     组合输入
    #
    #     :param modifiers: 比如 ctrl+shift 就是 Key.Ctrl|Key.Shift
    #     :param value: 输入的值 比如 abc
    #     :return:
    #     """

    def click(self, count: int = 1, button: str = "left", simulation: bool = True):
        """
        执行点击

        :param count: 点击次数
        :param button: 代表鼠标的按键，如：none（不触发按键，代表光标）, left（左击）, middle（滚轮）, right（右击）, back（后退）, forward（前进）
        :param simulation: 模拟真实操作
        :return:
        """
        if not simulation:
            self.ele.eval_js_on_selector(js="this.click();", returnByValue=True)
        else:
            # 聚焦
            self.focus()

            # 获取元素坐标
            x, y = self.ele.coordinate_center

            # 移动
            self.page.cdp.input.dispatch_mouse_event(
                event_type="mouseMoved",
                x=x,
                y=y,
                button="none"
            )

            # 点击
            self.page.cdp.input.dispatch_mouse_event(
                event_type="mousePressed",
                x=x,
                y=y,
                button=button,
                clickCount=count
            )

            # 释放
            self.page.cdp.input.dispatch_mouse_event(
                event_type="mouseReleased",
                x=x,
                y=y,
                button=button,
                clickCount=count
            )

        return self


"""
    元素
"""


class Element(ActionChain):
    def __init__(
            self,
            node_id: int,
            page: PageDriver,
            is_iframe: bool = False,
            iframe_node_id: int = None,
            iframe_owner_page: PageDriver = None
    ):
        """
        生成节点

        如果是 iframe 那么这里获取的实际上就是 iframe 的 dom 而不是 iframe 自身
        :param node_id 当前节点的 id（iframe 的话就是 iframe document 的 node_id）
        :param page PageDriver 对象（iframe 的话就是 iframe 自身的 driver）
        :param is_iframe 是不是 iframe
        :param iframe_node_id iframe 自身的 node_id
        :param iframe_owner_page iframe 所在页面
        :return:
        """
        if is_iframe:
            super().__init__(iframe_node_id, iframe_owner_page, self)
        else:
            super().__init__(node_id, page, self)

        self._back_end_node_id = None
        self._obj_id = None
        self._is_iframe = is_iframe
        self._iframe_node_id = iframe_node_id
        self._iframe_owner_page = iframe_owner_page
        self._iframe_page = page
        self._iframe_document_node_id = node_id

        self.__tagName: str = None if not is_iframe else "iframe"  # type:ignore

    def query_selector(
            self,
            selector: str,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementNotFound]:
        """
        选择元素

        通过这种绕一圈的书写方式，就可以有编辑器的提示了

        :param selector: 选择器（支持 css、xpath）
        :param raise_err: 是否报错
        :return:
        """
        if self._is_iframe:
            return self._iframe_page.query_selector(
                selector=selector,
                node_id=self._iframe_document_node_id,
                raise_err=raise_err
            )
        return self.page.query_selector(
            selector=selector,
            node_id=self.node_id,
            raise_err=raise_err
        )

    def query_selector_all(
            self,
            selector: str,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementNotFound]:
        """
        选择元素

        :param selector: 选择器（支持 css、xpath）
        :param raise_err: 是否报错
        :return:
        """
        if self._is_iframe:
            return self._iframe_page.query_selector_all(
                selector=selector,
                node_id=self._iframe_document_node_id,
                raise_err=raise_err
            )
        return self.page.query_selector_all(
            selector=selector,
            node_id=self.node_id,
            raise_err=raise_err,
        )

    def wait_for_selector(
            self,
            selector: str,
            timeout: int = None,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementWaitTimeout]:
        """
        等待某个元素

        :param timeout:
        :param selector:
        :param raise_err:
        :return:
        """
        if self._is_iframe:
            return self._iframe_page.wait_for_selector(
                selector=selector,
                timeout=timeout,
                node_id=self._iframe_document_node_id,
                raise_err=raise_err
            )
        return self.page.wait_for_selector(
            selector=selector,
            timeout=timeout,
            node_id=self.node_id,
            raise_err=raise_err
        )

    def wait_for_selectors(
            self,
            selectors: List[str],
            timeout: int = None,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementWaitTimeout]:
        """
        等待多个元素，谁先拿到就返回谁（所以要自己注意放入的顺序）

        :param timeout:
        :param selectors: 元素列表
        :param raise_err:
        :return:
        """
        if self._is_iframe:
            return self._iframe_page.wait_for_selectors(
                selectors=selectors,
                timeout=timeout,
                node_id=self._iframe_document_node_id,
                raise_err=raise_err
            )
        return self.page.wait_for_selectors(
            selectors=selectors,
            timeout=timeout,
            node_id=self.node_id,
            raise_err=raise_err
        )

    def eval_js_on_selector(self, js: str, **kwargs) -> Tuple[bool, dict]:
        """
        执行 js 脚本（会自动使用 function 包裹，不然无法执行）

        学习链接：https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-evaluate

        :param js: 路径或者 js 字符串
        :return:
        """
        js = "function (){ %s }" % js
        return self.page.cdp.runtime.call_function_on(js=js, object_id=self.object_id, **kwargs)

    @property
    def style(self) -> dict:
        """
        获取 style

        :return:
        """
        status, content = self.page.cdp.css.get_computed_style_for_node(node_id=self.node_id)
        if not status:
            return {}

        return dict([[i["name"], i["value"]] for i in content["computedStyle"]])

    @property
    def is_visible(self) -> bool:
        """
        元素是否可见（全部可见）

        :return:
        """
        js = """
            return function (el) {
                var rect = el.getBoundingClientRect();
                var isVisible = (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
                );
            
                if (!isVisible) return false;
            
                var style = window.getComputedStyle(el);
                if (style.visibility === 'hidden' || style.display === 'none') return false;
            
                if (rect.width === 0 || rect.height === 0) return false;
            
                var elementBelow = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
                if (elementBelow && elementBelow !== el && !el.contains(elementBelow)) return false;
            
                return true;
            }(this)
        """
        status, val = self.eval_js_on_selector(js=js)
        if not status:
            return False

        return val["result"]["value"]

    @property
    def is_displayed(self) -> bool:
        """
        元素是否显示

        :return:
        """
        style = self.style

        if style.get("visibility") == 'hidden':
            return True

        if style.get("display") == 'none':
            return True

        if self.attrs.get("hidden"):
            return True

        status, val = self.eval_js_on_selector(js="return this.offsetParent === null;")
        if status and val["result"]["value"]:
            return True

        return False

    @property
    def is_enable(self) -> bool:
        """
        元素是否可用

        :return:
        """
        status, val = self.eval_js_on_selector(js="return this.disabled;")
        if not status:
            return False
        return val["result"]["value"]

    @property
    def is_checked(self) -> bool:
        """
        元素是否被选择

        :return:
        """
        status, val = self.eval_js_on_selector(js="return this.checked;")
        if not status:
            return False
        return val["result"]["value"]

    @property
    def is_selected(self) -> bool:
        """
        元素是否被选择

        :return:
        """
        status, val = self.eval_js_on_selector(js="return this.selected;")
        if not status:
            return False
        return val["result"]["value"]

    @property
    def coordinates(self) -> dict:
        """
        获取元素的坐标信息
        返回的比如 content 有 4 个坐标，分别是
        - 左上顶点
        - 右上顶点
        - 右下顶点
        - 左下顶点

        :return:
        """
        # 获取元素坐标
        status, content = self.page.cdp.dom.get_box_model(nodeId=self.node_id)
        if not status:
            return {}

        return content['model']

    @property
    def coordinate_center(self) -> tuple:
        """
        元素中心点坐标

        :return:
        """
        content = self.coordinates["content"]
        return browser_utils.parse_box_center_coordinate(data=content)

    @property
    def attrs(self) -> dict:
        """
        属性

        :return:
        """
        status, attrs = self.page.cdp.dom.get_attributes(node_id=self.node_id)

        if not status:
            return {}

        attrs_list = attrs["attributes"]
        attrs = dict(zip(attrs_list[::2], attrs_list[1::2]))

        return attrs or {}

    @property
    def tag_name(self) -> str:
        """
        节点名称

        :return:
        """
        if not self.__tagName:
            status, describe = self.page.cdp.dom.describe_node(nodeId=self.node_id)
            if status and describe:
                self.__tagName = describe['node']['nodeName'].lower()
        return self.__tagName

    @property
    def html(self) -> str:
        """
        html 文本

        iframe 获取的是 iframe document 的 html

        :return: <input type="submit" id="su" value="百度一下" class="bg s_btn">
        """
        if self._is_iframe:
            describe_status, node = self._iframe_page.cdp.dom.describe_node(nodeId=self._iframe_document_node_id)
            if not describe_status:
                return ""
            iframe_document_back_end_node_id = node['node']['backendNodeId']
            status, html = self._iframe_page.cdp.dom.get_outer_html(backendNodeId=iframe_document_back_end_node_id)
        else:
            status, html = self.page.cdp.dom.get_outer_html(backendNodeId=self.back_end_node_id)

        if not status:
            return ""

        return html["outerHTML"]

    @property
    def text(self):
        """
        获取除了标签以外的内容

        :return:
        """
        return self.soup.get_text()

    @property
    def selector(self) -> Selector:
        """
        获取 parsel 解析器

        :return:
        """
        return Selector(self.html)

    @property
    def soup(self) -> BeautifulSoup:
        """
        获取 bs4 解析器

        :return:
        """
        return BeautifulSoup(self.html, "lxml")

    @property
    def back_end_node_id(self) -> int:
        """
        获取 backendNodeId

        :return:
        """
        if not self._back_end_node_id:
            _, node = self.page.cdp.dom.describe_node(nodeId=self.node_id)
            self._back_end_node_id = node['node']['backendNodeId']

        return self._back_end_node_id

    @property
    def object_id(self) -> str:
        """
        获取 object_id

        :return:
        """
        if not self._obj_id:
            _, node = self.page.cdp.dom.resolve_node(backendNodeId=self.back_end_node_id)
            self._obj_id = node['object']['objectId']

        return self._obj_id

    def __repr__(self):
        attrs = self.attrs
        attrs_text = ' '.join([f'{i}="{attrs[i]}"' for i in attrs.keys()])
        return f"<{self.__class__.__name__} {self.tag_name} {attrs_text}>"
