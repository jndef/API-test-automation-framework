import requests

class HttpRequestBuilder:
    def __init__(self):
        self._request_data = {}
        self._request_timeout = 10.0

    def set_headers(self, headers):
        """
        Method to set headers for request builder
        :param headers:
        :return: self
        """
        self._request_data["headers"] = headers
        return self

    def set_url(self, url: str):
        """
        Method to set request url for request builder
        :param url:
        :return: self
        """
        self._request_data["url"] = url
        return self

    def set_request_body(self, json):
        """
        Method to set request body (json) for request builder if required
        :param json:
        :return: self
        """
        self._request_data["json"] = json
        return self

    def set_query_params(self, **kwargs):
        """
        Method to set request query params for request builder if required
        :param kwargs: query and value params
        :return: self
        """
        self._request_data["params"] = {}
        for key, value in kwargs.items():
            self._request_data["params"][key] = value
        return self

    def send(self,method: str):
        assert method.upper() in ["GET", "POST", "PUT", "PATCH", "DELETE"]
        return getattr(requests, method.lower())(
            **self._request_data,
            timeout=self._request_timeout,
        )