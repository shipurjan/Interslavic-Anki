import json
from re import L

def main():
    DICTIONARY_PATH = "json/basic.json"
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as d_json:
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

    parts_of_speech = [
        'n.', 'v.tr. pf.', 'f.', 'pron.indef.', 'adj.', 
        'v.tr. ipf.', 'adv.', 'n.sg.', 'v.intr. ipf.', 
        'f.sg.', 'm.', 'm.anim.', 'v.tr. ipf./pf.', 'num.ord.', 
        'f.pl.', 'pron.pers.', 'm.sg.', 'v.refl. pf.', 
        'num.card.', 'v.intr. pf.', 'conj.', 'pron.int.', 
        'pron.poss.', 'prep.', 'pron.refl.', 'm./f.', 'v.aux. ipf.', 
        'v.refl. ipf.', 'num.coll.', 'pron.rec.', 'v.ipf.', 'phrase', 
        'm.pl.', 'prefix', 'pron.dem.', 'v.pf.', 'n.pl.', 'n.indecl.', 
        'particle', 'intj.', 'pron.rel.', 'v.aux. pf.', 'num.fract.', 
        'num.subst.', 'num.', 'suffix', 'v.intr. ipf./pf.', 'm.indecl.', 
        'num.mult.', 'num.diff.', 'v.tr.ipf', 
        'v.refl. ipf./pf.', 'f.indecl.', 'adj']

    for _ in range(1,20):
        
        w = Word(_)
        print(
            w.id,
            w.pos,
            w.interslavic,
            w.english,
            w.russian,
            w.polish,
        sep="\t")
        
    
    print(parts_of_speech)
if __name__ == '__main__':
    main()