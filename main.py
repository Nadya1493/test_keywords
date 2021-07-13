import csv
import itertools

lst_row = []
group_words = {}
is_first_el = True

# открытие csv файла, работа с файлом
with open('keywords (1).csv', 'r', encoding='utf-8') as file:
    csv_obj = csv.reader(file)
    for row in csv_obj:
        # исключение первой строки заголовков
        if is_first_el:
            is_first_el = False
            continue
        row = ', '.join(row).split(';')

        # удаление из столбца Keyword слов, начинающихся со знака минус
        if '-' in row[3]:
            row[3] = row[3][:row[3].find(' -')]

        # удаление из столбца Keyword символов '[' и ']'
        if ('[' or ']') in row[3]:
            row[3] = row[3].replace('[', '').replace(']', '')

        stripped = row[3].strip("'")
        lst = stripped.split()

        # приведение к нижнему регистру, создание кортежа из списка слов из Keyword
        for i in range(len(lst)):
            lst[i] = lst[i].lower()
        set_words = set(lst)

        # добавление в основной список row кортежа со списком слов; добавление списка row в отдельный lst_row
        row.append(set_words)
        lst_row.append(row)

        # создание словаря, где ключ - group_id (соответствует AdGroupId), значение - данные из кортежа set_words
        group_id = row[0]
        if group_id in group_words.keys():
            group_words[group_id].extend(set_words)
            group_words[group_id] = list(set(group_words[group_id]))
        else:
            group_words[group_id] = list(set_words)

# запись в csv файл пересечений из разных групп AdGroupId
with open('keywords_ext.csv', 'w', newline='') as f:
    wtr = csv.writer(f, delimiter=";")
    wtr.writerow(['Keyword_x', 'AdGroupId_x', 'Keyword_y', 'AdGroupId_y', 'crossed'])
    for pair in itertools.combinations(group_words.keys(), r=2):
        cross = set(group_words[pair[0]]) & set(group_words[pair[1]])
        if len(cross) > 1:
            wtr.writerow([', '.join(group_words[pair[0]]), pair[0], ', '.join(group_words[pair[1]]), pair[1], ', '.join(cross)])
