import requests

class HttpRequestBuilder:
    _session = requests.Session()

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

    def set_multipart_file(self, file_name: str,  file_content: bytes, content_type: str, field_name: str = "file"):
        """
        Set file for multipart/form-data request.

        :param file_name: file name
        :param file_content: binary file content
        :param content_type: type of the file
        :param field_name: multipart field name
        :return: self
        """
        self._request_data["files"] = {
            field_name:(
            file_name,
            file_content,
            content_type)
        }
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
        return getattr(self._session, method.lower())(
            **self._request_data,
            timeout=self._request_timeout,
        )