import rest_client


class TestGetPaymentsId(object):
    valid_x_request_id = "99391c7e-ad88-49ec-a2ad-99ddcb1f7721"
    valid_x_api_key = "8ef7a502-056d-4113-adba-ac7a3c2dce0a"
    valid_debtor_account_iban = "BANK95273278098985433"
    valid_creditor_name = "Merchant123"
    valid_creditor_account_iban = "DE02100100109307118603"
    valid_instructed_amount_currency = "EUR"
    valid_instructed_amount_content = "123.50"

    def test_mandatory_params_only(self):
        payment_id = self.get_valid_payments_id()
        r = self.get_v1_payments_payment_id(payment_id=payment_id)
        assert r.status_code == 200
        assert r.json()["transactionStatus"] == "RCVD"
        assert r.json()["_links"]["self"]["href"] == "/v1/payments/{}".format(payment_id)
        assert r.json()["instructedAmount"]["currency"] == self.valid_instructed_amount_currency
        assert r.json()["instructedAmount"]["content"] == self.valid_instructed_amount_content
        assert r.json()["remittanceInformationUnstructured"] == "Ref Number Merchant"

    def test_all_params(self):
        payment_id = self.get_valid_payments_id(all_params=True)
        r = self.get_v1_payments_payment_id(payment_id=payment_id)
        assert r.status_code == 200
        assert r.json()["transactionStatus"] == "RCVD"
        assert r.json()["_links"]["self"]["href"] == "/v1/payments/{}".format(payment_id)
        assert r.json()["instructedAmount"]["currency"] == self.valid_instructed_amount_currency
        assert r.json()["instructedAmount"]["content"] == self.valid_instructed_amount_content
        assert r.json()["remittanceInformationUnstructured"] == "Ref Number Merchant"
        assert r.json()["debtorAccount"]["iban"] == self.valid_debtor_account_iban
        assert r.json()["creditorName"] == self.valid_creditor_name
        assert r.json()["creditorAccount"]["iban"] == "DE02100100109307118603"

    def test_empty_payment_id(self):
        r = self.get_v1_payments_payment_id(payment_id="")
        assert r.status_code == 404
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "RESOURCE_UNKNOWN"

    def test_invalid_payment_id(self):
        r = self.get_v1_payments_payment_id(payment_id="abc123")
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"

    def test_empty_x_request_id(self):
        payment_id = self.get_valid_payments_id()
        r = self.get_v1_payments_payment_id(payment_id=payment_id, x_request_id="")
        print(r.json())
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"

    def test_invalid_x_request_id(self):
        payment_id = self.get_valid_payments_id()
        r = self.get_v1_payments_payment_id(payment_id=payment_id, x_request_id="123abc")
        print(r.json())
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"

    def test_empty_x_api_key(self):
        payment_id = self.get_valid_payments_id()
        r = self.get_v1_payments_payment_id(payment_id=payment_id, x_api_key="")
        print(r.json())
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"

    def test_invalid_x_api_key(self):
        payment_id = self.get_valid_payments_id()
        r = self.get_v1_payments_payment_id(payment_id=payment_id, x_api_key="abc123")
        print(r.json())
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"


    def get_v1_payments_payment_id(
            self,
            payment_id,
            x_request_id=valid_x_request_id,
            x_api_key=valid_x_api_key):

        return rest_client.get_v1_payments_payment_id(payment_id, x_request_id, x_api_key)

    def get_valid_payments_id(self, all_params=False):
        product = "sepa-credit-transfers"
        valid_content_type = "application/json"
        valid_tpp_redirect_uri = "https://client.example.com/code_challenge_method='S2_56'"
        valid_psu_ip_address = "127.0.0.1"

        if all_params:
            result = rest_client.post_v1_payments(
                product,
                valid_content_type,
                self.valid_x_request_id,
                self.valid_x_api_key,
                valid_tpp_redirect_uri,
                valid_psu_ip_address,
                self.valid_instructed_amount_currency,
                self.valid_instructed_amount_content,
                self.valid_debtor_account_iban,
                self.valid_creditor_name,
                self.valid_creditor_account_iban)
        else:
            result = rest_client.post_v1_payments(
                product,
                valid_content_type,
                self.valid_x_request_id,
                self.valid_x_api_key,
                valid_tpp_redirect_uri,
                valid_psu_ip_address,
                self.valid_instructed_amount_currency,
                self.valid_instructed_amount_content,
                "",
                "",
                "")
        return result.json()["paymentId"]
