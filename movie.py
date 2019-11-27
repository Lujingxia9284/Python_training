import requests
import json
import jsonpath
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import re

def get_all_day():
    '''
    获取日期列表
    '''
    start='2017-12-31'
    end='2018-12-31'
    
    datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
    dateend=datetime.datetime.strptime(end,'%Y-%m-%d')
    day = []
    while datestart<dateend:
        datestart+=datetime.timedelta(days=1)
        # print (datestart.strftime('%Y-%m-%d'))
        day.append(datestart.strftime('%Y-%m-%d'))
    return day


def get_data_oneday(day):
    '''
    获取选定日期的电影票房数据
    :param day:日期
    '''


    url = 'http://dianying.nuomi.com/movie/boxrefresh'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}
    postdata = {"isAjax":"true", "date": day}
    data=requests.post(url,headers=headers,data = postdata)
    data=json.loads(data.text)
    movieID =jsonpath.jsonpath(data,'$..movieId')
    movieName =jsonpath.jsonpath(data,'$..movieName')
    data_oneday = [movieID,movieName]
    for i in range(1,13):
        data_oneday.append(jsonpath.jsonpath(data,'$..attribute.%s.attrValue'%i))
    index = ['movieId','电影名称','上映天数','累计票房','实时票房','票房占比','排片占比','上座率','排座占比','场次','人次','场均人次','场均收入','平均票价']
    data_oneday = pd.DataFrame(data_oneday,columns=[day]*len(movieID),index = index).T   
    return data_oneday

def get_movie_detail(movieId):
    '''
    获取电影详细信息
    :param:movieId:电影Id
    '''
    url = 'http://dianying.nuomi.com/movie/detail?movieId=%s'%movieId
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}
    html = requests.get(url,headers = headers).content
    soup = BeautifulSoup(html,'html.parser',from_encoding = 'utf-8')
    movieName = soup.find('h4',class_ = "subtitle").text
    info = soup.find('div',id= 'infoCopy').find('div',class_ = "content").text
    director = ''.join(re.findall(r"(?<=导演：)[\u4E00-\u9FA5]+",info))
    actor = ''.join(re.findall(r"(?<=主演：)([a-zA-Z0-9\u4e00-\u9fa5\·]{1,10})",info))
    zone = ''.join(re.findall(r"(?<=地区：)[\u4E00-\u9FA5]+",info))
    movieTime = ''.join(re.findall(r"(?<=片长：)[0-9]+[\u4E00-\u9FA5]+",info))
    movieDetail = pd.DataFrame([movieId,movieName,director,actor,zone,movieTime],index = ['movieId','电影名称','导演','主演','地区','片长']).T
    
    return movieDetail

    

if __name__ == "__main__":
    # all_day = get_all_day()
    # df_all = pd.DataFrame()
    # for i in range(len(all_day)):
    #     df = get_data_oneday(all_day[i])
    #     df_all = df_all.append(df)
    # df_all.to_csv("test.csv",encoding='utf_8_sig',sep=',')
    # movieID = list(set(df_all['movieId'].tolist()))
    movieID = [10266, 10287, 10313, 10323, 10331, 47656, 94864, 94870, 94873, 94882, 94891, 94898, 94906, 94925, 94959, 94973, 94983, 95021, 95024, 95034, 95067, 95080, 95088, 95089, 41845, 95125, 95126, 39841, 95142, 95150, 95152, 95154, 95155, 95157, 95167, 95175, 95191, 95210, 95221, 95225, 95227, 95250, 95251, 95258, 95260, 95264, 95271, 95278, 95280, 95284, 95285, 95289, 37949, 95294, 95303, 95307, 95308, 95309, 95310, 76884, 95322, 95326, 95327, 95328, 93288, 95339, 95340, 95344, 95351, 95353, 95355, 95362, 95368, 95369, 95371, 95372, 95373, 95374, 95379, 95380, 95388, 95389, 95390, 95391, 95392, 95393, 95394, 95395, 15528, 95401, 95400, 15531, 95405, 95407, 95408, 95410, 95413, 95414, 95419, 95422, 95423, 95424, 95427, 95431, 95436, 95437, 95438, 95439, 95444, 95445, 95447, 95450, 95452, 95454, 95456, 95461, 95463, 95464, 95465, 95468, 95469, 95470, 95471, 95472, 95473, 95476, 95481, 95483, 95486, 95489, 95491, 95492, 95497, 95498, 95500, 95501, 95504, 95505, 95506, 95508, 95512, 95514, 95517, 95518, 95519, 95520, 95521, 95523, 95526, 95530, 95531, 95534, 95535, 95536, 95537, 95539, 95542, 95543, 95544, 95549, 95550, 95555, 95557, 95558, 95559, 95562, 95564, 95565, 95566, 95567, 95568, 38226, 95571, 95572, 95573, 95574, 95577, 95579, 95580, 95582, 95584, 95586, 95587, 95589, 95591, 95592, 95593, 95595, 95598, 95599, 95600, 95601, 64880, 95603, 95609, 95610, 95611, 95612, 95613, 95614, 95616, 95618, 95619, 95620, 95621, 95622, 95623, 95627, 95628, 95630, 95634, 95635, 95638, 95639, 95640, 95641, 95645, 95646, 95648, 95649, 95650, 95652, 95653, 95655, 95656, 95660, 95661, 95662, 95663, 95665, 95666, 9651, 95667, 95669, 95668, 95670, 95673, 95674, 95675, 95676, 95678, 95680, 95682, 95684, 95685, 95686, 95687, 95688, 95692, 95693, 95694, 95695, 95696, 95698, 95699, 95700, 95701, 95704, 95705, 62938, 95709, 95710, 95715, 95716, 95721, 95722, 95725, 95726, 95730, 95734, 95736, 95738, 95739, 95741, 95742, 95743, 95744, 95745, 95749, 95751, 95752, 95753, 95754, 95755, 95757, 95760, 95762, 95763, 95765, 95766, 95768, 95769, 95770, 95773, 95774, 95775, 63008, 95777, 95778, 95780, 95781, 63014, 95782, 95785, 95786, 95787, 63019, 95789, 95790, 95791, 95793, 95795, 95797, 95798, 95799, 95804, 95806, 95807, 95808, 95809, 95810, 95811, 95812, 95813, 95818, 95822, 63055, 95823, 95824, 95826, 95828, 95834, 95835, 63067, 95837, 95838, 95841, 95844, 95845, 95849, 95851, 95855, 95856, 95857, 95860, 95863, 95864, 95865, 95866, 95867, 95868, 95869, 95871, 95872, 95873, 95875, 95876, 95880, 95884, 95886, 95887, 95888, 95889, 95890, 95891, 95893, 95896, 95897, 95898, 95901, 95903, 95905, 95906, 95907, 95908, 95913, 95916, 95917, 95919, 95920, 95921, 95923, 95924, 95930, 95931, 95935, 95936, 95943, 95944, 95946, 95948, 95950, 95954, 95967, 95969, 95980, 95981, 95983, 95984, 95986, 95988, 95990, 95992, 9979, 95995, 95996, 95998, 96003, 96005, 96006, 9992, 96013, 96020, 96022, 96026, 96032, 10023, 12098, 10062, 10070, 10073, 10079, 30568, 10103, 10135, 10164, 10190, 10191, 10192, 10193, 10195, 10199, 10206]
    df_detail_all = pd.DataFrame()
    for i in range(len(movieID)):
        df_detail = get_movie_detail(str(movieID[i]))
        df_detail_all = df_detail_all.append(df_detail)
    df_detail_all.to_csv("movieDetail.csv",encoding='utf_8_sig',sep=',')

    
    
    
