from coffee_bean.score_calculator.ScoreCalculator import ScoreCalculator
from coffee_bean.tests.parameters import parameters


def pytest_generate_tests(metafunc):
    if 'message' in metafunc.fixturenames:
        metafunc.parametrize("message, expected", parameters)


def test_evaluate(message, expected):
    score_cal = ScoreCalculator()

    recommendation = score_cal.evaluate(message)

    print(recommendation)
    assert recommendation.verdict is expected
