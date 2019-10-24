import requests
from decouple import config

naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')

url = 'https://openapi.naver.com/v1/papago/n2mt'
text = '띵작'
headers = {
    'X-Naver-Client-Id': naver_client_id,
    'X-Naver-Client-Secret': naver_client_secret
}
data = {
    'source': 'ko',
    'target': 'en',
    'text': text
}
response = requests.post(url, data=data, headers=headers).json()
print(response.get('message').get('result').get('translatedText'))
