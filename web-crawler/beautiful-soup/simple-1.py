#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:45:13 2016

@author: kandy
"""

from bs4 import BeautifulSoup
import urllib

# Read the URL and get the html content
#url_obj = urllib.request.urlopen("http://www.google.com")
#url_obj = urllib.request.urlopen("https://en.wikipedia.org/wiki/J._K._Rowling")
#content = url_obj.read()
#print(content)


# use the soup parser
#soup = BeautifulSoup(open(content))

content = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""



soup = BeautifulSoup(content,"lxml")

for link in soup.find_all("a"):
    print(link.get("href"))

