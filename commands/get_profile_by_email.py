import json
import os
import sys
from bss.gigya import GigyaClient

try:
    email = sys.argv[1]
    info = GigyaClient(os.environ.get('P_G_AKEY')).do_gigya_query("select * FROM accounts where loginIDs.emails contains \"{}\" or loginIDs.unverifiedEmails contains \"{}\"".format(email, email))
    users = info['results']
    if info['totalCount'] == 0:
        print("No user found for {}".format(email))
        exit(0)
    for user in users:
        user = """
        Gigya UID: {uid}
        Premium: {premium}
        """.format(uid=user['UID'], premium='authorization' in user['data'])
        print(user)
except Exception as e:
    print(e)
