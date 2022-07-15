import json
import pprint
pp = pprint.PrettyPrinter()

def readDict(dict_path):
    with open(dict_path, 'r', encoding='utf-8') as d_json:
        dict = json.load(d_json)

    if (list(dict.keys()) != ['wordList', 'searchIndex']):
        return

    print(dict_path,"loaded.")
    word_list = dict['wordList']
    search_index = dict['searchIndex']

    word_list_header = word_list.pop(0)
    main_index = word_list_header.index('isv')

    main_dictionary = {}
    for line in word_list:
        isv = line[main_index]
        sub_dictionary = {}
        for i,key in enumerate(word_list_header):
            if(i!=main_index):
                sub_dictionary.update({key: line[i]})
        if isv in main_dictionary:
            main_dictionary[isv] = [sub_dictionary] + main_dictionary[isv]
        else:
            main_dictionary[isv] = [sub_dictionary]
    pp.pprint(main_dictionary)
    

def main():
    ISV_DICTIONARY_PATH = 'json/fake_dict.json'
    FREQ_RUSSIAN_PATH = 'json/freq_list_russian.json'
    FREQ_POLISH_PATH = 'json/freq_list_polish.json'

    isv_dict = readDict(ISV_DICTIONARY_PATH)
    
    with open(FREQ_RUSSIAN_PATH, 'r', encoding='utf-8') as f_json:
        freq_ru = json.load(f_json)

    with open(FREQ_POLISH_PATH, 'r', encoding='utf-8') as f_json:
        freq_pl = json.load(f_json)


if __name__ == '__main__':
    main()