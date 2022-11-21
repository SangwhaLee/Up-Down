import json
import requests 
from time import sleep

file_path = './datasetpython/myexcel.json'
with open(file_path,'r', encoding='UTF-8') as file:
    datas = json.load(file)

headerDict = {
    'X-Naver-Client-Id': 'A8fMBXU5thGRFAwf5QmM',
    'X-Naver-Client-Secret': 'quSkdkzvXh'
    } #네이버 검색 API에 쿼리를 보낼 때 필요한 Header

API_KEY = '469f9baab6501e0158c6f6d5bef8d9d2' #TMDB에 요청을 보내기 위한 API KEY
myjsonlist=[]
myunluckyjsonlist=[]

for i in range(len(datas)):      
    sleep(0.1) #네이버 API에서 짧은 시간 내에 요청하면 데이터를 반환 안해줌, 이를 해결하기 위함
    title = datas[i]['title']
    year = datas[i]['year']
    print(datas[i])
    #print(f'https://openapi.naver.com/v1/search/movie.json?query={title}')
    res = requests.get(f'https://openapi.naver.com/v1/search/movie.json?query={title}&display=100',headers=headerDict)
    myjson = res.json()['items'] #원하는 json 응답이 여기 들어있음.
    for j in range(len(myjson)):
        try:
            if myjson[j]['title'].replace(" ","")=='<b>'+str(title).replace(" ","")+'</b>' and (-1<=int(myjson[j]['pubDate'])-year<=1): #정확히 일치하는 것만 반환
                if myjson[j]['userRating']!="0.00":
                    # 필요한 것: link(네이버 댓글 크롤링 위함), userRating
                    datas[i]['userRating'] = int(myjson[j]['userRating'])
                    datas[i]['link'] = myjson[j]['link'].lstrip('https://movie.naver.com/movie/bi/mi/basic.nhn?code=')
        except:
            pass
    mytmdb = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=ko-KR&include_adult=true&query={title}').json()['results']
    #print(mytmdb)
    for j in range(len(mytmdb)):
        try:
            if str(mytmdb[j]['title']).replace(" ","")==str(title).replace(" ","") and int(mytmdb[j]['release_date'][0:4])==year:
                datas[i]['poster_path'] = 'https://image.tmdb.org/t/p/original/'+mytmdb[j]['poster_path']
                datas[i]['popularity']  = mytmdb[j]['popularity']
                break
        except:
            pass
    
    if len(datas[i])==6:
        myjsonlist.append(datas[i])
    else:
        myunluckyjsonlist.append(datas[i])

    file_path = './prototype.json'
    with open(file_path,'w', encoding='utf-8') as outfile:
        json.dump(myjsonlist, outfile, indent = 4,ensure_ascii=False)
    
    file_path = './unluckyjson.json'
    with open(file_path,'w', encoding='utf-8') as outfile:
        json.dump(myunluckyjsonlist, outfile, indent = 4,ensure_ascii=False)
            


