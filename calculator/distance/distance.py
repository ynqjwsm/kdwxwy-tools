from utils.Loader import load_txt, cvt_float
from utils.Writer import write_csv
from utils.GeoUtils import distance

result = []
data = load_txt('input', drop_header=False)
print(data)
for line in data:
    result.append(line + [distance(float(line[1]), float(line[2]), float(line[3]), float(line[4]))])
write_csv('output', result, ['id', 'srcLat', 'srcLng', 'dstLat', 'dstLng', 'distance(meter)'])
