from bss.stievie import create_gigya_user
from bss.helper import Helper

try:
    mock = Helper().create_mock_gigya_user()
    uid = create_gigya_user(mock['username'], mock['password'], mock['profile'])
except Exception as e:
    print('error')
user = """
Email: {email}
Password: {password}
Gigya UID: {uid}
""".format(email=mock['username'], password=mock['password'], uid=uid)

print(user)
