import requests
import json


class TestPayments(object):

    def test_one(self):
        url = "https://api.tieto.com/v1/payments/sepa-credit-transfers"
        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": "99391c7e-ad88-49ec-a2ad-99ddcb1f7721",
            "X-API-Key": "8ef7a502-056d-4113-adba-ac7a3c2dce0a"
        }
        payload = {
            "instructedAmount": {"currency": "EUR", "amount": "123.50"},
            "debtorAccount": {"iban": "DE40100100103307118608"},
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
