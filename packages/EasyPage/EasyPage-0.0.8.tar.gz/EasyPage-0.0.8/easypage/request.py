import json
from urllib import parse


class Request:
    def __init__(self, data: dict):
        self.request_id = data["requestId"]
        self.frame_id = data.get("frameId", "")
        self.resource_type = data["resourceType"] if "resourceType" in data else data["type"]
        self._request = data["request"]
        self._url_parse = parse.urlparse(self._request["url"])

    @property
    def url(self) -> str:
        return self._request["url"]

    @property
    def clean_url(self) -> str:
        return self._url_parse.scheme + "://" + self._url_parse.hostname + self._url_parse.path

    @property
    def method(self) -> str:
        return self._request.get("method", "")

    @property
    def headers(self) -> dict:
        return self._request.get("headers", {})

    @property
    def cookies(self) -> dict:
        cookie = self.headers.get("Cookie") or self.headers.get("cookie")
        if not cookie:
            return {}

        cookie_res = {}

        for c in cookie.split(";"):
            c = c.strip()
            index = c.index("=")
            cookie_res[c[:index]] = c[index + 1:]

        return cookie_res

    @property
    def post_data(self) -> dict:
        data = {}

        if self._request.get("hasPostData"):
            data = self._request.get("postData")
            if data:
                data = json.loads(data)

        return data

    @property
    def params(self) -> dict:
        data = {}

        if self._url_parse.query:
            for i in self._url_parse.query.split("&"):
                index = i.index("=")
                data[i[:index]] = i[index + 1:]

        return data

    def __repr__(self):
        return f"<Request method=\"{self.method}\" url=\"{self.url}\">"
