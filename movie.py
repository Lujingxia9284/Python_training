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
    all_day = get_all_day()
    df_all = pd.DataFrame()
    for i in range(len(all_day)):
        df = get_data_oneday(all_day[i])
        df_all = df_all.append(df)
    df_all.to_csv("boxoffice.csv",encoding='utf_8_sig',sep=',')
    movieID = list(set(df_all['movieId'].tolist()))
    df_detail_all = pd.DataFrame()
    for i in range(len(movieID)):
        df_detail = get_movie_detail(str(movieID[i]))
        df_detail_all = df_detail_all.append(df_detail)
    df_detail_all.to_csv("movieDetail.csv",encoding='utf_8_sig',sep=',')

    
    
    
