import json
import re
import spacy
from textblob import TextBlob


class ScoreCalculator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    def evaluate(self, message: str) -> bool:
        scores: list[float] = self.calculate_score(message)

        for i, score in enumerate(scores):
            print(f"Score for question {i+1}: {score}")

        final_score = sum(scores)
        print(f"Final score: {final_score}\n")

        if final_score > 3.5:
            print(f"My recommendation would be to verify this user.")
            return True
        else:
            print(f"My recommendation would be to not verify this user, currently.")
            return False

    def calculate_score(self, message: str) -> list[float]:
        scores: list[float] = []

        answers = self.find_answers(message)
        scores.append(self.process_first_answer(answers[0]))
        scores.append(self.process_similarities(answers[1], "gender_identities"))
        scores.append(self.process_similarities(answers[2], "sexualities"))
        scores.append(self.process_fourth_answer(answers[3]))
        scores.append(self.process_similarities(answers[4], "invitations"))
        scores.append(self.process_sixth_answer(answers[5]))

        return scores

    def find_answers(self, message: str) -> list[str]:
        answers = re.sub("What is your opinion on the LGBTQ\+ community\?(\n| )*", "", message)
        answers = re.sub("What is your gender\?(\n| )*", "", answers)
        answers = re.sub("What is your sexuality\?(\n| )*", "", answers)
        answers = re.sub("Please explain what pronouns are in your own words\.(\n| )*", "", answers)
        answers = re.sub("How did you find the server\?(\n| )*", "", answers)
        answers = re.sub("Restate one of the 📜「rules」 in your own words\.(\n| )*", "", answers)

        answers = re.findall("[1-6]\.[\w\d,.\-!'()<>+’; ]*", answers)

        if len(answers) != 6:
            raise Exception("Could not identify all answers.")
        else:
            return answers

    def process_first_answer(self, answer: str) -> float:
        blob = TextBlob(answer)
        return blob.sentiment_assessments.polarity

    def process_similarities(self, answer: str, filename: str) -> float:
        with open(f"./{filename}.json", "r") as file:
            data = json.load(file)

        similarities: list[float] = []

        # TODO: Sub doesn't remove numbers 1-6 properly
        improved_answer = re.sub("([1-6](\.|\)) )|\.|\,", "", answer).lower()
        answer_doc = self.nlp(improved_answer)

        for item in data:
            item = item.lower()
            item_doc = self.nlp(item)

            similarities.append(answer_doc.similarity(item_doc))

        max_sim = max(similarities)

        if max_sim < 0.6:
            print(f"Similarity between answer '{improved_answer}' and entries in '{filename}' is too low to be considered a "
                  f"match.")
            return 0
        else:
            return max_sim

    def process_fourth_answer(self, answer: str) -> float:
        improved_answer = re.sub("([1-6](\.|\)) )|\.|\,", "", answer).lower()
        answer_doc = self.nlp(improved_answer)
        definition_doc = self.nlp(
            "a word that can function as a noun phrase used by itself and that refers either to the participants "
            "in the discourse or to someone or something mentioned elsewhere in the discourse.")
        sim = answer_doc.similarity(definition_doc)

        if sim > 0.9:
            print(f"Answer 4 is too similar to the definition of pronouns to be considered 'in your own words'.")
            return -0.2
        elif sim < 0.3:
            print(f"Answer 4 is not similar enough to the definition of pronouns to be considered a valid "
                  f"answer.")
            return 0
        else:
            print(f"Answer 4 is considered a valid response, with similarity {sim*100}% to the definition of "
                  f"pronouns.")
            return sim

    def process_sixth_answer(self, answer: str) -> float:
        improved_answer = re.sub("([1-6](\.|\)) )|\.|\,", "", answer).lower()
        answer_doc = self.nlp(improved_answer)
        rules: list[str] = ["If you are found to be under the age requirement for Discord [13] you will be banned.",
                            "Treat everyone with respect. Absolutely no harassment, witch hunting, sexism, racism, "
                            "or hate speech will be tolerated.",
                            "No spam or self-promotion (server invites, advertisements, etc) unless in the correct "
                            "channel or with permission from an admin/mod. This includes DMing fellow members.",
                            "No NSFW or obscene content. This includes text, images, or links featuring nudity, sex, "
                            "hard violence, or other graphically disturbing content.",
                            "If you see something against the rules or something that makes you feel unsafe, "
                            "let admins/mods know. We want this server to be a welcoming space!",
                            "No pinging anyone excessively/for no reason.",
                            "Make sure to put trigger warnings and use spoilers on any sensitive issues. If you are "
                            "unsure if something needs a TW, ask a mod or admin or just put one just in case.",
                            "Swearing is allowed, but not in excessive amounts or when used to be discriminatory.",
                            "Please keep topics in correct channels.",
                            "If you are currently unverified, please check the verification channel to gain access to "
                            "the rest of the server.",
                            "Don't try and get around a ban with an alt account.",
                            "No mini-modding! If you see an issue simply let a staff member know and we will rectify "
                            "the "
                            "issue."]
        sims: list[float] = []

        for rule in rules:
            rule_doc = self.nlp(rule)
            sims.append(answer_doc.similarity(rule_doc))

        highest_sim = max(sims)

        if highest_sim > 0.9:
            print(f"Answer 6 is too similar to the one or more rule to be considered 'in your own words'.")
            return -0.1
        elif highest_sim < 0.25:
            print(f"Answer 6 is not similar enough to a rule to be considered a valid answer.")
            return 0
        else:
            print(
                f"Answer 6 is considered a valid response, with similarity {highest_sim * 100}% to one or "
                f"more rules.")
            return highest_sim
