import hmac
import hashlib
import json

class RequestHelper:
    public_key: str = ''
    private_key: str = ''

    def __init__(self, public_key: str, private_key: str) -> None:
        self.public_key = public_key
        self.private_key = private_key

    def create_hmac_hash(self, data: str) -> str:
        hmac_obj = hmac.new(key=self.private_key.encode(), msg=data.encode(), digestmod=hashlib.sha256)
        return hmac_obj.hexdigest()

    def prepare_form_data(self, form_data: dict) -> dict:
        form_data = self.cleanup_form_data(form_data)

        is_list = False
        data = {}
        if type(form_data) == dict:
            form_data = form_data.items()
        elif type(form_data) == list:
            form_data = enumerate(form_data)
            data = []
            is_list = True

        for key, val in form_data:
            if type(val) == dict or type(val) == list:
                data[key] = self.prepare_form_data(val)
            else:
                if type(val) == int or type(val) == float:
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
        if '_mosparo_submitToken' in form_data:
            form_data.pop('_mosparo_submitToken')

        if '_mosparo_validationToken' in form_data:
            form_data.pop('_mosparo_validationToken')

        is_list = False
        cleaned_data = {}
        if type(form_data) == dict:
            form_data = form_data.items()
        elif type(form_data) == list:
            form_data = enumerate(form_data)
            cleaned_data = []
            is_list = True

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
        return self.create_hmac_hash(self.to_json(form_data))

    def to_json(self, form_data: dict) -> str:
        json_string = json.dumps(form_data)

        return json_string.replace('[]', '{}')