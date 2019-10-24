import random
import requests
from decouple import config
from flask import Flask, request
token = config('TELEGRAM_TOKEN')
app = Flask(__name__)

@app.route('/')
def index():
    return 'chatbot!'

@app.route(f'/{token}',methods=['POST'])
def telegram():
    print(request.get_json())
    telegram_json = request.get_json()
    if telegram_json.get('message'):
    #메시지 내용 있을 때만 아래 작업 수행
        text = telegram_json.get('message').get('text')

        if '로또' in text:
            text = sorted(random.sample(range(1, 46),6))
        elif '비트코인' in text:
            currency = 'BTC'
            url = f'https://api.bithumb.com/public/ticker/{currency}'
            response = requests.get(url).json()
            text = response.get('data').get('opening_price')
        elif '/번역' == text[0:4]:
            naver_client_id = config('NAVER_CLIENT_ID')
            naver_client_secret = config('NAVER_CLIENT_SECRET')
            url = 'https://openapi.naver.com/v1/papago/n2mt'
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
            text = response.get('message').get('result').get('translatedText')

        #답장 메시지 보내기
        chat_id = 951399285
        base_url =f'https://api.telegram.org/bot{token}'
        url =f'{base_url}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(url)

    return '',200
#python app.py로 서버 실행, Debug모드로
if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT',5000))
    app.run(host='0.0.0.0', port=port, debug=True)