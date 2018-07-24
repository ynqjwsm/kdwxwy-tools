import math


class GpsConvert(object):
    x_pi = 3.14159265358979323846 * 3000.0 / 180.0
    a = 6378245.0
    ee = 0.00669342162296594323

    def __init__(self):
        pass

    def bd_to_wgs(self, bd_lat, bd_lng):
        gcj_data = self.bd_to_gcj(bd_lat, bd_lng)
        return self.gcj_to_wgs_exactly(gcj_data[0], gcj_data[1])

    def gcj_to_wgs(self, gcj_lat, gcj_lng):
        if self.out_of_china(gcj_lat, gcj_lng):
            return [gcj_lat, gcj_lng]
        delta_data = self.delta(gcj_lat, gcj_lng)
        return [gcj_lat - delta_data[0], gcj_lng - delta_data[1]]

    def gcj_to_wgs_exactly(self, gcj_lat, gcj_lng):
        init_delta = 0.01
        threshold = 0.000000001
        delta_lat = init_delta
        delta_lng = init_delta
        m_lat = gcj_lat - delta_lat
        m_lng = gcj_lng - delta_lng
        p_lat = gcj_lat + delta_lat
        p_lng = gcj_lng + delta_lng
        wgs_lat = 0
        wgs_lng = 0
        i = 0
        while True:
            i += 1
            wgs_lat = (m_lat + p_lat) / 2
            wgs_lng = (m_lng + p_lng) / 2
            tmp = self.wgs_to_gcj(wgs_lat, wgs_lng)
            delta_lat = tmp[0] - gcj_lat
            delta_lng = tmp[1] - gcj_lng
            if math.fabs(delta_lat) < threshold and math.fabs(delta_lng) < threshold:
                break
            if delta_lat > 0:
                p_lat = wgs_lat
            else:
                m_lat = wgs_lat
            if delta_lng > 0:
                p_lng = wgs_lng
            else:
                m_lng = wgs_lng
            if i > 10000:
                break
        return [wgs_lat, wgs_lng]

    def wgs_to_gcj(self, wgs_lat, wgs_lng):
        if self.out_of_china(wgs_lat, wgs_lng):
            return [wgs_lat, wgs_lng]
        return self.delta(wgs_lat, wgs_lng)

    def gcj_to_bd(self, gcj_lat, gcj_lng):
        x = gcj_lng
        y = gcj_lat
        z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * self.x_pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * self.x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return [bd_lat, bd_lng]

    def bd_to_gcj(self, bd_lat, bd_lng):
        x = bd_lng - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.x_pi)
        gcj_lon = z * math.cos(theta)
        gcj_lat = z * math.sin(theta)
        return [gcj_lat, gcj_lon]

    def wgs_to_gcj(self, wgs_lat, wgs_lng):
        if self.out_of_china(wgs_lat, wgs_lng):
            return [wgs_lat, wgs_lng]
        delta_lat = self.transform_lat(wgs_lng - 105.0, wgs_lat - 35.0)
        delta_lng = self.transform_lng(wgs_lng - 105.0, wgs_lat - 35.0)
        rad_lat = wgs_lat / 180.0 * math.pi
        magic = math.sin(rad_lat)
        magic = 1 - self.ee * magic * magic
        sqrt_magic = math.sqrt(magic)
        delta_lat = (delta_lat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrt_magic) * math.pi)
        delta_lng = (delta_lng * 180.0) / (self.a / sqrt_magic * math.cos(rad_lat) * math.pi)
        return [wgs_lat + delta_lat, wgs_lng + delta_lng]

    def delta(self, lat, lng):
        delta_lat = self.transform_lat(lng - 105.0, lat - 35.0)
        delta_lng = self.transform_lng(lng - 105.0, lat - 35.0)
        rad_lat = lat / 180.0 * math.pi
        magic = math.sin(rad_lat)
        magic = 1 - self.ee * magic * magic
        sqrt_magic = math.sqrt(magic);
        delta_lat = (delta_lat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrt_magic) * math.pi)
        delta_lng = (delta_lng * 180.0) / (self.a / sqrt_magic * math.cos(rad_lat) * math.pi)
        return [delta_lat, delta_lng]

    def transform(self, wgs_lat, wgs_lng):
        if self.out_of_china(wgs_lat, wgs_lng):
            return [wgs_lat, wgs_lng]
        delta_lat = self.transform_lat(wgs_lng - 105.0, wgs_lat - 35.0)
        delta_lng = self.transform_lng(wgs_lng - 105.0, wgs_lat - 35.0)
        rad_lat = wgs_lat / 180.0 * math.pi
        magic = math.sin(rad_lat)
        magic = 1 - self.ee * magic * magic
        sqrt_magic = math.sqrt(magic)
        delta_lat = (delta_lat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrt_magic) * math.pi)
        delta_lng = (delta_lng * 180.0) / (self.a / sqrt_magic * math.cos(rad_lat) * math.pi)
        return [wgs_lat + delta_lat, wgs_lng + delta_lng]

    def transform_lng(self, x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.fabs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
        return ret

    def transform_lat(self, x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.fabs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return ret

    # 判断是否在国内，不在国内则不做偏移
    def out_of_china(self,lat, lng):
        return (lng < 72.004 or lng > 137.8347) or ((lat < 0.8293 or lat > 55.8271) or False)
