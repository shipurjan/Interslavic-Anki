import json
import re
import csv

def remove_duplicates(list):

def main():
    DICTIONARY_PATH = 'json/interslavic_dict.json'
    FREQ_RUSSIAN_PATH = 'json/freq_list_russian.json'
    FREQ_POLISH_PATH = 'json/freq_list_polish.json'
    
    with open(DICTIONARY_PATH, 'r', encoding='utf-8') as d_json:
        dictionary = json.load(d_json)['wordList']
    
    with open(FREQ_RUSSIAN_PATH, 'r', encoding='utf-8') as f_json:
        freq_ru = json.load(f_json)

    with open(FREQ_POLISH_PATH, 'r', encoding='utf-8') as f_json:
        freq_pl = json.load(f_json)

    class Word:
        def __init__(self, list, n):
            self.__value = list[n]
            w = self.__value
            self.id          = w[0]
            self.addition    = w[2]
            self.pos         = w[3]
            self.interslavic = w[1]
            self.english     = w[4]  
            self.russian     = w[5]  # 150M
            self.belarusian  = w[6]  # 5.1M
            self.ukrainian   = w[7]  # 40M
            self.polish      = w[8]  # 45M
            self.czech       = w[9]  # 10.7M
            self.slovak      = w[10] # 5.2M
            self.bulgarian   = w[11] # 8M
            self.macedonian  = w[12] # 3M
            self.serbian     = w[13] # 12M
            self.croatian    = w[14] # 5.6M
            self.slovenian   = w[15] # 2.5M
        def __repr__(self):
            return(str(self.__value))

        #todo find verbs that are the same but begin with po, ot, etc.

    freq_common = freq_pl.copy()
    for freq, ru_word in freq_ru.items():
        freq_common.update({freq: freq_common[freq]+ru_word})
    
    freq_word_list = []
    for entry in freq_common.values():
        freq_word_list += entry

    final_interslavic_list = []
    for freq_word in freq_word_list[:10]:
        print(freq_word)
        for _ in range(1,len(dictionary)):
            w = Word(dictionary,_)
            word_pl = [re.sub(r"\((.*?)\)", "", x).strip() for x in w.polish.split(",")]
            word_ru = [re.sub(r"\((.*?)\)", "", x).strip() for x in w.russian.split(",")]
            if ((freq_word in word_pl or freq_word in word_ru) 
            and dictionary[_] not in final_interslavic_list):
                final_interslavic_list.append(dictionary[_])

    print(final_interslavic_list)

    with open("freq_interslavic.csv", "w") as f:
        pass

    DELIMITER = chr(31)
    for _ in range(0,len(final_interslavic_list)):
        w = Word(final_interslavic_list,_)
        data = [
            _+1,
            w.interslavic,
            w.addition,
            w.russian,
            w.belarusian,
            w.ukrainian,
            w.polish,
            w.czech,
            w.slovak,
            w.bulgarian,
            w.macedonian,
            w.serbian,
            w.croatian,
            w.slovenian,
            w.english,
            w.pos,
            w.id
        ]
        with open("freq_interslavic.csv", "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=DELIMITER)
            writer.writerow(data)
    
    print(len(final_interslavic_list))
    


if __name__ == '__main__':
    main()