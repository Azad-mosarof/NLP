from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import requests
import pandas as pd
from collections import deque
from urllib.parse import urlsplit

url = 'https://en.wikipedia.org/wiki/Natural_language_processing'

def get_html_soup(url):
    response = urllib2.urlopen(url=url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

soup = get_html_soup(url)

strhtm = soup.prettify()
# print(strhtm[:1000])

#Extracting tag value
print(soup.title)
print(soup.title.string)
print(soup.a.string)
print(soup.b.string)


#Extracting all text of a particular tag
def fetch_tag_data(url, tag):
    soup = get_html_soup(url=url)
    text = ""
    for x in soup.find_all(tag):
        text += '\n'+ x.text
    return text

# x = fetch_tag_data(url, 'p')
# print(x)

#stdcss = search tag data which contain specific string
def stdcss(url, tag, string):
    soup = get_html_soup(url=url)
    final_text = ""
    no_tag = 0
    for x in soup.find_all(tag):
        text = x.text
        txt = re.search(string, text)
        if txt:
            final_text += '\n'+(txt.string)
            no_tag += 1
    return no_tag, final_text

# no_tag, text = stdcss(url, 'p', "mental")
# print(no_tag)
# print(text)

def replace_string_in_text(url, tag, old_string, new_string):
    text = fetch_tag_data(url, tag)
    x = re.sub(old_string, new_string, text)
    return x

new_text = replace_string_in_text(url, 'p', "NLP", "RNN")
# new_text = replace_string_in_text(url, 'p', "\.", "?")
# print(new_text)
# print(re.search("NLP", new_text))

# Split at each white-space character:Tokenizing
# x = re.split('\s', new_text)
# print(x)

#find email
def get_all_address():
    original_url = str(input("Enter website url: "))
    file_name = str(input("Enter file name: "))
    unscraped = deque([original_url])

    scraped = set()
    emails = set()

    while len(unscraped):
        url = unscraped.popleft()
        scraped.add(url)

        parts = urlsplit(url) 

        #Input: 
        # "https://www.google.com/example"

        # Output:
        # SplitResult(scheme='https', netloc='www.google.com', path='/example', query='', fragment='')
            
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
            path = url[:url.rfind('/')+1]
        else:
            path = url
            
        print("Crawling URL: %s" % url) 
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com",response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, 'lxml')

        for anchor in soup.find_all('a'):
            if "href" in anchor.attrs:
                link = anchor.attrs["href"]
            else:
                link = ""
            
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link.endswith(".gz"):
                if not link in unscraped and not link in scraped:
                    unscraped.append(link)
        if emails:
            df = pd.DataFrame(emails, columns=["Emails"])
            df.to_csv(file_name, index=False)

get_all_address()

#for more data cleaning process go and check it out: https://www.w3schools.com/python/python_regex.asp#search

