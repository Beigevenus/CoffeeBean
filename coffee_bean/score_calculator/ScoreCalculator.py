import json
import re

import spacy
from textblob import TextBlob
from .Recommendation import Recommendation, Result
from spacy.lang.en.stop_words import STOP_WORDS


class ScoreCalculator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    def evaluate(self, message: str) -> Recommendation:
        recom: Recommendation = Recommendation()

        try:
            answers: list[str] = self.extract_answers(message)
        except SyntaxError:
            recom.error_message = "ERROR: ScoreCalculator was unable to extract six answers from the given message. " \
                                  "\nThis is most likely a limitation in the extraction, so if you wish for this " \
                                  "formatting to be supported in the future, please provide Zoe with the message in " \
                                  "question. "
            return recom

        recom.add_result(self.assess_polarity(answers[0]))
        recom.add_result(self.assess_similarity(answers[1], "gender_identities", Metric(0.6), remove_stop_words=True))
        recom.add_result(self.assess_similarity(answers[2], "orientations", Metric(0.6), remove_stop_words=True))
        recom.add_result(self.assess_similarity(answers[3], "pronoun_definitions", Metric(0.3, 0.9, -1),
                                                remove_stop_words=True))
        recom.add_result(self.assess_similarity(answers[4], "invitations", Metric(0.6), remove_stop_words=True))
        recom.add_result(self.assess_similarity(answers[5], "rules", Metric(0.25, 0.9, -0.1)))

        return recom

    @staticmethod
    def extract_answers(message: str) -> list[str]:
        message = re.sub(r"What is your opinion on the LGBTQ\+ community\?\s*", "", message)
        message = re.sub(r"What is your gender\?\s*", "", message)
        message = re.sub(r"What is your sexuality\?\s*", "", message)
        message = re.sub(r"Please explain what pronouns are in your own words\.\s*", "", message)
        message = re.sub(r"How did you find the server\?\s*", "", message)
        message = re.sub(r"Restate one of the 📜「rules」 in your own words\.\s*", "", message)

        answers = re.findall(r"[1-6]\.[\w\d,.\-!'()<>+’;:\[\]@\"“”/ ]*", message)

        for i, answer in enumerate(answers):
            answers[i] = re.sub(r"[1-6][.)]\s*", "", answer).lower()

        if len(answers) != 6:
            raise SyntaxError("Could not extract six answers from message.")
        else:
            return answers

    @staticmethod
    def assess_polarity(message: str) -> Result:
        blob = TextBlob(message)
        return Result(blob.sentiment_assessments.polarity, f"Given answer: '{message}'")

    def assess_similarity(self, message: str, filename: str, metric: 'Metric',
                          remove_stop_words: bool = False) -> Result:
        with open(f"./coffee_bean/metrics/{filename}.json", "r") as file:
            items = json.load(file)

        if remove_stop_words:
            message = self.remove_stop_words(message)
        message_doc = self.nlp(message)

        max_sim: float = 0
        for item in items:
            item = item.lower()
            if remove_stop_words:
                item = self.remove_stop_words(item)
            item_doc = self.nlp(item)
            sim = message_doc.similarity(item_doc)

            if sim > max_sim:
                max_sim = sim

        if max_sim < metric.lower:
            return Result(metric.lower_score, f"Similarity between '{message}' and every entry in '{filename}' is too "
                                              f"low to be considered a match. ")
        elif max_sim > metric.upper:
            return Result(metric.upper_score, f"Similarity between '{message}' and an entry in '{filename}' is "
                                              f"suspiciously high and can therefore not be considered a match. ")
        else:
            return Result(max_sim, f"Similarity between '{message}' and an entry in '{filename}' is within reasonable "
                                   f"boundaries and can be considered a match.")

    @staticmethod
    def remove_stop_words(text: str) -> str:
        remaining_words: list[str] = [i for i in text.split(' ') if i not in STOP_WORDS]
        return ' '.join(word for word in remaining_words)


class Metric:
    def __init__(self, lower: float = 0, upper: float = 100000, upper_score: float = 0, lower_score: float = 0):
        self.lower = lower
        self.upper = upper
        self.upper_score = upper_score
        self.lower_score = lower_score
