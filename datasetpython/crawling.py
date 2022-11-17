import requests
from bs4 import BeautifulSoup

url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code=184311&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false'
html = requests.get(url)
soup = BeautifulSoup(html.content,'html.parser')
reviews = soup.select("div.score_reple > p > span")
print(reviews)
mylist = [] 
for i in reviews:
    if i.text.strip()!='관람객':
        mylist.append(i.text.strip())

print(mylist[0])


