#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Template
from pprint import pprint
import os
import sqlite3
import datetime

basefolder = \
"/Users/shrsv/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/AEAnnotation_v10312011_1727_local.sqlite"

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

db = sqlite3.connect(basefolder)
cur = db.cursor()
res = cur.execute("select ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT from ZAEANNOTATION;")

today = datetime.date.isoformat(datetime.date.today())
template = Template(htmlcode)
op = template.render(obj={"highlights":res, "date":today})
print op.encode('utf-16')
