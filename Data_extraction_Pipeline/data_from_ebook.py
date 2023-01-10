import re
import requests
import ebooklib
import urllib
from ebooklib import epub
from bs4 import BeautifulSoup

url = 'https://www.gutenberg.org/files/2638/2638-0.txt'

def epubthtml(url):
    with urllib.request.urlopen(url) as url:
        book = url.read()
        soup = BeautifulSoup(book, 'html.parser')
        stml = soup.prettify()
        with open("sell.txt", '+a') as fileHandlar:
            fileHandlar.write("%s\n" % stml)
# epubthtml(url)


def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

blacklist = [   '[document]',   'noscript', 'header',   'html', 'meta', 'head','input', 'script', 'style'  ]
# there may be more elements you don't want, such as "style", etc.

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

out = epub2text('/home/azadm/Desktop/101 Internet Businesses You Can Start from Home.epub')

print(out)