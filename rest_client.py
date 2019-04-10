import requests
import json


def post_v1_payments(
        product,
        content_type,
        x_request_id,
        x_api_key,
        tpp_redirect_uri,
        psu_ip_address,
        instructed_amount_currency,
        instructed_amount_content,
        debtor_account_iban,
        creditor_name,
        creditor_account_iban):
    url = "https://api.tieto.com/v1/payments/{}".format(product)
    headers = {
        "Content-Type": content_type,
        "X-Request-ID": x_request_id,
        "X-API-Key": x_api_key,
        "TPP-Redirect-URI": tpp_redirect_uri,
        "PSU-IP-Address": psu_ip_address
    }
    payload = {
        "instructedAmount": {"currency": instructed_amount_currency,
                             "content": instructed_amount_content},
        "debtorAccount": {"iban": debtor_account_iban},
        "creditorName": creditor_name,
        "creditorAccount": {"iban": creditor_account_iban},
        "remittanceInformationUnstructured": "Ref Number Merchant"
    }

    return requests.post(url, data=json.dumps(payload), headers=headers)


def get_v1_payments_payment_id(payment_id, x_request_id, x_api_key):
    url = "https://api.tieto.com/v1/payments/{}".format(payment_id)
    headers = {
        "X-Request-ID": x_request_id,
        "X-API-Key": x_api_key
    }

    return requests.get(url, headers=headers)
