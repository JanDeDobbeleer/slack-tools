import json
import os
import sys
from bss.gigya import GigyaClient

try:
    email = sys.argv[1]
    info = GigyaClient(os.environ.get('P_G_AKEY')).do_gigya_query("select * FROM accounts where profile.email=\"{}\" and data.authorization is null".format(email))
    if info['totalCount'] == 0:
        print("No or not-non-premium record found for {}, aborting".format(email))
        exit()
    if info['totalCount'] != 1:
        print("No single record found for {}, aborting".format(email))
        exit()
    uid = info['results'][0]['UID']
    GigyaClient(os.environ.get('P_G_AKEY')).update_view_permissions(uid, True)
    info = GigyaClient(os.environ.get('P_G_AKEY')).get_account_info(user_id)
    user = """
    Gigya UID: {uid}
    Premium: {premium}
    """.format(uid=info['UID'], premium='authorization' in info['data'])
    print(user)
except Exception as e:
    print(e)
