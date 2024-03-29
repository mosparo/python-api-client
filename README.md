&nbsp;
<p align="center">
    <img src="https://github.com/mosparo/mosparo/blob/master/assets/images/mosparo-logo.svg?raw=true" alt="mosparo logo contains a bird with the name Mo and the mosparo text"/>
</p>

<h1 align="center">
    Python API Client
</h1>
<p align="center">
    This library offers the API client to communicate with mosparo to verify a submission.
</p>

-----

## Description
This Python library lets you connect to a mosparo installation and verify the submitted data.

## Installation

### Install using pip

Install this library by using pip:

```text
pip install mosparo-api-client
```

### Build from source

You need the module `build` to build the module from source.

1. Clone the repository
2. Build the package
```commandline
python -m build
```
3. Install the package
```commandline
pip install dist/mosparo_api_client-1.0.0-py3-none-any.whl
```

## Usage
1. Create a project in your mosparo installation
2. Include the mosparo script in your form
```html
<div id="mosparo-box"></div>

<script src="https://[URL]/build/mosparo-frontend.js" defer></script>
<script>
    var m;
    window.onload = function(){
        m = new mosparo('mosparo-box', 'https://[URL]', '[UUID]', '[PUBLIC_KEY]', {loadCssResource: true});
    };
</script>
```
3. Include the library in your project
```text
pip install mosparo-api-client
```
4. After the form is submitted, verify the data before processing it

```python
from mosparo_api_client import Client

api_client = Client(host, public_key, private_key)

your_post_data = {}  # This needs to be filled with the post data

mosparo_submit_token = your_post_data['_mosparo_submitToken']
mosparo_validation_token = your_post_data['_mosparo_validationToken']

result = api_client.verify_submission(your_post_data, mosparo_submit_token, mosparo_validation_token)

if result.is_submittable():
    # Send the email or process the data
    pass
else:
    # Show error message
    pass
```

## API Documentation

### Client

#### Client initialization

Create a new client object to use the API client.

```python
from mosparo_api_client import Client

api_client = Client(host, public_key, private_key, verify_ssl)
```

| Parameter   | Type | Description                                                 |
|-------------|------|-------------------------------------------------------------|
| host        | str  | The host of the mosparo installation                        |
| public_key  | str  | The public key of the mosparo project                       |
| private_key | str  | The private key of the mosparo project                      |
| verify_ssl  | bool | Set to False if the SSL certificate should not be verified. |

#### Verify form data

To verify the form data, call `verify_submission` with the form data in an array and the submit and validation tokens, which mosparo generated on the form initialization and the form data validation. The method will return a `VerificationResult` object.

```python
result = api_client.verify_submission(form_data, mosparo_submit_token, mosparo_validation_token)
```

| Parameter                | Type  | Description                                                                                                  |
|--------------------------|-------|--------------------------------------------------------------------------------------------------------------|
| form_data                | dict  | The dictionary with all the submitted form data.                                                             |
| mosparo_submit_token     | str   | The submit token which was generated by mosparo and submitted with the form data                             |
| mosparo_validation_token | str   | The validation token which mosparo generated after the validation and which was submitted with the form data |

#### Bypass protection

After the verification of the submission by mosparo, you have to verify that all required fields and all possible fields were verified correctly. For this you have to check that all your required fields are set in the result ([get_verified_fields](#get_verified_fields-list-see-constants)).

See [Bypass protection](https://documentation.mosparo.io/docs/integration/bypass_protection) in the mosparo documentation.

##### Example

```python
verified_fields = result.get_verified_fields()
required_field_difference = set(list_of_required_field_names) - set(verified_fields.keys())
verifiable_field_difference = set(list_of_verifiable_field_names) - set(verified_fields.keys())

# The submission is only valid if all required and verifiable fields got verified
if result.is_submittable() and not required_field_difference and not verifiable_field_difference:
    print('All good, send email')
else:
    raise Exception('mosparo did not verify all required fields. This submission looks like spam.')
```

`list_of_required_field_names` and `list_of_verifiable_field_names` contain the names of all required or verifiable fields. Verifiable fields are fields that mosparo can validate and verify (for example, text fields). A checkbox field, for example, will not be validated and verified by mosparo. 

### VerificationResult

#### Constants

- `FIELD_NOT_VERIFIED`: 'not-verified'
- `FIELD_VALID`: 'valid'
- `FIELD_INVALID`: 'invalid'

#### `is_submittable()`: bool

Returns `True` if the form is submittable. This means that the verification was successful and the 
form data are valid.

#### `is_valid()`: bool

Returns `True` if mosparo determined the form as valid. The difference to `is_submittable()` is, that this
is the original result from mosparo, while `is_submittable()` also checks if the verification was done correctly.

#### `get_verified_fields()`: list (see [Constants](#constants))

Returns an array with all verified field keys.

#### `get_verified_field(key)`: string (see [Constants](#constants))

Returns the verification status of one field.

#### `has_issues()`: bool

Returns `True` if there were verification issues.

#### `get_issues()`: list

Returns an array with all verification issues.

#### Get the statistic data by date

To get the statistic data grouped by date, call `get_statistic_by_date`. The method accepts a time range in seconds for which the data should be returned (last x seconds) or the start date from which the data should be returned. The method will return a `StatisticResult` object.

```python
result = api_client.get_statistic_by_date(range, start_date)
```

| Parameter  | Type          | Description                                                                         |
|------------|---------------|-------------------------------------------------------------------------------------|
| range      | int           | Time range in seconds (will be rounded up to a full day since mosparo v1.1)         |
| start_date | datetime.date | The start date from which the statistics are to be returned (requires mosparo v1.1) |

### StatisticResult

#### `get_number_of_valid_submissions()`: int

Return the number of valid submissions in the requested time range.

#### `get_number_of_spam_submissions()`: int

Return the number of spam submissions in the requested time range.

#### `get_numbers_by_date()`: dict

Return the numbers grouped by date.

## License

mosparo Python API Client is open-sourced software licensed under the [MIT License](https://opensource.org/licenses/MIT).
Please see the [LICENSE](LICENSE) file for the full license.