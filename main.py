from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def get_momo_history():
    # 1. Link API mới bạn vừa gửi (Lưu ý: Đây là phương thức GET)
    url = "https://api.momo.vn/transhis/api/transhis/chunks?requestId=refresh_1778810314489&startDate=2025-05-15T23%3A59%3A59&endDate=2026-05-15T23%3A59%3A59&chunkSize=20&dbPart=0&client=sync_app&page=0"

    # 2. Bộ Header "tươi" vừa bắt lúc 08:59
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiMDE2ODI5NjIxODIiLCJpbWVpIjoiNTAxMDMtMGUyYjQ4NTRkNzdhNTAyMWYzYTQ0N2JlN2ZkOTY1NGYwMDQ2ZDZjNDVkZWI0YWI5YzhiNjQwYjUwNzgxN2VlZiIsImhJbWVpIjoiQmV4RjYvbnliOW9mNlUySGVJZVBwQnBOdlY5dk1TZE1wRXZuMTdrVkY3bnpxWW1Sdis3dTRCMnVmTmFFLzV0TkswdTd0eEJKRG40S280bWRnVkRQV05wTVF4d01CZ3NvYUc1M3gzeGc3REU9IiwiTUFQX1NBQ09NX0NBUkQiOjAsIk5BTUUiOiJUcuG6p24gTmjhuq10IEhvw6BuZyIsIkRFVklDRV9PUyI6ImlvcyIsIkFQUF9WRVIiOjUwODAyLCJhZ2VudF9pZCI6MTEwMzM1MTY0LCJzZXNzaW9uS2V5IjoiaWpaeUpGbk5vWkwyNVhhTjZ1cUdZMmt0UUtna3NhYUJRbHNsSlNSczUzVzFUVmhNSlRlbnhRPT0iLCJ1c2VyX3R5cGUiOjEsImtleSI6Im1vbW8iLCJyYXBpZF9pZCI6ImJrc1NQcnhkZU00M1ZjT25QaWxpcG5NTTdqckxOZTVFc1lVZ0dPc2RtNFU0Uit1K2REeFhmc0tGZk14ellJMWNXN1UzaHY4MXpwcz0iLCJ1aWQiOiIwMTY4Mjk2MjE4MiIsImV4cCI6MTc3OTI0MjA4NH0.qUwunAzVcK_PTYRYdeKHld7Y9kGXrpFP0yRlHI4-O6IE39vlmZkGbQoYqxgSnCh7y53DRYnA2MMtndzO8BIWU_BGcJZgF2KX2bhbJzHg0CsdmF2L79e0tpAKWNM_JA2Xswp1_zNuG5x3UQZ99Swhs4XzXStYzZ3_eB7yvW8ghWx_ZKYt0ROPocmf-eWlcJhPftE-MPhwLqPTwVLMdxlGzKUDJ3FNHTShDPcDdMY0qN2BLsFeESGDCBpptlIo5hSJbDEAVtjl4-x2pyuplaZoUrC9JgDmpCHV8MOacwoRJ2MHti-dLUWKSvn7yd8gZbwsc8uV8nVC7N1KU4kZ7wWAxg",
        "wbSign": "MXTCJS+wGYDFwfJjK+K12A+wYsYZsPCFRie+dKccxOSNsll0BGpo3qf22cYfzuP/qCG8x3ssNjVz7cX0a8vSKCwcqsm4K8uuO4v3lNSt/hglbQ==",
        "wbmky": "Hl0WNHBapce1ghoEMMSa7p5opIwXU/Qow0XcbviObX1Lgs5kgN5wST2eBXl3+5N3Gf79lUKcqYmtGEafJ/bv3pBa3dKEFQBQxiHDv83k2kx6ONaf34lTSW+3xID6y+X16lX5jBSdOlUpetHrJ5WZOuJmd+onLlJDeq0Rv0j8RKhiply4SwTAFoHc3Y+6bYzVuAGf5cRTzZlihqGe9ICe2Flwszh2NcwZpTTwNawqT6sXH9dsIp5yTyhe7ylkXtvt6/Gy0kaNtn9e2rLEOoXWbyi1fJCGmt9gn7iJbHCgLR4t/BRqIMOGm4P5zbNOx0opHNz2fST6uOwZzj5vx7Vfyg==",
        "wbmtd": "CD+zC8T/ptaLkTzpK4DRQtov1kInPT2/vLRbbDjQ2L/hThXJKxeOJAHpbfKZAuRrBw0TMC0ZiPf8ROXf984RIwsFPTB+TWe1bt9P4b3C88QZ+xMiPPgndw7XbSIZFruZl0Etz3aeglPPMMgIC/9ENgX6W3XZMLRXQwCnAb0ZPA+emBcLLTwGvgwbG3xMyGSd70UEaLQ21P8XiZ1bveKH4xbvZkAFJsVwG2oiqNOqg7Rdl1ZjNYmWCrbYykRvsTJ/XyptBkDbBFRVkB4FnNMlTeHtted5qfyiBGUmzJNR3Ch9LSV3MBdR/shyVbl1kcr/NK56LPm0nTIxOCb/s0+Fu0NX3Q9RwUwg8wz8TaeKGlTDMrpjQ4Iq7XwmCLpeoeh3OyYWDtUHqFssdkTFKs1onzSb39euPV7xgv1GzlxtEjndeQrn6NgQdaUz/SA30yzbG7RAf12DyyjRV55s7E3p4jmEENafGaq5J1DIiuc8bgptINOS9+m9OkYqhvyyjrypGT2mz3q4aUzoduTF6aY355RSoAWKPpJLrQlBsBgvQ4F6gyvnbSpf8yVHJekKG+ieowTLVEw3qji4EhDurHPZAsgyvmy4eW39wurw5pcGG6CDS3MzjunurbXdqRJFjcb812EfqlnvQ4OjDXzymqxkFjZlsw+UVX3NA7opeyxHrY0/QAx5NHFPWj9b5/LreFHiGwvjqUQractncpIjuH638K4XCy9prNj0y7zuVK/0I8dLHiGUH2sYRbha9oZ4NMxAgiXVl20SfYBp2BNYTGJtXCndxSIFhLUw7umUUZM4CiHNgUFBRQduIJpsvUrc6s96rNtftJadWIhTa85fHjfBQT3etuQC/syHPAd9JS55gBr9WK1oYc9sf0ODhpbeRpFENNl4ubjcT/BAeWZCLbOFcHn4oY6gqRl3y4mBIViM8BMrj7F9mPqwHIUgStLxA18+",
        "User-Agent": "MoMoPlatform Store/5.8.0.50802 CFNetwork/1410.1 Darwin/22.6.0 (iPhone X iOS/16.7.11)",
        "M-Timestamp": "1778810314496",
        "M-Signature": "OyK2t5OadfCSefiyn/2mhz+H32dGRnawMZq1UKqaKl4=",
        "M-IsEncrypt": "true",
        "Accept": "application/json"
    }

    try:
        # Sử dụng requests.get thay vì post vì link chứa query params trực tiếp
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
