from xml.sax.saxutils import escape, quoteattr

def _escape(value):
    return escape(str(value))
def _quoteattr(value):
    return quoteattr(str(value))


def _indent(s, level, format):
    if format:
        s.write(u'    ' * level)


def _nl(s, format):
    if format:
        s.write(u'\n')


def _process_value(s, key, value, level, format):
    _indent(s, level, format)
    key = str(key)
    if value is not None:
        value = unicode(_escape(value))
        s.write(u'<%s>' % key)
        s.write(value)
        s.write(u'</%s>' % key)
    else:
        s.write(u'<%s />' % key)
    _nl(s, format)


def _process_list(s, key, value, level, format):
    _indent(s, level, format)
    key = str(key)
    if value is not None:
        s.write(u'<%s>' % key)
        _nl(s, format)
        for i in value:
            k, v = i.keys()[0], i.values()[0]
            _process(s, k, v, level + 1, format)
        _indent(s, level, format)
        s.write(u'</%s>' % key)
    else:
        s.write(u'<%s />' % key)
    _nl(s, format)


def _process(s, key, value, level, format):
    if isinstance(value, dict):
        _process_dict(s, key, value, level + 1, format)
    elif isinstance(value, list):
        _process_list(s, key, value, level + 1, format)
    else:
        _process_value(s, key, value, level + 1, format)


def _process_dict(s, key, value, level, format):
    _indent(s, level, format)
    s.write(u'<%s' % key)
    if '_' in value:
        for attr, attr_value in value['_'].items():
            s.write(u' %s=%s' % (attr, _quoteattr(attr_value)))
        del value['_']
    if value:
        s.write(u'>')
        _nl(s, format)
        for k, v in value.items():
            _process(s, k, v, level + 1, format)
        _indent(s, level, format)
        s.write(u'</%s>' % key)
    else:
        s.write(u' />')
    _nl(s, format)


def to_xml(stream, data, format=False):
    assert(isinstance(data, dict))
    for k, v in data.items():
        _process_dict(stream, k, v, 0, format)
