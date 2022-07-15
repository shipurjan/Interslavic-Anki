import csv
from enum import unique

def main():
    DELIMITER = chr(31)
    with open('freq_interslavic.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=DELIMITER)
        data = list(csv_reader)


if __name__ == '__main__':
    main()