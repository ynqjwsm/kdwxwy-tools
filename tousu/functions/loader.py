import csv, xlrd


def load_excel(src_file_name, sheet_index, drop_header=True, header_lines=1):
    workbook = xlrd.open_workbook(src_file_name)
    if sheet_index >= len(workbook.sheet_names()):
        return []
    sheet = workbook.sheet_by_index(sheet_index)
    return [sheet.row_values(x) for x in range(header_lines if drop_header else 0,sheet.nrows)]


def load_csv(src_file_name, drop_header=True, header_lines=1):
    with open(src_file_name, 'r') as csv_src:
        reader = csv.reader(csv_src)
        data = list(reader)[header_lines:] if drop_header else list(reader)
    return data


def load_txt(src_file_name, splitter='\t', drop_header=True, header_lines=1, enc='UTF-8'):
    with open(src_file_name, 'r', encoding=enc) as sCell:
        data = []
        for line in sCell.readlines():
            line_data = line.split(splitter)
            data.append(line_data)
    data = data[header_lines:] if drop_header else data
    return data
