class Recommendation:
    def __init__(self):
        self.results: list[Result] = []
        self.verdict: bool = False
        self.total: float = 0
        self.error_message: str = ""

    def add_result(self, result: 'Result') -> None:
        result.id = len(self.results) + 1
        self.results.append(result)
        self.issue_verdict()

    def issue_verdict(self) -> None:
        score_sum: float = 0

        for result in self.results:
            score_sum += result.score

        self.total = score_sum

        if score_sum < 3.9:
            self.verdict = False
        else:
            self.verdict = True

    def __str__(self) -> str:
        string: str = ""

        if not self.error_message:
            string += "Recommendation:\n"

            for result in self.results:
                string += f"\t{result.__str__()}\n"

            string += f"\tTotal {'%.2f' % self.total}\n"

            if self.verdict:
                string += "\nVerify this user."
            else:
                string += "\nDo not verify this user with the current information."
        else:
            string = self.error_message

        return string


class Result:
    def __init__(self, score: float, comment: str = None):
        self.id: int = 0
        self.score: float = score
        self.comment: str = comment

    def __str__(self) -> str:
        string: str = f"{self.id}) Score: {'%.2f' % self.score}"

        if self.comment:
            string += f" - {self.comment}"

        return string
