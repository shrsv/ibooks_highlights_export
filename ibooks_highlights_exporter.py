#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Template
from pprint import pprint
from glob import glob
import os
import sqlite3
import datetime

asset_title_tab = {}
base1 = "~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/"
base1 = os.path.expanduser(base1)
sqlite_file = glob(base1 + "*.sqlite")

if not sqlite_file:
    print "Couldn't find the iBooks database. Exiting."
    exit()
else:
    sqlite_file = sqlite_file[0]

base2 = "~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/"
base2 = os.path.expanduser(base2)
assets_file = glob(base2 + "*.sqlite")

if not assets_file:
    print "Couldn't find the iBooks assets database. Exiting."
    exit()
else:
    assets_file = assets_file[0]

db1 = sqlite3.connect(sqlite_file)
cur1 = db1.cursor()

db2 = sqlite3.connect(assets_file)
cur2 = db2.cursor()

def bold_text(selected_text, representative_text):
    left = representative_text.find(selected_text)
    right = left + len(selected_text)

    op = representative_text[:left] + "<b>" +  representative_text[left:right] + "</b>" + representative_text[right:]
    return op

def get_book_details(assetid):
    global cur2
    res2 = cur2.execute("select ZTITLE, ZAUTHOR from ZBKLIBRARYASSET where ZASSETID=?", (assetid,))
    t =  res2.fetchone()
    return t[0] + ", " + t[1]


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
        return "b_gray"

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
        <p class="{{ get_color(h[3]) }}">{{ bold_text(h[2], h[1]) }} <br />
        <small>{{ get_book_details(h[0]) }}</small></p>
    {% endif %}
{% endfor %}
</body>
</html>
"""

res1 = cur1.execute("select ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT, ZANNOTATIONSELECTEDTEXT, ZANNOTATIONSTYLE from ZAEANNOTATION order by ZANNOTATIONASSETID;")
today = datetime.date.isoformat(datetime.date.today())
template = Template(htmlcode)
template.globals['bold_text'] = bold_text
template.globals['get_color'] = get_color
template.globals['get_book_details'] = get_book_details

# beginning another way of doing the same thing, just more efficient
res2 = cur2.execute("select distinct(ZASSETID), ZTITLE, ZAUTHOR from ZBKLIBRARYASSET")
for assetid, title, author in res2:
    asset_title_tab[assetid] = [title, author]
exit()

op = template.render(obj={"highlights":res1, "date":today})
print op.encode('utf-16')
