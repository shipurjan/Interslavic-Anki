import json
import pprint
import random
import string
pp = pprint.PrettyPrinter()

def a(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret

def sanitize_list(l):
  l2 = []
  for s in l:
    c = a(s)
    c = c.replace("!","")
    c = c.strip()
    l2.append(c)
  return l2

def compare_lists(l1, l2):
    a_set = set(l1)
    b_set = set(l2)
    if len(a_set.intersection(b_set)) > 0:
        return True
    return False

def logPercent(ratio):
    r = str(ratio)[8:11]
    if(r == "".join([random.choice(string.digits) for _ in range(3)])):
        stratio = str(int(ratio*100))
        print(stratio+"%...")

def saveJSON(dictionary, dict_path):
    with open(dict_path, 'w', encoding='utf-8') as outfile:
        json.dump(dictionary, outfile, ensure_ascii=False)

def readJSON(freq_path):
    with open(freq_path, 'r', encoding='utf-8') as f_json:
        freq = json.load(f_json)
    print("read",freq_path,"...")
    return freq

def appendConjugations(dict, search_source):
    id = dict['id']
    for line in search_source:
        line_id = line[0]
        if(line_id == id):
            conjugations = line[1]
            dict.update({
                'conjugations': conjugations
            })

def generateDict(word_list, search_source):
    def idx(s):
        return headers.index(s)
    headers = word_list.pop(0)
    language_indexes = ['en', 'ru', 'be', 'uk', 'pl', 'cs', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl']

    print("generating a dict from json file...")
    dict = {}
    for i,line in enumerate(word_list):
        word_isv = line[idx('isv')]
        logPercent(i/len(word_list))
        subdict = {}
        for (i, key) in enumerate(headers):
            if key in language_indexes:
                line[i] = line[i].split(", ")
            if key != 'isv':
                subdict.update({key: line[i]})
        appendConjugations(subdict, search_source)
        dict[word_isv] = ( [subdict] + dict[word_isv] 
            if word_isv in dict 
            else [subdict] )
    return dict

def makeDict(dict_path):
    dict = readJSON(dict_path)
    if (list(dict.keys()) != ['wordList', 'searchIndex']):
        print(dict_path,"is in wrong format.")
        return

    word_list = dict['wordList']
    search_index = dict['searchIndex']
    search_source = search_index["isv-src"]

    refactored_dict = generateDict(word_list, search_source)
    return refactored_dict
    
def addFreqValuesToDict(dict, *freqs):
    for freq in freqs:
        language_tag = freq[0]
        freq_key = language_tag+"_freq"
        print("searching for common elements between",freq_key,"and the dictionary...")
        freq_dict = freq[1][0]
        for i,dict_definitions in enumerate(dict.values()):
            logPercent(i/len(dict))
            for dict_definition in dict_definitions:
                for freq_position, entries in freq_dict.items():
                    print(entries, dict_definition[language_tag])
                    if(compare_lists(entries, dict_definition[language_tag])):
                        dict_definition[freq_key] = freq_position

def main():
    ISV_DICTIONARY_PATH = 'json/interslavic_dict.json'
    FREQ_RUSSIAN_PATH = 'json/freq_list_russian.json'
    FREQ_POLISH_PATH = 'json/freq_list_polish.json'

    OUTPUT_PATH = 'json/frequency_dict.json'
    BUILT_DICTIONARY_PATH = 'json/built_dict.json'
    MAKE = False

    isv_dict = makeDict(ISV_DICTIONARY_PATH) if MAKE else readJSON(BUILT_DICTIONARY_PATH)
    if isv_dict is None:
        print("Error")
        return
    if MAKE:
        saveJSON(isv_dict, BUILT_DICTIONARY_PATH)

    freq_ru = readJSON(FREQ_RUSSIAN_PATH)
    freq_pl = readJSON(FREQ_POLISH_PATH)

    addFreqValuesToDict(isv_dict, freq_ru, freq_pl)
    saveJSON(isv_dict, OUTPUT_PATH)

if __name__ == '__main__':
    main()