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

print sqlite_file

htmlcode = """<html>
<head>
<title>ibooks exported highlights ({{obj.date}})</title>
</head>
<body>
<h1>ibooks exported highlights ({{obj.date}})</h1>
{% for h in obj.highlights %}
    {% if h[1] %}
        <p>{{ h[1] }} <br /> <small>{{ h[0] }}</small></p>
    {% endif %}
{% endfor %}
</body>
</html>
"""

db = sqlite3.connect(sqlite_file)
cur = db.cursor()
res = cur.execute("select ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT from ZAEANNOTATION;")

today = datetime.date.isoformat(datetime.date.today())
template = Template(htmlcode)
op = template.render(obj={"highlights":res, "date":today})
print op.encode('utf-16')
