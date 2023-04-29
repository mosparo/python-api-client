class VerificationResult:
    """
    A VerificationResult object will be returned by the `verify_submission` method of the API client and
    holds all information which the API returned.

    :param bool submittable: Is True, when the submission was verified correctly and can be submitted
    :param bool valid: Is True, when the form data were transmitted correctly
    :param dict verified_fields: A dictionary with all the fields and their respective status.
    :param list issues: Possible issues which mosparo detected while verifing the data
    """

    FIELD_NOT_VERIFIED: str = 'not-verified'
    FIELD_VALID: str = 'valid'
    FIELD_INVALID: str = 'invalid'

    submittable: bool = False
    valid: bool = False
    verified_fields: dict = {}
    issues: list = []

    def __init__(self, submittable: bool, valid: bool, verified_fields: dict, issues: list):
        self.submittable = submittable
        self.valid = valid
        self.verified_fields = verified_fields
        self.issues = issues

    def is_submittable(self) -> bool:
        """
        Returns True, if the submission was verified correctly and is submittable

        :return: True, if the submission is submittable
        :rtype: bool
        """
        return self.submittable

    def is_valid(self) -> bool:
        """
        Returns True, if the form data was transmitted correctly

        :return: True, if the submission is valid
        :rtype: bool
        """
        return self.valid

    def get_verified_fields(self) -> dict:
        """
        Returns a dictionary with all the form fields and their status

        :return: Dictionary with all the form fields and their status
        :rtype: dict
        """
        return self.verified_fields

    def get_verified_field(self, key: str) -> str:
        """
        Returns the status for the given form field key

        :param str key: The form field key for which the status should be returned
        :return: The status of the form field
        :rtype: str
        """
        if not key in self.verified_fields:
            return self.FIELD_NOT_VERIFIED

        return self.verified_fields[key]

    def has_issues(self) -> bool:
        """
        Returns True if there are issues available, which occurred in the verification of the form data

        :return: True, if there are issues available
        :rtype: bool
        """
        return len(self.issues) > 0

    def get_issues(self) -> list:
        """
        Returns the list of occurred issues

        :return: List of occurred issues
        :rtype: list
        """
        return self.issues