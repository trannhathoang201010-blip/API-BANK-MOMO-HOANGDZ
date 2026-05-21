import requests
import time
import threading
from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "MoMo API History Bot is running!"

# --- URL VÀ THAM SỐ CỦA BẠN ---
URL = "https://api.momo.vn/transhis/api/transhis/chunks"
PARAMS = {
    'requestId': 'refresh_1779354883438',
    'startDate': '2025-05-21T23:59:59',
    'endDate': '2026-05-21T23:59:59',
    'chunkStart': '2026-05-17T05:51:44',
    'chunkSize': '20',
    'dbPart': '0',
    'client': 'sync_app',
    'page': '0'
}

# --- BỘ HEADER ĐẦY ĐỦ TỪ GÓI TIN BẠN GỬI ---
HEADERS = {
    'Host': 'api.momo.vn',
    'Cache-Control': 'max-age=3600',
    'M-Timezone': 'Asia/Ho_Chi_Minh',
    'User-Agent': 'MoMoPlatform Store/5.9.0.50900 CFNetwork/1410.1 Darwin/22.6.0 (iPhone X iOS/16.7.11)',
    'wbmtd': 'wLzT5gUr1gJCu0E7jM/rbkqhe42XtSi/pAcqdjFg43QBlAFPPdDd7zCgQvcQ+/XoOufHUQ0J7VCrRVQaqB2BO1BiZEnMwtwP/ULGdtdnjvLCMbgez9Z4uh/B/tYKLBjOfDunT7xHR/Lpj19GuZrc1emhK7rQS6KbUWrwPxZigCHF3kppcoCsAY9vNFl/AdO4hj1YumwudKu7w0TapMIkKWYsbH4VIBfC4CCWOae/l5CdGji/CEqoHbq/GncL/mVjM2MT4qFRrqZE5CXi4Q0TdEhNZ/olt74ELN3XuGVLoRP4H/WozCI3jbD87O1z7tvlveS+0KFyIo/XqOTGU/vBgqqhH2qjXjJW3ebZDaxBIVuuT+Vzet2lCKqbka7GFP7RJ1h6QT/X2EOPNX2crNRXyIKkuG0/Ai7iBKYOHxw+5H7S9MB98SXjxq2DKPpbq++t3G3wrwF+JpP8VKW2Sbp573Jff2SBbogD+ktEPJcqQ0BkWyXoycekog75JsLRPHg46G7xiR18AJT1Fcn2dpcjbx7atG3XExKgyh4BCZ/b4komTuracOG1CWqxtfp8reEFLsXjBqhXV4fH0MhxtbUd4m8Xfey3SQWZsAk+8J0oaXol3gQyiMLMvkjiJOkcEz6Tiej4DsNG3lnRv4MM/GTTurJScF8VWhdz6IKPVI6GaO+uYjupeb1BBJVCaFhKkw8EHo9Tb1R8SAYpl/Cm69HLmOegQq4aEO2lD7KyG4UXKzv3JBnjQswIwkC95gGbpb//s9NG2vEcmGtriI6CT4a64gNz/CZNzQADW2Da+JjW/V42Omhby/TwK3CsLsUQakDXfqFNazf6bqXT8cVWIUvJOSrKBsnM8nZl0LLLyl6FpPitjXc9kVUDOvukn3IqrrtVCJqUWjQIsCP6hlvyRyidVmJXrGVUV6ZpMi1w/ZzncA+fJFRUsRRc8CMjMI2O4W6P',
    'app_version': '50900',
    'wbmky': 'IVjWJIEjzNqS5pIDKlPr5A3DacPRonr0lxXyPmILWdfn/8wz5cnn+kL0fhP4idZK0xyNi2b9UZ/N5cZhkcoXZ5UAXVe8RWvw+fVeeSC1thqwI192va8DZAi2dDQkpvy5VEaEMjTW8toLy9tdyMt4J+KuJ354faOCTSgimWbBGZV1qPnKVn8L6iSOYpzk6e/NMfIC+8yBUGpEZlVhDRm7IkG0Nxlhi35ewStna6vL4Pr+5TNk1l9m0wTucRPT9DOAkZyhRzkYVtwZtlu7b3891jZcjDP6mGKuhQGQlpPCKzFwbx04MCYN1lKJyQFIVbBt7tHUdPmDd/NluqJpChe8kA==',
    'encodedQueryParams': '',
    'M-IsEncrypt': 'true',
    'Connection': 'keep-alive',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiMDE2ODI5NjIxODIiLCJpbWVpIjoiNTAxMDMtMGUyYjQ4NTRkNzdhNTAyMWYzYTQ0N2JlN2ZkOTY1NGYwMDQ2ZDZjNDVkZWI0YWI5YzhiNjQwYjUwNzgxN2VlZiIsImhJbWVpIjoiQmV4RjYvbnliOW9mNlUySGVJZVBwQnBOdlY5dk1TZE1wRXZuMTdrVkY3bnpxWW1Sdis3dTRCMnVmTmFFLzV0TkswdTd0eEJKRG40S280bWRnVkRQV05wTVF4d01CZ3NvYUc1M3gzeGc3REU9IiwiTUFQX1NBQ09NX0NBUkQiOjAsIk5BTUUiOiJUcuG6p24gTmjhuq10IEhvw6BuZyIsIkRFVklDRV9PUyI6ImlvcyIsIkFQUF9WRVIiOjUwOTAwLCJhZ2VudF9pZCI6MTEwMzM1MTY0LCJzZXNzaW9uS2V5IjoiZFNYdnR0Q2JoSy84cEpYZklFQUcrVG1HRUt1RXc0YVBuSmk5UTU0dGlsUU9peUVnNVRWdFR3PT0iLCJ1c2VyX3R5cGUiOjEsImtleSI6Im1vbW8iLCJyYXBpZF9pZCI6IjlsVGdsYWtEdktqT1BsVFlGVE1SU0U2eXo2Q0tDN1pQT2t1cFhMdzJYV3JZNkpxOUxyMmlIS0R4OGZvdEp6cmRVblJhZFFWQlBWbz0iLCJ1iOiIwMTY4Mjk2MjE4MiIsImV4cCI6MTc3OTc4Njg2OX0.Kh48Z4Xz9ztF827TDUbfA3QRNbAM5xp087Qpth_lX2_1MBI1nYpGzcBrPyaeeZNuTMFcaj21DwyvfEGP9kZ6C7XpNkq26nvaWumKwSGYD6Pft8oh25cg0KiFAKn7IxdJcVS1qZUmaJjq4GF2G3tYGOYIBcfsK6aXDGuhM1iUBtvfNa_8DavbFPJbsAaJneoZ7ZphbbsmCv2mrwFmkGjpFFY55_eRN9_Nen6saenO1lV-VCzaWJ2SR79K297A9D3_aQSop0XPFTNrCPF1k4_idQrEMhcC5uaT9_-I6oqSBOhRNlffT14ENs88cyKr3bPh68KdqiPNpnSyv6di2__fww',
    'env': 'production',
    'app_type': 'production',
    'timezone': 'Asia/Ho_Chi_Minh',
    'M-Signature': '6qZEtseSo/KAaj3suGlb1IaK1BvDZBrsFLsuefd0/rs=',
    'M-Lang': 'vi',
    'Accept': 'application/json',
    'Accept-Charset': 'UTF-8',
    'sentry-trace': '67e9361ae2d94425a3a7ad276ec76638-9eed2a3d9b0a4be0-0',
    'Accept-Language': 'vi-VN,vi;q=0.9',
    'wbSign': 'K1QUKPoL9NwPC+vv6Y62/+iifuPFj1RNDhc5pJ6kCs7rFKENw5vYZ44mQaE74vlr1mNSWurjAXwvwojzFD/2O57JId4JByHdEWrWcv4zpRyDgj8='
}

def fetch_momo():
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        try:
            # Tạo các chuỗi timestamp động để tránh lệch múi giờ hoặc hết hạn phiên cơ bản
            current_time_ms = str(int(time.time() * 1000))
            HEADERS['M-RequestId'] = f"11BD5874-6631-456B-83AB-E90F94A3993C.{current_time_ms}"
            HEADERS['M-Timestamp'] = current_time_ms
            HEADERS['wbCode'] = f"0&{current_time_ms}"
            HEADERS['http-process-timestamp'] = current_time_ms
            HEADERS['platform-timestamp'] = str(int(time.time() * 1000) + 2)

            # Thực hiện lệnh gọi API
            response = requests.get(URL, headers=HEADERS, params=PARAMS, timeout=15)
            
            if response.status_code == 200:
                res_data = response.json()
                # Kiểm tra xem có dính Captcha bảo mật hay không
                if res_data.get("riskMsg", {}).get("errorCode") == "881200001":
                    print(f"[{now}] Hệ thống MoMo yêu cầu giải Captcha hình ảnh.")
                else:
                    print(f"[{now}] Kết nối thành công! Dữ liệu: {response.text[:120]}...")
            else:
                print(f"[{now}] Phản hồi lỗi từ Server (Mã HTTP {response.status_code})")
                
        except Exception as e:
            print(f"[{now}] Lỗi hệ thống: {e}")
            
        # Chờ đúng 60 giây (1 phút) trước khi thực hiện lượt quét tiếp theo
        time.sleep(60)

if __name__ == "__main__":
    # Kích hoạt luồng chạy ngầm để lấy lịch sử
    threading.Thread(target=fetch_momo, daemon=True).start()
    # Chạy Web Server giả để tránh lỗi deploy trên Render
    app.run(host='0.0.0.0', port=10000)
