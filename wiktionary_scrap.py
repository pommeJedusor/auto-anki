import requests
from bs4 import BeautifulSoup
import re

URL = "https://en.wiktionary.org/wiki/"

def get_word_page(word):
    r = requests.get(URL+word)
    return r

def get_definitions(res):
    soup = BeautifulSoup(res.content,"html.parser")
    etymology = soup.find(id=re.compile("Etymology+"))
    definitions = []
    for sibling in etymology.parent.next_siblings:
        #ol = definition list
        if sibling.name=="ol":
            #get the direct li of the ol (not the sub li)
            for li in sibling.find_all("li",recursive=False):
                #remove the sub ul
                for ul in li.find_all("ul"):
                    ul.extract()
                #add the definition
                if li.text:
                    definitions.append(li.text.replace("\n",""))
            break
    return definitions

def get_audio_link(res):
    soup = BeautifulSoup(res.content, 'html.parser')
    elements = soup.find_all(attrs={"class": "audiofile"})
    elements = [element.span.span.audio.find_all("source") for element in elements]
    srcs = []
    for element in elements:
        for el in element:
            src = el['src']
            if "En-uk" in src or "En-us" in src:
                srcs.append(src.replace("//",""))
    return srcs