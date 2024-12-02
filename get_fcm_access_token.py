import json
import jwt # PyJWT library
import requests
import time

SERVICE_ACCOUNT_FILE='./file/fir-notify-1-e4261-firebase-adminsdk-2.json'

# Đọc file JSON
with open(SERVICE_ACCOUNT_FILE, 'r') as file:
    service_account = json.load(file)
    
# Tạo JWT
now = int(time.time()) # Thời gian hiện tại (epoch time)
payload = {
    "iss": service_account["client_email"],  # Issuer - Email tài khoản dịch vụ
    "scope": "https://www.googleapis.com/auth/firebase.messaging",  # Quyền truy cập API FCM
    "aud": "https://oauth2.googleapis.com/token",  # Audience
    "iat": now,  # Issued At - Thời gian phát hành
    "exp": now + 3600  # Expiration Time - Token có hiệu lực trong 1 giờ
}

# Thay thế các ký tự "\\n" bằng ký tự xuống dòng thực
private_key = service_account["private_key"].replace("\\n", "\n")

# Ký JWT bằng thuật toán RS256
jwt_token = jwt.encode(payload, private_key, algorithm='RS256')

# print("Token: ", jwt_token)

# Gửi yêu cầu ddeeesn endpoint OAuth 2.0 của Google để lấy access token
url = "https://oauth2.googleapis.com/token"
headers = {
    "Content-Type":"application/x-www-form-urlencoded"
}
data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": jwt_token
}

response = requests.post(url, headers=headers, data=data)

# print("Response: ", response)
# Xử lý kết quả
if response.status_code == 200:
    access_token = response.json().get("access_token")
    print("Access Token: ", access_token)
else:
    print("Error: ", response.status_code, response.json())