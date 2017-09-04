import os
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from .gigya import GigyaClient

def do_soap_call(payload):
    querystring = {"wsdl":""}   
    headers = {
        'content-type': "text/xml",
        'authorization': "Basic {}".format(os.environ.get('BSS_AUTH_HEADER')),
        'cache-control': "no-cache"
    }
    response = requests.request("POST", os.environ.get('BSS_WSDL'), data=payload, headers=headers, params=querystring)
    return response

def do_soap_status_call(payload):
    response = do_soap_call(payload)
    soup = BeautifulSoup(response.text, "lxml")
    codes = soup.find_all('statuscode')
    statuscode = codes[0].string
    status = 'OK'
    if statuscode != '200':
        status = 'FAILED'
    return {
        'status': status
    }

def create_gigya_user(email, password, profile):
    uid = GigyaClient().register_account(email, password, profile)
    return uid

def create_premium_user(email, password, profile):
    uid = create_gigya_user(email, password, profile)
    payload = "<soap-env:Envelope xmlns:soap-env=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap-env:Body>\n    <ns0:mergeCustomer xmlns:ns0=\"{}/\">\n      <user>{}</user>\n      <customerId></customerId>\n     <firstName>{}</firstName>\n      <lastName>{}</lastName>\n      <sex>Female</sex>\n      <dateOfBirth>20-05-1990</dateOfBirth>\n     <placeOfBirth>{}</placeOfBirth>\n      <email>{}</email>\n      <contactMobilePhone>0486128963</contactMobilePhone>\n      <companyName></companyName>\n      <VAT></VAT>\n      <marketingPermission>true</marketingPermission>\n      <brand>Stievie</brand>\n      <gigyaID>{}</gigyaID>\n      <mgmMemberId></mgmMemberId>\n      <street>{}</street>\n      <houseNumber>{}</houseNumber>\n     <houseNumberBox>{}</houseNumberBox>\n      <postalCode>{}</postalCode>\n      <city>{}</city>\n      <country>Belgium</country>\n     <language>Dutch</language>\n      <identityDocumentType></identityDocumentType>\n      <identityDocumentIssuer></identityDocumentIssuer>\n     <identityDocumentNumber></identityDocumentNumber>\n    </ns0:mergeCustomer>\n  </soap-env:Body>\n</soap-env:Envelope>".format(os.environ.get('BSS_NAMESPACE'), os.environ.get('BSS_USER'), profile.first_name, profile.last_name, profile.place_of_birth,email, uid, profile.street, profile.house_number, profile.box_number, profile.postal_code, profile.city)
    response = do_soap_call(payload)
    soup = BeautifulSoup(response.text, "lxml")
    codes = soup.find_all('customercode')
    customercode = codes[0].string
    subscription_response = create_subscription(customercode)
    if subscription_response['status'] != 'OK':
        raise Exception('The BSS user was created but the creation of premium failed')
    return {
        'email': email,
        'password': password,
        'gigya_id': uid,
        'sbss_id': customercode
    }

def create_mandate(subscription_id, mandate_id):
    payload = '<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"><soap-env:Body><ns0:mergePaymentData xmlns:ns0="{}/"><user>{}</user><customerCode></customerCode><paymentDataType>MLN.Credit card VISA</paymentDataType><paymentDataId></paymentDataId><subscriptionId>{}</subscriptionId><bic></bic><iban></iban><sepaMandateId></sepaMandateId><tokenId>{}</tokenId><cardExpiryDate>31-05-2022</cardExpiryDate><accountNumber>3680</accountNumber><owner>Steven Desloovere</owner></ns0:mergePaymentData></soap-env:Body></soap-env:Envelope>'.format(os.environ.get('BSS_NAMESPACE'), os.environ.get('BSS_USER'), subscription_id, mandate_id)
    return do_soap_status_call(payload)

def create_subscription(customercode):
    payload = "<soap-env:Envelope xmlns:soap-env=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap-env:Body>\n    <ns0:createContract xmlns:ns0=\"{}/\">\n      <user>{}</user>\n      <customerCode>{}</customerCode>\n     <simIccid></simIccid>\n      <donorSimIccid></donorSimIccid>\n      <msisdn>+32475563671</msisdn>\n      <firstMonthFree>false</firstMonthFree>\n     <donorRequestType></donorRequestType>\n      <donorAccountNumber></donorAccountNumber>\n      <isBillingAddress>false</isBillingAddress>\n     <billingAddress>\n        <city>peer</city>\n        <country>belgium</country>\n        <houseNumber>3</houseNumber>\n       <houseNumberBox></houseNumberBox>\n        <postalCode>3990</postalCode>\n        <street>bannaanlaan</street>\n      </billingAddress>\n     <isShippingAddress>false</isShippingAddress>\n      <shippingAddress>\n        <city>peer</city>\n        <country>belgium</country>\n       <houseNumber>3</houseNumber>\n        <houseNumberBox></houseNumberBox>\n        <postalCode>3990</postalCode>\n        <street>bannaanlaan</street>\n     </shippingAddress>\n      <productOfferingId>{}</productOfferingId>\n      <productOfferingVersion>1</productOfferingVersion>\n     <productOfferingVariant>1</productOfferingVariant>\n      <parentSubscriptionId></parentSubscriptionId>\n      <paymentDataId></paymentDataId>\n     <accountDistributionChannel>P</accountDistributionChannel>\n      <productOfferingChilds/>\n    </ns0:createContract>\n </soap-env:Body>\n</soap-env:Envelope>".format(os.environ.get('BSS_NAMESPACE'), os.environ.get('BSS_USER'), customercode, os.environ.get('OFFERING_ID'))
    return do_soap_status_call(payload)

def get_subscription(customercode):
    payload = "<?xml version='1.0' encoding='utf-8'?><soap-env:Envelope xmlns:soap-env=\"http://schemas.xmlsoap.org/soap/envelope/\"><soap-env:Body><ns0:getCustomerSubscriptions xmlns:ns0=\"{}/\"><user>{}</user><customerCode>{}</customerCode></ns0:getCustomerSubscriptions></soap-env:Body></soap-env:Envelope>".format(os.environ.get('BSS_NAMESPACE'), os.environ.get('BSS_USER'), customercode)
    response = do_soap_call(payload)
    soup = BeautifulSoup(response.text, "lxml")
    codes = soup.find_all('objectid')
    return {
        'id': codes[0].string
    }

def get_gigya_profile(email):
    profile = GigyaClient().get_profile_from_email(email)
    return profile
