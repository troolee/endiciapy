from xml import sax
from io import StringIO
import re


class _Handler(sax.handler.ContentHandler):
    def __init__(self):
        self.stack = []
        self.current_text = None
        self.res = {}

    def _write_to_res(self, path, key, value):
        d = self.res
        for p in path:
            if p not in d:
                d[p] = {}
            d = d[p]
        d[key] = value

    def startElement(self, name, attrs):
        self.current_text = None
        self._write_to_res(self.stack, name, {})
        self.stack.append(name)

    def characters(self, data):
        self.current_text = (self.current_text or '') + data

    def endElement(self, name):
        name = self.stack.pop()
        if self.current_text:
            self._write_to_res(self.stack, name, self.current_text)
            self.current_text = None
        else:
            pass
        
def _xml_to_dict(xml):
    handler = _Handler()
    xml_parser = sax.make_parser()
    xml_parser.setContentHandler(handler)
    response = re.sub('>\s+<', '><', xml)
    response = StringIO(response)
    xml_parser.parse(response)
    return handler.res
        

class Object:
    pass
        

def _extend(obj, d):
    for k, v in d.items():
        if isinstance(v, dict):
            value = Object()
            _extend(value, v)
        else:
            value = v
        setattr(obj, k, value)


class EndiciaResponse:
    def __init__(self, response):
        self._xml = response
        self._dict = _xml_to_dict(response)
        _extend(self, self._dict.values()[0])

    def __str__(self):
        return self._xml
