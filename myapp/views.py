from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
import random
from .models import movie, Scoreboard
import requests
from bs4 import BeautifulSoup

moviedata = list(movie.objects.all()) #moviedata 뽑아오기

def index(request):
    return render(request,'myapp/index.html')

def game(request):   
    selected = request.GET.getlist('stage')
    moviedata = list(movie.objects.all()) 
    #randomdata = random.sample(moviedata,30)
    #30개를 난이도별로 뽑기
    #처음엔 평점 2점차 이상, 그다음 1~2점차, 그다음 1점차 이내를 총 10개씩 30개 뽑는다.
    
    first_movie = random.sample(moviedata,1)[0] #맨 처음 영화는 랜덤으로 출력
    #추후에 범위를 지정할 수도 있음(6~8점대로 시작하도록)
    randomdata = [first_movie]

    current_movie = first_movie #current movie를 기준으로 다음 영화를 순차적으로 뽑아줌.
    #조건에 맞는 영화들을 필터/람다함수를 이용해
    #random sample로 뽑은 뒤, stack(randomdata 리스트)에 push
    
    if int(selected[0]) == 1:
        for i in range(2): # 1단계, 1.5점차 이상의 영화들 출력
            currating = current_movie.userRating
            templist = list(filter(lambda x: abs(currating-x.userRating) > 1.5 and currating-x.userRating!=0, moviedata))
            current_movie = random.sample(templist,1)[0]
            randomdata.append(current_movie)
            moviedata.remove(current_movie)

    elif int(selected[0]) == 2:
        for i in range(2): # 2단계, 0.7~1.5점차의 영화들 출력
            currating = current_movie.userRating
            templist = list(filter(lambda x: 0.7<= abs(currating-x.userRating) < 1.5 and currating-x.userRating!=0, moviedata))
            current_movie = random.sample(templist,1)[0]
            randomdata.append(current_movie)
            moviedata.remove(current_movie)
            print(len(moviedata))

    else:
        for i in range(2): # 3단계, 1점차 미만의 영화들 출력
            currating = current_movie.userRating
            templist = list(filter(lambda x: abs(currating-x.userRating) <= 0.6 and currating-x.userRating!=0, moviedata))
            current_movie = random.sample(templist,1)[0]
            randomdata.append(current_movie)
            moviedata.remove(current_movie)

    context = {   
        'randomdata': randomdata,
        'stage': int(selected[0]),
    }
    return render(request, 'myapp/game.html', context)

@require_POST
def gameover(request,score,stage):
    print(stage)

    moviedata = list(movie.objects.all()) 
    #평점과 popularity 기준으로 영화 추천
    #추후 수정
    if score <= 10:
        moviedata = list(filter(lambda x: x.popularity > 110 and x.userRating > 8.5, moviedata))
    # 1단계를 통과하지 못한 사람에게는 대중적이면서도 평점이 높은 영화 추천(필요하다면 장르까지 넣을 수도 있음)
    elif score <= 20:
        moviedata = list(filter(lambda x: 30 < x.popularity < 110 and x.userRating > 9.0, moviedata))
    # 2단계까지 간 사람에게는 적당히 유명하면서도 평점이 높은 영화를 추천.
    else:
        moviedata = list(filter(lambda x: 5 < x.popularity < 30  and x.userRating > 9.0, moviedata))
    # 2단계까지 통과했다면 영화에 관심이 많은 사람이니 적당히 마이너하면서 평가가 좋은 영화를 추천.
    # 위의 수치는 예시를 들어 만든 것이며 여러번 돌려보고 뽑혀나오는 표본이 너무 적을 경우 추후 수정 가능.

    movielist= []
    
    for i in range(3):
        selectedmovie = random.sample(moviedata,1)[0]
        url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={selectedmovie.link}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false'
        html = requests.get(url)
        soup = BeautifulSoup(html.content,'html.parser')
        reviews = soup.select("div.score_reple > p > span")
        mylist = [] 
        for i in reviews:
            if i.text.strip()!='관람객':
                mylist.append(i.text.strip())
        movielist.append({
            'movie' : selectedmovie,
            'review' : mylist[0]
        })

    context = {
        'movielist' : movielist,
        'score': score-1,
        'stage': stage,
    }
    return render(request,'myapp/gameover.html',context)
    #대중적이면서 평점 높은 영화 하나 뽑아서 리뷰와 함께 출력

@require_POST
def gameclear(request,stage):   
    moviedatas = list(filter(lambda x: x.popularity < 15  and x.userRating > 8.0, moviedata)) 
    movielist= []
    
    for i in range(3):
        movie = random.sample(moviedatas,1)[0]
        url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie.link}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false'
        html = requests.get(url)
        soup = BeautifulSoup(html.content,'html.parser')
        reviews = soup.select("div.score_reple > p > span")
        mylist = [] 
        for i in reviews:
            if i.text.strip()!='관람객':
                mylist.append(i.text.strip())
        movielist.append({
            'movie' : movie,
            'review' : mylist[0]
        })
        
    context = {
        'movielist' : movielist,
        'stage': stage,
    }
    return render(request, 'myapp/gameclear.html', context)
    #좋은 영화 데이터 하나 뽑아서 render

def scoreboard(request):
    #높은 점수 순으로 정렬
    scoreboard = sorted(list(Scoreboard.objects.all()), key=lambda person:(person.score),reverse=True)
    
    context = {
        'scoreboard': scoreboard
    }

    return render(request,'myapp/scoreboard.html',context)
    #스코어보드에 데이터 전송