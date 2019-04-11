import rest_client

class TestGetPaymentIdStatus(object):
    valid_x_request_id = "99391c7e-ad88-49ec-a2ad-99ddcb1f7721"
    valid_x_api_key = "8ef7a502-056d-4113-adba-ac7a3c2dce0a"
    
    def test_happy_path(self):
        payment_id, autorization_url = self.get_valid_payments_data()
        r = self.get_v1_payments_payment_id_status(payment_id=payment_id)
        assert r.status_code == 200
        assert r.json()["transactionStatus"] == "RCVD"
        assert autorization_url != ""

    def test_empty_payment_id(self):
        r = self.get_v1_payments_payment_id_status(payment_id="")
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"

    def test_invalid_payment_id(self):
        r = self.get_v1_payments_payment_id_status(payment_id="abc123")
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"

    def test_empty_x_request_id(self):
        payment_id, autorization_url = self.get_valid_payments_data()
        r = self.get_v1_payments_payment_id_status(payment_id=payment_id,x_request_id="")        
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"

    def test_invalid_x_request_id(self):
        payment_id, autorization_url = self.get_valid_payments_data()
        r = self.get_v1_payments_payment_id_status(payment_id=payment_id,x_request_id="abc123")        
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"  

    def test_empty_x_api_key(self):
        payment_id, autorization_url = self.get_valid_payments_data()
        r = self.get_v1_payments_payment_id_status(payment_id=payment_id,x_api_key="")        
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"  

    def test_invalid_x_api_key(self):
        payment_id, autorization_url = self.get_valid_payments_data()
        r = self.get_v1_payments_payment_id_status(payment_id=payment_id,x_api_key="abc123")        
        assert r.status_code == 400
        assert r.json()["tppMessages"][0]["category"] == "ERROR"
        assert r.json()["tppMessages"][0]["code"] == "FORMAT_ERROR"      


    def get_v1_payments_payment_id_status(
        self,
        payment_id,
        x_request_id=valid_x_request_id,
        x_api_key=valid_x_api_key):
        
        return rest_client.get_v1_payments_payment_id_status(payment_id, x_request_id, x_api_key)
    
    def get_valid_payments_data(self):
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
        print(result.json())
        return result.json()["paymentId"], result.json()["_links"]["scaRedirect"]["href"]