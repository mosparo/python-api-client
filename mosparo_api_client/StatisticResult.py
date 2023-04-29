class StatisticResult:
    """
    A StatisticResult object will be returned by the `get_statistic_by_date` method of the API client and
    holds all information which the API returned.

    :param int number_of_valid_submissions: The number of valid submissions in the requested time range
    :param int number_of_spam_submissions: The number of spam submissions in the requested time range
    :param dict numbers_by_date: A dictionary with all the data grouped by date
    """

    number_of_valid_submissions: int = 0
    number_of_spam_submissions: int = 0
    numbers_by_date: dict = {}

    def __init__(self, number_of_valid_submissions: int, number_of_spam_submissions: int, numbers_by_date: dict):
        self.number_of_valid_submissions = number_of_valid_submissions
        self.number_of_spam_submissions = number_of_spam_submissions
        self.numbers_by_date = numbers_by_date

    def get_number_of_valid_submissions(self) -> int:
        """
        Return the number of valid submissions in the requested time range

        :return: The number of valid submissions
        :rtype: int
        """
        return self.number_of_valid_submissions

    def get_number_of_spam_submissions(self) -> int:
        """
        Return the number of spam submissions in the requested time range

        :return: The number of spam submissions
        :rtype: int
        """
        return self.number_of_spam_submissions

    def get_numbers_by_date(self) -> dict:
        """
        Return the numbers grouped by date

        :return: The numbers grouped by date
        :rtype: dict
        """
        return self.numbers_by_date
