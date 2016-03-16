#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
from glob import glob
import os
import sqlite3
import datetime
import argparse
import re



PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)


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

db1 = sqlite3.connect(sqlite_file, check_same_thread=False)
cur1 = db1.cursor()

db2 = sqlite3.connect(assets_file, check_same_thread=False)
cur2 = db2.cursor()

def get_all_titles():
    global cur2
    res = cur2.execute("select ZASSETID, ZTITLE, ZAUTHOR from ZBKLIBRARYASSET;").fetchall()
    m = {}
    for r in res:
        m[r[0]] = {"ZTITLE": r[1], "ZAUTHOR": r[2]}

    return m


def get_all_relevant_assetids_and_counts():
    global cur1
    q = "select count(*), ZANNOTATIONASSETID from ZAEANNOTATION where ZANNOTATIONREPRESENTATIVETEXT " \
        "IS NOT NULL group by ZANNOTATIONASSETID;"
    res = cur1.execute(q).fetchall()
    return res

def get_all_relevant_titles():
    aids_and_counts = get_all_relevant_assetids_and_counts()
    print aids_and_counts
    all_titles = get_all_titles()

    op = {}

    for cnt, aid in aids_and_counts:
        all_titles[aid]["COUNT"] = cnt
        op[aid] = all_titles[aid]

    return op

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

def get_all_highlights():
    global cur1
    res1 = cur1.execute("select ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT, ZANNOTATIONSELECTEDTEXT, "
                        " ZANNOTATIONSTYLE from ZAEANNOTATION order by ZANNOTATIONASSETID, ZPLLOCATIONRANGESTART;")

    return res1

def get_chapter_name():
    global cur1
    res1 = cur1.execute("select ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT, ZANNOTATIONSELECTEDTEXT, "
                        " ZANNOTATIONSTYLE, ZFUTUREPROOFING5 from ZAEANNOTATION "
                        "order by ZANNOTATIONASSETID, ZPLLOCATIONRANGESTART ;")
    t =  res1.fetchone()
    return t[4]

def make_text_readable(text, every=80):
    return '\N'.join(text[i:i+every] for i in xrange(0, len(text), every))


def get_asset_title_tab():
    global cur2

    res2 = cur2.execute("select distinct(ZASSETID), ZTITLE, ZAUTHOR from ZBKLIBRARYASSET")
    for assetid, title, author in res2:
        asset_title_tab[assetid] = [title, author]

    return asset_title_tab


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

def get_mm_color (num):
    if num>7:
        return ((num - 2) % 6) + 2
    else:
        return num


parser = argparse.ArgumentParser(description='iBooks Highlights Exporter')
parser.add_argument('-o', action="store", default="output.html", dest="fname",
        help="Specify output filename (default: output.html)")
parser.add_argument('--notoc', action="store_true", help="Disable the javascript TOC in the output")
parser.add_argument('--nobootstrap', action="store_true", help="Disable the bootstrap library in the output")
parser.add_argument('--mindmap', action="store_true", help="Generate a Simple Mind Mind Map instead of .html file. "
                                                           "You need to specify a book first.")
parser.add_argument('--list', action="store_true", help="Lists a books having highlights.")
parser.add_argument('--book', action="store", help="Name of the book for which annotations will be exported",
                    dest="book")
args = parser.parse_args()




if args.list:
    #only prints a list of books with highlights and exists
    res2 = cur2.execute("select distinct(ZASSETID), ZTITLE, ZAUTHOR from ZBKLIBRARYASSET")
    for assetid, title, author in res2:
        print assetid,title, author

else:
    if args.mindmap:
        if args.book:
            if args.fname == 'output.html':
                args.fname = 'output.smmx'
            with open(args.fname, 'w') as f:
                template = TEMPLATE_ENVIRONMENT.get_template("simple_mind_template.xml")
                template.globals['get_mm_color'] = get_mm_color
                template.globals['make_text_readable'] = make_text_readable
                template.globals['get_book_details'] = get_book_details

                res1 = cur1.execute("select distinct(ZFUTUREPROOFING5) from ZAEANNOTATION "
                                "where (ZANNOTATIONSELECTEDTEXT not NULL)  AND  `ZANNOTATIONASSETID` = '"+str(args.book)+"' order by"
                                " ZANNOTATIONASSETID, ZPLLOCATIONRANGESTART ;")
                chapters = []
                for chapter in res1:
                    if chapter not in chapters:
                        chapters.append(chapter[0])
                print chapters


                chapters_list = []
                counter = 1
                for ch in chapters:
                    chapters_list.append([ch,chapters.index(ch)+1, counter])
                    counter += 1


                res1 = cur1.execute("select ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT, ZANNOTATIONSELECTEDTEXT, "
                                "ZFUTUREPROOFING5, ZANNOTATIONSTYLE, ZFUTUREPROOFING5 from ZAEANNOTATION "
                                "where (ZANNOTATIONSELECTEDTEXT not NULL)  AND  `ZANNOTATIONASSETID` = '"+str(args.book)+"' order by"
                                " ZANNOTATIONASSETID, ZPLLOCATIONRANGESTART ;")


                annotations = []
                for ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT, ZANNOTATIONSELECTEDTEXT, \
                       ZFUTUREPROOFING5, ZANNOTATIONSTYLE, ZFUTUREPROOFING5 in res1:
                    annotations.append([ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT, ZANNOTATIONSELECTEDTEXT,
                       ZFUTUREPROOFING5, ZANNOTATIONSTYLE, chapters.index(ZFUTUREPROOFING5) + 1, counter])
                    counter += 1

                # beginning another way of doing the same thing, just more efficient
                res2 = cur2.execute("select distinct(ZASSETID), ZTITLE, ZAUTHOR from ZBKLIBRARYASSET")
                for assetid, title, author in res2:
                    asset_title_tab[assetid] = [assetid, title, author]

                today = datetime.date.isoformat(datetime.date.today())
                print get_book_details(args.book)
                print args.book

                smmx = template.render(obj={"last":"###", "date":today, "highlights":annotations,
                    "assetlist":asset_title_tab, "notoc":args.notoc, "bookname": get_book_details(args.book),
                    "nobootstrap":args.nobootstrap, "chapters": chapters_list})
                f.write(smmx.encode('utf-8'))
        else:
            print 'Please, specify book for which you want MM to be created. List can be obtained with --list'

    else:
        with open(args.fname, 'w') as f:

            res1 = cur1.execute("select ZANNOTATIONASSETID, ZANNOTATIONREPRESENTATIVETEXT, ZANNOTATIONSELECTEDTEXT, "
                                "ZFUTUREPROOFING5, ZANNOTATIONSTYLE, ZFUTUREPROOFING5 from ZAEANNOTATION order by"
                                " ZANNOTATIONASSETID, ZPLLOCATIONRANGESTART ;")
            today = datetime.date.isoformat(datetime.date.today())


            # beginning another way of doing the same thing, just more efficient
            res2 = cur2.execute("select distinct(ZASSETID), ZTITLE, ZAUTHOR from ZBKLIBRARYASSET")
            for assetid, title, author in res2:
                asset_title_tab[assetid] = [title, author]

            template = TEMPLATE_ENVIRONMENT.get_template("simpletemplate.html")
            template.globals['bold_text'] = bold_text
            template.globals['get_color'] = get_color
            template.globals['get_book_details'] = get_book_details
            template.globals['get_chapter_name'] = get_chapter_name

            html = template.render(obj={"last":"###", "date":today, "highlights":res1,
                "assetlist":asset_title_tab, "notoc":args.notoc,
                "nobootstrap":args.nobootstrap})
            f.write(html.encode('utf-8'))