from requests import post, get


print(post('http://127.0.0.1:8000/auth/login', data={'name': 'string', 'password': 'string'}))
print(get(''))