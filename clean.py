import csv
import re


def make_numbers(number):
    first, last_suffix = number.split('/')
    first_suffix = first[-1]
    base = first[0:-1]
    return ['tel:+356{}{}'.format(base, x) for x in range(int(first_suffix), int(last_suffix) + 1)]

with open('HOTELLISTMALTA-csv.csv', 'rb') as csv_file:
    data_reader = csv.DictReader(csv_file, delimiter=',')

    # print data_reader.fieldnames
    max_nums = 0
    list_of_lists = []
    for row in data_reader:
        raw_row_list = re.split(' [\-/] ', row['Telephone'])
        raw_row_list = map(lambda s: s.strip(), raw_row_list)
        list_of_numbers = []
        for number in raw_row_list:
            if re.match('^tel:\+356[0-9]{8}$', number):
                list_of_numbers.append(number)
            else:
                number = number.replace(' ', '')
                if '/' not in number:
                    list_of_numbers.append('tel:+356' + number)
                    continue
                list_of_numbers.extend(make_numbers(number))
        list_of_lists.append(list_of_numbers)
        if len(list_of_numbers) > max_nums:
            max_nums = len(list_of_numbers)
    print max_nums

    new_fields = data_reader.fieldnames
    new_fields.remove('Telephone')
    tel_fields = ['Telephone {}'.format(x) for x in range(1, max_nums + 1)]
    new_fields.extend(tel_fields)

    with open('file.csv', 'w') as csv_file2:
        data_writer = csv.DictWriter(csv_file2, new_fields)
        data_writer.writeheader()
        csv_file.seek(0)
        for i, row in enumerate(csv.DictReader(csv_file)):
            print i
            for j, field in enumerate(tel_fields):
                try:
                    row[field] = list_of_lists[i][j]
                except IndexError:
                    pass
            del row['Telephone']
            data_writer.writerow(row)
