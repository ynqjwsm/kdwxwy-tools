from utils.Loader import load_excel, load_txt
from utils.Writer import write_xls
from utils.GeoUtils import IsPtInPoly
import datetime

out_header = ['工单号', '投诉等级', '联系号码', '投诉类型', '纬度', '经度', '单元格名称[单元格编号][所属支局编号]']
tousu = load_excel('source/tousu.xls', 0)
grids = {}
for grid_src in load_txt('source/Grid.tsv'):
    points = []
    for pair in grid_src[1].split(';'):
        point = pair.split(',')
        points.append((float(point[1]), float(point[0])))
    grids[grid_src[0]] = points

tousu_resp = []
for src in tousu:
    for grid in grids:
        if IsPtInPoly(float(src[4]), float(src[5]), grids[grid]):
            tousu_resp.append(src + [grid])
            break
    tousu_resp.append(src + ['无匹配单元格'])

counter = {}
for lst in tousu_resp:
    if lst[6] in counter.keys():
        counter[lst[6]] += 1
    else:
        counter[lst[6]] = 1
counter_list = [[k, counter[k]] for k in counter]


excel_data = {'总表': {'header': ['单元格名称[单元格编号][所属支局编号]', '工单数量'], 'data': counter_list}, '详表': {'header': out_header, 'data': tousu_resp}}
write_xls('output/投诉落最小单元格-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls', excel_data)
