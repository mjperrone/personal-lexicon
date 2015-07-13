#!/usr/bin/env bash
# usage: `sh parse_notes.sh  path/to/top/level/directory/with/.txtfiles/in/it
# requires libreoffice/openoffice v4+ be installed and the soffice binary be put
# in your path somehow
mkdir -p docs/
find "$1" \( -name '*.docx' -o -name '*.doc' -o -name '*.odt' -o -name '*.ods' \) -exec soffice --headless --convert-to "txt:Text (encoded):UTF8" --outdir docs/ {} \;
