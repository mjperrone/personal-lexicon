#!/usr/bin/env bash
# usage: `sh parse_notes.sh  path/to/top/level/directory/with/.txtfiles/in/it
find "$1" -name '*.txt' -exec cat {} \;
