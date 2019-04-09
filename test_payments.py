import requests
import json


class TestPayments(object):
    products = ["sepa-credit-transfers", "instant-sepa-credit-transfers", "target-2-payments",
                "cross-border-credit-transfers"]
    valid_content_type = "application/json"
    valid_x_request_id = "99391c7e-ad88-49ec-a2ad-99ddcb1f7721"
    valid_x_api_key = "8ef7a502-056d-4113-adba-ac7a3c2dce0a"
    valid_tpp_redirect_uri = "https://client.example.com/code_challenge_method='S2_56'"
    valid_psu_ip_address = "127.0.0.1"
    valid_instructed_amount_currency = "EUR"
    valid_instructed_amount_content = "123.50"
    valid_debtor_account_iban = "BANK95273278098985433"
    valid_creditor_name = "Merchant123"
    valid_creditor_account_iban = "DE02100100109307118603"

    invalid_product = "test_product"
    invalid_content_type = "application/x-www-form-urlencoded"
    invalid_x_request_id = "abc123"
    invalid_x_api_key = "abc123"

    def test_happy_paths_for_all_products(self):
        for product in self.products:
            r = self.v1_payments(
                product,
                self.valid_content_type,
                self.valid_x_request_id,
                self.valid_x_api_key,
                self.valid_tpp_redirect_uri,
                self.valid_psu_ip_address,
                self.valid_instructed_amount_currency,
                self.valid_instructed_amount_content,
                self.valid_debtor_account_iban,
                self.valid_creditor_name,
                self.valid_creditor_account_iban)
            if r.status_code != 201:
                error_messages = r.json()["tppMessages"][0]
                print("Transaction status: {}".format(r.json()["transactionStatus"]))
                print(
                    "ERROR CODE: {}\nCategory: {}\nCode: {}\nText: {}".format(r.status_code, error_messages["category"],
                                                                              error_messages["code"],
                                                                              error_messages["text"]))
            assert r.status_code == 201
            assert r.json()["transactionStatus"] == "RCVD"
            assert r.json()["paymentId"] != ""
            assert r.json()["_links"]["scaRedirect"]["href"] != ""

    def test_empty_product(self):
        r = self.v1_payments(
            "",
            self.valid_content_type,
            self.valid_x_request_id,
            self.valid_x_api_key,
            self.valid_tpp_redirect_uri,
            self.valid_psu_ip_address,
            self.valid_instructed_amount_currency,
            self.valid_instructed_amount_content,
            self.valid_debtor_account_iban,
            self.valid_creditor_name,
            self.valid_creditor_account_iban)

        assert r.status_code == 404
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_product(self):
        r = self.v1_payments(
            self.invalid_product,
            self.valid_content_type,
            self.valid_x_request_id,
            self.valid_x_api_key,
            self.valid_tpp_redirect_uri,
            self.valid_psu_ip_address,
            self.valid_instructed_amount_currency,
            self.valid_instructed_amount_content,
            self.valid_debtor_account_iban,
            self.valid_creditor_name,
            self.valid_creditor_account_iban)

        assert r.status_code == 404
        assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_content_type(self):
        r = self.v1_payments(
            self.products[0],
            "",
            self.valid_x_request_id,
            self.valid_x_api_key,
            self.valid_tpp_redirect_uri,
            self.valid_psu_ip_address,
            self.valid_instructed_amount_currency,
            self.valid_instructed_amount_content,
            self.valid_debtor_account_iban,
            self.valid_creditor_name,
            self.valid_creditor_account_iban)

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_content_type(self):
        r = self.v1_payments(
            self.products[0],
            self.invalid_content_type,
            self.valid_x_request_id,
            self.valid_x_api_key,
            self.valid_tpp_redirect_uri,
            self.valid_psu_ip_address,
            self.valid_instructed_amount_currency,
            self.valid_instructed_amount_content,
            self.valid_debtor_account_iban,
            self.valid_creditor_name,
            self.valid_creditor_account_iban)

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_x_request_id(self):
        r = self.v1_payments(
            self.products[0],
            self.valid_content_type,
            "",
            self.valid_x_api_key,
            self.valid_tpp_redirect_uri,
            self.valid_psu_ip_address,
            self.valid_instructed_amount_currency,
            self.valid_instructed_amount_content,
            self.valid_debtor_account_iban,
            self.valid_creditor_name,
            self.valid_creditor_account_iban)

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_x_request_id(self):
        r = self.v1_payments(
            self.products[0],
            self.valid_content_type,
            self.invalid_x_request_id,
            self.valid_x_api_key,
            self.valid_tpp_redirect_uri,
            self.valid_psu_ip_address,
            self.valid_instructed_amount_currency,
            self.valid_instructed_amount_content,
            self.valid_debtor_account_iban,
            self.valid_creditor_name,
            self.valid_creditor_account_iban)

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_x_api_key(self):
        r = self.v1_payments(
            self.products[0],
            self.valid_content_type,
            self.valid_x_request_id,
            "",
            self.valid_tpp_redirect_uri,
            self.valid_psu_ip_address,
            self.valid_instructed_amount_currency,
            self.valid_instructed_amount_content,
            self.valid_debtor_account_iban,
            self.valid_creditor_name,
            self.valid_creditor_account_iban)

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_x_api_key(self):
        r = self.v1_payments(
            self.products[0],
            self.valid_content_type,
            self.valid_x_request_id,
            self.invalid_x_api_key,
            self.valid_tpp_redirect_uri,
            self.valid_psu_ip_address,
            self.valid_instructed_amount_currency,
            self.valid_instructed_amount_content,
            self.valid_debtor_account_iban,
            self.valid_creditor_name,
            self.valid_creditor_account_iban)

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"


    def v1_payments(
            self,
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
