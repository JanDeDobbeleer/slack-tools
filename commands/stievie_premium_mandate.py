from bss.stievie import create_premium_user
from bss.stievie import get_subscription
from bss.stievie import create_mandate
from bss.helper import Helper

try:
    mock = Helper().create_mock_gigya_user()
    user = create_premium_user(mock['username'], mock['password'], mock['profile'])
    subscription = get_subscription(user['sbss_id'])
    status = create_mandate(subscription['id'], 'cst_trolololol')
except Exception as e:
    print('error')
user = """
Email: {email}
Password: {password}
Gigya UID: {uid}
SBSS ID: {sbss}
Subscription ID: {subscription}
""".format(email=user['email'], password=user['password'], uid=user['gigya_id'], sbss=user['sbss_id'], subscription=subscription['id'])

print(user)
