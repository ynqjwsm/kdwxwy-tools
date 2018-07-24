from utils.Loader import load_txt, cvt_float
from utils.Writer import write_csv
from utils.GeoUtils import distance

result = []
data = cvt_float(load_txt('input', drop_header=False))
for line in data:
    result.append(line + [distance(line[0], line[1], line[2], line[3])])
write_csv('output', result, ['srcLat', 'srcLng', 'dstLat', 'dstLng', 'distance(m)'])
