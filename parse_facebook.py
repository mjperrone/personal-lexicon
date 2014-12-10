#!/usr/bin/env python
# usage: `python path/to/facebook/output`

# here's the structure of the facebook output:
# html
#   body
#     div class contents
#       div
#         div class thread
#           div class message
#             div class message_header
#               span class user
#                 Michael Perrone
#               span class meta
#                 date...
#           p <text>
#           div class message ...
#           p <text>

import sys
import xml.etree.ElementTree as ElementTree


def parse_messages(filename):
    doc = ElementTree.iterparse(
        filename,
        ('start', 'end'),
        parser=ElementTree.XMLParser(
            target=ElementTree.TreeBuilder(),
            encoding='utf-8'
        )
    )

    user = ''
    for event, elem in doc:
        if event == 'start':
            if elem.attrib.get('class') == 'user':
                user = elem.text
            if elem.tag == 'p':
                if user in ('Mike Perrone', 'Michael Perrone'):
                    yield elem.text

data = parse_messages(sys.argv[1] + "html/messages.htm")
for message in data:
    print message
