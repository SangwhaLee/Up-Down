import json
import requests
from bs4 import BeautifulSoup
import os

print(os.listdir(os.getcwd()))

file_path = 'c:/Users/학습용/Desktop/final-pjt/datasetpython/prototype.json'
with open(file_path,'r', encoding='UTF-8') as file:
    datas = json.load(file)


print(len(datas))
dataset = []
noreview = []

for i in range(len(datas)):
    naverkey = datas[i]['link'] # 리뷰 없는 독립영화 데이터 걸러내기 위함
    # 미리 beautifulsoup를 사용해 데이터를 뽑아보고 점검
    # 
    url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={naverkey}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false'
    html = requests.get(url)
    soup = BeautifulSoup(html.content,'html.parser')
    reviews = soup.select("div.score_reple > p > span")
    mylist = [] 
    for j in reviews:
        if j.text.strip()!='관람객':
            mylist.append(j.text.strip())
    if mylist == []:
        noreview.append(datas[i]['title']) #불량 데이터 직접 수정하기 위함
    
    dataset.append({
        'model' : 'myapp.movie',
        'pk' : i+1,
        'fields': datas[i]
    }) #해당 부분은 프로젝트 이름에 맞춰 수정(특히 model 부분)
    print(i)
print(dataset[1])
print(noreview)
file_path = './datasets.json'
with open(file_path,'w', encoding='UTF-8') as outfile:
    json.dump(dataset, outfile, indent = 4,ensure_ascii=False)