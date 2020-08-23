from django.shortcuts import render
import requests 
from bs4 import BeautifulSoup


def index(request):
    #variables passed to template
    city = None
    time = None
    temp =None
    weather = None
    week = None

    #extract city from filled form
    if 'city' in request.GET:
        city = request.GET.get('city')

        
        url = "https://www.google.com/search?q=weather+"+city
        USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        
        #create browser session
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        
        #send request to URL
        req_page = session.get(url)

        #scrap weather data
        soup = BeautifulSoup(req_page.text, 'html.parser')
      
        #find data for current day
        city  = soup.find(id ="wob_loc").text
        time = soup.find(id ="wob_dts").text
        temp = soup.find(id = "wob_tm").text
        weather = soup.find(id =  "wob_dc").text
        
        #find data for whole week
        week = []
        days = soup.find_all(class_="wob_df")
        for d in days:
            day = d.find(class_="QrNVmd").text+"day"
            t1 = d.find_all(class_="wob_t")
            temper = []
            for t in t1:
                temper.append(t.text)
            week.append({'day':day,'temper':temper})


    return render(request, 'html/index.html', {'city': city,'time':time,'temp':temp,'weather':weather,'week':week})

