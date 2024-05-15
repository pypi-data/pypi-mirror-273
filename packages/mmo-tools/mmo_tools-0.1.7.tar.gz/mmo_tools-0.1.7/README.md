# mmo_tools
Đây là một thư viện Python chứa các hàm tiện ích để chuyển đổi dữ liệu và cấu hình proxy .

## service
- **convert_data**
- **headers**
- **checklive**
## funciton

### `convert_data`
- Chuyển đổi dữ liệu từ tệp đầu vào thành danh sách các đối tượng từ điển.
- **input**: path file input (str).
- **result**: dict (`[{},{}`]).
### `headers`
- return dict facebook headers 

### `check_facebook_account`
- Kiểm tra tài khoản bằng uid người dùng để biết trạng thái khóa
- **input** : user-id facebook account
- **result** : 1 / 0
### `cookie_confirm_auth_2fa`
- Xác nhận mã 2fa để hạn chế out cookie khi chạy requests
- **input** : session , code , fb_dtsg
- **result** : 1 / 0
## example
```python
import os , sys
from mmo_tools import *
# Giả sử file_path là đường dẫn tới tệp dữ liệu
file_path = 'data/mmo_tools.txt'
def func1():
    # Chuyển đổi dữ liệu từ tệp
    data = convert_data(file_path)

    print(data)  # [{'key': 'value'}, {'key2': 'value2'}]

def func2():
    headers = headers()
    print(headers) # {'user-agent':'my user-agent','accept':'*/*'...}

def func3():
    status = checlive(506356883)
    print(status) # result : 0 

def func4():
    text_header = """Accept:
        application/json
        Accept-Encoding:
        gzip, deflate, br
        Accept-Language:
        vi,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6
        Af-Ac-Enc-Dat:
        76febcb9e58ec473
        X-Sz-Sdk-Version:
        1.9.0"""
    r = convert_headers_web(text_header)
    print(r) # result : {'Accept': 'application/json', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'vi,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6', 'Af-Ac-Enc-Dat': '76febcb9e58ec473', 'Af-Ac-Enc-Sz-Token': '','X-Sz-Sdk-Version': '1.9.0'}
def func5():

    r = requests.Session()
    r.headers.update(headers())
    code = "12345678"
    fb_dtsg = "NA20202..."

    print(cookie_confirm_auth_2fa(r,code,fb_dtsg)) # False / Cuccess

```
## install
```bash
pip install mmo_tools

```
## update new version
``` update
pip install --upgrade mmo_tools
```
# contact
-  Youtube : [ilam](https://www.youtube.com/@iam_dlam)
- Facebbok : [Le Dinh Lam](https://www.facebook.com/IT.Admin.InF/)
- Telegram : [Lam](https://t.me/im_dlam)