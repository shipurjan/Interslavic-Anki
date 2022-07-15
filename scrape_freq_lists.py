import json
from numpy import False_
import requests
from bs4 import BeautifulSoup
import re

def save_json(dictionary, dict_path):
    with open(dict_path, 'w', encoding='utf-8') as outfile:
        json.dump(dictionary, outfile, ensure_ascii=False)
    print("saved", dict_path, "...")

def read_json(freq_path):
    with open(freq_path, 'r', encoding='utf-8') as f_json:
        freq = json.load(f_json)
    print("read",freq_path,"...")
    return freq

def getParserOutputDiv(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find('div', attrs={'class': 'mw-parser-output'})

def scrape_ru(path, lang):
    urls = [
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/1-1000',
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/1001-2000',
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/2001-3000',
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/3001-4000',
        'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/4001-5000'
    ]
    data = {}
    i = 1
    for url in urls:
        div = getParserOutputDiv(url)
        table = div.find('table', attrs={'class': 'wikitable'})
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')
        rows.pop(0)
        for row in rows:
            cols = row.find_all('td')
            words = []
            for idx,col in enumerate(cols):
                pure_word = col.text
                pure_word = pure_word.lower()
                pure_word = pure_word.strip()
                if pure_word and (idx!=0):
                    words.append(pure_word)
            data[str(i)] = words
            i += 1

    dictionary = [lang,[data]]
    save_json(dictionary, path)
    

def scrape_pl(path, lang):
    urls = [
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Polish_wordlist'
    ]
    data = {}
    i = 1
    for url in urls:
        div = getParserOutputDiv(url)
        ol = div.find('ol')
        words = ol.findAll('span', attrs={'lang': lang})
        for word in words:
            pure_word = word.find('a').text
            pure_word = pure_word.lower()
            pure_word = pure_word.strip()
            data[str(i)] = [pure_word]
            i += 1

    dictionary = [lang,[data]]
    save_json(dictionary, path)

def scrape_cs(path, lang):
    urls = [
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Czech_wordlist'
    ]
    data = {}
    i = 1
    for url in urls:
        div = getParserOutputDiv(url)
        ol = div.find('ol')
        words = ol.findAll('span', attrs={'lang': lang})
        for word in words:
            pure_word = word.find('a').text
            pure_word = pure_word.lower()
            pure_word = pure_word.strip()
            data[str(i)] = [pure_word]
            i += 1

    dictionary = [lang,[data]]
    save_json(dictionary, path)

def find_between(s, start, end):
    return (s.split(start))[1].split(end)[0]

def scrape_hr(path, lang):
    urls = [
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Serbo-Croatian_wordlist'
    ]
    data = {}
    i = 1
    for url in urls:
        div = getParserOutputDiv(url)
        ol = div.find('ol')
        words = ol.findAll('li')
        start = '|sh|'
        end = '}}'
        for word in words:
            a = word.find('a')
            
            pure_word = a.text if a else find_between(word.text, start, end)
            pure_word = pure_word.lower()
            pure_word = pure_word.strip()
            data[str(i)] = [pure_word]
            i += 1

    dictionary = [lang,[data]]
    save_json(dictionary, path)

def scrape_bg(path, lang):
    urls = [
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist',
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist/1001-2000',
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist/2001-3000',
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist/3001-4000',
        'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Bulgarian_wordlist/4001-5000'
    ]
    data = {}
    i = 1
    for url in urls:
        div = getParserOutputDiv(url)
        ol = div.find('ol')
        words = ol.findAll('span', attrs={'lang': lang})
        for word in words:
            pure_word = word.find('a').text
            pure_word = pure_word.lower()
            pure_word = pure_word.strip()
            data[str(i)] = [pure_word]
            i += 1

    dictionary = [lang,[data]]
    save_json(dictionary, path)

if __name__ == '__main__':
    scrape_ru('json/scraped/ru.json', 'ru')
    scrape_pl('json/scraped/pl.json', 'pl')
    scrape_cs('json/scraped/cs.json', 'cs')
    scrape_hr('json/scraped/hr.json', 'hr')
    scrape_bg('json/scraped/bg.json', 'bg')