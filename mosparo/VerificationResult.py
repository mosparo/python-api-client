class VerificationResult:
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
        return self.submittable

    def is_valid(self) -> bool:
        return self.valid

    def get_verified_fields(self) -> dict:
        return self.verified_fields

    def get_verified_field(self, key: str) -> str:
        if not key in self.verified_fields:
            return self.FIELD_NOT_VERIFIED

        return self.verified_fields[key]

    def has_issues(self) -> bool:
        return len(self.issues) > 0

    def get_issues(self) -> list:
        return self.issues