from mosparo_api_client import VerificationResult

def test_verification_result():
    verified_fields = {
        'name': VerificationResult.FIELD_VALID,
        'street': VerificationResult.FIELD_INVALID
    }
    issues = [
        {'name': 'street', 'message': 'Missing in form data, verification not possible'}
    ]

    vr = VerificationResult(False, True, verified_fields, issues)

    assert vr.is_submittable() is False
    assert vr.is_valid() is True
    assert verified_fields == vr.get_verified_fields()
    assert 'valid' == vr.get_verified_field('name')
    assert 'invalid' == vr.get_verified_field('street')
    assert 'not-verified' == vr.get_verified_field('number')
    assert vr.has_issues() is True
    assert issues == vr.get_issues()
