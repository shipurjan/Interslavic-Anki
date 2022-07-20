import csv
import js2py
eval_res, tempfile = js2py.run_file("transliteration.js")
import json
import pprint
import random
import string
pp = pprint.PrettyPrinter()

def log_percent(ratio):
    r = str(ratio)[8:11]
    p = "".join([random.choice(string.digits) for _ in range(3)])
    if(r == p):
        stratio = str(int(ratio*100))
        print(stratio+"%...")

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

def save_json(dictionary, dict_path):
    with open(dict_path, 'w', encoding='utf-8') as outfile:
        json.dump(dictionary, outfile, ensure_ascii=False)
    print("saved", dict_path, "...")

def read_json(freq_path):
    with open(freq_path, 'r', encoding='utf-8') as f_json:
        freq = json.load(f_json)
    print("read",freq_path,"...")
    return freq

def find_related_words(dictionary, lang):
    lang_dictionary = {}
    for category in dictionary:
        for entry in dictionary[category]:
            definitions = entry[1]['definitions']
            for definition in definitions:
                for word in sanitize_list(definition[lang]):
                    lang_dictionary[word] = ( [definition['id']] + lang_dictionary[word]
                        if word in lang_dictionary 
                        else [definition['id']] )
    return lang_dictionary

def find_definition_with_id(dictionary, id):
    for category in dictionary:
        for entry in dictionary[category]:
            definitions = entry[1]['definitions']
            for definition in definitions:
                if (definition['id'] == id):
                    defi = definition.copy()
                    defi['isv'] = [entry[0]]
                    defi['isv_freq'] = entry[1]['freq']
                    defi['isv_avg_freq'] = entry[1]['avg_freq']
                    return defi

def add_avg_freq_to_dict(dictionary):
    print("adding average freq...")
    for i, (entry, definitions) in enumerate(dictionary.items()):
        log_percent(i/len(dictionary))
        cumulative_freq = 0
        for definition in definitions:
            cumulative_freq += int(definition["freq"])
        avg_freq = str(int(cumulative_freq/len(definitions)))
        dictionary[entry] = {'avg_freq': avg_freq, 'definitions': definitions}

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
    print("normalizing...")
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

def merge_identical_definitions(dictionary):
    def find_intersection(m_list):
        for i,v in enumerate(m_list) : 
            for j,k in enumerate(m_list[i+1:],i+1):  
               if v & k:
                  s[i]=v.union(m_list.pop(j))
                  if("".join([random.choice(string.digits) for _ in range(3)]) == "000"):
                    print(len(m_list))
                  return find_intersection(m_list)
        return m_list
    print("finding identical definitions...")
    list_dict = list(dictionary.items())
    identical_definitions = []
    for i in range(len(list_dict)):
        log_percent(i/len(list_dict))
        for j in range(i+1, len(list_dict)):
            word1 = list_dict[i]
            word2 = list_dict[j]
            if(word1[1] == word2[1]):
                identical_definitions.append((word1[0], word2[0]))
    s=[set(i) for i in identical_definitions if i]
    print("merging identical definitions...")
    groups = find_intersection(s)
    keys_to_pop = []
    print("updating dictionary...")
    for i, group in enumerate(groups):
        log_percent(i/len(groups))
        keys_to_pop+=([x for x in sorted(group)])
        new_key = ", ".join(sorted(group))
        val = dictionary[list(group)[0]]
        dictionary[new_key] = val
    for key in keys_to_pop:
        dictionary.pop(key)

def add_cyryllic_transliteration_to_dict(dictionary):
    def transliterate_wordlist(list):
        newlist = []
        for word in list:
            newlist.append(tempfile.transliterate(word, 5, '3', 0, 1))
        return newlist
    for word, body in dictionary.items():
        definitions = body['definitions']
        for definition in definitions:
            definition["isv_cyr"] = transliterate_wordlist(definition['isv'])

def create_language_dict(dictionary, lang):
    related_words = find_related_words(dictionary, lang)
    print("converting the interslavic dictionary to a raw",lang,"dictionary...")
    d = {}
    for i,(word, ids) in enumerate(related_words.items()):
        log_percent(i/len(related_words))
        definitions = []
        for id in ids:
            definitions.append( find_definition_with_id(dictionary, id))
        d[word] = definitions
    merge_identical_definitions(d)
    add_avg_freq_to_dict(d)
    normalize_freq(d)
    add_cyryllic_transliteration_to_dict(d)
    new_d = sort_by_freq_and_split(d)
    return new_d

def sort_by_freq_and_split(dict):
    print("sorting...")
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
    
    dictionary = read_json('json/build/final_frequency_dict.json')
    language_codes = ['pl'] # ['en', 'ru', 'be', 'uk', 'pl', 'cs', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl']

    for language_code in language_codes:
        tmp_dict = create_language_dict(dictionary, language_code)
        save_json(tmp_dict, 'json/build/final_frequency_dict_'+language_code+'.json')


if __name__ == '__main__':
    main()