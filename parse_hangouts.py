#!/usr/bin/env python
# usage: `python parse_hangouts.py path/to/takeout/`

import json
import sys


# holy wow this format is a mess without any docs
def parse_hangouts(path):
    data = json.loads(open(path, 'r').read())
    ids = {}
    for conversation in data['conversation_state']:
        for x in conversation['conversation_state']['conversation']['participant_data']:
            if 'fallback_name' in x:
                ids[x['id']['gaia_id']] = x['fallback_name']
                for message in conversation['conversation_state']['event']:
                    sender = ids.get(message['sender_id']['gaia_id'], "notfound")
                    if sender in ('Mike Perrone', 'Michael Perrone')\
                            and 'chat_message' in message\
                            and 'segment' in message['chat_message']['message_content']:
                        for segment in message['chat_message']['message_content']['segment']:
                            if 'text' in segment:
                                print segment['text']


parse_hangouts(sys.argv[-1] + "Hangouts/Hangouts.json")
