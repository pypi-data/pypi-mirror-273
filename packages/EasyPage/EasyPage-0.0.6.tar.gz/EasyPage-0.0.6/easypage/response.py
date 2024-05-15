import base64
from typing import Union

from easypage.cdp import CDP
from easypage.request import Request


class Response:

    def __init__(self, data: dict, request: Request, cdp: "CDP"):
        """

        :param data: 响应体
        :param request: 请求
        :param cdp: cdp
        """
        self.__cdp = cdp
        self.request = request
        self.request_id = data["requestId"]
        self._response = data["response"]
        self.response_from = data["type"]

        # 发出获取响应体的请求（这个请求不能立刻获取结果不然会卡住，而且可能也没有加载完成）
        self._body: Union[str, bytes] = ""  # 暂时为空

    def _get_body(self):
        """
        获取响应体

        :return:
        """
        get_status, body_await = self.__cdp.network.get_response_body(
            request_id=self.request_id,
            need_callback=False
        )

        def body_callback(status: bool, body_data: dict):
            """
            body 获取到之后重新设置

            :param status: 回调是否正常
            :param body_data:
            :return:
            """
            # 根据结果重新设置 body
            if status:
                body = body_data.get("body", b"")

                if body_data.get('base64Encoded'):
                    body = base64.b64decode(body)

                self._body = body

            # 触发事件
            self.__cdp.emit(event=f"handle_response_{self.request_id}")

        # 发送成功的话，创建事件
        if get_status:
            self.__cdp.once(
                event=f"Network.getResponseBody-{body_await['id']}",
                callback=body_callback
            )

    @property
    def url(self) -> str:
        return self._response["url"]

    @property
    def status(self) -> int:
        return self._response.get("status", 0)

    @property
    def status_text(self) -> str:
        """
        状态字符串：'OK'

        :return:
        """
        return self._response.get("statusText", 0)

    @property
    def headers(self) -> dict:
        return self._response.get("headers", {})

    @property
    def mime_type(self) -> str:
        """
        类型如：'text/html'

        :return:
        """
        return self._response.get("mimeType", "")

    @property
    def charset(self) -> str:
        """
        编码格式如：'charset'

        :return:
        """
        return self._response.get("charset", "")

    @property
    def remote_ip_address(self) -> str:
        """
        远程端口

        :return:
        """
        return self._response.get("remoteIPAddress", "")

    @property
    def protocol(self) -> str:
        """
        协议：'http/1.1'

        :return:
        """
        return self._response.get("protocol", "")

    @property
    def security_details(self) -> dict:
        """
        安全详情

        返回值大概如下：
            {
                "protocol": "TLS 1.3",
                "keyExchange": "",
                "keyExchangeGroup": "X25519",
                "cipher": "AES_256_GCM",
                "certificateId": 0,
                "subjectName": "*.csdnimg.cn",
                "sanList": [
                    "*.csdnimg.cn",
                    "csdnimg.cn"
                ],
                "issuer": "RapidSSL Global TLS RSA4096 SHA256 2022 CA1",
                "validFrom": 1696809600,
                "validTo": 1728777599,
                "signedCertificateTimestampList": [],
                "certificateTransparencyCompliance": "unknown",
                "serverSignatureAlgorithm": 2052,
                "encryptedClientHello": false
            }

        :return:
        """
        return self._response.get("securityDetails", {})

    @property
    def body(self) -> Union[str, bytes]:
        """
        响应体

        大致的关系如下：
            响应类型                返回值类型
            image/png              bytes
            application/json       str

        :return:
        """
        return self._body

    def __repr__(self):
        return f"<Response status={self.status} url=\"{self.url}\">"
