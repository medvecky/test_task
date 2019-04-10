import json
import rest_client

class TestGetPaymentsId(object):
    valid_x_request_id = "99391c7e-ad88-49ec-a2ad-99ddcb1f7721"
    valid_x_api_key = "8ef7a502-056d-4113-adba-ac7a3c2dce0a"

    def test_payment_id(self):
        r = self.get_v1_payments_payment_id()
        print(r)
        print(r.json())
        assert False

    def get_v1_payments_payment_id(
        self,
        x_request_id=valid_x_request_id,
        x_api_key=valid_x_api_key):

        payment_id = self.get_payments_id()

        return rest_client.get_v1_payments_payment_id(payment_id, x_request_id, x_api_key)

    def get_payments_id(self):
        product = "sepa-credit-transfers"
        valid_content_type = "application/json"
        valid_tpp_redirect_uri = "https://client.example.com/code_challenge_method='S2_56'"
        valid_psu_ip_address = "127.0.0.1"
        valid_instructed_amount_currency = "EUR"
        valid_instructed_amount_content = "123.50"
        result = rest_client.post_v1_payments(
            product,
            valid_content_type,
            self.valid_x_request_id,
            self.valid_x_api_key,
            valid_tpp_redirect_uri,
            valid_psu_ip_address,
            valid_instructed_amount_currency,
            valid_instructed_amount_content,
            "",
            "",
            "")
        return result.json()["paymentId"]