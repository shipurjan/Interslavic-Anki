import csv
import json

def save_json(dictionary, dict_path):
    with open(dict_path, 'w', encoding='utf-8') as outfile:
        json.dump(dictionary, outfile, ensure_ascii=False)
    print("saved", dict_path, "...")

def read_json(freq_path):
    with open(freq_path, 'r', encoding='utf-8') as f_json:
        freq = json.load(f_json)
    print("read",freq_path,"...")
    return freq

def main():
    DELIMITER = chr(31)
    DICTIONARY_PATH = 'json/frequency_dict.json'
    dictionary = read_json(DICTIONARY_PATH)
    language_codes = ['en', 'ru', 'be', 'uk', 'pl', 'cs', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl']
    print(dictionary)


if __name__ == '__main__':
    main()