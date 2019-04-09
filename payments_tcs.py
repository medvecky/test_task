import requests
import json


class TestPayments(object):

    def test_one(self):
        url = "https://api.tieto.com/v1/payments/instant-sepa-credit-transfers"
        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": "99391c7e-ad88-49ec-a2ad-99ddcb1f7721",
            "X-API-Key": "8ef7a502-056d-4113-adba-ac7a3c2dce0a",
            "TPP-Redirect-URI": "https://client.example.com/code_challenge_method='S2_56'",
            "PSU-IP-Address": "127.0.0.1"
        }
        payload = {
            "instructedAmount": {"currency": "EUR", "content": "123.50"},
            "debtorAccount": {"iban": "BANK95273278098985433"},
            "creditorName": "Merchant123",
            "creditorAccount": {"iban": "DE02100100109307118603"},
            "remittanceInformationUnstructured": "Ref Number Merchant"
        }

        r = requests.post(url, data=json.dumps(payload), headers=headers)
        print("request")
        print(r.request.body)
        print("response")
        print(r.json())
        print(r.status_code)
        assert False

    # def test_two(self):
    #     x = "hello"
    #     assert hasattr(x, 'check')
