#### btc.py
```python
import requests as req

url = "https://api4.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
rel = req.get(url).text

btc = rel[29:34]          
won = str(int(btc) * 1450)     

print("비트코인 가격:", btc + "원")
print("원화가격:", won[:1] + "억 " + won[1:4] + "만 " + won[4:] + "원")
```

#### disp.py
```python
# print 응용2
import time as t
print("기대하세요.", end='\r')
t.sleep(1.5)
print("드디어~~~", end='\r')
t.sleep(1.5)
print("개방합니다!", end='\r')
t.sleep(1.5)
```

#### test.py
```python
print("테스트 해볼게요.")
a = 123
b = 234
print(a)
b
```

#### usd.py
```python
import requests as r

btc = "https://api4.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
usd = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={한국수출입은행 API키}&data=AP01"

r1 = r.get(btc).json()
r2 = r.get(usd).json()

usd_krw = float(
    [x['deal_bas_r'] for x in r2 if x['cur_unit'] == 'USD'][0]
    .replace(',', '')
)

r3 = float(r1['price']) * usd_krw

print(f"{int(r3):,}", "원")
```

#### web.py
```python
import requests as req
import webbrowser as wb

# 위성위치
url = "http://api.open-notify.org/iss-now.json"
# 탑승자 명단
url2 = "http://api.open-notify.org/astros.json"

result = req.get(url).json()
lat = result['iss_position']['latitude'] # 위도
lon = result['iss_position']['longitude'] # 경도

result2 = req.get(url2).json()["number"]

url = f"https://www.google.com/maps?q={lat}, {lon}"

print(f"현재 {result2}명이 탑승한 인공위성(국제우주정거장) 위치를 열겠습니다. 위도: {lat}, 경도: {lon}")
wb.open(url)
```

#### 03장 되새김 문제
##### 01 
```python
a = "Life is too short, you need python"

if "wife" in a: print("wife")
elif "python" in a and "you" not in a: print("python")
elif "shirt" not in a: print("shirt")
elif "need" in a: print("need")
else: print("none")
```

##### 02
```python
result = 0
i = 1
while i <= 1000:
    if (i % 3 == 0):
        result += i
    i += 1
print(result)
```

##### 03
```python
i = 0
while True:
    i += 1
    if i > 5 : break
    print('*' * i)
```

##### 04
```python
for i in range(1, 101):
    print(i)
```

##### 05
```python
A = [70, 60, 55, 75, 95, 90, 80, 80, 85, 100]
total = 0
for score in A:
    total += score
average = total / len(A)
print(average)
```

##### 06
```python
numbers = [1, 2, 3, 4, 5]
result = [n * 2 for n in numbers if n % 2 == 1]
print(result)
```
