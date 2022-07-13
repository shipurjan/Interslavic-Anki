import json
from re import L

def main():
    DICTIONARY_PATH = 'json/interslavic_dict.json'
    FREQ_RUSSIAN_PATH = 'json/freq_list_russian.json'
    FREQ_POLISH_PATH = 'json/freq_list_polish.json'
    
    with open(DICTIONARY_PATH, 'r', encoding='utf-8') as d_json:
        dictionary = json.load(d_json)['wordList']

    class Word:
        def __init__(self, n):
            self.__value = dictionary[n]
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
    for _ in range(1,500):
        w = Word(_)
        print(
            w.id,
            w.pos,
            w.interslavic,
            w.english,
            w.russian,
            w.polish,
        sep='\t')
        

if __name__ == '__main__':
    main()