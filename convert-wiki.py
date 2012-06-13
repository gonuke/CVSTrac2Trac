#!/usr/bin/python

import sqlite3
import re

def cvstrac2trac(sublist,oldwiki):
    
    for match,replace in sublist:
        newwiki = re.sub(match,replace,oldwiki)   
        oldwiki = newwiki
        
    return newwiki

sublistTrac = [
    ('(\s)=([^=]+)=','\\1`\\2`'),
    ('====+',' '),
    ('\-\-\-\-+','----'),
    ('\*\*\*\*+', ' '),
    ('(\s)\*\*\*', '\\1= '),
    ('\*\*\*(\s)', ' =\\1'),
    ('(\s)\*\*','\\1== '),
    ('\*\*(\s)', ' ==\\1'),
    ('\*:::: ','      <bullet> '),
    ('\*::: ','    <bullet> '),
    ('\*:: ','  <bullet> '),
    ('\*: ',"<bullet> "),
    ('\*',"'''"),
    ('([\s\b])_([^:])',"\\1''\\2"),
    ('_(\s)',"''\\1"),
    ('([0-9]+)::::','       \\1.'),
    ('([0-9]+):::','     \\1.'),
    ('([0-9]+)::','   \\1.'),
    ('([0-9]+):',' \\1.'),
    ('_::::','        '),
    ('_:::','      '),
    ('_::','    '),
    ('_:','  '),
    ("{linebreak}","[[BR]]"),
    ("<bullet> "," * "),
    ('{link: ([^}]+)}','[\\1]'),
    ('{wiki: ([^}]+)}','[wiki:\\1]'),
    ('{verbatim}','{{{'),
    ('{endverbatim}','}}}'),
    ('{anchor: (\S+) ([^}]+)}','\\2'),
    ('CnergSoftware','[wiki:WikiStart Svalinn Home]'),
    ('HomePage','[http://cnerg.engr.wisc.edu CNERG Home]'),
    ('\|','||')
    ]
    
sublistWP = [
    ('(\s)=([^=]+)=','\\1<pre>\\2</pre>'),
    ('====+',' '),
    ('\-\-\-\-+','<hr>'),
    ('\*\*\*\*+', ' '),
    ('(\s)\*\*\*([^\*]+)\*\*\*(\s)', '\\1<h1>\\2</h1>\\3'),
    ('(\s)\*\*([^\*]+)\*\*(\s)', '\\1<h2>\\2</h2>\\3'),
    ('\*:::: ','      <li> '),
    ('\*::: ','    <li> '),
    ('\*:: ','  <li> '),
    ('\*: ',"<li> "),
    ('([0-9]+)::::','       <li>'),
    ('([0-9]+):::','     <li>'),
    ('([0-9]+)::','   <li>'),
    ('([0-9]+):',' <li>'),
    ('_::::','      <dl> '),
    ('_:::','     <dl> '),
    ('_::','   <dl> '),
    ('_:',' <dl> '),
    ('(\s)\*([^\*]+)\*(\s)',"\\1<b>\\2</b>\\3"),
    ('(\s)_([^\*]+)_(\s)',"\\1<i>\\2</i>\\3"),
    ("{linebreak}","<br>"),
    ('{link: (\S+) ([^}]+)}','<a href="\\1">\\2</a>'),
    ('{verbatim}','<pre>'),
    ('{endverbatim}','</pre>'),
    ('{anchor: (\S+) ([^}]+)}','<a name="\\1">\\2</a>')
    ]

conn = sqlite3.connect('cvstrac.db')
conn.text_factory = str

c = conn.cursor()

sql_getNewestWikiText = '''
select w.name, w.invtime, w.text 
from (
    select name, min(invtime) as mintime 
    from wiki 
    group by name ) as x 
inner join wiki as w on w.name=x.name and w.invtime=x.mintime'''

wiki_pages = c.execute(sql_getNewestWikiText)

for page in wiki_pages:
    print "writing file for " + page[0] + " (" + str(page[1]) +")"
    raw_page_file = open('rawpages/'+page[0],'w')
    raw_page_file.write(page[2])
    raw_page_file.close()

    new_page_file = open('pages/'+page[0],'w')
    new_page_file.write(cvstrac2trac(sublistTrac,page[2]))
    new_page_file.close()

    wp_page_file = open('wppages/'+page[0],'w')
    wp_page_file.write(cvstrac2trac(sublistWP,page[2]))
    wp_page_file.close()


