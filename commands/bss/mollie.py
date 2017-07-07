"""
Mollie Python library
"""
import os
import Mollie

def get_client():
    """Creates the API client"""
    mollie = Mollie.API.Client()
    mollie.setApiKey(os.environ.get('M_KEY'))
    return mollie


def get_mandate_url():
    """return the create mandate URL"""
    mollie = get_client()
    customer_response_dict = mollie.customers.create({
        'consumerName': 'le_mandate'
    })
    consumer_id = customer_response_dict['id']
    mandate_response_dict = mollie.customer_mandates.withParentId(consumer_id).create({
        'mandateReference': 'InshAllah',
        'method': 'creditcard',
        'redirectUrl': 'https://www.google.be'
    })
    return {
        'link': mandate_response_dict['links']['verificationUrl'],
        'consumer': consumer_id
    }

def get_mandate(consumer_id: str, mandate_id: str) -> dict:
    """return the mandate data for a given consumer_id and mandate_id"""
    mollie = get_client()
    return mollie.customer_mandates.withParentId(consumer_id).get(mandate_id)

def get_mandates(consumer_id):
    """return the mandate data for a given consumer_id and mandate_id"""
    mollie = get_client()
    mandates = mollie.customer_mandates.withParentId(consumer_id)
    return mandates

def get_payment_url(amount, reference):
    """return the payment URL for the provided amount"""
    mollie = get_client()
    payment = mollie.payments.create({
        'amount':      amount,
        'description': 'My first API payment',
        'redirectUrl': 'http://google.be',
        'webhookUrl': 'https://mollie.unleashed.be',
        'metadata': {
            'reference_number': reference
        }
    })
    payment = mollie.payments.get(payment['id'])
    print(payment)
    return payment['links']['paymentUrl']
