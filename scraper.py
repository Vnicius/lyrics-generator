import sys
import re
import json
from dataclasses import dataclass, asdict
from typing import List
from urllib.request import urlopen

from bs4 import BeautifulSoup

base_url = 'https://www.letras.mus.br'
artist_url = f'{base_url}/%s/mais-tocadas.html'

@dataclass
class Song:
    name: str
    verses: List[str]

def get_songs(artist: str) -> List[Song]:
    html = urlopen(artist_url % (artist))
    bs = BeautifulSoup(html, 'html.parser')
    lyrics = []
    songs_list = bs.find('ul', {'class': 'cnt-list-songs'})

    if songs_list:
        for link in songs_list.find_all('a'):
            if 'href' in link.attrs:
                song_name = link.find('span').getText().strip()
                
                print(f'{len(lyrics) + 1} - {song_name}')

                verses = get_page_verses(link.attrs['href'])

                lyrics.append(Song(song_name, verses))

    return lyrics


def get_page_verses(page) -> List[str]:
    html = urlopen(f"{base_url}/{page}")
    bs = BeautifulSoup(html, 'html.parser')
    verses = []
    song_verses = bs.find('div', {'class': 'cnt-letra p402_premium'})

    if song_verses:
        for verse in song_verses.find_all('p'):
            p_removed = re.sub(r'(<p>)|(</p>)', "", str(verse))
            br_removed = re.sub(r'<[^<]*br[^>]*>', "\n", p_removed).strip()
            
            for v in br_removed.split("\n"):
                if len(v.split()) > 0:
                    verses.append(v)
    
    return verses

if __name__ == "__main__":
    lyrics = get_songs(sys.argv[1])
    
    with open(f"{sys.argv[1]}.json", "w", encoding="utf-8") as o:
        json.dump([asdict(l) for l in lyrics], o, ensure_ascii=False)