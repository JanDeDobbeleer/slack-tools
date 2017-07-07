
class GigyaErrorCode(object):
    """
    For a full list of response codes and their meaning, see
    http://developers.gigya.com/display/GD/Response+Codes+and+Errors+REST
    """
    UID_INVALID_FOR_SITE = 403005

    ACCOUNT_PENDING_VERIFICATION = 206002


class GigyaApiEndpoint(object):
    """
    For a full list of response codes and their meaning, see
    http://developers.gigya.com/display/GD/REST+API
    """
    ACCOUNTS_INIT_REGISTRATION = 'accounts.initRegistration'
    ACCOUNTS_GET_ACCOUNT_INFO = 'accounts.getAccountInfo'
    ACCOUNTS_REGISTER = 'accounts.register'
    ACCOUNTS_SEARCH = 'accounts.search'
    ACCOUNTS_SET_ACCOUNT_INFO = 'accounts.setAccountInfo'
