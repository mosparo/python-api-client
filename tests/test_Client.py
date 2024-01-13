import json
from datetime import date

import pytest
from mosparo_api_client import Client, RequestHelper, VerificationResult, StatisticResult, MosparoException

def test_verify_submission_without_tokens():
    api_client = Client('http://test.local', 'testPublicKey', 'testPrivateKey')

    with pytest.raises(MosparoException) as exc:
        result = api_client.verify_submission({'name': 'John Example'})

    assert 'Submit or validation token not available.' in str(exc.value)

def test_verify_submission_without_validation_tokens():
    api_client = Client('http://test.local', 'testPublicKey', 'testPrivateKey')

    with pytest.raises(MosparoException) as exc:
        result = api_client.verify_submission({'name': 'John Example', '_mosparo_submitToken': 'submitToken'})

    assert 'Submit or validation token not available.' in str(exc.value)

def test_verify_submission_form_tokens_empty_response(requests_mock):
    requests_mock.post('http://test.local/api/v1/verification/verify', text='')

    api_client = Client('http://test.local', 'testPublicKey', 'testPrivateKey')

    with pytest.raises(MosparoException) as exc:
        result = api_client.verify_submission({
            'name': 'John Example',
            '_mosparo_submitToken': 'submitToken',
            '_mosparo_validationToken': 'validationToken'
        })

    assert 'Response from API invalid.' in str(exc.value)

def test_verify_submission_tokens_as_argument_empty_response(requests_mock):
    requests_mock.post('http://test.local/api/v1/verification/verify', text='')

    api_client = Client('http://test.local', 'testPublicKey', 'testPrivateKey')

    with pytest.raises(MosparoException) as exc:
        result = api_client.verify_submission({
            'name': 'John Example'
        }, 'submitToken', 'validationToken')

    assert 'Response from API invalid.' in str(exc.value)

def test_verify_submission_connection_error(requests_mock):
    requests_mock.post('http://test.local/api/v1/verification/verify', exc='Connection failed')

    api_client = Client('http://test.local', 'testPublicKey', 'testPrivateKey')

    with pytest.raises(MosparoException) as exc:
        result = api_client.verify_submission({
            'name': 'John Example'
        }, 'submitToken', 'validationToken')

    assert 'An error occurred while sending the request to mosparo.' in str(exc.value)

def test_verify_submission_is_valid(requests_mock):
    public_key = 'testPublicKey'
    private_key = 'testPrivateKey'
    submit_token = 'submitToken'
    validation_token = 'validationToken'
    form_data = {'name': 'John Example'}

    request_helper = RequestHelper(public_key, private_key)

    prepared_form_data = request_helper.prepare_form_data(form_data)
    form_signature = request_helper.create_form_data_hmac_hash(prepared_form_data)

    validation_signature = request_helper.create_hmac_hash(validation_token)
    verification_signature = request_helper.create_hmac_hash(validation_signature + form_signature)

    requests_mock.post('http://test.local/api/v1/verification/verify', json={
        'valid': True,
        'verificationSignature': verification_signature,
        'verifiedFields': { 'name': VerificationResult.FIELD_VALID },
        'issues': []
    }, status_code=200)

    api_client = Client('http://test.local', public_key, private_key)

    result = api_client.verify_submission(form_data, submit_token, validation_token)

    assert type(result) == VerificationResult
    assert requests_mock.call_count == 1
    assert result.is_submittable() is True
    assert result.is_valid() is True
    assert result.get_verified_field('name') == VerificationResult.FIELD_VALID
    assert result.has_issues() is False

    request_data = json.loads(requests_mock.last_request.text)

    assert request_data['formData'] == prepared_form_data
    assert request_data['submitToken'] == submit_token
    assert request_data['validationSignature'] == validation_signature
    assert request_data['formSignature'] == form_signature

def test_verify_submission_is_not_valid(requests_mock):
    public_key = 'testPublicKey'
    private_key = 'testPrivateKey'
    submit_token = 'submitToken'
    validation_token = 'validationToken'
    form_data = {'name': 'John Example'}

    request_helper = RequestHelper(public_key, private_key)

    prepared_form_data = request_helper.prepare_form_data(form_data)
    form_signature = request_helper.create_form_data_hmac_hash(prepared_form_data)

    validation_signature = request_helper.create_hmac_hash(validation_token)

    requests_mock.post('http://test.local/api/v1/verification/verify', json={
        'error': True,
        'errorMessage': 'Validation failed.'
    }, status_code=200)

    api_client = Client('http://test.local', public_key, private_key)

    result = api_client.verify_submission(form_data, submit_token, validation_token)

    assert type(result) == VerificationResult
    assert requests_mock.call_count == 1
    assert result.is_submittable() is False
    assert result.is_valid() is False
    assert result.has_issues() is True
    assert result.get_issues()[0]['message'] == 'Validation failed.'

    request_data = json.loads(requests_mock.last_request.text)

    assert request_data['formData'] == prepared_form_data
    assert request_data['submitToken'] == submit_token
    assert request_data['validationSignature'] == validation_signature
    assert request_data['formSignature'] == form_signature

def test_get_statistic_by_date_without_range(requests_mock):
    public_key = 'testPublicKey'
    private_key = 'testPrivateKey'
    numbers_by_date = {
        '2021-04-29': {
            'numberOfValidSubmissions': 0,
            'numberOfSpamSubmissions': 10
        }
    }

    requests_mock.get('http://test.local/api/v1/statistic/by-date', json={
        'result': True,
        'data': {
            'numberOfValidSubmissions': 0,
            'numberOfSpamSubmissions': 10,
            'numbersByDate': numbers_by_date
        }
    }, status_code=200)

    api_client = Client('http://test.local', public_key, private_key)

    result = api_client.get_statistic_by_date()

    assert type(result) == StatisticResult
    assert requests_mock.call_count == 1

    assert result.get_number_of_valid_submissions() == 0
    assert result.get_number_of_spam_submissions() == 10
    assert numbers_by_date == result.get_numbers_by_date()

def test_get_statistic_by_date_with_range(requests_mock):
    public_key = 'testPublicKey'
    private_key = 'testPrivateKey'
    numbers_by_date = {
        '2021-04-29': {
            'numberOfValidSubmissions': 2,
            'numberOfSpamSubmissions': 5
        }
    }

    requests_mock.get('http://test.local/api/v1/statistic/by-date', json={
        'result': True,
        'data': {
            'numberOfValidSubmissions': 2,
            'numberOfSpamSubmissions': 5,
            'numbersByDate': numbers_by_date
        }
    }, status_code=200)

    api_client = Client('http://test.local', public_key, private_key)

    result = api_client.get_statistic_by_date(3600)

    assert type(result) == StatisticResult
    assert requests_mock.call_count == 1
    assert requests_mock.last_request.qs == {'range': ['3600']}

    assert result.get_number_of_valid_submissions() == 2
    assert result.get_number_of_spam_submissions() == 5
    assert numbers_by_date == result.get_numbers_by_date()

def test_get_statistic_by_date_with_start_date(requests_mock):
    public_key = 'testPublicKey'
    private_key = 'testPrivateKey'
    numbers_by_date = {
        '2021-04-29': {
            'numberOfValidSubmissions': 2,
            'numberOfSpamSubmissions': 5
        }
    }

    requests_mock.get('http://test.local/api/v1/statistic/by-date', json={
        'result': True,
        'data': {
            'numberOfValidSubmissions': 2,
            'numberOfSpamSubmissions': 5,
            'numbersByDate': numbers_by_date
        }
    }, status_code=200)

    api_client = Client('http://test.local', public_key, private_key)

    start_date = date.fromisoformat('2024-01-01')
    result = api_client.get_statistic_by_date(0, start_date)

    print(requests_mock.last_request.qs)
    assert type(result) == StatisticResult
    assert requests_mock.call_count == 1
    assert requests_mock.last_request.qs == {'startdate': ['2024-01-01']} # Test this with lowercase characters only because of https://requests-mock.readthedocs.io/en/latest/knownissues.html#case-insensitivity

    assert result.get_number_of_valid_submissions() == 2
    assert result.get_number_of_spam_submissions() == 5
    assert numbers_by_date == result.get_numbers_by_date()

def test_get_statistic_by_date_returns_error(requests_mock):
    public_key = 'testPublicKey'
    private_key = 'testPrivateKey'

    requests_mock.get('http://test.local/api/v1/statistic/by-date', json={
        'error': True,
        'errorMessage': 'Request not valid'
    }, status_code=200)

    api_client = Client('http://test.local', public_key, private_key)

    with pytest.raises(MosparoException) as exc:
        result = api_client.get_statistic_by_date()

    assert 'Request not valid' in str(exc.value)


