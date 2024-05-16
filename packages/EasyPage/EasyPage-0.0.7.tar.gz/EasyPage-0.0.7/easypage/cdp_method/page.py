from typing import Tuple
from urllib import parse
from easypage import errors
from easypage.conn import Conn


class Page:
    """
        Page

        https://chromedevtools.github.io/devtools-protocol/tot/Page
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def enable(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        启用页面功能（加载和管理页面、导航、截图等）

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-enable

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Page.enable",
            raise_err=raise_err,
            need_callback=need_callback,
        )

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
        return self.__conn.send(
            method="Page.enable",
            params={
                "ignoreCache": ignore_cache,
                "scriptToEvaluateOnLoad": scrip_to_evaluate_onload,
            },
            raise_err=raise_err,
            need_callback=need_callback,
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
        return self.__conn.send(
            method="Page.stopLoading",
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def add_script_to_evaluate_on_new_document(
            self,
            source: str,
            run_immediately: bool = False,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        每次加载新文档时执行脚本（在页面所有 scripts 执行之前执行，可以用作 hook 之类）

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-addScriptToEvaluateOnNewDocument

        :param source: 执行的脚本
        :param run_immediately: 是否立即执行（否的话只在新文档加载时执行）
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        send_data = {
            "source": source,
        }
        if run_immediately:
            send_data["runImmediately"] = run_immediately

        return self.__conn.send(
            method="Page.addScriptToEvaluateOnNewDocument",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def navigate(
            self,
            url: str,
            frame_id: str = None,
            ignore_url_check: bool = False,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        访问链接或本地文件

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-navigate

        :param url:
        :param frame_id:
        :param ignore_url_check: 忽略 url 检查
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return: 错误的时候会返回错误的原因
        """
        # url 检查
        if not ignore_url_check:
            url_parse = parse.urlparse(url)
            if not url_parse.scheme or not url_parse.hostname:
                raise errors.URLError(url)

        # 执行访问
        send_data = {
            "url": url,
        }

        if frame_id:
            send_data["frame_id"] = frame_id

        send_data.update(kwargs)

        return self.__conn.send(
            method="Page.navigate",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def get_frame_tree(
            self,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        获取当前页面的框架树

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-getFrameTree

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Page.getFrameTree",
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def capture_screenshot(
            self,
            format_type: str = "png",
            quality: int = None,
            clip: dict = None,
            from_surface: bool = True,
            capture_beyond_viewport: bool = False,
            optimize_for_speed: bool = False,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        截图

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-captureScreenshot

        clip 参考：https://chromedevtools.github.io/devtools-protocol/tot/Page/#type-Viewport

        :param format_type: jpeg, png, webp，默认值为 png
        :param quality: 压缩质量范围为 [0..100]（仅限 jpeg）
        :param clip: 仅捕获给定区域的屏幕截图（{x:1,y:1,width:1,height:1,scale:1}）
        :param from_surface: 从表面捕获屏幕截图，而不是从视图捕获屏幕截图，默认值为 true
        :param capture_beyond_viewport: 捕获视口之外的屏幕截图，默认值为 false
        :param optimize_for_speed: 优化图像编码以提高速度，而不是优化结果大小（默认为 false）
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return: {"data":""}
        """
        if format_type not in ["jpeg", "png", "webp"]:
            format_type = "png"

        send_data = {
            "format": format_type,
            "fromSurface": from_surface,
            "captureBeyondViewport": capture_beyond_viewport,
            "optimizeForSpeed": optimize_for_speed,
        }

        if clip:
            send_data["clip"] = clip
        if quality:
            send_data["quality"] = quality

        return self.__conn.send(
            method="Page.captureScreenshot",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def close(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        关闭当前页面

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-close

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Page.close",
            raise_err=raise_err,
            need_callback=need_callback,
        )
