import json
import os
import sys
from bss.gigya import GigyaClient

try:
    info = GigyaClient(os.environ.get('P_G_AKEY')).get_profile_from_email(sys.argv[1])
    pretty = json.dumps(info, indent=4, sort_keys=True)
    print(pretty)
except Exception as e:
    print('No user found with that email address.')
