import json
import csv
import pprint
pp = pprint.PrettyPrinter()

def save_csv(filename, list):
    DELIMITER = chr(31)
    with open(filename, "w") as f:
        pass
    print("saving",filename,"...")
    for row in list:
        with open(filename, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=DELIMITER)
            writer.writerow(row)

def read_json(freq_path):
    with open(freq_path, 'r', encoding='utf-8') as f_json:
        freq = json.load(f_json)
    print("read",freq_path,"...")
    return freq

def HTMLify_word(word, lang):
    return ''.join((
        "<div class='",lang," word'>",
            word,
        "</div>"
    ))

def HTMLify_freq(freq):
        return ''.join((
        "<div class='freq'>",
            freq,
        "</div>"
    ))

def HTMLify_partOfSpeech(definitions, lang):
    def getUniversality(str_freq_count, max_count):
        freq_count = int(str_freq_count)
        ratio = freq_count / max_count
        margins = sorted({
            'common': 0.8,
            'universal': 1,
            'unusual': 0.5,
            'uncommon': 1/max_count,
            'rare': 0
        }.items(), key=lambda x: x[1], reverse=True)
        for margin in margins:
            if margin[1] >= ratio:
                label = margin[0]
        return ''.join((
            "<span class='",label,"'>",
                label, " (", str(int(ratio*100)), "%*)",
            "</span>"
        ))

    ol_list = []
    translation_direction = "" if lang == 'isv' else "&lang=isv-"+lang
    for definition in definitions:
        li = ''.join((
            "<li>",
                "<a href='https://interslavic-dictionary.com/?text=id" + definition['id'] + translation_direction + "'>",
                    definition['partOfSpeech'],
                "</a>",
                "<span class='freq_info'>",
                getUniversality(definition['freq_count'], 5), " fr.", definition['freq'],
                "</span>",
            "</li>"
        ))
        ol_list.append(li)

    return ''.join((
        "<div class='partOfSpeech'>",
            "<ol>",
                *ol_list,
            "</ol>",
        "</div>"
    ))


def concat_isv(definitions):
    ol_list = []
    for definition in definitions:
        li = ''.join((
            "<li>",
                "<span data-text='",'; '.join(definition['conjugations']),"' class='tooltip translation'>",
                '; '.join(definition['isv']),
                "</span>",
            "</li>"
        ))
        ol_list.append(li)
    return ''.join((
        "<div class='language isv'>",
            "<ol>",
                *ol_list,
            "</ol>",
        "</div>"
    ))

def definitions_to_ol(definitions, key):
    ol_list = []
    for definition in definitions:
        li = ''.join((
            "<li>",
                '; '.join(definition[key]),
            "</li>"
        ))
        ol_list.append(li)
    return ''.join((
        "<div class='language ",key,"'>",
            "<ol>",
                *ol_list,
            "</ol>",
        "</div>"
    ))

def HTMLify_translations(definitions, lang):
    language_codes = ['isv', 'en', 'ru', 'be', 'uk', 'pl', 'cs', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl']
    translation_list = []
    for language_code in language_codes:
        if(language_code != lang):
            if(language_code == 'isv'):
                translation_list.append(concat_isv(definitions))
            else:
                translation_list.append(definitions_to_ol(definitions, language_code))
    if(len(translation_list) == len(language_codes) - 1):
        return translation_list
    return


def convert_to_flat_list(lang, original_list):
    flat_list = []
    for entry in original_list:
        row = []
        word = entry[0]
        if(word.endswith(')')):
            continue
        description = entry[1]
        definitions = description['definitions']
        sorted_definitions = sorted(definitions, key=lambda d: d['freq_count'], reverse=True) 
        row = [
            HTMLify_word(word, lang),
            HTMLify_freq(description['freq']),
            HTMLify_partOfSpeech(sorted_definitions, lang),
            *HTMLify_translations(sorted_definitions, lang),
        ]
        flat_list.append(row)
    return flat_list

def create_html_page(flat_list):
    with open("sample.html", "w", encoding='utf-8') as html_page:
        for word in flat_list:
            for tag in word:
                html_page.write(tag)

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
        lang = dict[0]
        frequency_list = convert_to_flat_list(lang, dict[1]["frequency_order"])
        rare_list = convert_to_flat_list(lang, dict[1]["random_order"])
        save_csv('csv/common_'+dict[0]+'.csv', frequency_list)
        save_csv('csv/rare_'+dict[0]+'.csv', rare_list)

if __name__ == '__main__':
    main()