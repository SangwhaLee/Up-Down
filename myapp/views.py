from django.shortcuts import render, redirect

import random
from .models import movie
import requests
from bs4 import BeautifulSoup

moviedata = list(movie.objects.all()) #moviedata 뽑아오기

def index(request):
    return render(request,'myapp/index.html')

def game(request):    
    #randomdata = random.sample(moviedata,30)
    #30개를 난이도별로 뽑기
    #처음엔 평점 2점차 이상, 그다음 1~2점차, 그다음 1점차 이내를 총 10개씩 30개 뽑는다.
    
    first_movie = random.sample(moviedata,1)[0] #맨 처음 영화는 랜덤으로 출력
    #추후에 범위를 지정할 수도 있음(6~8점대)
    randomdata = [first_movie]

    current_movie = first_movie #current movie를 기준으로 다음 영화를 순차적으로 뽑아줌.
    for i in range(10): # 1단계, 2점차 이상의 영화들 출력
        currating = current_movie.userRating
        templist = list(filter(lambda x: abs(currating-x.userRating) > 2 and currating-x.userRating!=0, moviedata))
        current_movie = random.sample(templist,1)[0]
        randomdata.append(current_movie)

    for i in range(10): # 2단계, 1~2점차의 영화들 출력
        currating = current_movie.userRating
        templist = list(filter(lambda x: 1<= abs(currating-x.userRating) <= 2 and currating-x.userRating!=0, moviedata))
        current_movie = random.sample(templist,1)[0]
        randomdata.append(current_movie)

    for i in range(10): # 3단계, 1점차 미만의 영화들 출력
        currating = current_movie.userRating
        templist = list(filter(lambda x: abs(currating-x.userRating) <= 1 and currating-x.userRating!=0, moviedata))
        current_movie = random.sample(templist,1)[0]
        randomdata.append(current_movie)

    print(len(randomdata))
    
    for i in range(30):
        print((randomdata[i+1].userRating)-(randomdata[i].userRating))
        

    context = {   
        'randomdata': randomdata
    }
    return render(request, 'myapp/game.html', context)

def gameover(request,score):
    context = {
        'score' : score
    }
    return render(request,'myapp/gameover.html',context)
    #대중적이면서 평점 높은 영화 하나 뽑아서 리뷰와 함께 출력

def gameclear(request):    
    movie = random.sample(moviedata,1)[0]
    
    url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie.link}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false'
    html = requests.get(url)
    soup = BeautifulSoup(html.content,'html.parser')
    reviews = soup.select("div.score_reple > p > span")
    mylist = [] 
    for i in reviews:
        if i.text.strip()!='관람객':
            mylist.append(i.text.strip())
    
    context = {
        'movie' : movie,
        'review' : mylist[0]
    }
    return render(request, 'myapp/gameclear.html', context)
    #좋은 영화 데이터 하나 뽑아서 render

def scoreboard(request):
    return render(request,'myapp/scoreboard.html')
    #좋은 영화 데이터 하나 뽑아서 render