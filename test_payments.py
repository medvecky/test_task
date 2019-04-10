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
    invalid_tpp_redirect_uri_list = ["abc","ftp://localhost:80"]
    invalid_psu_ip_address = "a.a.a"
    invalid_instructed_amount_currency_list = [15,"GO","33","CAT"]
    invalid_instructed_amount_content_list = [-12,"-13","12.345.670","12,60"]
    invalid_debtor_account_iban_list = [1234567,"test","1234","abd123"]
    invalid_creditor_name_list = [123,"XXXXXXXXX",]

    def test_happy_paths_for_all_products(self):

        for product in self.products:
            r = self.v1_payments(product=product)
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

    def test_happy_paths_for_all_products_mondatory_params_only(self):

        for product in self.products:
            r = self.v1_payments(product=product,debtor_account_iban="",creditor_account_iban="", creditor_name="")
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

        r = self.v1_payments(product="")

        assert r.status_code == 404
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_product(self):

        r = self.v1_payments(product=self.invalid_product)

        assert r.status_code == 404
        assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_content_type(self):

        r = self.v1_payments(content_type="")

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_content_type(self):

        r = self.v1_payments(content_type=self.invalid_content_type)

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_x_request_id(self):

        r = self.v1_payments(x_request_id="")

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_x_request_id(self):

        r = self.v1_payments(x_request_id=self.invalid_x_request_id)

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_x_api_key(self):

        r = self.v1_payments(x_api_key="")

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_x_api_key(self):

        r = self.v1_payments(x_api_key=self.invalid_x_api_key)

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_tpp_redirect_uri(self):

        r = self.v1_payments(tpp_redirect_uri="")

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_tpp_redirect_uri(self):

        for invalid_tpp_redirect_uri in self.invalid_tpp_redirect_uri_list:
            r = self.v1_payments(tpp_redirect_uri=invalid_tpp_redirect_uri)

            if r.status_code != 400:
                print("invalid_tpp_redirect_uri: {}".format(invalid_tpp_redirect_uri))
            assert r.status_code == 400
            assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_psu_ip_address(self):

        r = self.v1_payments(psu_ip_address="")

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_psu_ip_address(self):

        r = self.v1_payments(psu_ip_address=self.invalid_psu_ip_address)

        if r.status_code != 400:
            print("invalid_psu_ip_address: {}".format(self.invalid_psu_ip_address))
        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_instructed_amount_currency(self):

        r = self.v1_payments(instructed_amount_currency="")

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_instructed_amount_currency(self):

        for invalid_currecy in self.invalid_instructed_amount_currency_list:
            r = self.v1_payments(instructed_amount_currency=invalid_currecy)
            if r.status_code != 400:
                print("invalid_currency: {}".format(invalid_currecy))
            assert r.status_code == 400
            assert r.json()["transactionStatus"] == "Rejected"

    def test_empty_instructed_amount_content(self):

        r = self.v1_payments(instructed_amount_content="")

        assert r.status_code == 400
        assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_instructed_amount_content(self):

        for invalid_instructed_amount_content in self.invalid_instructed_amount_content_list:
            r = self.v1_payments(instructed_amount_content=invalid_instructed_amount_content)

            if r.status_code != 400:
                print("invalid_instructed_amount_content: {}".format(invalid_instructed_amount_content))

            assert r.status_code == 400
            assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_debtor_account_iban(self):

        for invalid_debtor_account_iban in self.invalid_debtor_account_iban_list:
            r = self.v1_payments(debtor_account_iban=invalid_debtor_account_iban)

            if r.status_code != 400:
                print("invalid_debtor_account_iban: {}".format(invalid_debtor_account_iban))

            assert r.status_code == 400
            assert r.json()["transactionStatus"] == "Rejected"

    def test_invalid_creditor_name(self):

        for invalid_creditor_name in self.invalid_creditor_name_list:
            r = self.v1_payments(creditor_name=invalid_creditor_name)

            if r.status_code != 400:
                print("invalid_creditor_name: {}".format(invalid_creditor_name))

            assert r.status_code == 400
            assert r.json()["transactionStatus"] == "Rejected"


    def test_invalid_creditor_account_iban(self):

            for invalid_iban in self.invalid_debtor_account_iban_list:

                r = self.v1_payments(creditor_account_iban=invalid_iban)

                if r.status_code != 400:
                    print("invalid_iban: {}".format(invalid_iban))
                assert r.status_code == 400
                assert r.json()["transactionStatus"] == "Rejected"


    def v1_payments(
            self,
            product = products[0],
            content_type = valid_content_type,
            x_request_id = valid_x_request_id,
            x_api_key = valid_x_api_key,
            tpp_redirect_uri = valid_tpp_redirect_uri,
            psu_ip_address = valid_psu_ip_address,
            instructed_amount_currency = valid_instructed_amount_currency,
            instructed_amount_content = valid_instructed_amount_content,
            debtor_account_iban = valid_debtor_account_iban,
            creditor_name = valid_creditor_name,
            creditor_account_iban = valid_debtor_account_iban):
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
