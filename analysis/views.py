from django.shortcuts import render, redirect, HttpResponse
from hanspell import spell_checker
import simplejson as json
from konlpy.tag import Komoran
from collections import Counter
import pytagcloud
import random
from . import senti_dict
import requests
# Create your views here.
from decouple import config
from django.contrib.auth.models import User, AnonymousUser
def index(request):


    return redirect('analysis:analysis')


def analysis(request):
    if request.user.username != "":
        try:
            if request.user.profile:
                pass
        except User.profile.RelatedObjectDoesNotExist:
            return redirect('accounts:profile_update')
    youtube = list()
    """ 
    key = config('KEY')
    url = "https://www.googleapis.com/youtube/v3/search"
    q = random.choice(["자기소개서","면접","자소서","면접왕이형"])
    my_type = "type=video"
    part = "part=snippet"
    maxResults = "maxResults=10"
    requestUrl = f"{url}?key={key}&{part}&{my_type}&q={q}&{maxResults}"
    print(requestUrl)
    response = requests.get(requestUrl)
    data = response.json()
    
    for i in data['items']:
        youtube.append((i['snippet']['thumbnails']['medium']['url'],i['snippet']['title'],i['snippet']['publishedAt'][0:10],i['id']['videoId']))
    """
    context = {
        'youtube':youtube,
    }
    return render(request, 'analysis/analysis.html', context)
    
def spell_check(request):
    # 가져온 텍스트 정제 1.줄바꿈 맞춰주기
    data = request.POST.get('data')
    data = data.replace("\n", "　")
    # 돌리기 최대 500자까지 지원함
    check_result = spell_checker.check(data).as_dict()
    checked = check_result.get('checked')
    words = check_result.get('words')

    # 결과 정제 1. 틀린단어 색표시, 출력화면 줄바꿈 맞춰주기
    temp = ""
    for data in words:
        if words.get(data) != 0:
            replaced = temp+"<b style='color:red;'>"+data+" </b>"
            checked = checked.replace(temp+data, replaced)
        temp = data+" "
    checked = checked.replace("　", "</p><p>")

    # 사용할 수 있는 메소드 목록
    """
    result = result.as_dict()
    words = result.get('words')
    original = result.get('original')
    checked = result.get('checked')
    """
    context = {
        'checked': checked
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


def words_check(request):

    # 필요한 라이브러리 및 변수 초기화
    data = request.POST.get('data')
    komoran = Komoran()
    words = Counter(komoran.nouns(data))
    # 1글자 단어 걸러내기
    nouns = dict()
    for data in words.keys():
        if len(data) != 1:
            nouns[data] = words.get(data)
    nouns = sorted(nouns.items(), key=lambda x: x[1], reverse=True)
    hashing = random.choice(range(100))
    context = {
        'nouns': nouns,
        'hashing': hashing,
    }
    # 워드클라우드
    taglist = pytagcloud.make_tags(nouns, minsize=10, maxsize=60)
    link = 'static/wordcloud/wordcloud'+str(hashing)+'.jpg'
    #link = 'static/wordcloud/wordcloud.jpg'
    pytagcloud.create_tag_image(taglist, link, size=(
        600, 600), layout=3, fontname='CookieRun', rectangular=True)

    return HttpResponse(json.dumps(context), content_type='application/json')


def senti_check(request):
    data = request.POST.get('data')
    komoran = Komoran()
    words = Counter(komoran.pos(data))
    pos = list()
    pos_p = 0
    pos_c = 0
    neg_p = 0
    neg_c = 0
    total = 0
    weight = 0
    i = 0
    for data in words.keys():
        # pos.append((data[0]+"/"+data[1],words.get(data)))
        if data[1] in ['VV', 'NNG', 'VA', 'VX', 'MAG', 'JKB']:
            pass
        else:
            continue
        wordname = data[0]+"/"+data[1]
        a, b, c = senti_dict.Singleton().data_list(wordname)
        pos.append((wordname, a, b,  c, words.get(data)))
        if(c == 'High'):
            weight = 3
        elif(c == 'Medium'):
            weight = 2
        elif(c == 'Medium'):
            weigh = 1
        if(a == 'POS'):
            pos_p = pos_p + b * words.get(data) * weight
            pos_c = pos_c + words.get(data) * weight
            total = total + b * words.get(data) * weight
        elif(a == 'NEG'):
            neg_p = neg_p + b * words.get(data) * weight
            neg_c = neg_c + words.get(data) * weight
            total = total - (b * words.get(data)) * weight
    if pos_c+neg_c != 0:
        total = total/(pos_c+neg_c)
    total = round(total*100,1)
    pos.sort(key=lambda element: element[4], reverse=True)
    context = {
        'pos': pos,
        'pos_p': round(pos_p,3),
        'neg_p': round(neg_p,3),
        'total': total,
    }
    return HttpResponse(json.dumps(context), content_type='application/json')
