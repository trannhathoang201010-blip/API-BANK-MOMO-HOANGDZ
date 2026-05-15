from fastapi import FastAPI
import requests
import json

app = FastAPI()

@app.get("/")
def get_momo_history():
    url = "https://api.momo.vn/transhis/api/transhis/search"
    
    # Header bạn đã bắt được
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...", # Chép nguyên cái Token dài vào đây
        "sessionKey": "86d18a3e-8f7e-4a93-b45e-b0179065084c",
        "wbSign": "XTQPgBgiNu/IXcPXUD0AUP5xnaMzlhm1vXH/T6Gxns6LQfYaR35LgpQsaoGlNP9TxavyhnIY28RHBEndO8nbX7779CetmvZHjRArknPRaEln",
        "user_phone": "01682962182",
        "userId": "01682962182",
        "User-Agent": "MoMoPlatform Store/5.8.0.50802 CFNetwork/1410.1 Darwin/22.6.0 (iPhone X iOS/16.7.11)",
        "Content-Type": "application/json"
    }

    # Body để lấy lịch sử
    payload = {
        "beginDate": "01/05/2026", 
        "endDate": "15/05/2026",
        "offset": 0,
        "limit": 10
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
    except Exception as e:
        return {"error": str(e)}
