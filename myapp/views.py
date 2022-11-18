from django.shortcuts import render, redirect

import random
from .models import movie
import requests
from bs4 import BeautifulSoup

moviedata = list(movie.objects.all())


def index(request):
    return render(request,'myapp/index.html')

def game(request):    
    randomdata = random.sample(moviedata,30)
    print(randomdata)

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