import csv
import json
import pprint
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

def save_json(dictionary, dict_path):
    with open(dict_path, 'w', encoding='utf-8') as outfile:
        json.dump(dictionary, outfile, ensure_ascii=False)
    print("saved", dict_path, "...")

def read_json(freq_path):
    with open(freq_path, 'r', encoding='utf-8') as f_json:
        freq = json.load(f_json)
    print("read",freq_path,"...")
    return freq

def find_related_words(dictionary, language_codes):
    for lang in language_codes:
        lang_dictionary = {}
        for entry in dictionary['frequency_order']:
           definitions = entry[1]['definitions']
           for definition in definitions:
                for word in sanitize_list(definition[lang]):
                    lang_dictionary[word] = ( [definition['id']] + lang_dictionary[word]
                        if word in lang_dictionary 
                        else [definition['id']] )
        pp.pprint(lang_dictionary)

def main():
    DELIMITER = chr(31)
    dictionary = read_json('json/build/final_frequency_dict.json')
    language_codes = ['en', 'pl']#['en', 'ru', 'be', 'uk', 'pl', 'cs', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl']
    find_related_words(dictionary, language_codes)


if __name__ == '__main__':
    main()