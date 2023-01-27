class StatisticResult:
    number_of_valid_submissions: int = 0
    number_of_spam_submissions: int = 0
    numbers_by_date: dict = {}

    def __init__(self, number_of_valid_submissions: int, number_of_spam_submissions: int, numbers_by_date: dict):
        self.number_of_valid_submissions = number_of_valid_submissions
        self.number_of_spam_submissions = number_of_spam_submissions
        self.numbers_by_date = numbers_by_date

    def get_number_of_valid_submissions(self) -> int:
        return self.number_of_valid_submissions

    def get_number_of_spam_submissions(self) -> int:
        return self.number_of_spam_submissions

    def get_numbers_by_date(self) -> dict:
        return self.numbers_by_date
