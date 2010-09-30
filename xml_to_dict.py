import re
from xml.dom.minidom import parseString, Text


def _process_node(node, res):
    distinct_node_name = set()
    for i in node.childNodes:
        if isinstance(i, Text):
            distinct_node_name.add('_')
        else:
            distinct_node_name.add(i.tagName)
    is_array = len(node.childNodes) > 1 and len(distinct_node_name) == 1
    if is_array:
        childs = []
        res[node.tagName] = childs
        for childNode in node.childNodes:
            child = {childNode.tagName: None}
            childs.append(_process_node(childNode, child))
    else: 
        childs = {}
        res[node.tagName] = childs
        for childNode in node.childNodes:
            if isinstance(childNode, Text):
                res[node.tagName][node.tagName] = childNode.data.strip()
            else:
                res[node.tagName].update(_process_node(childNode, res[node.tagName]))
        if node.tagName in childs and len(childs) == 1:
            res[node.tagName] = res[node.tagName][node.tagName]
    return res


def xml_to_dict(data):
    data = re.sub('>\s+<', '><', data.strip())
    dom = parseString(data)
    root = dom.documentElement
    
    res = {root.tagName: None}
    res = _process_node(root, res)

    return res


if __name__ == '__main__':
    data = '''<?xml version="1.0" encoding="UTF-8"?>
    <StatusResponse>
        <AccountID>750711</AccountID>
        <ErrorMsg/>
        <Test>Y</Test>
        <StatusList>
            <PICNumber>9122148008600123456781
                <Status>Not Found</Status>
                <StatusCode>-1</StatusCode>
            </PICNumber>
            <PICNumber>9122148008600123456781
                <Status>The tracking information for this item was received by the US Postal Service at 12:00 PM on 07/24/2007 but the item has not yet been scanned in the mailstream. Please check back later.</Status>
                <StatusCode>A</StatusCode>
            </PICNumber>
            <PICNumber>9122148008600123456781
                <Status>Your item was delivered at 10:09 AM on 08/06/2007 in PALO ALTO CA 94301.</Status>
                <StatusCode>D</StatusCode>
            </PICNumber>
            <PICNumber>9122148008600123456781
                <Status>Found - No Status</Status>
                <StatusCode>0</StatusCode>
            </PICNumber>
        </StatusList>
    </StatusResponse>
    '''
    res = xml_to_dict(data)
    from json import dumps
    print dumps(res, indent=2)
