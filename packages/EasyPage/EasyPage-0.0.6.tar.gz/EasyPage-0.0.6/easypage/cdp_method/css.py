from typing import Tuple
from easypage.conn import Conn


class CSS:
    """
        CSS

        https://chromedevtools.github.io/devtools-protocol/tot/CSS
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def enable(
            self,
            raise_err: bool = False,
            need_callback: bool = False
    ) -> Tuple[bool, dict]:
        """
        启用 css

        https://chromedevtools.github.io/devtools-protocol/tot/CSS/#method-enable

        :param raise_err:
        :param need_callback:
        :return:
        """
        return self.__conn.send(
            method="CSS.enable",
            raise_err=raise_err,
            need_callback=need_callback
        )

    def disable(
            self,
            raise_err: bool = False,
            need_callback: bool = False
    ) -> Tuple[bool, dict]:
        """
        启用 css

        https://chromedevtools.github.io/devtools-protocol/tot/CSS/#method-disable

        :param raise_err:
        :param need_callback:
        :return:
        """
        return self.__conn.send(
            method="CSS.disable",
            raise_err=raise_err,
            need_callback=need_callback
        )

    def get_computed_style_for_node(
            self,
            node_id: int,
            raise_err: bool = False,
            need_callback: bool = True
    ) -> Tuple[bool, dict]:
        """
        获取元素的 style

        https://chromedevtools.github.io/devtools-protocol/tot/CSS/#method-getComputedStyleForNode

        :param node_id:
        :param raise_err:
        :param need_callback:
        :return:
        """
        return self.__conn.send(
            method="CSS.getComputedStyleForNode",
            params={
                "nodeId": node_id
            },
            raise_err=raise_err,
            need_callback=need_callback
        )
