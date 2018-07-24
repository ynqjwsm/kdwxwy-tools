import csv, xlwt


def write_csv(dst_file, data, header):
    if len(data) == 0 or len(data[0]) != len(header):
        return
    with open(dst_file, 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)


"""
数据格式
{'sheet':{'header':[],'data':[]}}
"""


def write_xls(dst_file, data):
    workbook = xlwt.Workbook(encoding='utf8')
    for sheet_name in data:
        worksheet = workbook.add_sheet(sheet_name)
        for row in range(0, len(data[sheet_name]['header'])):
            for col in range(0, len(data[sheet_name]['header'][row])):
                worksheet.write(row, col, label=data[sheet_name]['header'][row][col])
        for row in range(0, len(data[sheet_name]['data'])):
            for col in range(0, len(data[sheet_name]['data'][row])):
                worksheet.write(row, col, label=data[sheet_name]['data'][row][col])
    workbook.save(dst_file)
