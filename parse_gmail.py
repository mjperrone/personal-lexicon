#!/usr/bin/env python
# usage: `python parse_gmail.py path/to/gmail/output.mbox`

import mailbox
import sys
from email_reply_parser import EmailReplyParser

mbox = mailbox.mbox(sys.argv[-1])
for message in mbox:
    if message['From'] in ("Michael Perrone <mjperrone@wpi.edu>", "Mike Perrone <mike.j.perrone@gmail.com>"):
        while message.is_multipart():
            message = message.get_payload(0)
        text = message.get_payload()
        reply = EmailReplyParser.parse_reply(text)
        signiture_index = reply.find('-Mike Perrone')
        if signiture_index >= 0:
            reply = reply[:signiture_index]
        print reply
