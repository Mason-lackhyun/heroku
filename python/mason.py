#import sys
import requests
import json

#보통 웹API의 결과는 JSON형식이나 XML형식 리턴을 한다.
#openweather에서는 JSON형식으로 리턴한다.
#따라서, JSON형식의 데이터를 파이썬 데이터 형식으로 변환해줘야 하는데
#이때 json모듈이 필요함.


#API키 및 webhook url설정
apikey="fa2c28b8566c6dac2d869658222919aa"
slack_webhook_url = "https://hooks.slack.com/services/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"

headers = {
    "Content-type": "application/json"
}


city_list = ["Seoul,KR", "usan,KR", "Daejeon,KR", "Cheonan,KR" , "Asan,KR"]

#API 지정
api="http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

# 켈빈 온도를 섭씨 온도로 변환하는 함수
k2C = lambda k: k - 273.15


#각 도시의 정보를 추출하기
  
for name in city_list:
    
    #API의 URL 구성하기
    url = api.format(city=name, key=apikey)

    #API요처을 보내 날씨 정보를 가져오기
    res = requests.get(url)

    #JSON형식의 데이터를 파이썬형으로 변환한다.
    data = json.loads(res.text)

    #eng -> kor
    if data["name"] == "Seoul": 
        data["name"] = "서울"
    elif data["name"] == "Asan":
        data["name"] = "아산"
    elif data["name"] == "Cheonan":
        data["name"] = "천안"
    elif data["name"] == "Daejeon":
        data["name"] = "대전"
    else:
        data["name"] = "부산"
    
    if data["weather"][0]["description"] == "mist": 
        data["weather"][0]["description"] = "안개 낀"
    elif data["weather"][0]["description"] == "overcast clouds": 
        data["weather"][0]["description"] = "구름이 많은 흐린"
    elif data["weather"][0]["description"] == "few clouds": 
        data["weather"][0]["description"] = "구름은 적은"
    elif data["weather"][0]["description"] == "clear sky": 
        data["weather"][0]["description"] = "맑은"
    elif data["weather"][0]["description"] == "broken clouds": 
        data["weather"][0]["description"] = "구름이 조금 많이 낀"
    elif data["weather"][0]["description"] == "moderate rain": 
        data["weather"][0]["description"] = "비가 옴"
    elif data["weather"][0]["description"] == "thunderstorm with light rain": 
        data["weather"][0]["description"] = "번개치고 집중 호우"
    elif data["weather"][0]["description"] == "scattered clouds": 
        data["weather"][0]["description"] = "구름이 잔뜩 낀"
    
    #결과를 출력하기
    f = open('stdout.txt' , 'a')
    
    print("도시 = ", data["name"],'\n'"날씨 = ", data["weather"][0]["description"],'\n'"최저기온 = ", str(round(k2C(data["main"]["temp_min"]),2)) +"°C" 
    ,'\n'"최고기온 = ", str(round(k2C(data["main"]["temp_max"]),2))+"°C" ,'\n'"습도 = ", str(data["main"]["humidity"]) +"%",'\n'"기압 = ", str(data["main"]["pressure"])+"hPa",
    '\n'"풍향 = ", str(data["wind"]["deg"])+"m/s",'\n'"풍속 = ", str(data["wind"]["speed"])+"m/s",'\n'"===================", file=f)

    f.close()

#slack으로 출력
f = open('stdout.txt' , "r")
data = { "text" : f.read()}

res = requests.post(slack_webhook_url, headers=headers, json=data)
print(res.status_code)

#txt 파일 삭제
f = open('stdout.txt' , 'w')
f.write('\n')
f.close()