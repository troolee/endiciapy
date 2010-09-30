from xml_to_dict import xml_to_dict


class Object:
    pass


def _extend(obj, d):
    for k, v in d.items():
        if isinstance(v, list):
            value = []
            for item in v:
                o = Object()
                _extend(o, item)
                value.append(o)
        elif isinstance(v, dict):
            value = Object()
            _extend(value, v)
        else:
            value = v
        setattr(obj, k, value)


class EndiciaResponse:
    def __init__(self, response):
        self._xml = response
        self._dict = xml_to_dict(response)
        _extend(self, self._dict.values()[0])

    def __str__(self):
        return self._xml
