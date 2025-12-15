from kiteconnect import KiteConnect

api_key = "mtb3ovyzkoxwuovq"
api_secret = "uf698sbvsadg1znnukqdr5z47mkpcaaq"
request_token = "X0TPTko5P7hw6eChF1SoSDMj23VN0GhE"

kite = KiteConnect(api_key=api_key)
data = kite.generate_session(request_token=request_token, api_secret=api_secret)
access_token = data["access_token"]
print("ACCESS_TOKEN:", access_token)
