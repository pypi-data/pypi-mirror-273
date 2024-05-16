"""
    Driver 的基类
"""
from easypage.cdp import CDP
from abc import abstractmethod
from easypage.conn import Conn, DRIVER_TYPE
from easypage.options import BrowserOptions


class Driver:
    def __init__(self, opts: BrowserOptions, driver_type: DRIVER_TYPE, driver_id: str):
        """

        :param opts:
        :param driver_type:
        :param driver_id:
        """
        self._opts = opts
        self.__conn = Conn(
            address=opts.address,
            driver_type=driver_type,
            driver_id=driver_id,
            timeout=opts.timeout
        )
        self.__cdp = CDP(conn=self.__conn)

    @property
    def cdp(self) -> CDP:
        """
        获取 Chrome DevTools Protocol 实例

        :return:
        """
        return self.__cdp

    @abstractmethod
    def close(self):
        """
        资源回收

        :return:
        """
