import hmac
import hashlib
import json

class RequestHelper:
    """
    The request helper supports the client with the creation of the hashes and cleaning up the form data.

    :param str public_key: The public key of the mosparo project
    :param str private_key: The private key of the mosparo project
    """

    public_key: str = ''
    private_key: str = ''

    def __init__(self, public_key: str, private_key: str) -> None:
        self.public_key = public_key
        self.private_key = private_key

    def create_hmac_hash(self, data: str) -> str:
        """
        Create the HMAC hash for the given data.

        :param str data: The data to create the HMAC hash for as a string
        :return: The HMAC hash
        :rtype: str
        """
        hmac_obj = hmac.new(key=self.private_key.encode(), msg=data.encode(), digestmod=hashlib.sha256)
        return hmac_obj.hexdigest()

    def prepare_form_data(self, form_data: dict) -> dict:
        """
        Prepares the form data to be sent to mosparo

        :param dict form_data: The submitted form data
        :return: The prepared form data
        :rtype: dict
        """
        form_data = self.cleanup_form_data(form_data)

        is_list = False
        data = {}
        if type(form_data) == list:
            form_data = enumerate(form_data)
            data = []
            is_list = True
        else:
            form_data = form_data.items()

        for key, val in form_data:
            if type(val) == dict or type(val) == list:
                data[key] = self.prepare_form_data(val)
            else:
                if type(val) == int or type(val) == float or type(val) == bool:
                    val = str(val)

                hash_obj = hashlib.sha256()
                hash_obj.update(val.encode())
                valHash = hash_obj.hexdigest()

                if is_list:
                    data.append(valHash)
                else:
                    data[key] = valHash

        if not is_list:
            data = dict(sorted(data.items()))

        return data

    def cleanup_form_data(self, form_data: dict) -> dict:
        """
        Cleanups the given form data

        :param dict form_data: The uncleaned form data
        :return: The cleaned form data
        :rtype: dict
        """
        if '_mosparo_submitToken' in form_data:
            form_data.pop('_mosparo_submitToken')

        if '_mosparo_validationToken' in form_data:
            form_data.pop('_mosparo_validationToken')

        is_list = False
        cleaned_data = {}
        if type(form_data) == list:
            form_data = enumerate(form_data)
            cleaned_data = []
            is_list = True
        else:
            form_data = form_data.items()

        for key, val in form_data:
            if type(key) == str and '[]' in key:
                pos = key.find('[]')
                key = key[0:pos]

            if type(val) == dict or type(val) == list:
                val = self.cleanup_form_data(val)
            elif type(val) == str:
                val = val.replace("\r\n", "\n")

            if is_list:
                cleaned_data.append(val)
            else:
                cleaned_data[key] = val

        if not is_list:
            cleaned_data = dict(sorted(cleaned_data.items()))

        return cleaned_data

    def create_form_data_hmac_hash(self, form_data: dict) -> str:
        """
        Dumps the form data to a JSON string and creates the HMAC hash for the JSON string

        :param dict form_data: The form data
        :return: The HMAC hash for the given form data
        :rtype: str
        """
        return self.create_hmac_hash(self.to_json(form_data))

    def to_json(self, form_data: dict) -> str:
        """
        Converts the given form data to a JSON string

        :param dict form_data: The form data
        :return: The JSON string for the given form data
        :rtype: str
        """
        json_string = json.dumps(form_data, separators=(',', ':'))

        return json_string.replace('[]', '{}')