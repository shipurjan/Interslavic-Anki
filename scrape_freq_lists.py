import json
from numpy import False_
import requests
from bs4 import BeautifulSoup
import re

def getSoup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')

def scrape_russian_freq_list(path):
    urls = [
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/1-1000',
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/1001-2000',
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/2001-3000',
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/3001-4000',
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/4001-5000'
    ]
    data = {}
    for url in urls:
        soup = getSoup(url)
        table = soup.find('table', class_='wikitable')
        for row in table.find_all('tr'):
            id = ''
            for cell in row.find_all('td'):
                c = cell.text
                c = ''.join(c.split())
                if(c == 'Rank'):
                    break
                if(c and not id): 
                    id = c
                    data[id] = []
                elif(c):
                    data[id].append(c)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    

def scrape_polish_freq_list(path):
    urls = [
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Polish_wordlist'
    ]
    data = {}
    for url in urls:
        soup = getSoup(url)
        div = soup.find('div', class_='mw-parser-output')
        list = div.find('ol')
        for i,word in enumerate(list):
            w = word.text
            w = ''.join(w.split())
            w = re.sub('[0123456789]', '', w)
            if(w):
                data[int(i/2+1)] = [w]
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def scrape_czech_freq_list(path):
    urls = [
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Czech_wordlist'
    ]
    data = {}
    for url in urls:
        soup = getSoup(url)
        div = soup.find('div', class_='mw-parser-output')
        list = div.find('ol')
        for i,word in enumerate(list):
            w = word.text
            w = ''.join(w.split())
            w = re.sub('[0123456789]', '', w)
            if(w):
                data[int(i/2+1)] = [w]
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def scrape_serbocroatian_freq_list(path):
    urls = [
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Serbo-Croatian_wordlist'
    ]
    data = {}
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        div = soup.find('div', class_='mw-parser-output')
        list = div.find('ol')
        for i,word in enumerate(list):
            w = word.text
            w = ''.join(w.split())
            w = re.sub('[0123456789]', '', w)
            if(w):
                data[int(i/2+1)] = [w]
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def scrape_bulgarian_freq_list(path):
    urls = [
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist',
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist/1001-2000',
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist/2001-3000',
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist/3001-4000',
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist/4001-5000'
    ]
    data = {}
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        div = soup.find('div', class_='mw-parser-output')
        list = div.find('ol')
        for i,word in enumerate(list):
            w = word.text
            w = ''.join(w.split())
            w = re.sub('[0123456789]', '', w)
            if(w):
                data[int(i/2+1)] = [w]
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

if __name__ == '__main__':
    scrape_polish_freq_list('json/freq_list_polish.json')