import json
import os
import sys
from bss.gigya import GigyaClient

try:
    uid = sys.argv[1]
    GigyaClient(os.environ.get('P_G_AKEY')).update_view_permissions(uid, True)
    info = GigyaClient(os.environ.get('P_G_AKEY')).get_account_info(uid)
    user = """
    Gigya UID: {uid}
    Premium: {premium}
    """.format(uid=info['UID'], premium='authorization' in info['data'])
    print(user)
except Exception as e:
    print(e)


