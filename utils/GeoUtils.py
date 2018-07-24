from geopy.distance import vincenty


def distance(s_lat, s_lng, d_lat, d_lng):
    src = (s_lat, s_lng)
    dst = (d_lat, d_lng)
    return vincenty(src, dst).meters


def IsPtInPoly(aLon, aLat, pointList):
    '''
    :param aLon: double 经度
    :param aLat: double 纬度
    :param pointList: list [(lon, lat)...] 多边形点的顺序需根据顺时针或逆时针，不能乱
    '''

    iSum = 0
    iCount = len(pointList)

    if iCount < 3:
        return False

    for i in range(iCount):

        pLon1 = pointList[i][0]
        pLat1 = pointList[i][1]

        if i == iCount - 1:

            pLon2 = pointList[0][0]
            pLat2 = pointList[0][1]
        else:
            pLon2 = pointList[i + 1][0]
            pLat2 = pointList[i + 1][1]

        if ((aLat >= pLat1) and (aLat < pLat2)) or ((aLat >= pLat2) and (aLat < pLat1)):

            if abs(pLat1 - pLat2) > 0:

                pLon = pLon1 - ((pLon1 - pLon2) * (pLat1 - aLat)) / (pLat1 - pLat2)

                if pLon < aLon:
                    iSum += 1

    if iSum % 2 != 0:
        return True
    else:
        return False
