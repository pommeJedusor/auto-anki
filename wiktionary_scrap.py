import requests
from bs4 import BeautifulSoup

URL = "https://en.wiktionary.org/wiki/"

def get_word_page(word):
    r = requests.get(URL+word)
    return r

def get_definition(res):
    pass

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