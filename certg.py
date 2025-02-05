#!/usr/bin/env python3

# Copyright 2013 Facundo Batista
# This file is GPL v3, part of http://github.com/facundobatista/certg
# project; refer to it for more info.

import subprocess
import sys
import tempfile

import yaml


if len(sys.argv) != 2:
    print("Usage: {} <config.yaml>".format(sys.argv[0]))
    exit()

with open(sys.argv[1], 'rt', encoding="utf-8") as fh:
    config = yaml.safe_load(fh)

with open(config['svg_source'], "rt", encoding="utf-8") as fh:
    content_base = fh.read()

# get all the replacing attrs
replacing_attrs = set()
for data in config['replace_info']:
    replacing_attrs.update(data)

for data in config['replace_info']:

    # replace content
    content = content_base
    for attr in replacing_attrs:
        value = data.get(attr)
        if value is None:
            # both because the attr is not supplied, or supplied empty
            value = ""
        print(value)
        content = content.replace("{{" + attr + "}}", value)

    # write the new svg
    _, tmpfile = tempfile.mkstemp()
    with open(tmpfile, "wt", encoding="utf-8") as fh:
        fh.write(content)

    # generate PDF
    distinct = data[config['result_distinct']].lower().replace(" ", "_")
    result = "{}-{}.pdf".format(config['result_prefix'], distinct)

    # Below you need to add the route to the executable of inkscape
    # e.g Windows: C:/Program Files/Inkscape/inkscape.exe
    # e.g Mac: /Applications/Inkscape.app/Contents/MacOS/inkscape
    cmd = ["/Applications/Inkscape.app/Contents/MacOS/inkscape", '--export-pdf={}'.format(result), tmpfile]
    subprocess.check_call(cmd)
