import requests
import json


class TestPayments(object):
    products = ["sepa-credit-transfers", "instant-sepa-credit-transfers", "target-2-payments", "cross-border-credit-transfers"]
    valid_content_type = "application/json"
    valid_x_reaquest_id = "99391c7e-ad88-49ec-a2ad-99ddcb1f7721"
    valid_x_api_key = "8ef7a502-056d-4113-adba-ac7a3c2dce0a"
    valid_tpp_redirect_uri = "https://client.example.com/code_challenge_method='S2_56'"
    valid_psu_ip_address = "127.0.0.1"
    valid_instructed_amount_currency = "EUR"
    valid_instructed_amount_content = "123.50"
    valid_debtor_account_iban = "BANK95273278098985433"
    valid_creditor_name = "Merchant123"
    valid_creditor_account_iban = "DE02100100109307118603"


    def test_happy_paths_for_all_products(self):
        for product in self.products:
            url = "https://api.tieto.com/v1/payments/{}".format(product)
            headers = {
                "Content-Type": self.valid_content_type,
                "X-Request-ID": self.valid_x_reaquest_id,
                "X-API-Key": self.valid_x_api_key,
                "TPP-Redirect-URI": self.valid_tpp_redirect_uri,
                "PSU-IP-Address": self.valid_psu_ip_address
            }
            payload = {
                "instructedAmount": {"currency": self.valid_instructed_amount_currency, "content": self.valid_instructed_amount_content},
                "debtorAccount": {"iban": self.valid_debtor_account_iban},
                "creditorName": self.valid_creditor_name,
                "creditorAccount": {"iban": self.valid_debtor_account_iban},
                "remittanceInformationUnstructured": "Ref Number Merchant"
            }

            r = requests.post(url, data=json.dumps(payload), headers=headers)
            if r.status_code != 201:
                error_mesages = r.json()["tppMessages"][0]
                print("Transaction status: {}".format(r.json()["transactionStatus"]))
                print("ERROR CODE: {}\nCategory: {}\nCode: {}\nText: {}".format(r.status_code,error_mesages["category"],error_mesages["code"],error_mesages["text"]))
            assert r.status_code == 201