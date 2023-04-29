from mosparo_api_client import StatisticResult

def test_statistic_result():
    byDate = {
        '2021-04-29': {
            'numberOfValidSubmissions': 2,
            'numberOfSpamSubmissions': 5
        }
    }

    sr = StatisticResult(10, 20, byDate)

    assert 10 == sr.get_number_of_valid_submissions()
    assert 20 == sr.get_number_of_spam_submissions()
    assert byDate == sr.get_numbers_by_date()
