import json
import re
import csv

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

def remove_duplicates(freq_list):
    duplicates = {}
    for i,a in enumerate(freq_list):
        for j,b in enumerate(freq_list):
            if(i!=j and a[2] == b[2]):
                if a[0] not in duplicates:
                    duplicates[a[2]] = [ a[0] ]
                if(b[0]) not in duplicates[a[2]]:
                    duplicates.update({
                        a[2]: duplicates[a[2]] + [ b[0] ]
                    }) 
    idx_to_pop = []
    for dups in duplicates.values():
        min_freq = min(dups)
        dups.remove(min_freq)
        for idx in dups:
            l1 = freq_list[min_freq]
            l2 = freq_list[idx]
            for i in range(5,len(l1)):
                v1 = [x.strip() for x in l1[i].split(",")]
                v2 = [x.strip() for x in l2[i].split(",")]
                l1[i] = ", ".join(list(set(v1+v2)))
            idx_to_pop.append(idx)
    idx_to_pop.sort(reverse=1)
    for idx in idx_to_pop:
        freq_list.pop(idx)
    for el in freq_list:
        el.pop(0)

def getAlternatingFreqList(list1, list2):
    bigger_list = list1 if len(list1) > len(list2) else list2
    smaller_list = list2 if bigger_list==list1 else list1

    freq_common = bigger_list.copy()
    for freq, word in smaller_list.items():
        freq_common.update({freq: freq_common[freq] + word})
    
    freq_word_list = []
    for entry in freq_common.values():
        freq_word_list += entry

    return list(dict.fromkeys(freq_word_list))

def getFinalFreqList(freq_word_list, dictionary):
    final_freq_list = []
    for freq_word in freq_word_list[:10]:
        print(freq_word)
        for _ in range(1,len(dictionary)):
            w = Word(dictionary,_)
            word_pl = [re.sub(r"\((.*?)\)", "", x).strip() for x in w.polish.split(",")]
            word_ru = [re.sub(r"\((.*?)\)", "", x).strip() for x in w.russian.split(",")]
            if ((freq_word in word_pl or freq_word in word_ru) 
            and dictionary[_] not in final_freq_list):
                final_freq_list.append(dictionary[_])
    for i,e in enumerate(final_freq_list):
        final_freq_list[i] = [i] + e
    return final_freq_list

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

    freq_word_list = getAlternatingFreqList(freq_pl, freq_ru)
    final_interslavic_list = getFinalFreqList(freq_word_list, dictionary)

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