#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Template
from pprint import pprint
from glob import glob
import os
import sqlite3
import datetime

base = "~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/"
base = os.path.expanduser(base)
sqlite_file = glob(base + "*.sqlite")

if not sqlite_file:
    print "Couldn't find the iBooks database. Exiting"
    exit()
else:
    sqlite_file = sqlite_file[0]

def bold_text(selected_text, representative_text):
    left = representative_text.find(selected_text)
    right = left + len(selected_text)

    op = representative_text[:left] + "<b>" +  representative_text[left:right] + "</b>" + representative_text[right:]
    return op

htmlcode = """<html>
<head>
<title>ibooks exported highlights ({{obj.date}})</title>
</head>
<body>
<h1>ibooks exported highlights ({{obj.date}})</h1>
{% for h in obj.highlights %}
    {% if h[1] %}
        <p>{{ bold_text(h[2], h[1]) }} <br /> <small>{{ h[0] }}</small></p>
    {% endif %}
{% endfor %}
</body>
</html>
"""

db = sqlite3.connect(sqlite_file)
cur = db.cursor()
res = cur.execute("select ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT, ZANNOTATIONSELECTEDTEXT from ZAEANNOTATION;")

today = datetime.date.isoformat(datetime.date.today())
template = Template(htmlcode)
template.globals['bold_text'] = bold_text
op = template.render(obj={"highlights":res, "date":today})
print op.encode('utf-16')
