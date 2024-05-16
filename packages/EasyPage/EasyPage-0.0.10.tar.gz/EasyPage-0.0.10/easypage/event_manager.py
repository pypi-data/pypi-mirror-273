"""
    事件管理器

    用来管理 enable、disable

    TODO 可以试试装饰器模式
"""
from threading import Lock
from easypage.cdp import CDP
from easypage.logger import logger


class EventManager:
    def __init__(self):
        self.events = {}

    def enable(self, driver_id: str, cdp: CDP, event_name: str):
        """
        启用事件

        :param driver_id: 页面的 id
        :param cdp: cdp 对象
        :param event_name: 例如 css
        :return:
        """
        self.execute(driver_id, cdp, event_name, True, "enable")

    def disable(self, driver_id: str, cdp: CDP, event_name: str):
        """
        禁用事件

        :param driver_id: 页面的 id
        :param cdp: cdp 对象
        :param event_name: 例如 css
        :return:
        """
        self.execute(driver_id, cdp, event_name, False, "disable")

    def execute(self, driver_id: str, cdp: CDP, event_name: str, status: bool, func_name: str, **kwargs):
        """
        事件

        :param driver_id: 页面的 id
        :param cdp: cdp 对象
        :param event_name: 例如 css
        :param status: 启用还是禁用
        :param func_name: 启用的方法名称如：enable、disable
        :return:
        """
        # 判断有没有当前方法
        cdp_method = getattr(cdp, event_name, False)
        if cdp_method is False:
            logger.warning(f"cdp 没有事件 {event_name}")
            return

        func = getattr(cdp_method, func_name, False)
        if func is False:
            logger.warning(f"{event_name} 没有方法 {func_name}")
            return

        # 初始化数据
        if event_name not in self.events:
            self.events[driver_id] = {
                "lock": Lock(),
            }

        # 判断是否在启用状态
        with self.events[driver_id]["lock"]:
            if self.events[driver_id][event_name]:
                return

            # 设置启用状态并启用
            self.events[driver_id][event_name] = status
            func(**kwargs)
