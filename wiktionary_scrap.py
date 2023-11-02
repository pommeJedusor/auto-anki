import requests
from bs4 import BeautifulSoup
import re
import json

with open("datas.json","r") as f:
    DATAS = json.loads(f.read())
HEADERS = {
  'Authorization': DATAS["Access token"],
  'User-Agent': DATAS["user-agent"]
}
BASE_URL = 'https://api.wikimedia.org/core/v1/commons/file/'
URL = "https://en.wiktionary.org/wiki/"

def get_word_page(word):
    r = requests.get(URL+word)
    return r

def get_definitions(res,):
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

def get_audio_links(res):
    soup = BeautifulSoup(res.content, 'html.parser')
    elements = soup.find_all(attrs={"class": "audiofile"})
    elements = [element.span.span.audio.find_all("source") for element in elements]
    srcs = []
    for element in elements:
        for el in element:
            src = el['src']
            #get only the english sounds
            if ("En" in src or "en" in src) and not "transcoded" in src:
                srcs.append(f"File:{src.split('/')[-1]}")
    return srcs

def download_file(file):
    #get the datas
    url = BASE_URL + file
    response = requests.get(url,headers=HEADERS )
    response = json.loads(response.text)

    #parse the datas
    display_title = response['title']
    attribution_url = 'https:' + response['file_description_url']
    file_url = response['original']['url']
    print(f"display title: {display_title}")
    print(f"attribution url: {attribution_url}")
    print(f"file url: {file_url}")
    print()

    #download the file
    file = requests.get(file_url,headers=HEADERS )
    if file.ok:
        with open(f"word_sounds/{display_title}", "wb+") as f:
            f.write(file.content)
        print(f"successfully downloaded {display_title}")
    else:
        print(f"error : {file.status_code}")