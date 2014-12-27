#!/usr/bin/env python
# usage: `python parse_gmail.py path/to/gmail/output.mbox`

import mailbox
import sys
from email_reply_parser import EmailReplyParser


def first_non_neg(iter):
    for i in iter:
        if i >= 0:
            return i
    return -1


def parse_mbox(path):
    mbox = mailbox.mbox(path)
    messages = []
    for message in mbox:
        if message['From'] in ("Michael Perrone <mjperrone@wpi.edu>", "Mike Perrone <mike.j.perrone@gmail.com>"):
            while message.is_multipart():
                message = message.get_payload(0)
            text = message.get_payload()

            # use Zapier's port of Github's open source reply parser to parse just the reply and not the quoted text.
            reply = EmailReplyParser.parse_reply(text)

            # I'm very consistent with my signature, so trim off anything after
            # it, in case EmailReplyParser couldn't figure that out. Also,
            # EmailReplyParser can't figure out gmail's forwarded message thing
            signature_index = first_non_neg([
                reply.find('-Mike Perrone'),
                reply.find('-Michael Perrone'),
                reply.find("---------- Forwarded message ----------")
            ])
            if signature_index >= 0:
                reply = reply[:signature_index]
            messages.append(reply)
    return messages

print parse_mbox(sys.argv[-1])
