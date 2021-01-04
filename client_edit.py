import logging

import aiohttp.client
from lxml import etree
from multidict import MultiDict

import exceptions_edit
from common_edit import py2xml, schema, xml2py
from exceptions_edit import xml2py_exception


log = logging.getLogger(__name__)


class ServerProxy(object):
    __slots__ = "client", "url", "loop", "headers", "encoding", "huge_tree"

    USER_AGENT = (
        "aiohttp XML-RPC client "
        "(Python: 3.9, version: 0.1)"
    )

    def __init__(self, url, client=None, headers=None, encoding=None, huge_tree=False, **kwargs):
        self.headers = MultiDict(headers or {})

        self.headers.setdefault("Content-Type", "text/xml")
        self.headers.setdefault("User-Agent", self.USER_AGENT)

        self.encoding = encoding
        self.huge_tree = huge_tree

        self.url = str(url)
        self.client = client or aiohttp.client.ClientSession(**kwargs)

    @staticmethod
    def _make_request(method_name, *args, **kwargs):
        root = etree.Element("methodCall")
        method_el = etree.Element("methodName")
        method_el.text = method_name

        root.append(method_el)

        params_el = etree.Element("params")
        root.append(params_el)

        for arg in args:
            param = etree.Element("param")
            val = etree.Element("value")
            param.append(val)
            params_el.append(param)
            val.append(py2xml(arg))

        if kwargs:
            param = etree.Element("param")
            val = etree.Element("value")
            param.append(val)
            params_el.append(param)
            val.append(py2xml(kwargs))

        return root

    def _parse_response(self, body, method_name):
        try:
            if log.getEffectiveLevel() <= logging.DEBUG:
                log.debug("Server response: \n%s", body.decode())

            parser = etree.XMLParser(huge_tree=self.huge_tree)
            response = etree.fromstring(body, parser)
            schema.assertValid(response)
        except etree.DocumentInvalid:
            raise ValueError("Invalid body")

        result = response.xpath("//params/param/value")
        if result:
            if len(result) < 2:
                return xml2py(result[0])

            return [xml2py(item) for item in result]

        fault = response.xpath("//fault/value")
        if fault:
            err = xml2py(fault[0])

            raise xml2py_exception(
                err.get("faultCode", exceptions_edit.SystemError.code),
                err.get("faultString", "Unknown error"),
                default_exc_class=exceptions_edit.ServerError,
            )

        raise exceptions_edit.ParseError(
            'Respond body for method "%s" '
            "not contains any response.", method_name,
        )

    async def __remote_call(self, method_name, *args, **kwargs):
        async with self.client.post(
            str(self.url),
            data=etree.tostring(
                self._make_request(method_name, *args, **kwargs),
                xml_declaration=True,
                encoding=self.encoding,
            ),
            headers=self.headers,
        ) as response:
            response.raise_for_status()

            return self._parse_response((await response.read()), method_name)

    def __getattr__(self, method_name):
        return self[method_name]

    def __getitem__(self, method_name):
        def method(*args, **kwargs):
            return self.__remote_call(method_name, *args, **kwargs)

        return method

    def __aenter__(self):
        return self.client.__aenter__()

    def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.client.__aexit__(exc_type, exc_val, exc_tb)

    def close(self):
        return self.client.close()
