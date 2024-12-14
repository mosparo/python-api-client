import json
import requests
from datetime import date

from .RequestHelper import RequestHelper
from .VerificationResult import VerificationResult
from .StatisticResult import StatisticResult
from .MosparoException import MosparoException

class Client:
    """
    The client is needed to communicate with the mosparo installation.

    :param str host: The host of the mosparo installation
    :param str public_key: The public key of the mosparo project
    :param str private_key: The private key of the mosparo project
    :param bool verify_ssl: Set to False, if the SSL certificate should not be verified.
    """

    host: str = ''
    public_key: str = ''
    private_key: str = ''
    verify_ssl: bool = True

    def __init__(self, host: str, public_key: str, private_key: str, verify_ssl=True):
        self.host = host
        self.public_key = public_key
        self.private_key = private_key
        self.verify_ssl = verify_ssl

    def verify_submission(self, form_data: dict, submit_token: str = None,
                          validation_token: str = None) -> VerificationResult:
        """
        Verifies the given form data with mosparo.

        :param dict form_data: The dictionary with all the form data.
        :param str submit_token: The submit token which was submitted with the form
        :param str validation_token: The validation token which was submitted with the form
        :return: A VerificationResult object
        :rtype: VerificationResult
        :raises MosparoException: if an error occurred
        """
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
                'Content-Type': 'application/json'
            },
            'data': request_data
        }

        res = self._send_request('POST', api_endpoint, data)

        is_submittable = False
        is_valid = False

        verified_fields = {}
        if 'verifiedFields' in res and res['verifiedFields']:
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

    def get_statistic_by_date(self, range: int = 0, start_date: date = None) -> StatisticResult:
        """
        Returns the statistic data, grouped by date.

        :param int range: Time range in seconds (will be rounded up to a full day since mosparo v1.1)
        :param datetime.date start_date: The start date from which the statistics are to be returned (requires mosparo v1.1)
        :return: A StatisticResult object
        :rtype: StatisticResult
        :raises MosparoException: if an error occurred or was returned from mosparo
        """
        request_helper = RequestHelper(self.public_key, self.private_key)

        api_endpoint = '/api/v1/statistic/by-date'
        query_data = {}
        if range > 0:
            query_data['range'] = range

        if start_date is not None:
            query_data['startDate'] = start_date.strftime('%Y-%m-%d')

        request_signature = request_helper.create_hmac_hash(api_endpoint + request_helper.to_json(query_data))

        data = {
            'auth': (self.public_key, request_signature),
            'headers': {
                'Accept': 'application/json'
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
        """
        Sends the request to mosparo and parses the response.

        :param str method: The method which is used (GET or POST)
        :param str uri: The URI of the API endpoint
        :param dict data: The data which needs to be sent to the API
        :return: The data which the API returned
        :rtype: dict
        :raises MosparoException: if an error occurred while sending the request to mosparo
        :raises MosparoException: if the response from mosparo is empty
        """
        req = None
        try:
            if method == 'GET':
                req = requests.get(self.host + uri,
                                   params=data['data'],
                                   auth=data['auth'],
                                   headers=data['headers'],
                                   verify=self.verify_ssl)
            elif method == 'POST':
                req = requests.post(self.host + uri,
                                    data=json.dumps(data['data']),
                                    auth=data['auth'],
                                    headers=data['headers'],
                                    verify=self.verify_ssl)
        except Exception as exc:
            raise MosparoException('An error occurred while sending the request to mosparo.') from exc

        if req and not req.text:
            raise MosparoException('Response from API invalid.')

        return req.json()
