#!/usr/bin/env python
# usage: `python path/to/facebook/output`


import sys
import xml.etree.ElementTree as ElementTree


# here's the structure of the facebook messages output:
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


# here's the structure of the facebook wall output:
# html
#   body
#     div class contents
#       div
#         div class meta
#           date...
#         Mike Perrone updated his status
#         div class comment
#           <status update>
#         p
#         p
#         div class meta
#           date...
#       ...
#
# let's just look for status updates for now...
def parse_wall(filename):
    doc = ElementTree.iterparse(
        filename,
        ('start', 'end'),
        parser=ElementTree.XMLParser(
            target=ElementTree.TreeBuilder(),
            encoding='utf-8'
        )
    )
    status = False

    for event, elem in doc:
        if event == 'start':
            if status and elem.attrib.get('class') == 'comment':
                yield elem.text
            if elem.tag == 'div':
                status = elem.tail and 'Mike Perrone updated his' in elem.tail


data = parse_wall(sys.argv[1] + "html/wall.htm")
for message in data:
    print message

data = parse_messages(sys.argv[1] + "html/messages.htm")
for message in data:
    print message
