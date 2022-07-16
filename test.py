import json
import pprint
pp = pprint.PrettyPrinter() 

def read_json(freq_path):
    with open(freq_path, 'r', encoding='utf-8') as f_json:
        freq = json.load(f_json)
    print("read",freq_path,"...")
    return freq

def main():
    dicts = [
        ["isv", read_json('json/build/final_frequency_dict.json')],
        ["be", read_json('json/build/final_frequency_dict_be.json')],
        ["bg", read_json('json/build/final_frequency_dict_bg.json')],
        ["cs", read_json('json/build/final_frequency_dict_cs.json')],
        ["en", read_json('json/build/final_frequency_dict_en.json')],
        ["hr", read_json('json/build/final_frequency_dict_hr.json')],
        ["mk", read_json('json/build/final_frequency_dict_mk.json')],
        ["pl", read_json('json/build/final_frequency_dict_pl.json')],
        ["ru", read_json('json/build/final_frequency_dict_ru.json')],
        ["sk", read_json('json/build/final_frequency_dict_sk.json')],
        ["sl", read_json('json/build/final_frequency_dict_sl.json')],
        ["sr", read_json('json/build/final_frequency_dict_sr.json')],
        ["uk", read_json('json/build/final_frequency_dict_uk.json')]
    ]
    for dict in dicts:
        num = 0
        for category in dict[1]:
            count = 0
            for word in dict[1][category]:
                w = word[0]
                d = word[1]
                if(w.endswith(')')):
                    count += 1
            num += len(dict[1][category]) - count
        print(dict[0],num)

if __name__ == '__main__':
    main()