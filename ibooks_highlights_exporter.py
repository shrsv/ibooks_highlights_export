#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Template
from pprint import pprint
from glob import glob
import os
import sqlite3
import datetime

base1 = "~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/"
base1 = os.path.expanduser(base1)
sqlite_file = glob(base1 + "*.sqlite")

if not sqlite_file:
    print "Couldn't find the iBooks database. Exiting."
    exit()
else:
    sqlite_file = sqlite_file[0]

def bold_text(selected_text, representative_text):
    left = representative_text.find(selected_text)
    right = left + len(selected_text)

    op = representative_text[:left] + "<b>" +  representative_text[left:right] + "</b>" + representative_text[right:]
    return op

def get_color(num):
    if num == 0:
        return "b_gray"
    elif num == 1:
        return "b_green"
    elif num == 2:
        return "b_blue"
    elif num == 3:
        return "b_yellow"
    elif num == 4:
        return "b_pink"
    elif num == 5:
        return "b_violet"
    else:
        return

htmlcode = """<html>
<head>
<title>ibooks exported highlights ({{obj.date}})</title>
<style>
p {
    padding: 5px;
}
.b_gray {
    border-left: 10px solid #F2F2F2;
}

.b_green {
    border-left: 10px solid #B4F13D;
}

.b_blue {
    border-left: 10px solid #9FBFFB;
}

.b_yellow {
    border-left: 10px solid #F8EE49;
}

.b_pink {
    border-left: 10px solid #ED95C7;
}

.b_violet {
    border-left: 10px solid #CF96EA;
}
</style>
</head>
<body>
<h1>ibooks exported highlights ({{obj.date}})</h1>
{% for h in obj.highlights %}
    {% if h[1] %}
        <p class="{{ get_color(h[3]) }}">{{ bold_text(h[2], h[1]) }} <br /> <small>{{ h[0] }}</small></p>
    {% endif %}
{% endfor %}
</body>
</html>
"""

db = sqlite3.connect(sqlite_file)
cur = db.cursor()
res = cur.execute("select ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT, ZANNOTATIONSELECTEDTEXT, ZANNOTATIONSTYLE from ZAEANNOTATION;")

today = datetime.date.isoformat(datetime.date.today())
template = Template(htmlcode)
template.globals['bold_text'] = bold_text
template.globals['get_color'] = get_color
op = template.render(obj={"highlights":res, "date":today})
print op.encode('utf-16')
