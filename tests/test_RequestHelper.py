from mosparo_api_client import RequestHelper

publicKey = 'publicKey'
privateKey = 'privateKey'

def test_create_hmac_hash():
    reqHelp = RequestHelper(publicKey, privateKey)

    data = 'testData'

    assert '0646b5f2e09db205a8b3eb0e7429645561a1b9fdff1fcdb1fed9cd585108d850' == reqHelp.create_hmac_hash(data)

def test_prepare_form_data():
    reqHelp = RequestHelper(publicKey, privateKey)

    data = {
        'name': 'Test Tester',
        'address': {
            'street': 'Teststreet',
            'number': 123
        },
        'email[]': [
            'test@example.com',
            'test2@example.com'
        ],
        'data': {}
    }

    targetArray = {
        'address': {
            'street': 'cc0bdb0377d3ba87046028784e8a4319972a7c9df31c645e80e14e8dd8735b6b',
            'number': 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
        },
        'name': '153590093b8c278bb7e1fef026d8a59b9ba02701d1e0a66beac0938476f2a812',
        'email': [
            '973dfe463ec85785f5f95af5ba3906eedb2d931c24e69824a89ea65dba4e813b',
            '8cc62c145cd0c6dc444168eaeb1b61b351f9b1809a579cc9b4c9e9d7213a39ee'
        ],
        'data': {}
    }

    assert targetArray == reqHelp.prepare_form_data(data)

def test_cleanup_form_data():
    reqHelp = RequestHelper(publicKey, privateKey)

    data = {
        '_mosparo_submitToken': 'submitToken',
        '_mosparo_validationToken': 'validationToken',
        'name': 'Test Tester',
        'address': {
            'street': "Teststreet\r\nTest\r\nStreet",
            'number': 123
        },
        'valid': False,
        'email[]': [
            'test@example.com',
            'test2@example.com'
        ],
        'data': {}
    }

    targetArray = {
        'address': {
            'number': 123,
            'street': "Teststreet\nTest\nStreet"
        },
        'data': {},
        'email': [
            'test@example.com',
            'test2@example.com'
        ],
        'name': 'Test Tester',
        'valid': False
    }

    assert targetArray == reqHelp.cleanup_form_data(data)

def test_to_json():
    reqHelp = RequestHelper(publicKey, privateKey)

    data = {
        'name': 'Test Tester',
        'address': {
            'street': 'Teststreet',
            'number': 123
        },
        'valid': False,
        'data': {}
    }

    targetJson = '{"name":"Test Tester","address":{"street":"Teststreet","number":123},"valid":false,"data":{}}'

    assert targetJson == reqHelp.to_json(data)

def test_create_form_data_hmac_hash():
    reqHelp = RequestHelper(publicKey, privateKey)

    data = {
        'name': 'Test Tester',
        'address': {
            'street': 'Teststreet',
            'number': 123
        },
        'valid': False,
        'data': {}
    }

    assert '408f7cfd222dcf2369c8c1655df2f8de489858e23d9e100233a5b09e748fd360' == reqHelp.create_form_data_hmac_hash(data)
