# Test task 
### Example of using pytest and requests for testing REST API app

## Installation
* Clone project.
* In project directory execute:
```
pip3 install -r requirements.txt
```
## Test run
* For running all tests
```
pytest
```

* For particular test 
```
putest <file_with_test_class.py>
```
* For html report generation 
```
pytest --html=report.html
```

or
```
pytest --html=report.html --self-contained-html
```

## Description 

### rest_api_client.py 

Contains realisations of REST API calls which used in tests

### test_post_payments.py

Contains test cases set for 
```
POST https://api.tieto.com/v1/payments
```
### test_get_payments_id.py

Contains test cases set for 
```
GET https://api.tieto.com/v1/payments/{paymentId}
```
### test_post_payments_id_status.py

Contains test cases set for 
```
GET https://api.tieto.com/v1/payments/{paymentId}/status
```
Tests mainly focused on parameters verification. 

For more complicated test cases creation need more information about system logic in common. 
