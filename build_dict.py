import json
import pprint
import random
import string
pp = pprint.PrettyPrinter()

def remove_parentheses(test_str):
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
    c = remove_parentheses(s)
    c = c.replace("!","")
    c = c.strip()
    c = c.lower()
    l2.append(c)
  return l2

def compare_lists(l1, l2):
    a_set = set(sanitize_list(l1))
    b_set = set(sanitize_list(l2))
    if len(a_set.intersection(b_set)) > 0:
        return True
    return False

def log_percent(ratio):
    r = str(ratio)[8:11]
    p = "".join([random.choice(string.digits) for _ in range(3)])
    if(r == p):
        stratio = str(int(ratio*100))
        print(stratio+"%...")

def save_json(dictionary, dict_path):
    with open(dict_path, 'w', encoding='utf-8') as outfile:
        json.dump(dictionary, outfile, ensure_ascii=False)
    print("saved", dict_path, "...")

def read_json(freq_path):
    with open(freq_path, 'r', encoding='utf-8') as f_json:
        freq = json.load(f_json)
    print("read",freq_path,"...")
    return freq

def append_conjugations(dict, search_source):
    id = dict['id']
    for line in search_source:
        line_id = line[0]
        if(line_id == id):
            conjugations = line[1]
            dict.update({
                'conjugations': conjugations
            })

def generate_dict(word_list, search_source):
    def idx(s):
        return headers.index(s)
    headers = word_list.pop(0)
    language_indexes = ['en', 'ru', 'be', 'uk', 'pl', 'cs', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl']

    print("generating a dict from json file...")
    dict = {}
    for i,line in enumerate(word_list):
        word_isv = line[idx('isv')]
        log_percent(i/len(word_list))
        subdict = {}
        for (i, key) in enumerate(headers):
            if key in language_indexes:
                line[i] = line[i].split(", ")
            if key != 'isv':
                subdict.update({key: line[i]})
        append_conjugations(subdict, search_source)
        dict[word_isv] = ( [subdict] + dict[word_isv] 
            if word_isv in dict 
            else [subdict] )
    return dict

def make_dict(dict_path):
    dict = read_json(dict_path)
    if (list(dict.keys()) != ['wordList', 'searchIndex']):
        print(dict_path,"is in wrong format.")
        return

    word_list = dict['wordList']
    search_index = dict['searchIndex']
    search_source = search_index["isv-src"]

    refactored_dict = generate_dict(word_list, search_source)
    return refactored_dict
    
def add_freq_values_to_dict(dict, *freqs):
    for freq in freqs:
        language_tag = freq[0]
        freq_key = language_tag+"_freq"
        print("searching for common elements between",freq_key,"and the dictionary...")
        freq_dict = freq[1][0]
        for i,dict_definitions in enumerate(dict.values()):
            log_percent(i/len(dict))
            for dict_definition in dict_definitions:
                for freq_position, entries in freq_dict.items():
                    if(compare_lists(entries, dict_definition[language_tag])):
                        dict_definition[freq_key] = freq_position

def add_avg_freq_to_dict(dict):
    language_indexes = ['en', 'ru', 'be', 'uk', 'pl', 'cs', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl']
    for word,dict_definitions in dict.items():
        for dict_definition in dict_definitions:
            lang_count = 0
            cumulative_freq = 0
            for lang in language_indexes:
                if(lang+"_freq" in dict_definition):
                    lang_count += 1
                    cumulative_freq += int(dict_definition[lang+"_freq"])
            dict_definition["freq_count"] = str(lang_count)
            if(lang_count > 0):
                dict_definition["freq"] = str(int(cumulative_freq/lang_count))
            else:
                dict_definition["freq"] = "0"
        cumulative_freq = 0
        for dict_definition in dict_definitions:
            cumulative_freq += int(dict_definition["freq"])
        avg_freq = str(int(cumulative_freq/len(dict_definitions)))
        dict[word] = {"avg_freq": avg_freq, "definitions": dict_definitions}

def normalize_freq(dict):
    positive_freq_count = 0
    max_freq = 0
    for word, body in dict.items():
        freq = int(body['avg_freq'])
        if(freq != 0):
            positive_freq_count += 1
            if(freq > max_freq):
                max_freq = freq
        else:
            body['freq'] = "0"

    current_freq = max_freq
    left_to_normalize = positive_freq_count
    while(left_to_normalize > 0):
        log_percent(1 - (current_freq/max_freq))
        for word, body in dict.items():
            freq = int(body['avg_freq'])
            if(freq == current_freq):
                body['freq'] = str(left_to_normalize)
                left_to_normalize -= 1
        current_freq -= 1

def sort_by_freq_and_split(dict):
    sorted_dict = [[*row] for row in sorted(
        dict.items(), key=lambda x:int(x[1]['freq'])
    )]
    freq_count = 0
    for entry in sorted_dict:
        if entry[1]['freq'] != "0":
            freq_count += 1
    
    dictionary = {
        'frequency_order': sorted_dict[-freq_count:],
        'random_order': sorted_dict[:-freq_count]
    }
    return dictionary
    

def main():
    MAKE = True

    # step 0
    isv_dict = make_dict('json/interslavic_dict.json') if MAKE else read_json('json/build/0.json')
    if isv_dict is None:
        print("Error")
        return
    if MAKE:
        save_json(isv_dict, 'json/build/0.json')
    
    freq_cs = read_json('json/scraped/cs.json')
    freq_bg = read_json('json/scraped/bg.json')
    freq_sr = read_json('json/scraped/sr.json')
    freq_ru = read_json('json/scraped/ru.json')
    freq_pl = read_json('json/scraped/pl.json')


    # step 1
    add_freq_values_to_dict(isv_dict, freq_cs, freq_bg, freq_sr, freq_pl, freq_ru)
    save_json(isv_dict, 'json/build/1.json')

    # TODO: prioritize words with that are in all freq_lists in step 2
    #step 2
    add_avg_freq_to_dict(isv_dict)
    save_json(isv_dict, 'json/build/2.json')

    # step 3
    isv_dict = read_json('json/build/2.json')
    normalize_freq(isv_dict)
    save_json(isv_dict, 'json/build/3.json')

    # step 4
    isv_dict = sort_by_freq_and_split(isv_dict)
    save_json(isv_dict, 'json/build/4.json')

    #  final dictionary
    save_json(isv_dict, 'json/build/final_frequency_dict.json')



if __name__ == '__main__':
    main()