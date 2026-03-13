import requests as req
url = "https://api4.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
rel = req.get(url).text
btc = rel[29:34]          
won = str(int(btc) * 1450)     
# print(won)
# print("원화가격:", won[:1] + "억 " + won[1:4] + "만 " + won[4:] + "원")
print(((won[-12:-8] + "억") if won[-12:-8] else ""), won[-8:-4] + "만", won[-4:] + "원")