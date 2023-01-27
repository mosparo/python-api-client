import json
import requests

from .RequestHelper import RequestHelper
from .VerificationResult import VerificationResult
from .StatisticResult import StatisticResult
from .MosparoException import MosparoException

class Client:
    host: str = ''
    public_key: str = ''
    private_key: str = ''
    clientArguments: dict = {}

    def __init__(self, host: str, public_key: str, private_key: str, client_arguments=None):
        self.host = host
        self.public_key = public_key
        self.private_key = private_key

        if client_arguments is not None:
            self.client_arguments = client_arguments

    def validate_submission(self, form_data: dict, submit_token: str = None,
                            validation_token: str = None) -> VerificationResult:
        request_helper = RequestHelper(self.public_key, self.private_key)

        if submit_token is None and '_mosparo_submitToken' in form_data:
            submit_token = form_data['_mosparo_submitToken']

        if validation_token is None and '_mosparo_validationToken' in form_data:
            validation_token = form_data['_mosparo_validationToken']

        if submit_token is None or validation_token is None:
            raise MosparoException('Submit or validation token not available.')

        form_data = request_helper.prepare_form_data(form_data)
        form_signature = request_helper.create_form_data_hmac_hash(form_data)

        validation_signature = request_helper.create_hmac_hash(validation_token)
        verification_signature = request_helper.create_hmac_hash(validation_signature + form_signature)

        api_endpoint = '/api/v1/verification/verify'
        request_data = {
            'submitToken': submit_token,
            'validationSignature': validation_signature,
            'formSignature': form_signature,
            'formData': form_data
        }
        request_signature = request_helper.create_hmac_hash(api_endpoint + request_helper.to_json(request_data))

        data = {
            'auth': (self.public_key, request_signature),
            'headers': {
                'Accept': 'application/json',
            },
            'data': request_data
        }

        res = self._send_request('POST', api_endpoint, data)

        is_submittable = False
        is_valid = False

        verified_fields = {}
        if 'verifiedFields' in res:
            verified_fields = res['verifiedFields']

        issues = []
        if 'issues' in res:
            issues = res['issues']

        if 'valid' in res \
                and res['valid'] \
                and 'verificationSignature' in res \
                and res['verificationSignature'] == verification_signature:
            is_submittable = True
            is_valid = True
        elif 'error' in res and res['error']:
            issues.append({'message': res['errorMessage']})

        return VerificationResult(
            is_submittable,
            is_valid,
            verified_fields,
            issues
        )

    def get_statistic_by_date(self, range: int = 0) -> StatisticResult:
        request_helper = RequestHelper(self.public_key, self.private_key)

        api_endpoint = '/api/v1/statistic/by-date'
        query_data = {}
        if range > 0:
            query_data['range'] = range

        request_signature = request_helper.create_hmac_hash(api_endpoint + request_helper.to_json(query_data))

        data = {
            'auth': (self.public_key, request_signature),
            'headers': {
                'Accept': 'application/json',
            },
            'data': query_data
        }

        res = self._send_request('GET', api_endpoint, data)

        if 'error' in res:
            error_message = 'An error occurred in the connection to mosparo.'
            if 'errorMessage' in res:
                error_message = res['errorMessage']

            raise MosparoException(error_message)

        return StatisticResult(
            res['data']['numberOfValidSubmissions'],
            res['data']['numberOfSpamSubmissions'],
            res['data']['numbersByDate']
        )

    def _send_request(self, method: str, uri: str, data: dict) -> dict:
        req = None
        try:
            if method == 'GET':
                req = requests.get(self.host + uri, params=data['data'], auth=data['auth'], headers=data['headers'])
            elif method == 'POST':
                req = requests.post(self.host + uri, data=json.dumps(data['data']), auth=data['auth'], headers=data['headers'])
        except Exception as exc:
            raise MosparoException('An error occurred while sending the request to mosparo.') from exc

        if req and not req.text:
            raise MosparoException('Response from API invalid.')

        return req.json()
