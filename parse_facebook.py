#!/usr/bin/env python
# usage: `python parse_facebook.py path/to/facebook/output`

import sys
import xml.etree.ElementTree as ElementTree
import glob


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
def parse_wall(filename):
    doc = ElementTree.iterparse(
        filename,
        ('start', 'end'),
        parser=ElementTree.XMLParser(
            target=ElementTree.TreeBuilder(),
            encoding='utf-8'
        )
    )
    my_content = False

    for event, elem in doc:
        if event == 'start':
            if my_content and elem.attrib.get('class') == 'comment':
                yield elem.text
            if elem.tag == 'div':
                my_content = elem.tail and any(map(
                    lambda x: x in elem.tail,
                    ['Mike Perrone updated his',
                     'Mike Perrone shared a link',
                     'Mike Perrone added a new photo to the album']))


# here's the structure of the facebook photos output:
# html
#   body
#     div class contents
#       div class block
#         div
#           div class meta
#             <date photo posted>
#           div class comment
#             span class user
#               <name of commenter>
#             <the comment>
#             span class meta
#               <date of comment>
#           div class comment
#           ... and so on for more comments on thie photo ...
#       div class block
#         ... and  so on for more pictures in this album ...
def parse_photo_comments(filename):
    doc = ElementTree.iterparse(
        filename,
        ('start', 'end'),
        parser=ElementTree.XMLParser(
            target=ElementTree.TreeBuilder(),
            encoding='utf-8'
        )
    )

    for event, elem in doc:
        if event == 'start':
            if elem.attrib.get('class') == 'user' and elem.text == 'Mike Perrone':
                yield elem.tail


data = parse_wall(sys.argv[1] + "html/wall.htm")
for message in data:
    print message

data = parse_messages(sys.argv[1] + "html/messages.htm")
for message in data:
    print message

for photo in glob.glob(sys.argv[1] + "photos/*/index.htm"):
    data = parse_photo_comments(photo)
    for message in data:
        print message
