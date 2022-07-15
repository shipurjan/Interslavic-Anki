import json
import pprint
import random
import string
import time
pp = pprint.PrettyPrinter()

def logPercent(ratio):
    r = str(ratio)[8:11]
    if(r == "".join([random.choice(string.digits) for _ in range(3)])):
        stratio = str(int(ratio*100))
        print(stratio+"%...")

def readFreq(freq_path):
    with open(freq_path, 'r', encoding='utf-8') as f_json:
        freq = json.load(f_json)
    return freq

def readDict(dict_path):
    def appendConjugations(dict, word, search_source):
        id = dict['id']
        for line in search_source:
            line_id = line[0]
            if(line_id == id):
                conjugations = line[1]
                filtered_conjugations = list(filter(lambda x: x != word, conjugations))
                dict.update({
                    'conjugations': filtered_conjugations
                })

    def generateDict(word_list, group_index, headers, search_source):
        dict = {}
        print("generating a dict from json file...")
        for i,line in enumerate(word_list):
            word_isv = line[group_index]
            logPercent(i/len(word_list))
            subdict = {}
            for (i, key) in enumerate(headers):
                if i != group_index:
                    subdict.update({key: line[i]})
            appendConjugations(subdict, word_isv, search_source)
            dict[word_isv] = ( [subdict] + dict[word_isv] 
                if word_isv in dict 
                else [subdict] )
        return dict



    with open(dict_path, 'r', encoding='utf-8') as d_json:
        dict = json.load(d_json)

    if (list(dict.keys()) != ['wordList', 'searchIndex']):
        return

    print(dict_path,"loaded.")
    word_list = dict['wordList']
    search_index = dict['searchIndex']

    word_group_index = 'isv'
    search_source = search_index["isv-src"]

    word_list_header = word_list.pop(0)
    isv_index = word_list_header.index(word_group_index)

    refactored_dict = generateDict(word_list, isv_index, word_list_header, search_source)
    return refactored_dict
    
def addFreqValuesToDict(dict, *freqs):
    for freq in freqs:
        print(freq[0])

def main():
    ISV_DICTIONARY_PATH = 'json/fake_dict.json'
    FREQ_RUSSIAN_PATH = 'json/freq_list_russian.json'
    FREQ_POLISH_PATH = 'json/freq_list_polish.json'

    isv_dict = readDict(ISV_DICTIONARY_PATH)
    freq_ru = readFreq(FREQ_RUSSIAN_PATH)
    freq_pl = readFreq(FREQ_POLISH_PATH)

    addFreqValuesToDict(isv_dict, freq_pl, freq_pl)

if __name__ == '__main__':
    main()