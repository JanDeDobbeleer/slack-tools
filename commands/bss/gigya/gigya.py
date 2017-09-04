import os
from .constants import GigyaApiEndpoint, GigyaErrorCode
from .exceptions import GigyaClientException
from .GSSDK import GSRequest

class GigyaClient(object):
    """Concrete implementation of the client that communicates with the Gigya REST API"""

    def __init__(self, api_key = None):
        self.api_key = os.environ.get('G_AKEY') if api_key is None else api_key
        self.user_key = os.environ.get('G_UKEY')
        self.secret_key = os.environ.get('G_SKEY')
        self.domain = "eu1.gigya.com"

    def _call_gigya(self, method, params):
        """
        Private method that will actually use the Gigya client request library to make a request and to check if the
        response was success. If not it raises an exception.
        :param method: all possible methods: http://developers.gigya.com/display/GD/REST+API
        :param params: a dict depending on the request that is made.
        :return: dict of response data
        """
        # params.copy() because GSSDK adds parameters to this dict.
        # We are using the user key for authentication so secret, is the secret of the console user who has API rights.
        request = GSRequest(apiKey=self.api_key, apiMethod=method, params=params.copy(), useHTTPS=True,
                            userKey=self.user_key, secretKey=self.secret_key)

        request.setAPIDomain(self.domain)
        response = request.send()

        if response.getErrorCode() == 0:
            return response.data
        else:
            raise GigyaClientException(response)

    def exchange_uid_signature(self, uid, uid_signature, signature_timestamp):
        """
        Check if the user has logged in into the fronted. These parameters are returned by the login request or if
        you request account info.
        """

        params = {
            'UID': uid,
            'UIDSignature': uid_signature,
            'signatureTimestamp': signature_timestamp,
            'userKey': self.user_key,
        }
        method = 'accounts.exchangeUIDSignature'
        response = self._call_gigya(method, params)
        return response.get('errorCode', -1) == 0

    def register_account(self, email, password, profile):
        """
        http://developers.gigya.com/display/GD/accounts.initRegistration+REST
        http://developers.gigya.com/display/GD/accounts.register+REST

        This method will do two calls. The first call will set how further communication will proceed (response format,
        error codes). The second call will do the actual registration.

        Email (and not a username) is used as main identifier for the user.
        :return: The UID of the new user.
        :rtype: unicode
        """
        init_reponse = self._call_gigya(GigyaApiEndpoint.ACCOUNTS_INIT_REGISTRATION, {})
        reg_token = init_reponse['regToken']

        profile_data = {
            'firstName': profile.first_name,
            'lastName': profile.last_name,
            'birthDay': profile.birth_date.day if profile.birth_date else '',
            'birthMonth': profile.birth_date.month if profile.birth_date else '',
            'birthYear': profile.birth_date.year if profile.birth_date else '',
            'city': profile.city,
            'gender': profile.gender,
            'zip': profile.postal_code
            # TODO phones number + type as a dict
        }

        extra_data = {
            'street': profile.street,
            'housenumber': profile.house_number,
            'boxnumber': profile.box_number
            # TODO
            #  registrationSource: null,
            #  terms: null, // boolean,
            #  terms_Stievie: null,
            # subscribe & autologin ?
        }

        registration_params = {
            'regToken': reg_token,
            'finalizeRegistration': True,
            'email': email,
            'password': password,
            'profile': profile_data,
            'data': extra_data
        }

        # The accountOptions policy verifyEmail is "true" and the confirmation email redirects to another page out of
        # our control. So we can not conclude the registration without breaking the existing flows.
        # A separate dev env for Stievie Premium would allow us to set verifyEmail to false or redirect
        # to a page of our control.
        #
        # More info http://developers.gigya.com/display/GD/Accounts+API  # AccountsAPI-ErrorCodesandMessages
        # The "Account pending verification" error is returned (error code 206002) when the account has already been
        # verified, and a user tries to log in with a loginID (usually an email address) that we have not yet verified
        # that actually belongs to this person.
        # When the accountOptions policy states that  verifyEmail  is "true", the account must be validated by using
        # the available email addresses. When the policy states that  allowUnverifiedLogin  is "false", users are not
        # allowed to login before they have verified their emails. So, in this case, when a user tries to login, and
        # his account has not been verified yet, and verifyEmail is "true" in the policy and  allowUnverifiedLogin  is
        # "false" in the policy, the "Account pending verification" error is returned.

        try:
            registration_response = self._call_gigya(GigyaApiEndpoint.ACCOUNTS_REGISTER, registration_params)
        except GigyaClientException as ge:
            if ge.error_code == GigyaErrorCode.ACCOUNT_PENDING_VERIFICATION:  # reason, see comments above
                registration_response = ge.response
            else:
                raise ge
        return registration_response.data['UID']

    # Don't know if we need it already but I consider it highly likely.
    def update_account_profile(self, uid, profile):
        """
        Updates profile info for a specific account.
        Uses http://developers.gigya.com/display/GD/accounts.setAccountInfo+REST
        :param uid: The UID of the user for whom you want to update the profile.
        :type uid: str or unicode
        :param profile: Profile fields to update.
        :type profile: stievie_bss.shared.identity.mappings.Profile
        """
        profile_data = {
            'email': profile.email,
            'firstName': profile.first_name,
            'lastName': profile.last_name,
            'birthDay': profile.birth_date.day,
            'birthMonth': profile.birth_date.month,
            'birthYear': profile.birth_date.year,
            'city': profile.municipality,
            'gender': profile.gender,
            'zip': profile.postal_code
        }

        extra_data = {
            'street': profile.street,
            'housenumber': profile.house_number,
            'boxnumber': profile.box_number
        }

        self._call_gigya(GigyaApiEndpoint.ACCOUNTS_SET_ACCOUNT_INFO, {'uid': uid, 'profile': profile_data,
                                                                      'data': extra_data, 'isVerified': True})

    # currently not used but keeping it around because it might chance again.
    def login(self, login_id, password):
        """Login into Gigya with the given credentials"""
        params = {
            'loginID': login_id,
            'password': password,
            'userKey': self.user_key,
        }
        method = 'accounts.login'
        response = self._call_gigya(method, params)
        return response

    def get_account_info(self, uid):
        """Login into Gigya with the given credentials"""
        params = {
            'UID': uid,
            'include': "identities-active,identities-all,identities-global,loginIDs,emails,profile,data,password,lastLoginLocation,regSource,irank,rba,subscriptions"
        }
        method = 'accounts.getAccountInfo'
        response = self._call_gigya(method, params)
        return response

    def get_profile_from_email(self, email):
        """
        Get a UID for an email address
        """

        params = {
            'query': "select * FROM accounts where profile.email=\"{}\"".format(email)
        }
        method = 'accounts.search'
        response = self._call_gigya(method, params)
        return response

    def get_available_channels(self, enabled):
        return {
            '_2be': enabled,
            'bbcfirst': enabled,
            'canvas': enabled,
            'caz': enabled,
            'ccflan': enabled,
            'discovl': enabled,
            'een': enabled,
            'eursbe': enabled,
            'kadet': enabled,
            'ketnet': enabled,
            'kzoom': enabled,
            'mtvvl': enabled,
            'ngc': enabled,
            'ngcwild': enabled,
            'npo1': enabled,
            'npo2': enabled,
            'npo3': enabled,
            'qmusic': enabled,
            'tlcvl': enabled,
            'vier': enabled,
            'vijf': enabled,
            'vitaya': enabled,
            'vtm': enabled,
            'zes': enabled
        }

    def update_view_permissions(self, uid, is_premium_subscription):
        """
        Updates the view permissions (permission string) for a specific account.
        Uses http://developers.gigya.com/display/GD/accounts.setAccountInfo+REST
        :param uid: the user id in gigya
        :param is_premium_subscription: indicates if it's a premium subscription or not
        """
        data = {
            'authorization': {
                'Stievie_free': {
                    'subscription': {
                        'id': 'premium' if is_premium_subscription else 'free'
                    },
                    'streams': {
                        'concurrency': 1
                    },
                    'npvr': {
                        'enabled': True if is_premium_subscription else False,
                        'max': 200 if is_premium_subscription else 0,
                        'expires': 14400 if is_premium_subscription else 0,
                    },
                    'pvr': {
                        'enabled': True if is_premium_subscription else False
                    },
                }
            }
        }

        channels = self.get_available_channels(is_premium_subscription)
        channels_dict = {}
        for channel_code, channel_enabled in channels.items():
            channels_dict[channel_code] = {'enabled': channel_enabled}
        data['authorization']['Stievie_free'].update({'channels': channels_dict})

        self._call_gigya(GigyaApiEndpoint.ACCOUNTS_SET_ACCOUNT_INFO, {'uid': uid, 'data': data})
